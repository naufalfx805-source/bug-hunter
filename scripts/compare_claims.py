#!/usr/bin/env python3
"""Compare OIDC claim artifacts for subject confusion indicators."""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List

COMPARE_KEYS = [
    "sub",
    "repository",
    "repository_id",
    "repository_owner",
    "repository_owner_id",
    "aud",
    "ref",
    "job_workflow_ref",
]

IDENTITY_KEYS = [
    "repository",
    "repository_id",
    "repository_owner",
    "repository_owner_id",
]

TRUST_KEYS = [
    "sub",
    "aud",
    "ref",
    "job_workflow_ref",
]


def load_claims(path: str) -> Dict[str, object]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("oidc_claims", data)


def val(claims: Dict[str, object], key: str) -> str:
    value = claims.get(key)
    return "<missing>" if value is None else str(value)


def row(before: Dict[str, object], after: Dict[str, object], key: str) -> Dict[str, str]:
    before_value = val(before, key)
    after_value = val(after, key)
    return {
        "claim": key,
        "before": before_value,
        "after": after_value,
        "status": "same" if before_value == after_value else "changed",
    }


def detect(before: Dict[str, object], after: Dict[str, object]) -> List[Dict[str, str]]:
    findings: List[Dict[str, str]] = []
    sub_same = val(before, "sub") == val(after, "sub")
    identity_changed = any(val(before, key) != val(after, key) for key in IDENTITY_KEYS)
    trust_same = [key for key in TRUST_KEYS if val(before, key) == val(after, key)]

    if sub_same and identity_changed:
        findings.append({
            "id": "SUB_COLLISION_WITH_IDENTITY_CHANGE",
            "severity": "high",
            "title": "Subject collision while repository or owner identity changed",
            "evidence": "sub stayed identical while one or more identity claims changed",
        })

    if val(before, "repository") == val(after, "repository") and val(before, "repository_id") != val(after, "repository_id"):
        findings.append({
            "id": "MUTABLE_REPO_NAME_REUSED",
            "severity": "medium",
            "title": "Same repository full name maps to a different repository_id",
            "evidence": "repository stayed identical while repository_id changed",
        })

    if val(before, "repository_owner") == val(after, "repository_owner") and val(before, "repository_owner_id") != val(after, "repository_owner_id"):
        findings.append({
            "id": "MUTABLE_OWNER_NAME_REUSED",
            "severity": "medium",
            "title": "Same owner name maps to a different repository_owner_id",
            "evidence": "repository_owner stayed identical while repository_owner_id changed",
        })

    if len(trust_same) == len(TRUST_KEYS) and identity_changed:
        findings.append({
            "id": "TRUST_POLICY_AMBIGUITY",
            "severity": "high",
            "title": "Common trust-policy fields are identical across changed identity",
            "evidence": "sub, aud, ref, and job_workflow_ref are identical while identity changed",
        })

    return findings


def print_markdown_table(rows: List[Dict[str, str]]) -> None:
    print("| Claim | Before | After | Status |")
    print("|---|---|---|---|")
    for item in rows:
        print(f"| `{item['claim']}` | `{item['before']}` | `{item['after']}` | {item['status']} |")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare before/after OIDC claims.")
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--csv", dest="csv_path", help="Write comparison matrix as CSV")
    parser.add_argument("--json", dest="json_path", help="Write full analysis as JSON")
    args = parser.parse_args()

    before = load_claims(args.before)
    after = load_claims(args.after)
    matrix = [row(before, after, key) for key in COMPARE_KEYS]
    findings = detect(before, after)

    print("# Collision Matrix")
    print_markdown_table(matrix)
    print("\n# Findings")
    if findings:
        for finding in findings:
            print(f"- [{finding['severity'].upper()}] {finding['id']}: {finding['title']}")
            print(f"  Evidence: {finding['evidence']}")
    else:
        print("- No subject collision or trust-policy ambiguity detected.")

    output = {"matrix": matrix, "findings": findings}
    if args.csv_path:
        with Path(args.csv_path).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["claim", "before", "after", "status"])
            writer.writeheader()
            writer.writerows(matrix)
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
