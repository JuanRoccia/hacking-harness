#!/usr/bin/env python3
"""Wrapper unificado para Caido REST API."""

from __future__ import annotations

import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone


def run(target: str, args: list[str] | None = None) -> dict:
    start = time.time()
    api_url = args[0] if args and args[0] else "http://127.0.0.1:8080"
    api_url = api_url.rstrip("/")

    try:
        health_req = urllib.request.Request(f"{api_url}/api/health")
        with urllib.request.urlopen(health_req, timeout=5) as resp:
            health = json.loads(resp.read().decode())
    except Exception as e:
        return {
            "tool": "caido", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"caido api on {api_url}",
            "duration_ms": int((time.time() - start) * 1000),
            "error": f"Cannot connect to Caido API: {e}", "findings": []
        }

    try:
        scan_payload = json.dumps({"target": target, "replay": True}).encode()
        scan_req = urllib.request.Request(
            f"{api_url}/api/replay",
            data=scan_payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(scan_req, timeout=60) as resp:
            result = json.loads(resp.read().decode())

        findings = []
        entries = result if isinstance(result, list) else [result]
        for entry in entries:
            status_code = entry.get("status", 0)
            path = entry.get("path", "/")
            has_vuln = any(
                kw in str(entry.get("responseBody", "")).lower()
                for kw in ["root:", "nobody:", "daemon:", "<?ph"]
            )
            if has_vuln:
                findings.append({
                    "id": f"caido-{path}-{status_code}",
                    "severity": "high",
                    "title": f"Sensitive data in response: {path}",
                    "description": f"Response body may contain sensitive info on {path}",
                    "url": f"{target}{path}",
                    "evidence": str(entry.get("responseBody", ""))[:300]
                })
            elif status_code >= 301 and status_code < 400:
                findings.append({
                    "id": f"redirect-{path}",
                    "severity": "info",
                    "title": f"Redirect {status_code}: {path}",
                    "description": f"Resource redirects to {entry.get('headers', {}).get('location', 'unknown')}",
                    "url": f"{target}{path}",
                    "port": 443 if target.startswith("https") else 80,
                    "protocol": "https" if target.startswith("https") else "http"
                })

        return {
            "tool": "caido", "status": "success",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"caido replay {target} via {api_url}",
            "duration_ms": int((time.time() - start) * 1000),
            "summary": {"total": len(findings)},
            "findings": findings,
            "raw_output": json.dumps(result)
        }
    except urllib.error.HTTPError as e:
        return {
            "tool": "caido", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"caido replay {target}",
            "duration_ms": int((time.time() - start) * 1000),
            "error": f"HTTP {e.code}: {e.reason}", "findings": []
        }
    except Exception as e:
        return {
            "tool": "caido", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"caido replay {target}",
            "duration_ms": int((time.time() - start) * 1000),
            "error": str(e), "findings": []
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"tool": "caido-wrapper", "status": "error",
                          "error": "Usage: caido-wrapper.py <target> [api_url]"}))
        sys.exit(1)
    print(json.dumps(run(sys.argv[1], sys.argv[2:]), indent=2))
