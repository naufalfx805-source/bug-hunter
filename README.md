# GitHub Actions OIDC Subject Confusion Lab

This lab validates potential GitHub Actions OIDC subject confusion using only self-owned GitHub accounts, organizations, and repositories. It avoids real cloud access and models trust decisions locally.

## Safety Rules

- Test only organizations, repositories, branches, and accounts you control.
- Do not test third-party organizations or attempt to reclaim names previously owned by other people.
- Do not connect this lab to production AWS, Azure, GCP, npm, or other services.
- Do not print or store raw JWTs. Store decoded, selected claims only.
- Stop if any test exposes data or permissions outside your own assets.

## Files

- `.github/workflows/oidc-claims.yml`: generates decoded selected OIDC claims.
- `.github/workflows/oidc-template-inspection.yml`: captures configured OIDC subject templates.
- `.github/workflows/oidc-claims-matrix.yml`: minimal matrix run for repeatability.
- `scripts/extract_claims.py`: normalizes claim artifacts.
- `scripts/compare_claims.py`: generates collision matrix and findings.
- `scripts/build_policy_from_claims.py`: creates local dummy trust policy from baseline claims.
- `scripts/dummy_trust_verifier.py`: evaluates decoded claims against a local policy.
- `scripts/compare_templates.py`: compares template config and runtime indicators.
- `docs/testing-methodology.md`: practical test workflow.
- `docs/validation-checklist.md`: step-by-step checklist.
- `docs/hackerone-report-template.md`: report template for confirmed collisions.

## Quick Start

1. Create two GitHub organizations you control:
   - `oidc-lab-a-<random>`
   - `oidc-lab-b-<random>`
2. Create a private repository in org A:
   - `oidc-subject-lab`
3. Copy `.github/workflows/*.yml` into that repository.
4. Commit and push.
5. Run `OIDC Claim Inspection` with scenario `baseline`.
6. Download the `oidc-claims-...` artifact.
7. Build a dummy policy:

```bash
python scripts/build_policy_from_claims.py baseline/oidc-claims.json -o baseline-policy.json
```

8. Rename or transfer the self-owned repo, run the workflow again, then compare:

```bash
python scripts/compare_claims.py baseline/oidc-claims.json after/oidc-claims.json
python scripts/dummy_trust_verifier.py baseline-policy.json after/oidc-claims.json
```

If the after-state claims satisfy the baseline trust policy while repository or owner identity changed, investigate for subject confusion.
