"""Conservative SynapShield reaction-diffusion research model.

This module evaluates a *hypothetical* local sink in a one-dimensional domain.
It does not model Parkinson's disease incidence, clinical efficacy, safety,
implant lifetime, or patient outcomes. Parameters are synthetic defaults until
measured in vitro or in vivo.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class ModelParameters:
    length_m: float = 2.0e-3
    sink_width_m: float = 5.0e-4
    grid_points: int = 121
    duration_s: float = 7.0 * 24.0 * 3600.0
    output_steps: int = 101
    source_concentration_mol_m3: float = 1.0e-2
    diffusivity_tissue_m2_s: float = 5.0e-11
    diffusivity_sink_m2_s: float = 1.0e-13
    sink_vmax_mol_m3_s: float = 2.5e-6
    sink_km_mol_m3: float = 1.0e-1

    def validate(self) -> None:
        if self.length_m <= 0:
            raise ValueError("length_m must be positive")
        if not 0 < self.sink_width_m < self.length_m:
            raise ValueError("sink_width_m must lie inside the domain")
        if self.grid_points < 11:
            raise ValueError("grid_points must be at least 11")
        if self.duration_s <= 0 or self.output_steps < 2:
            raise ValueError("duration_s and output_steps must be positive")
        for name in (
            "source_concentration_mol_m3",
            "diffusivity_tissue_m2_s",
            "diffusivity_sink_m2_s",
            "sink_vmax_mol_m3_s",
            "sink_km_mol_m3",
        ):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True)
class SimulationResult:
    x_m: np.ndarray
    t_s: np.ndarray
    concentration_mol_m3: np.ndarray
    interface_index: int
    success: bool
    message: str

    @property
    def final_profile(self) -> np.ndarray:
        return self.concentration_mol_m3[:, -1]

    @property
    def interface_concentration(self) -> float:
        return float(self.final_profile[self.interface_index])


def _harmonic_mean(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    denominator = a + b
    return np.divide(2.0 * a * b, denominator, out=np.zeros_like(denominator), where=denominator > 0)


def simulate(params: ModelParameters, *, sink_enabled: bool = True) -> SimulationResult:
    """Solve the 1-D finite-volume reaction-diffusion model.

    Boundary conditions:
    - x=0: zero diffusive flux
    - x=L: fixed source concentration

    The final grid node is imposed as a Dirichlet boundary and is excluded from
    the ODE state vector. Face diffusivities use harmonic averaging so flux is
    continuous across the sink/tissue interface.
    """
    params.validate()
    x = np.linspace(0.0, params.length_m, params.grid_points)
    dx = float(x[1] - x[0])
    dynamic_points = params.grid_points - 1
    interface_index = int(np.argmin(np.abs(x - params.sink_width_m)))

    diffusivity = np.where(
        x <= params.sink_width_m,
        params.diffusivity_sink_m2_s,
        params.diffusivity_tissue_m2_s,
    )
    face_diffusivity = _harmonic_mean(diffusivity[:-1], diffusivity[1:])
    sink_mask = (x[:dynamic_points] <= params.sink_width_m).astype(float)
    vmax = params.sink_vmax_mol_m3_s if sink_enabled else 0.0

    def rhs(_t: float, state: np.ndarray) -> np.ndarray:
        full = np.empty(params.grid_points, dtype=float)
        full[:-1] = state
        full[-1] = params.source_concentration_mol_m3

        flux = -face_diffusivity * np.diff(full) / dx
        derivative = np.empty(dynamic_points, dtype=float)
        derivative[0] = -flux[0] / dx
        derivative[1:] = (flux[:-1] - flux[1:]) / dx

        if vmax > 0:
            nonnegative = np.maximum(state, 0.0)
            reaction = vmax * nonnegative / (params.sink_km_mol_m3 + nonnegative)
            derivative -= sink_mask * reaction
        return derivative

    initial = np.zeros(dynamic_points, dtype=float)
    evaluation_times = np.linspace(0.0, params.duration_s, params.output_steps)
    solution = solve_ivp(
        rhs,
        (0.0, params.duration_s),
        initial,
        method="BDF",
        t_eval=evaluation_times,
        rtol=1e-7,
        atol=1e-11,
    )

    concentration = np.empty((params.grid_points, solution.t.size), dtype=float)
    concentration[:-1, :] = solution.y
    concentration[-1, :] = params.source_concentration_mol_m3
    minimum = float(np.min(concentration))
    success = bool(solution.success and minimum >= -1e-9 and np.all(np.isfinite(concentration)))
    concentration = np.maximum(concentration, 0.0)

    message = solution.message
    if minimum < -1e-9:
        message += f"; nonphysical minimum concentration {minimum:.3e}"

    return SimulationResult(
        x_m=x,
        t_s=solution.t,
        concentration_mol_m3=concentration,
        interface_index=interface_index,
        success=success,
        message=message,
    )


def compare_to_baseline(params: ModelParameters) -> dict[str, float | bool | str]:
    """Compare the candidate sink model against an identical no-sink control."""
    baseline = simulate(params, sink_enabled=False)
    candidate = simulate(params, sink_enabled=True)
    denominator = baseline.interface_concentration
    reduction = 0.0 if denominator <= 0 else 1.0 - candidate.interface_concentration / denominator
    return {
        "baseline_interface_concentration_mol_m3": baseline.interface_concentration,
        "candidate_interface_concentration_mol_m3": candidate.interface_concentration,
        "relative_reduction": float(reduction),
        "baseline_solver_success": baseline.success,
        "candidate_solver_success": candidate.success,
        "interpretation": (
            "Synthetic model comparison only; not evidence of disease prevention, "
            "clinical efficacy, safety, or implant durability."
        ),
    }


def uncertainty_sweep(
    params: ModelParameters,
    *,
    samples: int = 100,
    seed: int = 20260716,
) -> dict[str, float | int | str]:
    """Propagate broad parameter uncertainty through baseline comparisons.

    Diffusivities and kinetic parameters are independently sampled log-uniformly
    over one order of magnitude below and above the nominal values. This is a
    stress test, not a calibrated posterior distribution.
    """
    if samples < 1:
        raise ValueError("samples must be positive")
    rng = np.random.default_rng(seed)
    reductions: list[float] = []
    failures = 0
    fields = (
        "diffusivity_tissue_m2_s",
        "diffusivity_sink_m2_s",
        "sink_vmax_mol_m3_s",
        "sink_km_mol_m3",
    )
    for _ in range(samples):
        multipliers = 10.0 ** rng.uniform(-1.0, 1.0, size=len(fields))
        varied = params
        for field, multiplier in zip(fields, multipliers, strict=True):
            varied = replace(varied, **{field: getattr(params, field) * float(multiplier)})
        result = compare_to_baseline(varied)
        if result["baseline_solver_success"] and result["candidate_solver_success"]:
            reductions.append(float(result["relative_reduction"]))
        else:
            failures += 1

    if not reductions:
        raise RuntimeError("all uncertainty simulations failed")
    values = np.asarray(reductions)
    return {
        "samples_requested": samples,
        "samples_completed": int(values.size),
        "solver_failures": failures,
        "reduction_p05": float(np.quantile(values, 0.05)),
        "reduction_median": float(np.quantile(values, 0.50)),
        "reduction_p95": float(np.quantile(values, 0.95)),
        "fraction_positive_reduction": float(np.mean(values > 0.0)),
        "interpretation": "Exploratory one-order-of-magnitude stress test using synthetic priors.",
    }


def release_half_life_seconds(first_order_rate_s: float) -> float:
    if first_order_rate_s <= 0:
        raise ValueError("first_order_rate_s must be positive")
    return float(np.log(2.0) / first_order_rate_s)


def reservoir_fraction_remaining(first_order_rate_s: float, duration_s: float) -> float:
    if first_order_rate_s < 0 or duration_s < 0:
        raise ValueError("rate and duration must be nonnegative")
    return float(np.exp(-first_order_rate_s * duration_s))


def _write_json(path: Path | None, payload: dict) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True)
    if path is None:
        print(text)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration-days", type=float, default=7.0)
    parser.add_argument("--grid-points", type=int, default=121)
    parser.add_argument("--uncertainty-samples", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(list(argv) if argv is not None else None)

    params = ModelParameters(
        duration_s=args.duration_days * 24.0 * 3600.0,
        grid_points=args.grid_points,
    )
    payload: dict[str, object] = {
        "model_parameters": asdict(params),
        "baseline_comparison": compare_to_baseline(params),
        "release_math_check": {
            "implemented_combined_rate_s^-1": 1.6e-5,
            "half_life_hours": release_half_life_seconds(1.6e-5) / 3600.0,
            "fraction_remaining_after_1_year": reservoir_fraction_remaining(
                1.6e-5, 365.0 * 24.0 * 3600.0
            ),
        },
    }
    if args.uncertainty_samples:
        payload["uncertainty_sweep"] = uncertainty_sweep(
            params, samples=args.uncertainty_samples
        )
    _write_json(args.output, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
