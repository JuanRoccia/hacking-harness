#!/usr/bin/env python3
"""Wrapper unificado para ffuf (fuzzing web)."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone


def run(target: str, args: list[str] | None = None) -> dict:
    start = time.time()
    wordlist = args[0] if args and args[0] else "/usr/share/wordlists/dirb/common.txt"
    extra = args[1:] if args and len(args) > 1 else []

    # If target already contains FUZZ, use it directly; otherwise append /FUZZ
    if "FUZZ" not in target:
        url = f"{target.rstrip('/')}/FUZZ"
    else:
        url = target

    cmd = ["ffuf", "-u", url, "-w", wordlist, "-json"] + extra
    cmd_str = " ".join(cmd)

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300
        )
    except subprocess.TimeoutExpired:
        return {
            "tool": "ffuf", "status": "timeout",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": cmd_str, "duration_ms": int((time.time() - start) * 1000),
            "error": "Timeout after 300s", "findings": []
        }
    except FileNotFoundError:
        return {
            "tool": "ffuf", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": cmd_str, "duration_ms": int((time.time() - start) * 1000),
            "error": "ffuf not found", "findings": []
        }

    if result.returncode != 0 and not result.stdout:
        return {
            "tool": "ffuf", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": cmd_str, "duration_ms": int((time.time() - start) * 1000),
            "error": result.stderr.strip()[:500], "findings": []
        }

    findings = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            status = entry.get("status", 0)
            length = entry.get("length", 0)
            words = entry.get("words", 0)
            lines = entry.get("lines", 0)
            url_found = entry.get("url", "")

            sev = "info"
            if status == 200:
                sev = "medium" if length > 500 else "low"
            elif status in (403, 401):
                sev = "low"
            elif status in (301, 302, 307, 308):
                sev = "low"

            findings.append({
                "id": f"ffuf-{status}-{hash(url_found) % 100000}",
                "severity": sev,
                "title": f"HTTP {status}: {url_found}",
                "description": f"Status: {status}, Size: {length}B, Words: {words}, Lines: {lines}",
                "url": url_found,
                "evidence": f"{status} {length}B"
            })
        except json.JSONDecodeError:
            pass

    return {
        "tool": "ffuf", "status": "success",
        "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": cmd_str, "duration_ms": int((time.time() - start) * 1000),
        "summary": {"total": len(findings)},
        "findings": findings,
        "raw_output": result.stdout
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"tool": "ffuf-wrapper", "status": "error",
                          "error": "Usage: ffuf-wrapper.py <url> [wordlist] [extra args...]"}))
        sys.exit(1)
    print(json.dumps(run(sys.argv[1], sys.argv[2:]), indent=2))
