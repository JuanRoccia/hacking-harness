# Tools — Wrappers de Integración de Herramientas Externas

Este directorio contiene los wrappers que integran herramientas externas de hacking
en el Hacking Harness, normalizando todas las salidas a un formato JSON unificado.

## Estructura

```
tools/
├── wrappers/
│   ├── nmap-wrapper.py       # Nmap (CLI → XML → JSON)
│   ├── msf-wrapper.py        # Metasploit (msfrpc JSON-RPC)
│   ├── burp-wrapper.py       # Burp Suite Pro (REST API)
│   ├── caido-wrapper.py      # Caido (REST API)
│   ├── sqlmap-wrapper.py     # sqlmap (CLI batch mode)
│   └── ffuf-wrapper.py       # ffuf (CLI JSON output)
├── schemas/
│   └── tool-output-schema.json  # Schema de salida unificada
└── README.md
```

## Schema de Salida

Todos los wrappers devuelven un JSON con esta estructura base:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `tool` | str | Nombre de la herramienta |
| `status` | str | success / error / timeout / no_target |
| `timestamp` | str | ISO 8601 |
| `target` | str | Target analizado |
| `command` | str | Comando ejecutado |
| `error` | str | Mensaje de error (si status != success) |
| `summary` | obj | Resumen (total, open, vulnerable) |
| `findings` | arr | Lista de hallazgos |
| `raw_output` | str | Salida original de la herramienta |
| `duration_ms` | int | Duración en milisegundos |

## Uso

```bash
python3 tools/wrappers/nmap-wrapper.py <target>
python3 tools/wrappers/ffuf-wrapper.py <url> [wordlist]
python3 tools/wrappers/sqlmap-wrapper.py <url> [extra args...]
python3 tools/wrappers/burp-wrapper.py <url> [api_host] [api_port]
python3 tools/wrappers/caido-wrapper.py <url> [api_url]
python3 tools/wrappers/msf-wrapper.py <target> [password]
```

## Requisitos

- **Wrappers CLI**: la herramienta debe estar instalada en el sistema
- **Wrappers API**: el servicio debe estar corriendo (Burp, Caido, msfrpcd)
- Python 3.9+ (sin dependencias externas, solo stdlib)
