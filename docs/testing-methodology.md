# Testing Methodology

## Research Goal

Determine whether GitHub Actions OIDC tokens can produce trust-relevant claim collisions across repository lifecycle changes:

- repository rename
- organization transfer
- optional self-owned name recreation

The focus is identity and trust-boundary confusion, not cloud privilege escalation.

## Trust-Relevant Claims

Compare these claims in every run:

| Claim | Why It Matters |
|---|---|
| `sub` | Primary subject commonly used in relying-party trust policies |
| `repository` | Mutable owner/repo name |
| `repository_id` | Immutable repository object identity |
| `repository_owner` | Mutable owner name |
| `repository_owner_id` | Immutable owner identity |
| `aud` | Relying-party audience |
| `ref` | Branch/tag trust condition |
| `job_workflow_ref` | Workflow identity and reusable workflow boundary |

## Repository Setup

1. Create two organizations you control:
   - `oidc-lab-a-<random>`
   - `oidc-lab-b-<random>`
2. In org A, create `oidc-subject-lab`.
3. Copy the lab workflows into `.github/workflows/`.
4. Commit on `main`.
5. Confirm Actions is enabled.

## Baseline Capture

1. Run `OIDC Template Inspection` with scenario `baseline`.
2. Run `OIDC Claim Inspection` with scenario `baseline` and audience `https://example.invalid/oidc-subject-lab`.
3. Download artifacts.
4. Normalize if needed:

```bash
python scripts/extract_claims.py baseline/oidc-claims.json -o baseline-normalized.json
```

5. Build a local trust policy:

```bash
python scripts/build_policy_from_claims.py baseline/oidc-claims.json -o baseline-policy.json
```

## Repository Rename Test Plan

1. Rename the repository in the same organization from `oidc-subject-lab` to `oidc-subject-lab-renamed`.
2. Run `OIDC Template Inspection` with scenario `rename-after`.
3. Run `OIDC Claim Inspection` with scenario `rename-after`.
4. Compare:

```bash
python scripts/compare_claims.py baseline/oidc-claims.json rename-after/oidc-claims.json --csv rename-collision-matrix.csv --json rename-analysis.json
python scripts/dummy_trust_verifier.py baseline-policy.json rename-after/oidc-claims.json
```

## Organization Transfer Test Plan

1. Transfer the repository from org A to org B.
2. Keep branch and workflow unchanged.
3. Run `OIDC Template Inspection` with scenario `transfer-after`.
4. Run `OIDC Claim Inspection` with scenario `transfer-after`.
5. Compare:

```bash
python scripts/compare_claims.py baseline/oidc-claims.json transfer-after/oidc-claims.json --csv transfer-collision-matrix.csv --json transfer-analysis.json
python scripts/dummy_trust_verifier.py baseline-policy.json transfer-after/oidc-claims.json
```

## Config/Runtime Mismatch Test

```bash
python scripts/compare_templates.py baseline/oidc-template-inspection.json transfer-after/oidc-template-inspection.json --before-claims baseline/oidc-claims.json --after-claims transfer-after/oidc-claims.json
```

## Expected Secure Behavior

- `repository_id` remains stable for the same repository object.
- `repository_owner_id` changes when ownership changes.
- `sub` should not let a new or different identity impersonate a prior trusted identity.
- Runtime `sub` should match documented or configured OIDC subject template behavior.
- A local dummy policy built from baseline identity should not authorize a materially different identity unless that is explicitly intended by the policy fields.

## Unexpected Behavior

Treat these as suspicious:

- `sub` remains identical while `repository_id` changes.
- `sub` remains identical while `repository_owner_id` changes.
- `repository` remains identical while `repository_id` changes.
- `repository_owner` remains identical while `repository_owner_id` changes.
- `sub`, `aud`, `ref`, and `job_workflow_ref` all match baseline while repository or owner identity changed.
- OIDC template API output indicates one subject format while runtime token claims use another.

## Potential Security Impact

A real relying party may authorize a GitHub-signed OIDC token based on `sub`, `aud`, `ref`, and `job_workflow_ref`. If those fields collide across different repository identities, a workflow from the wrong repository context may satisfy a trust policy intended for the original repository.

Do not demonstrate this with real cloud privilege escalation. Show local policy equivalence with decoded claims and a dummy verifier.
