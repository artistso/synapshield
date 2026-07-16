#!/usr/bin/env python3
"""Scan text-bearing repository files for high-risk unsupported claim language."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

TEXT_SUFFIXES = {".md", ".html", ".txt", ".py", ".json", ".yml", ".yaml", ".cff"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules"}

RULES: dict[str, re.Pattern[str]] = {
    "clinical_proof": re.compile(r"\b(science is proven|clinically validated|clinical validation successful|proves? (?:that )?.*(?:prevents?|treats?|cures?))\b", re.I),
    "guaranteed_outcome": re.compile(r"\b(never starts|never arrives|future is protected|guaranteed|zero systemic toxicity|no gastric ulcers|no renal damage)\b", re.I),
    "availability": re.compile(r"\b(available for early adopters|when .* becomes available|talk to your doctor.*gut-based.*prevention)\b", re.I),
    "fabricated_personal_claim": re.compile(r"\b(Richard.*(?:Parkinson|tremor|stiffness|patient)|Richard(?:'s|’s) wife.*(?:said|Parkinson))\b", re.I),
    "unverified_regulatory": re.compile(r"\b(IRB.*waiver granted|FDA pre-IND|FDA-approved precursor|Declaration of Helsinki compliant)\b", re.I),
    "unverified_publication": re.compile(r"\b(10\.1101/TBD|medRxiv.*submitted|bioRxiv.*pending)\b", re.I),
    "overstated_validation": re.compile(r"\b(validation successful|mechanically and chemically validated|ready for clinical translation|mathematical proof(?:s)? that .*works)\b", re.I),
}

# Files whose purpose is to document/retract prior language may contain quoted prohibited phrases.
ALLOWLIST_PATHS = {
    "audit/README.md",
    "tools/static_claim_audit.py",
    "README.md",
    "TECHNICAL_PAPER.md",
    "RICHARD_HANDOUT.html",
}

@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    line: int
    excerpt: str


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def scan(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(lines, start=1):
            for rule, pattern in RULES.items():
                if pattern.search(line):
                    # Retraction and audit documents may name a phrase while explicitly denying it.
                    lowered = line.lower()
                    is_retraction = any(token in lowered for token in ("false", "retract", "unsupported", "not ", "no clinical evidence"))
                    if rel in ALLOWLIST_PATHS and is_retraction:
                        continue
                    findings.append(Finding(rule, rel, number, line.strip()[:280]))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    findings = scan(root)
    payload = {
        "status": "pass" if not findings else "review_required",
        "finding_count": len(findings),
        "findings": [asdict(item) for item in findings],
        "note": "Pattern matches require human review; absence of matches does not prove scientific validity.",
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if args.fail_on_findings and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
