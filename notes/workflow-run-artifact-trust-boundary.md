# GitHub Actions `workflow_run` Artifact Trust Boundary

Date: 2026-05-16
Status: Expected behavior, useful risk pattern

## Summary

This note documents a controlled GitHub Actions test where a default-branch `workflow_run` consumer downloaded an artifact produced by a lower-trust branch workflow run.

This is not a GitHub authorization-boundary vulnerability by itself. The API exposes enough provenance for a correctly written consumer workflow to identify where the artifact came from. The risk appears when a privileged consumer treats the artifact as trusted input without checking that provenance.

## What Was Tested

The lab used two workflows:

- a producer workflow running from a lower-trust branch
- a default-branch consumer workflow triggered through `workflow_run`

The consumer used the triggering run ID to download the producer artifact and inspect its metadata.

## Evidence

Evidence window: 2026-05-16 21:46-21:53 UTC

Observed values:

- Low-trust producer run: `25973891795`
- Low-trust branch: `tb-lowtrust-artifact-cache`
- Low-trust head SHA: `abe565d32b48324dfc335d8dee51f9f828584abc`
- Consumer run: `25973895584`
- Consumer ref: `refs/heads/main`
- Artifact: `tb-workflow-run-producer-25973891795-1`
- Downloaded marker: `LOWTRUST_ARTIFACT_MARKER_2026-05-17TLOCAL`

Artifact provenance was available through the API object:

- `workflow_run.id=25973891795`
- `head_branch=tb-lowtrust-artifact-cache`
- `head_sha=abe565d32b48324dfc335d8dee51f9f828584abc`

Local evidence path:

- `runs/tb-evidence/consumer_branch_after_merge/workflow-run-consumer.json`

## Why This Is Expected Behavior

A `workflow_run` consumer is allowed to run from the default branch after another workflow completes. If the consumer explicitly uses the triggering `run_id`, it can download artifacts from that triggering run.

The important point is that GitHub includes provenance fields that identify the producer run, branch, and commit. A secure consumer can reject artifacts from untrusted refs or unexpected repositories.

## When It Becomes Risky

This pattern can become risky when a privileged default-branch consumer workflow:

- downloads artifacts from a triggering workflow run
- parses or executes artifact contents
- uploads results to a privileged location
- deploys, signs, publishes, or comments based on artifact contents
- skips validation of `head_branch`, `head_sha`, `head_repository_id`, or equivalent provenance

In that design, a lower-trust workflow may influence a higher-trust workflow through artifact contents.

## Maintainer Checklist

Before trusting artifacts in a `workflow_run` consumer:

- verify the triggering repository identity
- verify the triggering branch or tag
- verify the triggering commit SHA if the workflow expects a specific ref
- reject artifacts from forks or low-trust branches unless explicitly intended
- treat artifact contents as untrusted input
- avoid executing files directly from artifacts
- prefer structured, validated data over arbitrary files
- keep privileged tokens away from artifact-processing steps when possible

## Classification

Result: expected secure platform behavior.

No deterministic GitHub authorization-boundary vulnerability was confirmed in this scenario. The useful finding is the implementation risk pattern: privileged consumers must validate artifact provenance before trusting data from `workflow_run` artifacts.

## Related Lab Material

- `docs/trust-boundary-harness-summary.md`
- `.github/workflows/tb-workflow-run-producer.yml`
- `.github/workflows/tb-workflow-run-consumer.yml`
