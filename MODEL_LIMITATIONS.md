# Model limitations and falsification criteria

## Scope

The current model is a synthetic one-dimensional reaction–diffusion calculation. It is useful for checking numerical behavior and deriving experimental requirements. It is not a physiological digital twin.

## Structural limitations

1. **One-dimensional geometry.** No villi, crypts, vasculature, enteric neurons, vagal terminals, mucus, lumen flow, or heterogeneous tissue architecture.
2. **Single concentration field.** No monomer/oligomer/fibril distinction, conformational conversion, aggregation, cellular uptake, axonal transport, degradation, or immune response.
3. **Synthetic boundary condition.** The fixed source concentration is not derived from measured enteroendocrine secretion or tissue concentrations.
4. **Synthetic sink kinetics.** `Vmax` and `Km` are placeholders, not measured binding constants for a specified material and α-synuclein species.
5. **No convective transport.** Peristalsis, interstitial flow, lymphatic transport, and vascular clearance are omitted.
6. **No PK/PD model.** Concentration reduction is not connected to exposure, target engagement, neuron survival, symptoms, or disease probability.
7. **No population heterogeneity.** No genetics, body-first/brain-first subtype, age, sex, microbiome, environmental exposure, or comorbidity structure.
8. **No device mechanics.** The mechanics scripts provide sanity checks only; they do not establish implant residence or fatigue life.

## Numerical limitations

- Finite-volume discretization requires grid-convergence testing for every reported parameter regime.
- Stiff nonlinear sinks can produce solver sensitivity; tolerances and failure rates must be reported.
- Positivity checks detect but do not mathematically guarantee positivity for every configuration.
- A matched no-sink control is necessary but not sufficient for causal biological interpretation.

## Falsification criteria

The concept should be rejected or substantially redesigned if any of the following occur:

- no reproducible binding to defined pathological α-synuclein species;
- binding capacity is negligible relative to measured local production/transport;
- physiological proteins competitively saturate the material;
- bound species remain seeding-competent or are released under gastrointestinal conditions;
- the material causes epithelial injury, inflammation, obstruction, migration, ulceration, or systemic toxicity;
- measured release or degradation differs materially from the model;
- realistic geometry and measured parameters eliminate the modeled effect;
- the relevant disease subtype does not involve an accessible gut-to-brain pathway;
- benefit cannot be separated from selection bias, diagnostic uncertainty, or surrogate endpoints.

## Evidence hierarchy

Model output < in-vitro measurement < ex-vivo replication < animal feasibility < regulated human research < independent clinical replication.

No lower level should be described using the language of a higher level.
