import math

import numpy as np

from simulations.python.synapshield_model_v2 import (
    ModelParameters,
    compare_to_baseline,
    release_half_life_seconds,
    reservoir_fraction_remaining,
    simulate,
    uncertainty_sweep,
)


def fast_params() -> ModelParameters:
    return ModelParameters(grid_points=41, duration_s=24 * 3600, output_steps=15)


def test_solution_is_finite_and_nonnegative():
    result = simulate(fast_params())
    assert result.success
    assert np.all(np.isfinite(result.concentration_mol_m3))
    assert np.min(result.concentration_mol_m3) >= 0


def test_dirichlet_source_boundary_is_preserved():
    params = fast_params()
    result = simulate(params)
    assert np.allclose(result.concentration_mol_m3[-1, :], params.source_concentration_mol_m3)


def test_sink_does_not_increase_interface_concentration_at_default_parameters():
    result = compare_to_baseline(fast_params())
    assert result["baseline_solver_success"]
    assert result["candidate_solver_success"]
    assert 0.0 <= result["relative_reduction"] <= 1.0


def test_zero_vmax_matches_no_sink_control():
    params = ModelParameters(
        grid_points=41,
        duration_s=24 * 3600,
        output_steps=15,
        sink_vmax_mol_m3_s=0.0,
    )
    result = compare_to_baseline(params)
    assert math.isclose(result["relative_reduction"], 0.0, abs_tol=1e-12)


def test_release_math_matches_closed_form():
    rate = 1.6e-5
    assert math.isclose(release_half_life_seconds(rate), math.log(2) / rate)
    assert math.isclose(reservoir_fraction_remaining(rate, 10), math.exp(-rate * 10))


def test_uncertainty_sweep_returns_ordered_quantiles():
    summary = uncertainty_sweep(fast_params(), samples=4, seed=7)
    assert summary["samples_completed"] == 4
    assert summary["reduction_p05"] <= summary["reduction_median"] <= summary["reduction_p95"]
