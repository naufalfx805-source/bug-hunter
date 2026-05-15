# GitHub Actions OIDC Subject Confusion After Repository Lifecycle Change

## Summary

I identified a GitHub Actions OIDC subject collision or trust ambiguity after a repository lifecycle change performed only on repositories and organizations I control.

The issue is that `<describe collision>` caused trust-relevant claims to remain equivalent while repository or owner identity changed.

## Affected Asset

- Service: GitHub Actions OIDC
- Issuer: `https://token.actions.githubusercontent.com`
- Tested organizations: `<ORG_A>`, `<ORG_B>`
- Tested repository: `<OWNER>/<REPO>`
- Workflow: `.github/workflows/oidc-claims.yml`

## Policy Compliance

All testing was performed using only self-owned accounts, organizations, and repositories. I did not access third-party data, perform scanning, use phishing, or assume real production cloud privileges. I included only decoded selected claims, not raw JWTs.

## Impact

Many relying parties authorize GitHub Actions workloads by matching claims such as `iss`, `aud`, `sub`, `ref`, and `job_workflow_ref`. If these claims remain equivalent across a changed repository or owner identity, a workflow from an unintended identity may satisfy a trust policy intended for another identity.

No real cloud role was assumed. I validated the ambiguity with a local dummy trust verifier.

## Steps to Reproduce

1. Create org A: `<ORG_A>`.
2. Create org B: `<ORG_B>`.
3. Create repo: `<ORG_A>/<REPO>`.
4. Add `.github/workflows/oidc-claims.yml`.
5. Run workflow with scenario `baseline`.
6. Save decoded selected claims.
7. Build a local dummy policy from baseline claims.
8. Perform lifecycle change: `<rename/transfer/recreate details>`.
9. Run workflow again with scenario `<scenario>`.
10. Compare claims and evaluate the after-state claims against the baseline local policy.

## Evidence

### Baseline Claims

```json
<baseline selected claims>
```

### After-State Claims

```json
<after selected claims>
```

### Collision Matrix

| Claim | Baseline | After | Status |
|---|---|---|---|
| `sub` | `<value>` | `<value>` | `<same/changed>` |
| `repository` | `<value>` | `<value>` | `<same/changed>` |
| `repository_id` | `<value>` | `<value>` | `<same/changed>` |
| `repository_owner` | `<value>` | `<value>` | `<same/changed>` |
| `repository_owner_id` | `<value>` | `<value>` | `<same/changed>` |
| `aud` | `<value>` | `<value>` | `<same/changed>` |
| `ref` | `<value>` | `<value>` | `<same/changed>` |
| `job_workflow_ref` | `<value>` | `<value>` | `<same/changed>` |

### Dummy Trust Verifier Result

```json
<dummy verifier output>
```

## Expected Behavior

The OIDC `sub` and related trust-relevant claims should not create ambiguity across repository rename, transfer, or recreation events. A different repository or owner identity should not be able to satisfy a trust policy intended for a previous identity unless that equivalence is explicit and documented.

## Actual Behavior

`<describe exact unexpected behavior>`

## Security Relevance

This is security-relevant because the token is GitHub-signed and intended for external authorization decisions. A relying party that matches the observed trust fields would authorize both the baseline and after-state identity.

## Suggested Remediation

- Bind default subject claims to immutable owner and repository identifiers.
- Prevent old mutable-name subjects from being minted by different identities.
- Ensure runtime token claims match OIDC customization template API output.
- Provide explicit migration or warning signals for legacy mutable subject formats.

## Attachments

- Baseline workflow run: `<url>`
- After workflow run: `<url>`
- `baseline-claims.json`
- `after-claims.json`
- `collision-analysis.json`
- `dummy-verifier-output.json`
