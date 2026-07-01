# Security Policy — SynapShield

**Maintainer:** Steven Owens — ORCID: [0009-0006-0211-4812](https://orcid.org/0009-0006-0211-4812)  
**Contact:** artistso@github.com  
**Version:** v1.0.1 — June 30, 2026

---

## Reporting a Vulnerability

Email **artistso@github.com** with subject `[SECURITY] SynapShield`.

- Response time: <72 hours
- Coordinated disclosure preferred
- Open-source MIT — public repo

---

## Known Exposures (documented, accepted risk)

As of 2026-06-30, the following GitHub tokens have been exposed in this repository and in related communications. The author is aware and accepts the risk (no billing attached, tokens will be revoked per operational workflow).

| Token prefix | Location | Status |
|--------------|----------|--------|
| `REDACTED-GH-TOKEN-REVOKED` | `DEPLOYMENT_GUIDE.md` line 104, commit `131ba09` | **EXPOSED in public git history** — revoke immediately if still active |
| `github_pat_11CFIM5QQ0...` | Provided in support chat 2026-06-30, used in `git remote -v` origin URL | **EXPOSED** — user states: "I'm not worried … tokens will eventually be revoked" |

**Mitigation (recommended, not yet applied):**
1. Revoke both at https://github.com/settings/tokens
2. `git filter-repo --replace-text` to purge `131ba09`
3. Force-push clean history
4. Enable GitHub secret scanning: Settings → Code security → Secret scanning → Enable
5. Add pre-commit hook: `trufflehog` or `gitleaks`

The repository owner has explicitly declined immediate revocation ("I'm not worried … It says a token issue thing. I just have to keep redoing workspaces").

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.1   | ✅ Yes — current |
| 1.0.0   | ✅ Yes |
| <1.0.0  | ❌ No |

---

## Security Best Practices for Contributors

- Never commit tokens, API keys, PATs
- Use GitHub fine-grained PATs, 7-day expiry, repo:read minimum
- Enable 2FA on GitHub account
- Run `gitleaks detect --source . -v` before push
- See `.github/secret_scanning.yml` (planned)

---

## Medical Disclaimer

SynapShield is **computational research software — NOT a medical device**.

- Research use only. Not FDA approved.
- No clinical claims until Phase I-III completion.
- MIT License — NO WARRANTY.
- Always consult licensed physicians.

Preprint: medRxiv 10.1101/TBD — ORCID 0009-0006-0211-4812

---

*Hope, not just science. — Dedicated to Richard, Ocean Shores, WA*
