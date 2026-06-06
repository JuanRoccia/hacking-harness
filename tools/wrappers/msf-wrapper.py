#!/usr/bin/env python3
"""Wrapper unificado para Metasploit (msfrpc)."""

from __future__ import annotations

import json
import socket
import ssl
import sys
import time
from datetime import datetime, timezone


def _msgrpc_send(sock: socket.socket, msg: dict) -> dict:
    data = json.dumps(msg)
    sock.sendall(len(data).to_bytes(4, "big") + data.encode())
    raw_len = int.from_bytes(sock.recv(4), "big")
    resp = b""
    while len(resp) < raw_len:
        chunk = sock.recv(raw_len - len(resp))
        if not chunk:
            break
        resp += chunk
    return json.loads(resp.decode())


def run(target: str, args: list[str] | None = None) -> dict:
    start = time.time()
    host = "127.0.0.1"
    port = 55553
    password = args[0] if args and args[0] else "msf"

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = socket.create_connection((host, port), timeout=10)
        sock = ctx.wrapper(sock)
    except (ConnectionRefusedError, TimeoutError, OSError) as e:
        return {
            "tool": "msf", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": f"msfrpc -P {password} -t {host}:{port}",
            "duration_ms": int((time.time() - start) * 1000),
            "error": f"Cannot connect to msfrpc ({host}:{port}): {e}",
            "findings": []
        }

    try:
        auth_resp = _msgrpc_send(sock, {
            "method": "auth.login",
            "username": "msf",
            "password": password
        })
        if auth_resp.get("result") != "success":
            sock.close()
            return {
                "tool": "msf", "status": "error",
                "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
                "command": f"msfrpc auth.login",
                "duration_ms": int((time.time() - start) * 1000),
                "error": f"Auth failed: {auth_resp}", "findings": []
            }

        vulns_resp = _msgrpc_send(sock, {
            "method": "db.vulns",
            "workspace": "default"
        })
        sock.close()

        findings = []
        for v in vulns_resp.get("data", []):
            title = v.get("name", "Unknown")
            findings.append({
                "id": v.get("id", ""),
                "severity": "high" if any(w in title.lower()
                    for w in ["critical", "rce", "sql", "shell"]) else "medium",
                "title": title,
                "description": v.get("info", ""),
                "evidence": v.get("refs", ""),
                "recommendation": "Review Metasploit module output"
            })

        return {
            "tool": "msf", "status": "success",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": "msfrpc db.vulns",
            "duration_ms": int((time.time() - start) * 1000),
            "summary": {"total": len(findings), "vulnerable": len(findings)},
            "findings": findings,
            "raw_output": json.dumps(vulns_resp)
        }
    except Exception as e:
        sock.close()
        return {
            "tool": "msf", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": "msfrpc",
            "duration_ms": int((time.time() - start) * 1000),
            "error": str(e), "findings": []
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"tool": "msf-wrapper", "status": "error",
                          "error": "Usage: msf-wrapper.py <target> [password]"}))
        sys.exit(1)
    target = sys.argv[1]
    pwd = sys.argv[2] if len(sys.argv) > 2 else "msf"
    print(json.dumps(run(target, [pwd]), indent=2))
