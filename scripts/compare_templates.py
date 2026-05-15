#!/usr/bin/env python3
"""Compare OIDC template inspection output before and after lifecycle events."""

import argparse
import json
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_claims(path: str) -> dict:
    data = load(path)
    return data.get("oidc_claims", data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect OIDC template config/runtime mismatch indicators.")
    parser.add_argument("before_template")
    parser.add_argument("after_template")
    parser.add_argument("--before-claims")
    parser.add_argument("--after-claims")
    args = parser.parse_args()

    before_template = load(args.before_template)
    after_template = load(args.after_template)
    result = {
        "repo_template_changed": before_template.get("repo_template") != after_template.get("repo_template"),
        "org_template_changed": before_template.get("org_template") != after_template.get("org_template"),
        "before_template": before_template,
        "after_template": after_template,
        "runtime_notes": [],
    }

    if args.before_claims and args.after_claims:
        before_claims = load_claims(args.before_claims)
        after_claims = load_claims(args.after_claims)
        if before_claims.get("sub") == after_claims.get("sub") and before_claims.get("repository") != after_claims.get("repository"):
            result["runtime_notes"].append("Runtime sub stayed identical while repository changed.")
        if before_claims.get("sub") == after_claims.get("sub") and before_claims.get("repository_owner_id") != after_claims.get("repository_owner_id"):
            result["runtime_notes"].append("Runtime sub stayed identical while repository_owner_id changed.")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
