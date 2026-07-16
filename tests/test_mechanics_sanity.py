import math

from simulations.python.fenicsx_poroelastic import MechanicsAssumptions, mechanics_sanity_report


def test_default_linear_strain_scale():
    report = mechanics_sanity_report(MechanicsAssumptions())
    assert math.isclose(report["linear_strain_scale"], 0.1)
    assert report["validated"] is False
    assert report["service_to_simulation_time_ratio"] > 1e7
