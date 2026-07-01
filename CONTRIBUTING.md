# Contributing to SynapShield

Thank you for your interest in SynapShield — intercepting Parkinson's disease at the gut-bbrain axis.

**Author:** Steven Owens — ORCID: [0009-0006-0211-4812](https://orcid.org/0009-0006-0211-4812)  
**Preprint:** medRxiv — 10.1101/TBD (submitted June 30, 2026)  
**License:** MIT

> "Hope, not just science." — Dedicated to Richard, Ocean Shores, WA

---

## How to Contribute

### 1. Researchers / Computational
- Fork https://github.com/artistso/synapshield
- Run: `python simulations/python/synapshield_pde_solver.py`
- Improve PDE solver, add 3D geometry, validate parameters
- Submit PR with benchmark results

### 2. Clinicians
- Review `docs/CLINICAL_BRIEFING.md` — CPT 43256
- Suggest inclusion/exclusion criteria refinements
- Contact: artistso@github.com — ORCID 0009-0006-0211-4812

### 3. Bioengineers
- Hydrogel formulation improvements welcome
- Shear-thinning validation, FEniCSx poroelastic

### 4. Patients / Advocates
- Share https://artistso.github.io/synapshield/
- Sign Ocean Shores petition (on site)
- Email your story: artistso@github.com

---

## Development

```bash
git clone https://github.com/artistso/synapshield.git
cd synapshield
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python simulations/python/synapshield_pde_solver.py
```

**Code style:** Black, PEP8, numpy docstrings  
**Tests:** pytest — add to `tests/`  
**Commits:** Conventional Commits

---

## Citation

If you use SynapShield, cite:

> Owens, S. (2026). SynapShield: Intercepting Parkinson's Disease at the Gut-Brain Interface. *medRxiv*. doi:10.1101/TBD  
> ORCID: 0009-0006-0211-4812

See `CITATION.cff`.

---

## Code of Conduct

- Respectful, inclusive, patient-first
- No medical advice — research use only until FDA approval
- Open-source forever — MIT License

---

**From PDEs to Richard's tablet. Hope, not just science.**
