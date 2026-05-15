# Collision Matrix

| Claim | Baseline | After Rename | After Transfer | Trust-Relevant? | Expected |
|---|---|---|---|---|---|
| `sub` | `<value>` | `<value>` | `<value>` | Yes | Must not be ambiguous across different identities |
| `repository` | `<value>` | `<value>` | `<value>` | Yes | May change on rename/transfer |
| `repository_id` | `<value>` | `<value>` | `<value>` | Yes | Stable for same repo object; changed for recreated repo |
| `repository_owner` | `<value>` | `<value>` | `<value>` | Yes | May change on transfer |
| `repository_owner_id` | `<value>` | `<value>` | `<value>` | Yes | Changes on transfer to a different owner |
| `aud` | `<value>` | `<value>` | `<value>` | Yes | Same if same requested audience |
| `ref` | `<value>` | `<value>` | `<value>` | Yes | Same if branch unchanged |
| `job_workflow_ref` | `<value>` | `<value>` | `<value>` | Yes | Should reflect actual workflow repo/ref |

## Decision

| Indicator | Present? | Notes |
|---|---:|---|
| Subject collision | `<yes/no>` | `<notes>` |
| Config/runtime mismatch | `<yes/no>` | `<notes>` |
| Mutable vs immutable inconsistency | `<yes/no>` | `<notes>` |
| Dummy policy ambiguity | `<yes/no>` | `<notes>` |
