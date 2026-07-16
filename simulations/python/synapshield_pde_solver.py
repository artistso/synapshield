"""Compatibility entry point for the conservative SynapShield model v2.

The former implementation and its claimed 94–99.99% validation are deprecated.
Run this file from the repository root to produce a transparent JSON comparison
against a matched no-sink baseline.
"""
from synapshield_model_v2 import main

if __name__ == "__main__":
    raise SystemExit(main())
