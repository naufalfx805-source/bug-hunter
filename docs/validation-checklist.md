# Validation Checklist

## Setup

- [ ] I own/control all GitHub accounts used.
- [ ] I own/control org A.
- [ ] I own/control org B.
- [ ] I created a new private lab repo.
- [ ] I copied only the lab workflows into the repo.
- [ ] I did not connect the repo to production cloud resources.
- [ ] I used a non-production audience value.

## Baseline

- [ ] Ran `OIDC Template Inspection`.
- [ ] Ran `OIDC Claim Inspection`.
- [ ] Downloaded decoded claim artifact.
- [ ] Saved workflow run URL.
- [ ] Built local dummy trust policy from baseline claims.

## Rename Scenario

- [ ] Renamed self-owned repo.
- [ ] Ran template inspection after rename.
- [ ] Ran claim inspection after rename.
- [ ] Compared baseline vs rename claims.
- [ ] Ran dummy verifier using baseline policy against rename-after claims.
- [ ] Recorded whether baseline policy allowed rename-after claims.

## Transfer Scenario

- [ ] Transferred self-owned repo from org A to org B.
- [ ] Ran template inspection after transfer.
- [ ] Ran claim inspection after transfer.
- [ ] Compared baseline vs transfer claims.
- [ ] Ran dummy verifier using baseline policy against transfer-after claims.
- [ ] Recorded whether baseline policy allowed transfer-after claims.

## Collision Indicators

- [ ] `sub` same while `repository` changed.
- [ ] `sub` same while `repository_id` changed.
- [ ] `sub` same while `repository_owner` changed.
- [ ] `sub` same while `repository_owner_id` changed.
- [ ] `repository` same while `repository_id` changed.
- [ ] `repository_owner` same while `repository_owner_id` changed.
- [ ] `aud`, `sub`, `ref`, `job_workflow_ref` all same while identity changed.
- [ ] Template config and runtime claims disagree.

## Report Quality

- [ ] Reproduction is deterministic.
- [ ] Evidence includes decoded selected claims, not raw JWTs.
- [ ] Impact is tied to a realistic trust policy.
- [ ] No third-party resource was accessed.
- [ ] No real cloud privilege was assumed.
- [ ] The report explains expected vs actual behavior.
