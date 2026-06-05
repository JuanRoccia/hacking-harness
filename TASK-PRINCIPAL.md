# TAREA PRINCIPAL DEL WORKFLOW DE HACKING

## Contexto del Proyecto

**Hacking Harness** - Sistema de orquestación de agentes de IA para auditorías de seguridad y pentesting.

### Stack Tecnológico Típico de Objetivos
- **Web**: React/Vue/Angular + Node.js/Django/Spring + bases de datos
- **Red**: Infraestructura cloud, servidores on-premise, contenedores
- **Móvil**: Apps Android/iOS con APIs REST/GraphQL
- **Servicios**: APIs REST, GraphQL, WebSockets, microservicios

### Fases del Pentesting

| Fase | Nombre | Descripción |
|------|--------|-------------|
| 1 | Reconocimiento (Footprinting) | Recolección de información pasiva y activa |
| 2 | Escaneo y Enumeración | Mapeo de red, puertos, servicios y vulnerabilidades |
| 3 | Obtención de Acceso | Explotación de vulnerabilidades para ingresar al sistema |
| 4 | Mantenimiento de Acceso | Persistencia, backdoors y movimiento lateral |
| 5 | Borrado de Huellas | Limpieza de logs, manipulación de evidencia forense |

---

## OBJETIVO GLOBAL

Proporcionar un **sistema de orquestación genérico** que permita a múltiples agentes de IA trabajar de forma coordinada en auditorías de seguridad y pentesting, manteniendo trazabilidad, metodología estructurada y buenas prácticas de hacking ético.

---

## Tareas Asignadas por Agente

### 1. RECON-AGENT (big-pickle)
**Ubicación**: `tasks/task-recon.md`

**Responsabilidad principal**: Footprinting y OSINT - recolección de información pasiva y activa del objetivo.

**Técnicas**:
- Google Dorking y búsqueda avanzada
- WHOIS, DNS enumeration, subdomain discovery
- Shodan/Censys recon
- Recolección de leaks y credenciales filtradas
- OSINT en redes sociales y fuentes públicas

---

### 2. SCAN-AGENT (claude-sonnet-4)
**Ubicación**: `tasks/task-scan.md`

**Responsabilidad principal**: Escaneo de puertos, enumeración de servicios y detección de vulnerabilidades.

**Técnicas**:
- Nmap scanning (TCP/UDP, SYN, version detection)
- Web enumeration (gobuster, dirsearch, nikto)
- Vulnerability scanning (Nessus, OpenVAS)
- Service fingerprinting y banner grabbing
- Análisis de vulnerabilidades conocidas (CVE)

---

### 3. EXPLOIT-AGENT (kimi-k2.5-free)
**Ubicación**: `tasks/task-exploit.md`

**Responsabilidad principal**: Explotación de vulnerabilidades y obtención de acceso inicial.

**Técnicas**:
- SQL Injection (SQLi) manual y automatizado
- Cross-Site Scripting (XSS) y CSRF
- Remote Code Execution (RCE)
- Metasploit Framework
- Fuzzing y bypass de autenticación
- File upload exploitation

---

### 4. PERSIST-AGENT (big-pickle)
**Ubicación**: `tasks/task-persist.md`

**Responsabilidad principal**: Establecer persistencia, escalada de privilegios y movimiento lateral.

**Técnicas**:
- Creación de backdoors y webshells
- Escalada de privilegios (Linux/Windows)
- Cron jobs y tareas programadas
- Movimiento lateral (Pass-the-Hash, PSExec)
- Creación de cuentas de administrador ocultas
- Establecimiento de túneles C2

---

### 5. CLEANUP-AGENT (minimax-m2.1-free)
**Ubicación**: `tasks/task-cleanup.md`

**Responsabilidad principal**: Eliminación de huellas, manipulación de logs y preparación del informe.

**Técnicas**:
- Limpieza de logs (syslog, auth.log, auditd)
- Manipulación de timestamps (timestomp)
- Eliminación de herramientas y artefactos
- Restauración de configuraciones modificadas
- Generación de informe técnico detallado

