"""Mechanical sanity checks for SynapShield.

This module intentionally does not claim finite-element, fatigue, residence, or
implant validation. The legacy FEniCSx script simulated seconds and could not
support multi-year or multi-cycle conclusions.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json


@dataclass(frozen=True)
class MechanicsAssumptions:
    pressure_pa: float = 5_000.0
    youngs_modulus_pa: float = 50_000.0
    simulated_duration_s: float = 10.0
    claimed_service_years: float = 15.0

    def validate(self) -> None:
        if self.pressure_pa < 0:
            raise ValueError("pressure_pa must be nonnegative")
        if self.youngs_modulus_pa <= 0:
            raise ValueError("youngs_modulus_pa must be positive")
        if self.simulated_duration_s <= 0 or self.claimed_service_years <= 0:
            raise ValueError("durations must be positive")


def mechanics_sanity_report(params: MechanicsAssumptions) -> dict[str, object]:
    params.validate()
    strain_scale = params.pressure_pa / params.youngs_modulus_pa
    service_seconds = params.claimed_service_years * 365.25 * 24 * 3600
    return {
        "assumptions": asdict(params),
        "linear_strain_scale": strain_scale,
        "service_to_simulation_time_ratio": service_seconds / params.simulated_duration_s,
        "validated": False,
        "interpretation": (
            "Linear pressure/modulus sanity check only. It does not establish "
            "poroelastic response, fatigue life, adhesion, migration, damage, "
            "retention, safety, or service lifetime."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pressure-pa", type=float, default=5_000.0)
    parser.add_argument("--youngs-modulus-pa", type=float, default=50_000.0)
    args = parser.parse_args()
    report = mechanics_sanity_report(
        MechanicsAssumptions(
            pressure_pa=args.pressure_pa,
            youngs_modulus_pa=args.youngs_modulus_pa,
        )
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
