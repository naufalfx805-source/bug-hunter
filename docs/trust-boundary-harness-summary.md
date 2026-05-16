# Trust-Boundary Harness Summary

UTC evidence window: 2026-05-16 21:46-21:53.

## Scenario 1: `workflow_run` Artifact Trust

Expected: a default-branch `workflow_run` consumer is triggered by completion of the producer workflow and can download artifacts from the triggering run when explicitly given the triggering `run_id`.

Evidence:

- Low-trust producer run: `25973891795`
- Low-trust branch: `tb-lowtrust-artifact-cache`
- Low-trust head SHA: `abe565d32b48324dfc335d8dee51f9f828584abc`
- Consumer run: `25973895584`
- Consumer ref/SHA: `refs/heads/main` / `314bda21d9a91e99f92f5026481245cdedecd0b4`
- Artifact: `tb-workflow-run-producer-25973891795-1`
- Artifact provenance in API object: `workflow_run.id=25973891795`, `head_branch=tb-lowtrust-artifact-cache`, `head_sha=abe565d32b48324dfc335d8dee51f9f828584abc`
- Downloaded marker: `LOWTRUST_ARTIFACT_MARKER_2026-05-17TLOCAL`
- Local evidence: `runs/tb-evidence/consumer_branch_after_merge/workflow-run-consumer.json`

Classification: interesting but expected. No authorization-boundary break by itself because provenance is present and the consumer used the triggering run ID. Exploitable only if a privileged consumer treats the producer artifact as trusted without checking `head_branch`, `head_sha`, and `head_repository_id`.

## Scenario 2: Branch-Originated Cache Poisoning

Expected: a default-branch run should not restore a cache saved only from a non-default branch using the same key.

Evidence:

- Branch cache producer run: `25973891794`
- Cache key: `tb-cross-branch-cache-v1`
- Branch marker: `LOWTRUST_CACHE_MARKER_2026-05-17TLOCAL`
- Branch ref/SHA: `refs/heads/tb-lowtrust-artifact-cache` / `abe565d32b48324dfc335d8dee51f9f828584abc`
- Final main cache consumer run: `25973918555`
- Main ref/SHA: `refs/heads/main` / `e21b4ed3d486bf39e275c516d155c182031a3af0`
- Cache hit: empty / false
- Restored marker: empty
- Local evidence: `runs/tb-evidence/cacheprod_branch_after_merge/cache-producer.json`, `runs/tb-evidence/cachemain_final/cache-consumer.json`

Classification: expected secure behavior. Dead end for lower-trust branch to main cache poisoning in this harness.

## Scenario 3: Reusable Workflow Permission Propagation

Expected: a reusable workflow cannot obtain `id-token: write` unless the caller grants it; when granted, OIDC claims should bind both the caller ref and the reusable workflow ref/SHA.

Evidence:

- No-id-token caller run: `25973849239`
- Result: `startup_failure`, zero jobs created
- Interpretation: secure enforcement before execution; the callee's `id-token: write` request was not allowed under a caller job without `id-token`.

Positive control:

- Main caller run: `25973872730`
- Main OIDC `sub`: `repo:naufalfx805-source/bug-hunter:ref:refs/heads/main`
- Main `job_workflow_ref`: `naufalfx805-source/bug-hunter/.github/workflows/tb-reusable-callee.yml@refs/heads/main`
- Main `job_workflow_sha`: `314bda21d9a91e99f92f5026481245cdedecd0b4`
- Local evidence: `runs/tb-evidence/reusable_with_id/reusable-callee-reusable-caller-with-id-token.json`

Low-trust branch control:

- Branch caller run: `25973891790`
- Branch OIDC `sub`: `repo:naufalfx805-source/bug-hunter:ref:refs/heads/tb-lowtrust-artifact-cache`
- Branch `job_workflow_ref`: `naufalfx805-source/bug-hunter/.github/workflows/tb-reusable-callee.yml@refs/heads/tb-lowtrust-artifact-cache`
- Branch `job_workflow_sha`: `abe565d32b48324dfc335d8dee51f9f828584abc`
- Local evidence: `runs/tb-evidence/reusable_branch/reusable-callee-reusable-caller-with-id-token.json`

Classification: expected secure behavior. No caller/callee provenance confusion observed; branch-originated reusable calls remain distinguishable in `sub`, `ref`, `job_workflow_ref`, and `job_workflow_sha`.

## Current Escalation Status

No deterministic GitHub authorization-boundary vulnerability found in these scenarios. The only interesting behavior is the documented `workflow_run` pattern where default-branch consumers can process artifacts from lower-trust branch runs; the evidence includes sufficient provenance for a correctly written consumer to reject those artifacts.