---

### 6. GHOST (big-pickle)
**Ubicación**: `tasks/task-ghost.md`

**Responsabilidad principal**: Agente flexible para tareas variables en cualquier fase del pentesting.

**Modos disponibles**:
- EXPLORADOR: Mapear superficie de ataque
- QUICK FIX: Ajustes rápidos en scripts/exploits
- AUDITOR: Revisión profunda de hallazgos
- CRYPTO: Análisis criptográfico
- FUZZER: Testing de entradas y payloads
- INVESTIGADOR: Análisis de exploits complejos

---

### 7. QA-BROWSER (big-pickle)
**Ubicación**: `tasks/task-qa-browser.md`

**Responsabilidad principal**: Validación de seguridad en navegador real, testeo de payloads XSS/CSRF, verificación de vulnerabilidades web.

**Técnicas**:
- XSS manual validation en navegador
- CSRF token analysis
- Session management testing
- Clickjacking y UI redressing
- DOM-based vulnerability detection
- Reporte con screenshots de hallazgos

---

## Flujo de Trabajo Recomendado (Fases de Pentesting)

```
FASE 1: RECON-AGENT (big-pickle)
   └─> Footprinting y OSINT del objetivo

FASE 2: SCAN-AGENT (claude-sonnet-4)
   └─> Escaneo y enumeración de servicios

FASE 3: EXPLOIT-AGENT (kimi-k2.5-free)
   └─> Explotación de vulnerabilidades

FASE 4: PERSIST-AGENT (big-pickle)
   └─> Persistencia y movimiento lateral

FASE 5: CLEANUP-AGENT (minimax-m2.1-free)
   └─> Limpieza de huellas + informe final

VALIDACIÓN: QA-BROWSER (big-pickle)
   └─> Validación en navegador real (transversal)

SOPORTE: GHOST (big-pickle)
   └─> Tareas flexibles en cualquier fase
```

---

## Estructura de Archivos

```
hacking-harness/
├── AGENTS.md                 # Punto de entrada
├── init.sh                   # Script de inicialización
├── feature_list.json         # Lista de tareas
├── agents/                   # Definiciones de roles de hacking
│   ├── 01-recon-agent.md
│   ├── 02-scan-agent.md
│   ├── 03-exploit-agent.md
│   ├── 04-persist-agent.md
│   ├── 05-cleanup-agent.md
│   ├── 06-ghost.md
│   └── 07-qa-browser.md
├── tasks/                    # Tareas por agente
│   ├── task-recon.md
│   ├── task-scan.md
│   ├── task-exploit.md
│   ├── task-persist.md
│   ├── task-cleanup.md
│   ├── task-ghost.md
│   └── task-qa-browser.md
├── skills/                   # Skills especializados
│   └── [skills según fase de hacking]
├── docs/                     # Documentación del harness
│   ├── methodology.md         # Metodología de pentesting
│   ├── conventions.md         # Convenciones de código
│   └── verification.md        # Criterios de verificación
├── progress/                 # Seguimiento de sesiones
│   ├── current.md
│   ├── history.md
│   └── [informes de sesión]
├── qa/                       # Validación de seguridad (Playwright)
│   ├── qa-runner.mjs
│   ├── qa-register.mjs
│   ├── setup-qa-local.sh
│   └── qa-reports/
├── tests/                    # Tests automáticos
└── ...
```

---

## Inicio del Workflow

Para comenzar el workflow:

1. Ejecuta `./init.sh` para verificar el entorno
2. Lee `AGENTS.md` para entender el sistema
3. Lee tu archivo de tarea en `tasks/task-[rol].md`
4. Analiza el objetivo y comienza a trabajar

**Nota**: Cada agente debe leer primero la documentación relevante antes de comenzar su trabajo.

---

*Documento adaptado para hacking-harness - Metodología de Pentesting Estructurada*
*Fecha: Junio 2026*
