# Bug Hunter

Security research and bug-fixing workspace focused on GitHub Actions, CI/CD trust boundaries, OIDC, and reproducible proof-of-concept labs.

This repository is used to keep research notes, controlled experiments, report templates, and small utilities that turn a suspected bug into evidence that can be reviewed and fixed.

## Research Areas

- GitHub Actions workflow permissions and trust boundaries
- OIDC claim behavior across repository, branch, and workflow changes
- Reusable workflow permission propagation
- Artifact and cache handling between low-trust and high-trust workflow contexts
- Minimal open-source bug fixes with clear reproduction steps

## Repository Structure

| Path | Purpose |
|---|---|
| `.github/workflows/` | Controlled GitHub Actions labs and evidence-capture workflows |
| `docs/` | Methodology, validation checklists, and report templates |
| `labs/` | Lab descriptions and repeatable experiment plans |
| `notes/` | Research notes, dead ends, and investigation logs |
| `pocs/` | Proof-of-concept writeups and reproduction assets |
| `reports/` | Draft security reports and responsible disclosure material |
| `runs/` | Local evidence snapshots from completed test runs |
| `scripts/` | Helpers for claim extraction, comparison, and local policy checks |

## Active Labs

### GitHub Actions OIDC Subject Confusion

Validates whether GitHub Actions OIDC tokens can produce trust-relevant claim collisions across repository lifecycle changes such as rename, transfer, and self-owned name recreation.

Key documents:

- [`docs/testing-methodology.md`](docs/testing-methodology.md)
- [`docs/validation-checklist.md`](docs/validation-checklist.md)
- [`docs/collision-matrix-template.md`](docs/collision-matrix-template.md)
- [`docs/hackerone-report-template.md`](docs/hackerone-report-template.md)

### GitHub Actions Trust-Boundary Harness

Tests workflow-run artifacts, branch-originated cache behavior, and reusable workflow permission propagation.

Current result: no deterministic GitHub authorization-boundary vulnerability confirmed in the tested scenarios. The useful output is a repeatable harness and evidence model for checking whether privileged workflow consumers validate provenance correctly.

Summary:

- [`docs/trust-boundary-harness-summary.md`](docs/trust-boundary-harness-summary.md)

## Quick Start

Run local helpers against captured claim artifacts:

```bash
python scripts/build_policy_from_claims.py baseline/oidc-claims.json -o baseline-policy.json
python scripts/compare_claims.py baseline/oidc-claims.json after/oidc-claims.json
python scripts/dummy_trust_verifier.py baseline-policy.json after/oidc-claims.json
```

If the after-state claims satisfy the baseline trust policy while repository or owner identity changed, investigate for subject confusion.

## Safety Rules

- Test only organizations, repositories, branches, and accounts you control.
- Do not test third-party organizations or attempt to reclaim names previously owned by other people.
- Do not connect these labs to production AWS, Azure, GCP, npm, or other external services.
- Do not print or store raw JWTs. Store decoded, selected claims only.
- Stop if any test exposes data or permissions outside your own assets.

## Reporting Standard

Every useful finding should include:

- clear impact statement
- affected trust boundary
- exact reproduction steps
- expected and observed behavior
- evidence artifacts or run IDs
- minimal fix or mitigation
- dead-end notes when behavior is expected or not exploitable

Use [`reports/report-template.md`](reports/report-template.md) for new drafts.
