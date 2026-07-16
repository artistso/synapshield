# SynapShield

## Exploratory reaction–diffusion model for a hypothetical local α-synuclein sink

[![CI](https://github.com/artistso/synapshield/actions/workflows/ci.yml/badge.svg)](https://github.com/artistso/synapshield/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Research status](https://img.shields.io/badge/status-computational%20hypothesis-orange.svg)](#research-status)

> **Research-only repository.** SynapShield is not a medical device, drug, diagnostic, preventive treatment, clinical protocol, or evidence that Parkinson’s disease can be stopped by an implanted hydrogel.

SynapShield now has a narrower, falsifiable purpose: test whether a hypothetical localized sink can reduce a modeled concentration field under explicit one-dimensional transport assumptions. The repository separates mathematical behavior from biological, engineering, regulatory, and clinical claims.

## Research status

| Question | Current status |
|---|---|
| Does the numerical solver run reproducibly? | Yes; automated tests cover positivity, boundary conditions, controls, and release arithmetic. |
| Does a sink reduce concentration in the synthetic model? | Under some parameter sets, yes. The magnitude is strongly parameter-dependent. |
| Is the model calibrated to measured α-synuclein transport or binding data? | No. |
| Has the material been synthesized or characterized? | No evidence is included here. |
| Has safety, residence time, dosing, toxicity, or mechanical durability been demonstrated? | No. |
| Does this prevent, slow, or treat Parkinson’s disease? | Unknown; this repository provides no clinical evidence. |
| Is there a verified public preprint DOI or IRB determination? | Not currently documented in this repository. |

## Important correction

Earlier versions incorrectly attributed Parkinson’s disease, symptoms, and quotations to Richard and his wife. Those statements were false and have been retracted. Neither person should be represented as a patient, study participant, testimonial source, or clinical motivation. See [`RICHARD_HANDOUT.html`](RICHARD_HANDOUT.html) for the correction notice.

## What changed in v0.2

The repository was stress-tested against its own equations and code.

1. **Release kinetics contradicted the 10–15 year claim.** The previous combined first-order rate was `1.6e-5 s^-1`, which has a half-life of about **12.0 hours** and leaves about **7.3e-220** of the reservoir after one year.
2. **The previous baseline was missing.** A sink model cannot establish effect without an identical no-sink control.
3. **The previous output was labeled “proof” despite synthetic parameters.** Outputs are now explicitly labeled model-dependent and non-clinical.
4. **The previous multiphysics code contained execution and formulation defects.** It used test functions before defining them, instantiated the nonlinear problem before adding traction, simulated seconds while claiming years or hundreds of millions of cycles, and lacked empirical calibration.
5. **The public site contained fabricated health claims, quotations, activity counts, and guaranteed outcomes.** These have been removed.

## Model v2

The conservative model solves

```text
∂C/∂t = ∂/∂x(D(x) ∂C/∂x) - I_sink(x) Vmax C/(Km + C)
```

with:

- zero flux at `x = 0`;
- fixed source concentration at `x = L`;
- harmonic-mean face diffusivity across material interfaces;
- a matched no-sink control;
- non-negativity and finite-value checks;
- optional uncertainty propagation over broad synthetic parameter ranges.

The model does **not** map concentration reduction to disease risk, neuron survival, clinical progression, or treatment efficacy.

## Run

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
```

Legacy command compatibility is retained:

```bash
python simulations/python/synapshield_pde_solver.py
```

## Interpreting results

A positive modeled reduction means only that the chosen sink term lowered the modeled concentration at the selected interface relative to the matched no-sink control. It does not establish:

- physical binding of α-synuclein;
- selectivity for pathological species;
- transport through real gastrointestinal tissue;
- access to relevant enteric or vagal compartments;
- hydrogel biocompatibility or long-term stability;
- drug efficacy, dose, release, or safety;
- applicability to brain-first or other Parkinson’s subtypes;
- prevention of Parkinson’s disease.

## Real-world validation gates

The concept should not advance to human-facing claims unless each prior gate is passed with preregistered criteria and independent replication.

| Gate | Minimum evidence |
|---|---|
| 0. Computational integrity | Unit tests, convergence analysis, mass-balance analysis, no-sink controls, parameter provenance, reproducible artifacts. |
| 1. Molecular feasibility | Measured binding kinetics and capacity for defined α-synuclein species; selectivity and reversibility characterized. |
| 2. Material feasibility | Rheology, swelling, degradation, sterilization, leachables, and release measured—not inferred. |
| 3. In-vitro safety | Cytotoxicity, inflammatory response, epithelial integrity, and off-target adsorption. |
| 4. Ex-vivo transport | Relevant tissue geometry and experimentally measured boundary conditions. |
| 5. In-vivo feasibility | Residence, migration, local injury, systemic exposure, retrieval, and failure modes. |
| 6. Regulatory strategy | Product classification, quality system, pre-submission interaction, manufacturing controls, and formal toxicology plan. |
| 7. Clinical research | Approved protocol, verified ethics review, informed consent, monitoring, and statistically justified endpoints. |

## Repository map

```text
.
├── index.html
├── README.md
├── TECHNICAL_PAPER.md
├── MODEL_LIMITATIONS.md
├── RICHARD_HANDOUT.html
├── pyproject.toml
├── simulations/python/
│   ├── synapshield_model_v2.py
│   ├── synapshield_pde_solver.py
│   ├── fenicsx_poroelastic.py
│   └── multiphysics_integration.py
├── tests/
│   ├── test_model_v2.py
│   └── test_mechanics_sanity.py
└── .github/workflows/ci.yml
```

## Scientific framing

The gut-first/body-first pathway is an active hypothesis and likely does not describe every Parkinson’s case. Evidence of association or animal-model propagation does not establish that a local gastrointestinal sink will prevent human disease. Caffeine and NSAID associations likewise do not justify chronic implanted delivery without pharmacology and toxicology data.

## Citation status

Do not cite this repository as a validated therapy or clinical study. A public preprint DOI, journal publication, ethics determination, or trial registration should be added only after a verifiable public record exists.

## License

MIT. The license permits reuse of code; it does not certify medical validity, regulatory compliance, safety, or fitness for clinical use.
