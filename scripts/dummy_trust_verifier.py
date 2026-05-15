#!/usr/bin/env python3
"""Local verifier for trust-policy ambiguity.

This intentionally does not validate a live JWT or assume any cloud role. It
models how a relying party might compare decoded claims to a trust policy.
"""

import argparse
import json
from pathlib import Path
from typing import Dict


def load_claims(path: str) -> Dict[str, object]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("oidc_claims", data)


def load_policy(path: str) -> Dict[str, str]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evaluate(policy: Dict[str, str], claims: Dict[str, object]) -> Dict[str, object]:
    checks = []
    for key, expected in policy.items():
        actual = claims.get(key)
        checks.append({
            "claim": key,
            "expected": expected,
            "actual": actual,
            "matched": str(actual) == str(expected),
        })
    return {
        "allowed": all(item["matched"] for item in checks),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate decoded OIDC claims against a local dummy trust policy.")
    parser.add_argument("policy", help="JSON object mapping claim names to required values")
    parser.add_argument("claims", help="Decoded claims JSON or workflow artifact JSON")
    args = parser.parse_args()

    result = evaluate(load_policy(args.policy), load_claims(args.claims))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
