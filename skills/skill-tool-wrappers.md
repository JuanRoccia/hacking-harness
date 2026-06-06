# Skill: Tool Wrappers - Integración de Herramientas Externas

## Descripción
Wrappers unificados en `tools/wrappers/` que normalizan la interfaz de herramientas externas de hacking a un formato JSON común. Cada wrapper acepta un target y argumentos, y devuelve un diccionario con el schema definido en `tools/schemas/tool-output-schema.json`.

## Wrappers Disponibles

| Wrapper | Herramienta | API | Puerto por defecto |
|---------|-------------|-----|--------------------|
| `nmap-wrapper.py` | Nmap | CLI (XML parsing) | - |
| `msf-wrapper.py` | Metasploit | msfrpc (JSON-RPC) | 55553 |
| `burp-wrapper.py` | Burp Suite Pro | REST API | 1337 |
| `caido-wrapper.py` | Caido | REST API | 8080 |
| `sqlmap-wrapper.py` | sqlmap | CLI (batch mode) | - |
| `ffuf-wrapper.py` | ffuf | CLI (JSON output) | - |

## Formato de Salida Unificado

```json
{
  "tool": "nmap",
  "status": "success",
  "timestamp": "2026-06-06T12:00:00Z",
  "target": "target.com",
  "command": "nmap -sS -T4 target.com",
  "summary": { "total": 5, "open": 5 },
  "findings": [
    {
      "id": "port-80",
      "severity": "info",
      "title": "Open port 80/tcp",
      "description": "Service: http Apache 2.4.49",
      "port": 80,
      "protocol": "tcp",
      "evidence": "80/tcp open http Apache 2.4.49"
    }
  ],
  "duration_ms": 12345
}
```

## Uso Básico

```bash
# Nmap scan
python3 tools/wrappers/nmap-wrapper.py target.com

# ffuf directory enumeration
python3 tools/wrappers/ffuf-wrapper.py https://target.com /usr/share/wordlists/dirb/common.txt

# sqlmap injection test
python3 tools/wrappers/sqlmap-wrapper.py "https://target.com/page?id=1"

# BurpSuite scan (requires Burp running with REST API)
python3 tools/wrappers/burp-wrapper.py https://target.com

# Caido replay (requires Caido running)
python3 tools/wrappers/caido-wrapper.py https://target.com

# Metasploit vulns (requires msfrpcd running)
python3 tools/wrappers/msf-wrapper.py target.com msf_password
```

## Ejecutar msfrpcd
```bash
msfrpcd -P msf -S -a 127.0.0.1
```

## Referencias
- `tools/schemas/tool-output-schema.json` — Schema JSON de salida
- `tools/README.md` — Documentación detallada
