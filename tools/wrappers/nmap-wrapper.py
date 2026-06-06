#!/usr/bin/env python3
"""Wrapper unificado para Nmap."""

from __future__ import annotations

import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


def run(target: str, args: list[str] | None = None) -> dict:
    start = time.time()
    cmd = ["nmap"] + (args or ["-sS", "-T4", "--top-ports", "1000"])
    cmd.append(target)
    command_str = " ".join(cmd)

    try:
        result = subprocess.run(
            cmd + ["-oX", "-"],
            capture_output=True, text=True, timeout=300
        )
    except subprocess.TimeoutExpired:
        return {
            "tool": "nmap", "status": "timeout",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": command_str, "duration_ms": int((time.time() - start) * 1000),
            "error": "Timeout after 300s", "findings": []
        }
    except FileNotFoundError:
        return {
            "tool": "nmap", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": command_str, "duration_ms": int((time.time() - start) * 1000),
            "error": "nmap not found", "findings": []
        }

    if result.returncode != 0:
        return {
            "tool": "nmap", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": command_str, "duration_ms": int((time.time() - start) * 1000),
            "error": result.stderr.strip(), "findings": []
        }

    findings = []
    open_ports = 0
    try:
        root = ET.fromstring(result.stdout)
        for host in root.findall("host"):
            addr_el = host.find("address")
            ip = addr_el.get("addr", target) if addr_el is not None else target
            for port in host.findall(".//port"):
                state_el = port.find("state")
                if state_el is not None and state_el.get("state") == "open":
                    open_ports += 1
                    port_id = port.get("portid", "0")
                    proto = port.get("protocol", "tcp")
                    service_el = port.find("service")
                    svc_name = service_el.get("name", "unknown") if service_el is not None else "unknown"
                    svc_product = service_el.get("product", "") if service_el is not None else ""
                    svc_version = service_el.get("version", "") if service_el is not None else ""
                    findings.append({
                        "id": f"port-{port_id}",
                        "severity": "info",
                        "title": f"Open port {port_id}/{proto}",
                        "description": f"Service: {svc_name} {svc_product} {svc_version}".strip(),
                        "port": int(port_id),
                        "protocol": proto,
                        "evidence": f"{port_id}/{proto}  open  {svc_name} {svc_product} {svc_version}".strip()
                    })
            for script in host.findall(".//script"):
                script_id = script.get("id", "unknown")
                output = script.get("output", "")
                if script_id.startswith("vuln") or "VULNERABLE" in output:
                    findings.append({
                        "id": script_id,
                        "severity": "high",
                        "title": f"NSE: {script_id}",
                        "description": f"Vulnerability detected by NSE script {script_id}",
                        "evidence": output[:500]
                    })
    except ET.ParseError as e:
        return {
            "tool": "nmap", "status": "error",
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": command_str, "duration_ms": int((time.time() - start) * 1000),
            "error": f"XML parse error: {e}", "findings": []
        }

    return {
        "tool": "nmap", "status": "success",
        "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": command_str, "duration_ms": int((time.time() - start) * 1000),
        "summary": {"total": len(findings), "open": open_ports},
        "findings": findings,
        "raw_output": result.stdout
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"tool": "nmap-wrapper", "status": "error",
                          "error": "Usage: nmap-wrapper.py <target> [args...]"}))
        sys.exit(1)
    target = sys.argv[1]
    extra_args = sys.argv[2:] if len(sys.argv) > 2 else None
    output = run(target, extra_args)
    print(json.dumps(output, indent=2))
