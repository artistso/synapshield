# Cover Letter - medRxiv / bioRxiv Submission

**Date:** June 30, 2026  
**To:** The Editors, medRxiv / bioRxiv - Cold Spring Harbor Laboratory

---

Dear Editors,

I am pleased to submit the attached manuscript entitled:

**"SynapShield: Intercepting Parkinson's Disease at the Gut-Brain Interface - A Bioengineered Hydrogel Approach with Computational Validation"**

for consideration as a preprint on **medRxiv** and **bioRxiv**.

**Author:**  
Steven Owens  
Computational Bioengineering Laboratory  
Ocean Shores, Washington, USA  
ORCID: https://orcid.org/0009-0006-0211-4812  
Email: artistso@github.com  
Corresponding author: Yes

---

### What we report

Parkinson's disease is diagnosed 15-20 years after the neurodegenerative cascade begins, when 60-80% of substantia nigra neurons are already lost. We present **SynapShield**: an open-source, interceptive therapeutic - a shear-thinning HA-Tyramine / Alginate IPN hydrogel injected submucosally at the pyloric/duodenal vagus nerve interface (CPT 43256), acting as a pathological sink for misfolded alpha--synuclein, with 15-year zero-order release of caffeine, chlorogenic acid, and ibuprofen.

Computational contribution:

- First **4-species PDE model tracking the pathogen (alpha--synuclein) itself**, not just drug concentrations
- `∂C₄/∂t = D₄∇^2C₄ - Vmax*C₄/(Km+C₄) - k_clear*(C₁+C₂)*C₄`
- Python (scipy BDF), MATLAB (pdepe), and FEniCSx poroelastic validation - fully reproducible
- **>94% alpha--synuclein reduction at 7 days, >99.99% at 1 year**
- Validation: `C₄(x=L_gel) = 3.33x10⁻^1⁷ mol/m^3`

All code, data, and documentation are open-source under MIT License:  
https://github.com/artistso/synapshield  
Live interactive demo: https://artistso.github.io/synapshield/

---

### Why medRxiv / bioRxiv

1. **Urgency:** 10 million people live with Parkinson's worldwide. Interceptive, pre-motor therapeutics cannot wait for traditional 18-month journal cycles.
2. **Open science:** Full computational reproducibility - 4-species PDE solver, FEniCSx multiphysics, clinical briefing (CPT 43256, DTI-ALPS endpoints) - all MIT licensed.
3. **Community relevance:** Dedicated to a real patient - Richard, Ocean Shores, WA - bridging computational bioengineering with community medicine.
4. **Preprint precedent:** Gut-brain axis alpha--synuclein propagation (Kim et al., Nature Neuroscience 2019; Braak et al., 2003) urgently needs translational, interceptive frameworks in the open literature.

I confirm:

- This work is original, computational only, no human subjects - no IRB required
- No competing interests - self-funded / open-source - MIT License
- All authors approve submission - Steven Owens (sole author, ORCID 0009-0006-0211-4812)
- Data availability: https://github.com/artistso/synapshield
- Code availability: MIT - https://github.com/artistso/synapshield/tree/main/simulations
- Preprint license: CC BY 4.0 (software: MIT)
- Not under consideration elsewhere as a preprint (first submission: medRxiv / bioRxiv, June 30, 2026)
- Clinical trial registration: N/A - computational validation - Pre-IND planned 2026-2027

A clinical briefing for practicing gastroenterologists / neurologists is included as supplementary material: `docs/CLINICAL_BRIEFING.md` - CPT 43256, DTI-ALPS primary endpoint, Phase I-III roadmap to FDA PMA 2031.

---

### Suggested reviewers / communities

- Gut-brain axis / vagus nerve alpha--synuclein propagation
- Computational drug delivery / PDE modeling / FEniCSx
- Interventional GI endoscopy / neurodegenerative interception
- Open-source medicine / computational bioengineering

Keywords: Parkinson's disease; gut-brain axis; alpha-synuclein; vagus nerve; hydrogel; PDE modeling; interceptive therapeutics; computational bioengineering; open-source medicine; FEniCSx

---

Thank you for considering SynapShield for medRxiv / bioRxiv. I believe open, computable, interceptive neurodegenerative therapeutics deserve rapid, transparent dissemination - because behind every equation is a person waiting.

This work is dedicated to **Richard**, Ocean Shores, Washington - whose courage in the face of Parkinson's inspired this project.

> *"Hope, not just science."*  
> *"From PDEs to Richard's tablet."*

I look forward to your positive response and am available for any revisions or clarifications.

Sincerely,

**Steven Owens**  
Computational Bioengineering Laboratory  
Ocean Shores, Washington, USA  
ORCID: https://orcid.org/0009-0006-0211-4812  
Email: artistso@github.com  
GitHub: https://github.com/artistso  
Repository: https://github.com/artistso/synapshield  
Live Demo: https://artistso.github.io/synapshield/  
Preprint DOI: 10.1101/TBD (pending)

---

**Enclosures:**
1. Manuscript PDF - `SynapShield_medRxiv_2026-06-30_v1.0.2.pdf` (77 KB)
2. Technical Paper (Markdown) - `TECHNICAL_PAPER.md`
3. Clinical Briefing - `docs/CLINICAL_BRIEFING.md`
4. Code repository - https://github.com/artistso/synapshield
5. 4-species PDE validation figure - `simulations/results/synapshield_results.png`
   - alpha--syn at nerve: 3.33e-17 mol/m^3
6. CITATION.cff / codemeta.json / .zenodo.json
7. JOSS paper - `paper.md` + `paper.bib`
8. ORCID: 0009-0006-0211-4812
9. License: MIT

*SynapShield Research Consortium - Open-source under MIT License - v1.0.2 - June 30, 2026*  
*Dedicated to Richard - Ocean Shores, Washington*
