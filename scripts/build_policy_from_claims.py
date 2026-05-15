#!/usr/bin/env python3
"""Build a dummy trust policy from decoded claims."""

import argparse
import json
from pathlib import Path

DEFAULT_POLICY_KEYS = ["iss", "aud", "sub", "ref", "job_workflow_ref"]


def load_claims(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("oidc_claims", data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a local dummy trust policy from decoded OIDC claims.")
    parser.add_argument("claims")
    parser.add_argument("-o", "--output", default="dummy-trust-policy.json")
    parser.add_argument("--keys", nargs="+", default=DEFAULT_POLICY_KEYS)
    args = parser.parse_args()

    claims = load_claims(args.claims)
    policy = {key: claims.get(key) for key in args.keys}
    Path(args.output).write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(policy, indent=2))


if __name__ == "__main__":
    main()
