"""Legacy-path smoke test.

Substantive tests live in ``tests/test_model_v2.py``.
"""

from pathlib import Path


def test_compatibility_entry_point_is_nonclinical() -> None:
    text = Path(__file__).with_name("computational_core.py").read_text(encoding="utf-8")
    assert "synthetic, non-clinical" in text
    assert "ClinicalStressTestEngine" not in text.splitlines()[-1]
