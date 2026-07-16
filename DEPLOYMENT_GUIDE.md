# SynapShield research deployment guide

## Status

SynapShield is an exploratory computational repository. Deployment means publishing reproducible code and clearly labeled synthetic results. It does **not** mean deploying a medical intervention, recruiting patients, advising clinicians, or representing the concept as validated.

## Safe repository deployment

```bash
git clone https://github.com/artistso/synapshield.git
cd synapshield
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
pytest
python simulations/python/synapshield_model_v2.py \
  --duration-days 1 \
  --grid-points 41 \
  --uncertainty-samples 100 \
  --output model-report.json
python tools/static_claim_audit.py \
  --root . \
  --output audit/static-claim-report.json \
  --fail-on-findings
python tools/hf_model_audit.py \
  --root . \
  --numerical-report model-report.json \
  --output audit/model-panel-packet.json \
  --dry-run
```

## Credential handling

Never place a GitHub or Hugging Face token in a remote URL, source file, issue, prompt, screenshot, or committed shell history. Use GitHub authentication helpers, environment variables, or repository secrets. Revoke any credential that has been exposed.

## GitHub Pages

The static site may be published from `main` through repository settings. The page must preserve all research-only warnings and may not present synthetic animation or model output as a physiological observation.

## Hugging Face review panel

The optional audit harness uses:

- `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B`;
- `Qwen/Qwen3-8B`;
- `Qwen/Qwen2.5-Math-7B-Instruct`.

Model responses are review suggestions. They cannot establish mechanism, material feasibility, safety, efficacy, regulatory status, publication status, or clinical readiness.

## Release gate

A public release should fail when any of the following is present:

- fabricated personal health information or quotations;
- an unverified DOI, submission, IRB, FDA, trial, institutional, or reimbursement claim;
- a safety, toxicity, efficacy, prevention, treatment, or availability claim unsupported by measured data;
- a long-term durability claim inferred from a seconds-long simulation;
- a model percentage presented as disease-risk reduction;
- missing matched controls, units, source provenance, or reproducibility instructions.

## Real-world sequence

1. Computational verification and mesh/time convergence.
2. Molecular binding measurements and competitive adsorption.
3. Material synthesis, rheology, degradation, release, and fatigue testing.
4. In-vitro transport and seeding assays.
5. Ex-vivo tissue retention and transport studies.
6. Appropriate in-vivo studies under approved protocols.
7. Independent replication and regulatory consultation.
8. Human research only after all prior gates and formal authorization.

No calendar date is assigned to these gates because the required evidence does not yet exist.
