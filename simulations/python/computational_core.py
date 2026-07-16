"""Compatibility entry point for the SynapShield synthetic uncertainty model.

The former ``ClinicalStressTestEngine`` labeled arbitrary parameter draws as
patients and clinical covariates. That terminology and interpretation were
not justified. This module now delegates to ``synapshield_model_v2`` and
produces only synthetic, non-clinical sensitivity results.
"""

from synapshield_model_v2 import main


if __name__ == "__main__":
    raise SystemExit(main())
