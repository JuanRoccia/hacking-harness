#!/usr/bin/env python3
"""Wrapper unificado para sqlmap."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone


def run(target: str, args: list[str] | None = None) -> dict:
    start = time.time()
    extra = args or []
    cmd = ["sqlmap", "-u", target, "--batch", "--random-agent"] + extra
    if "--output-dir" not in str(cmd):
        cmd += ["--output-dir=/tmp/sqlmap-output"]
    cmd_str = " ".join(cmd)

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600
        )
    except subprocess.TimeoutExpired:
        return {
            "tool": "sqlmap", "status": "timeout",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": cmd_str, "duration_ms": int((time.time() - start) * 1000),
            "error": "Timeout after 600s", "findings": []
        }
    except FileNotFoundError:
        return {
            "tool": "sqlmap", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": cmd_str, "duration_ms": int((time.time() - start) * 1000),
            "error": "sqlmap not found", "findings": []
        }

    output = result.stdout + result.stderr
    findings = []
    vulnerable_params = []
    for line in output.splitlines():
        if "Parameter:" in line and "GET" in line:
            vulnerable_params.append(line.strip())
        if "GET parameter" in line and "is vulnerable" in line.lower():
            vulnerable_params.append(line.strip())

    for param in set(vulnerable_params):
        findings.append({
            "id": f"sqli-{hash(param) % 100000}",
            "severity": "critical",
            "title": "SQL Injection vulnerability",
            "description": param,
            "url": target,
            "evidence": param,
            "recommendation": "Use parameterized queries / prepared statements"
        })

    if result.returncode != 0 and not findings:
        return {
            "tool": "sqlmap", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": cmd_str, "duration_ms": int((time.time() - start) * 1000),
            "error": result.stderr.strip()[:500], "findings": []
        }

    return {
        "tool": "sqlmap", "status": "success",
        "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": cmd_str, "duration_ms": int((time.time() - start) * 1000),
        "summary": {"total": len(findings), "vulnerable": len(findings)},
        "findings": findings,
        "raw_output": output
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"tool": "sqlmap-wrapper", "status": "error",
                          "error": "Usage: sqlmap-wrapper.py <url> [extra args...]"}))
        sys.exit(1)
    print(json.dumps(run(sys.argv[1], sys.argv[2:]), indent=2))
