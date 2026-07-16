# SynapShield: a computational hypothesis and falsification plan

**Author:** Steven Owens  
**Repository:** https://github.com/artistso/synapshield  
**Version:** 0.2  
**Status:** exploratory computational work; not a clinical study or validated therapy

## Abstract

This repository evaluates a narrow mathematical question: under a hypothetical one-dimensional transport model, can a localized saturable sink lower a concentration field relative to an otherwise identical no-sink control? Earlier versions overstated this result as proof of Parkinson’s disease prevention and included unsupported personal, clinical, mechanical, pharmacological, publication, and ethics claims. Version 0.2 retracts those claims, introduces an explicit control, corrects release-kinetic arithmetic, adds automated tests, and defines experimental falsification gates. The model can demonstrate internal consequences of assumptions; it cannot establish biological feasibility, safety, disease modification, or clinical benefit.

## 1. Research question

Let `C(x,t)` denote a generic α-synuclein concentration proxy in a one-dimensional domain of length `L`. The candidate model asks whether a localized sink in `0 ≤ x ≤ L_sink` lowers `C` at a selected interface compared with a matched no-sink model.

This is not equivalent to asking whether an implanted hydrogel prevents Parkinson’s disease.

## 2. Governing equation

The candidate model is

```text
∂C/∂t = ∂/∂x(D(x) ∂C/∂x) - I_sink(x) Vmax C/(Km + C).
```

The control model sets `Vmax = 0` while retaining all other parameters.

Boundary conditions:

```text
-D ∂C/∂x |x=0 = 0
C(L,t) = C_source
```

Initial condition:

```text
C(x,0) = 0 for x < L
C(L,0) = C_source
```

The spatial operator is discretized by a finite-volume method with harmonic face diffusivities. The method-of-lines system is integrated with SciPy’s BDF solver.

## 3. Primary computational estimand

```text
relative reduction = 1 - C_candidate(x_interface,T) / C_control(x_interface,T)
```

This ratio is a model comparison. It is not a risk ratio, treatment effect, biomarker response, or clinical endpoint.

## 4. Release-kinetic audit

Earlier code used two first-order depletion terms:

```text
dC3/dt = -(1.5e-5 + 1.0e-6) C3.
```

Thus

```text
k_total = 1.6e-5 s^-1
half-life = ln(2)/k_total ≈ 4.33e4 s ≈ 12.0 h
C3(1 year)/C3(0) = exp(-k_total × 1 year) ≈ 7.3e-220.
```

That implementation cannot support a 10–15 year release claim. Long-duration release must be established from measured material degradation, diffusion, binding, geometry, and loading—not from selecting an extremely small rate constant.

## 5. Mechanics audit

Earlier scripts claimed durability over `10^5` to `10^8` cycles while simulating approximately 10 seconds. They also contained formulation defects, including use of undefined test functions and construction of the nonlinear problem before adding traction. Version 0.2 replaces “validation” language with a transparent linear-elastic sanity check:

```text
strain scale ≈ pressure / Young's modulus.
```

For `5 kPa / 50 kPa`, the strain scale is `0.1` or 10%. This does not predict retention, fatigue, damage, interface delamination, or poroelastic response.

## 6. Reproducibility

Automated tests cover:

- finite and nonnegative concentrations;
- source boundary preservation;
- matched no-sink control;
- zero-sink equivalence;
- closed-form release arithmetic;
- uncertainty-summary consistency;
- mechanics sanity arithmetic.

Continuous integration runs on Python 3.10–3.12 and uploads a JSON model report.

## 7. Uncertainty

The optional sweep varies four synthetic parameters independently over one order of magnitude above and below nominal values. This is not Bayesian calibration. It is a stress test that makes parameter dependence visible.

Any reported result must include:

- nominal parameters and units;
- control output;
- solver status;
- uncertainty range;
- grid/time convergence;
- provenance for every empirically derived parameter;
- a statement that clinical interpretation is unsupported.

## 8. Biological uncertainty

The gut-first/body-first hypothesis is plausible for some Parkinson’s phenotypes but is neither universal nor sufficient to validate this intervention. The model omits:

- brain-first disease;
- α-synuclein species and seeding activity;
- cellular production and clearance;
- enteric and vagal anatomy;
- immune and microbiome effects;
- transport barriers and competing proteins;
- toxicology and device failure modes.

## 9. Required experiments

Before any therapeutic language is used, the following must be measured:

1. binding affinity, capacity, selectivity, and reversibility for defined α-synuclein species;
2. whether captured material remains seeding-competent;
3. hydrogel rheology, swelling, degradation, sterilization stability, and leachables;
4. release kinetics under relevant pH, enzymes, flow, and mechanical loading;
5. epithelial cytotoxicity, inflammatory signaling, and barrier integrity;
6. retention, migration, ulceration, obstruction, retrieval, and systemic exposure;
7. realistic transport using measured geometry and boundary conditions.

## 10. Ethics and publication status

This repository does not claim a verified IRB waiver, clinical-trial status, public preprint DOI, or peer review. Such statements require publicly verifiable documentation. No private person is a patient partner, study participant, or testimonial source in this work.

## 11. Conclusion

Version 0.2 converts SynapShield from a claimed treatment into what the evidence supports: an exploratory computational hypothesis with controls, tests, explicit limitations, and a sequence of experiments capable of falsifying it.
