#!/usr/bin/env python3
"""Wrapper unificado para Burp Suite REST API."""

from __future__ import annotations

import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone


def run(target: str, args: list[str] | None = None) -> dict:
    start = time.time()
    api_host = args[0] if args and args[0] else "127.0.0.1"
    api_port = args[1] if len(args or []) > 1 else "1337"
    base_url = f"http://{api_host}:{api_port}"

    try:
        req = urllib.request.Request(f"{base_url}/health")
        with urllib.request.urlopen(req, timeout=5) as resp:
            health = json.loads(resp.read().decode())
    except Exception as e:
        return {
            "tool": "burp", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"burp api health on {base_url}",
            "duration_ms": int((time.time() - start) * 1000),
            "error": f"Cannot connect to Burp API: {e}", "findings": []
        }

    try:
        scan_req = urllib.request.Request(
            f"{base_url}/v0.1/scan",
            data=json.dumps({"urls": [target], "scope": {}}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(scan_req, timeout=30) as resp:
            scan_result = json.loads(resp.read().decode())

        findings = []
        issues = scan_result.get("issues", scan_result.get("data", []))
        if not isinstance(issues, list):
            issues = [issues]

        for issue in issues:
            sev_map = {
                "high": "high", "medium": "medium", "low": "low",
                "information": "info", "certain": "high", "firm": "medium",
                "tentative": "low"
            }
            sev = issue.get("severity", issue.get("confidence", "info")).lower()
            mapped = sev_map.get(sev, "info")
            findings.append({
                "id": issue.get("id", issue.get("name", "unknown")),
                "severity": mapped,
                "title": issue.get("name", issue.get("issue", "Unknown")),
                "description": issue.get("description", issue.get("detail", "")),
                "url": issue.get("url", target),
                "evidence": issue.get("evidence", issue.get("request", "")),
                "recommendation": issue.get("remediation", issue.get("solution", ""))
            })

        return {
            "tool": "burp", "status": "success",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"burp scan on {target} via {base_url}",
            "duration_ms": int((time.time() - start) * 1000),
            "summary": {
                "total": len(findings),
                "vulnerable": len([f for f in findings if f["severity"] in ("critical", "high", "medium")])
            },
            "findings": findings,
            "raw_output": json.dumps(scan_result)
        }
    except urllib.error.HTTPError as e:
        return {
            "tool": "burp", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"burp scan on {target}",
            "duration_ms": int((time.time() - start) * 1000),
            "error": f"HTTP {e.code}: {e.reason}", "findings": []
        }
    except Exception as e:
        return {
            "tool": "burp", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"burp scan on {target}",
            "duration_ms": int((time.time() - start) * 1000),
            "error": str(e), "findings": []
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"tool": "burp-wrapper", "status": "error",
                          "error": "Usage: burp-wrapper.py <target> [api_host] [api_port]"}))
        sys.exit(1)
    print(json.dumps(run(sys.argv[1], sys.argv[2:]), indent=2))
