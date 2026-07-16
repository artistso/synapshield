#!/usr/bin/env python3
"""Run a reproducible multi-model critique through Hugging Face Inference Providers.

Model output is untrusted review material. This script never edits source files and never
labels model consensus as scientific validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_MODELS = [
    "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
    "Qwen/Qwen3-8B",
    "Qwen/Qwen2.5-Math-7B-Instruct",
]

AUDIT_FILES = [
    "README.md",
    "TECHNICAL_PAPER.md",
    "docs/math-models.md",
    "docs/MODEL_LIMITATIONS.md",
    "simulations/python/synapshield_model_v2.py",
    "simulations/python/mechanics_sanity.py",
    "tests/test_model_v2.py",
]

SYSTEM_PROMPT = """You are an adversarial scientific and numerical reviewer.
Do not infer clinical efficacy, safety, causality, or disease prevention from a synthetic model.
Do not provide hidden chain-of-thought. Return only concise findings in the requested JSON schema.
Every finding must identify a source file or equation and a reproducible verification step.
Unknown is an acceptable conclusion. Never invent citations, measurements, patients, datasets, or experiments."""

RUBRIC = """Audit the supplied repository packet under these categories:
1. dimensional consistency and units;
2. PDE/ODE formulation, signs, source and sink terms;
3. initial and boundary conditions;
4. discretization, convergence, stiffness, positivity and conservation;
5. parameter provenance, calibration and identifiability;
6. biological mechanism and competing hypotheses;
7. gap between modeled concentration and clinical outcome;
8. unsupported factual, regulatory, publication, safety or efficacy claims;
9. missing controls, sensitivity analyses and falsification tests;
10. software defects and reproducibility.

Return a single JSON object with this exact top-level structure:
{
  "verdict": "pass|revise|reject_current_claim",
  "findings": [
    {
      "severity": "critical|major|minor|note",
      "category": "string",
      "source": "path:line-or-equation",
      "claim": "what is wrong or uncertain",
      "evidence": "specific reason, dimensional check, or code behavior",
      "verification": "deterministic test or primary-data requirement",
      "recommended_change": "remove, qualify, test, or replace"
    }
  ],
  "claims_that_remain_supported": ["narrow statements only"],
  "unresolved_data_requirements": ["measured quantities needed"]
}

Do not wrap JSON in Markdown fences."""


def read_packet(root: Path, numerical_report: Path | None) -> tuple[str, dict[str, str]]:
    sections: list[str] = []
    hashes: dict[str, str] = {}
    for rel in AUDIT_FILES:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        digest = hashlib.sha256(text.encode()).hexdigest()
        hashes[rel] = digest
        sections.append(f"[FILE {rel} SHA256 {digest}]\n{text}")
    if numerical_report and numerical_report.exists():
        text = numerical_report.read_text(encoding="utf-8")
        rel = numerical_report.as_posix()
        digest = hashlib.sha256(text.encode()).hexdigest()
        hashes[rel] = digest
        sections.append(f"[NUMERICAL REPORT {rel} SHA256 {digest}]\n{text}")
    return "\n\n".join(sections), hashes


def parse_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].lstrip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end < start:
        raise ValueError("Model response contained no JSON object")
    return json.loads(cleaned[start : end + 1])


def run_model(model: str, prompt: str, token: str) -> dict[str, Any]:
    try:
        from huggingface_hub import InferenceClient
    except ImportError as exc:
        raise RuntimeError("Install huggingface_hub to run the model panel") from exc

    client = InferenceClient(model=model, token=token, provider="auto")
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=6000,
        temperature=0.2,
        top_p=0.9,
    )
    content = response.choices[0].message.content or ""
    parsed = parse_json_object(content)
    return {"model": model, "parsed": parsed, "raw_sha256": hashlib.sha256(content.encode()).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--numerical-report", type=Path)
    parser.add_argument("--output", type=Path, default=Path("audit/model-panel-report.json"))
    parser.add_argument("--models", nargs="*", default=DEFAULT_MODELS)
    parser.add_argument("--dry-run", action="store_true", help="Build and hash the packet without calling models")
    args = parser.parse_args()

    root = args.root.resolve()
    packet, hashes = read_packet(root, args.numerical_report)
    prompt = RUBRIC + "\n\nRepository packet follows:\n\n" + packet
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()

    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "packet_only" if args.dry_run else "completed",
        "warning": "LLM outputs are untrusted review suggestions, not validation or evidence.",
        "models": args.models,
        "source_hashes": hashes,
        "prompt_sha256": prompt_hash,
        "results": [],
    }

    if not args.dry_run:
        token = os.environ.get("HF_TOKEN")
        if not token:
            raise SystemExit("HF_TOKEN is required unless --dry-run is used")
        for model in args.models:
            try:
                report["results"].append(run_model(model, prompt, token))
            except Exception as exc:  # retain failures without discarding other reviewers
                report["results"].append({"model": model, "error": f"{type(exc).__name__}: {exc}"})
                report["status"] = "completed_with_errors"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
