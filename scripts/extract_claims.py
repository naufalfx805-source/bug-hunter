#!/usr/bin/env python3
"""Normalize decoded GitHub Actions OIDC claim artifacts.

This script does not decode raw JWTs. It expects JSON emitted by the lab
workflow or a raw decoded OIDC claim object.
"""

import argparse
import json
from pathlib import Path

KEYS = [
    "iss",
    "aud",
    "sub",
    "repository",
    "repository_id",
    "repository_owner",
    "repository_owner_id",
    "repository_visibility",
    "ref",
    "ref_type",
    "workflow",
    "job_workflow_ref",
    "job_workflow_sha",
    "event_name",
]


def load_json(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("oidc_claims", data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract trust-relevant OIDC claims.")
    parser.add_argument("input", help="Decoded claims JSON or workflow artifact JSON")
    parser.add_argument("-o", "--output", help="Write normalized claims to this path")
    args = parser.parse_args()

    claims = load_json(args.input)
    normalized = {key: claims.get(key) for key in KEYS}

    text = json.dumps(normalized, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
