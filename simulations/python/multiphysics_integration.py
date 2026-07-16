"""Transparent integration report; not a validated multiphysics simulation."""
from __future__ import annotations

import json

from fenicsx_poroelastic import MechanicsAssumptions, mechanics_sanity_report
from synapshield_model_v2 import ModelParameters, compare_to_baseline


def build_report() -> dict[str, object]:
    return {
        "transport": compare_to_baseline(ModelParameters(duration_s=24 * 3600, grid_points=41)),
        "mechanics": mechanics_sanity_report(MechanicsAssumptions()),
        "coupled": False,
        "interpretation": (
            "The transport and mechanics calculations are reported side by side. "
            "No two-way coupling, empirical calibration, or biological validation is claimed."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2, sort_keys=True))
