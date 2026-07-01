# Changelog

All notable changes to SynapShield are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.1] - 2026-06-30

### Added
- **ORCID integration:** Steven Owens - https://orcid.org/0009-0006-0211-4812 - across all files
- **medRxiv preprint metadata:** submitted June 30, 2026 - DOI 10.1101/TBD (pending)
- `LICENSE` - MIT, with ORCID + dedication
- `CITATION.cff` - machine-readable citation, v1.2.0
- `codemeta.json` - CodeMeta 2.0
- `.zenodo.json` - Zenodo archival metadata
- `AUTHORS.md` - CRediT roles, ORCID, affiliations, BibTeX
- `CONTRIBUTING.md` - contributor guide
- `docs/medrxiv_submission.md` - preprint checklist
- `CHANGELOG.md` - this file
- Cite section in `index.html` (#cite) with BibTeX, ORCID badge, medRxiv banner
- preprint banner in `index.html` (top, persistent)
- citation meta tags in `<head>` (`citation_author_orcid`, `citation_doi`, etc.)
- Live GitHub API integration (replacing simulated counters)

### Changed
- `README.md` - full academic rewrite: badges (medRxiv, ORCID, DOI, License), author block, preprint citation, pinned requirements, metadata table
- `TECHNICAL_PAPER.md` - author: Steven Owens, ORCID 0009-0006-0211-4812, medRxiv header, updated references, Data/Code Availability section, v1.0.1
- `docs/CLINICAL_BRIEFING.md` - added ORCID, medRxiv DOI, v1.0.1 header, updated contact block
- `index.html` - medRxiv preprint banner, ORCID in header/nav/footer, #cite section, fixed duplicate #neuralCanvas CSS, GitHub API live data
- `requirements.txt` - pinned: numpy==1.26.4, scipy==1.13.1, matplotlib==3.9.0, pandas==2.2.2, scikit-learn==1.5.0, pytest==8.2.2, numba==0.60.0

### Fixed
- Removed duplicate `#neuralCanvas` CSS in `index.html`
- `kErosion` slider step noted (Chrome 1e-8 rounding - documented)
- requirements versions unpinned → now fully pinned reproducible stack

### Security
- Documented exposed tokens: `REDACTED-GH-TOKEN-REVOKED` (in git history 131ba09) and `github_pat_11CFIM5QQ0...` - see `SECURITY.md`
- Added secret-scanning recommendation

---

## [1.0.0] - 2026-06-30

### Added
- Initial public release - tagged v1.0.0
- `index.html` - 1,178-line interactive web app, split-screen PDE + simulation
- `simulations/python/synapshield_pde_solver.py` - 4-species PDE solver (361 lines)
- `simulations/matlab/synapshield_pde_solver.m`
- `simulations/python/fenicsx_poroelastic.py`
- `simulations/python/multiphysics_integration.py`
- `TECHNICAL_PAPER.md` - publication-ready
- `docs/CLINICAL_BRIEFING.md` - CPT 43256, DTI-ALPS endpoints
- `docs/math-models.md`
- `RICHARD_HANDOUT.html`
- `TECHNICAL_TRANSCRIPT.md`
- `DEPLOYMENT_GUIDE.md`
- `deploy_synapshield.sh`
- GitHub Pages workflow `.github/workflows/deploy-pages.yml`
- Live site: https://artistso.github.io/synapshield/

**Author:** artistso / Steven Owens  
**Dedication:** Richard - Ocean Shores, WA  
**License:** MIT

---

## Preprint

- **medRxiv:** submitted 2026-06-30
- **DOI:** 10.1101/TBD (pending)
- **ORCID:** 0009-0006-0211-4812
- **Author:** Steven Owens, Computational Bioengineering Laboratory, Ocean Shores, Washington, USA
