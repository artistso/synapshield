# SynapShield model-audit pipeline

This directory defines a reproducible adversarial review process for SynapShield.

## Scope

Large language models are used only as independent reviewers of:

- dimensional consistency;
- boundary and initial conditions;
- numerical formulation;
- parameter identifiability;
- biological assumptions;
- evidence provenance;
- prohibited clinical inference.

They do **not** generate experimental evidence, establish safety or efficacy, replace numerical solvers, or convert synthetic outputs into medical claims.

## Reviewer panel

Default Hugging Face models:

1. `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B` — adversarial reasoning and code review.
2. `Qwen/Qwen3-8B` — independent general scientific critique.
3. `Qwen/Qwen2.5-Math-7B-Instruct` — dimensional analysis and algebraic checks.

The panel is configurable. A finding is not accepted merely because multiple language models agree. Every accepted finding must be linked to a concrete equation, source line, numerical test, or external primary source.

## Required order of operations

1. Run deterministic tests.
2. Produce a machine-readable numerical report.
3. Run the static claim scanner.
4. Build an audit packet from current repository files.
5. Submit the same packet and rubric to each reviewer model.
6. Parse reviewer outputs as untrusted suggestions.
7. Reproduce each mathematical or software finding independently.
8. Record accepted, rejected, and unresolved findings.
9. Remove or qualify unsupported claims.

## Commands

```bash
python -m pip install -e '.[test]'
pytest
python simulations/python/synapshield_model_v2.py \
  --duration-days 1 \
  --grid-points 41 \
  --uncertainty-samples 100 \
  --output model-report.json
python tools/static_claim_audit.py --root . --output audit/static-claim-report.json
```

To run the model panel through Hugging Face Inference Providers:

```bash
python -m pip install huggingface_hub
export HF_TOKEN=your_token
python tools/hf_model_audit.py \
  --root . \
  --numerical-report model-report.json \
  --output audit/model-panel-report.json
```

A local OpenAI-compatible endpoint can instead be used by adapting the provider function. Do not commit tokens, endpoint credentials, private health information, or model chain-of-thought.

## Acceptance rule

A proposed correction is accepted only when at least one of the following is present:

- a reproducible failing test;
- a unit or dimensional contradiction;
- a violated conservation or boundary condition;
- a primary-source contradiction;
- an unsupported factual assertion;
- an inference that exceeds the modeled quantity.

Model prose alone is never sufficient evidence.

## Compute status

The repository owner is authenticated to Hugging Face. A GPU Job attempt on 2026-07-16 was rejected because the account had insufficient prepaid compute credit. The pipeline remains usable through Inference Providers, local models, or Hugging Face Jobs once compute credit is available.
