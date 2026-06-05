# Metodología — Las 5 Fases del Pentesting

> Este documento define la metodología de pentesting que el Hacking Harness
> sigue. Los agentes evalúan su trabajo contra este archivo.

## Principios

1. **Fases secuenciales.** El hacking sigue 5 fases ordenadas:
   - Fase 1: Reconocimiento (recolección de información)
   - Fase 2: Escaneo y Enumeración (mapeo de superficie de ataque)
   - Fase 3: Obtención de Acceso (explotación de vulnerabilidades)
   - Fase 4: Mantenimiento de Acceso (persistencia y movimiento lateral)
   - Fase 5: Borrado de Huellas (limpieza forense e informe)

2. **No saltar fases.** Cada fase produce información que la siguiente necesita.
   No se puede explotar sin haber escaneado, no se puede escanear sin haber
   recolectado información.

3. **Documentación continua.** Cada hallazgo se documenta en el momento,
   no al final. Usar `progress/current.md` como bitácora viva.

4. **Ética primero.** Este harness es para auditorías autorizadas y pentesting
   legal. Nunca operar sin consentimiento explícito por escrito.

## Flujo del Workflow

```
usuario ─→ init.sh (verificación del entorno de hacking)
           │
           ├─→ AGENTS.md (lee instrucciones)
           │
           ├─→ FASE 1: RECON-AGENT
           │    └─→ tasks/task-recon.md
           │
           ├─→ FASE 2: SCAN-AGENT
           │    └─→ tasks/task-scan.md
           │
           ├─→ FASE 3: EXPLOIT-AGENT
           │    └─→ tasks/task-exploit.md
           │
           ├─→ FASE 4: PERSIST-AGENT
           │    └─→ tasks/task-persist.md
           │
           ├─→ FASE 5: CLEANUP-AGENT
           │    └─→ tasks/task-cleanup.md
           │
           └─→ QA-BROWSER (validación transversal)
                └─→ tasks/task-qa-browser.md
```

## Fase 1: Reconocimiento (Footprinting)

### Objetivo
Recolectar la mayor cantidad de información posible sobre el objetivo
sin interactuar directamente con los sistemas (pasivo) o con interacción
mínima (activo).

### Sub-fases
- **Pasivo**: WHOIS, Google Dorking, Shodan, redes sociales, leaks públicos
- **Activo**: DNS enumeration, subdomain discovery, tecnologías identificadas

### Herramientas típicas
- `whois`, `nslookup`, `dig` - Consultas DNS
- `theHarvester` - OSINT automation
- Google Dorking manual
- Shodan/Censys - Dispositivos expuestos
- `whatweb`, `wappalyzer` - Fingerprinting de tecnologías

### Entregables
- Inventario de dominios/subdominios
- Tecnologías identificadas
- Emails/usuarios filtrados
- Superficie de ataque mapeada

## Fase 2: Escaneo y Enumeración

### Objetivo
Identificar puertos abiertos, servicios activos, y vulnerabilidades
potenciales en la infraestructura del objetivo.

### Sub-fases
- **Port scanning**: TCP/UDP, SYN stealth, version detection
- **Web enumeration**: Directorios ocultos, parámetros, endpoints
- **Vulnerability scanning**: CVE detection, misconfigurations

### Herramientas típicas
- `nmap` - Escaneo de puertos y servicios
- `gobuster`/`dirsearch` - Enumeración web
- `nikto` - Web vulnerability scanner
- `OpenVAS`/`Nessus` - Vulnerability assessment
- `netcat` - Banner grabbing manual

### Entregables
- Mapa de red con puertos/servicios
- Lista de vulnerabilidades potenciales (con CVEs)
- Endpoints web descubiertos
- Configuraciones erróneas identificadas

## Fase 3: Obtención de Acceso (Explotación)

### Objetivo
Explotar las vulnerabilidades descubiertas para obtener acceso
al sistema objetivo.

### Sub-fases
- **Web exploitation**: SQLi, XSS, RCE, File Upload, SSRF
- **Network exploitation**: Metasploit, manual exploitation
- **Credential attacks**: Brute force, password spraying, hash cracking
- **Social engineering**: Phishing (simulado, autorizado)

### Herramientas típicas
- `sqlmap` - SQL Injection automation
- `Metasploit Framework` - Exploitation framework
- `Burp Suite` - Web proxy e interceptación
- `hydra`/`john` - Password attacks
- Payloads personalizados

### Entregables
- Acceso inicial obtenido (shell, webshell, RCE)
- Credenciales encontradas/descifradas
- Prueba de concepto (PoC) de cada exploit
- Documentación de vectores de ataque

## Fase 4: Mantenimiento de Acceso

### Objetivo
Asegurar el acceso persistente al sistema comprometido y expandir
el control a otros sistemas en la red.

### Sub-fases
- **Persistencia**: Backdoors, webshells, cron jobs, servicios
- **Escalada de privilegios**: Root/Administrator, sudo, suid
- **Movimiento lateral**: Pass-the-Hash, PSExec, SSH tunneling

### Herramientas típicas
- Webshells (PHP/ASP/JSP)
- Reverse shells persistentes
- Cron jobs / Scheduled tasks
- SSH keys backdoor
- Túneles C2 (ngrok, meterpreter)

### Entregables
- Puntos de persistencia documentados
- Rutas de escalada de privilegios
- Mapa de movimiento lateral
- Acceso a sistemas adicionales

## Fase 5: Borrado de Huellas (Limpieza)

### Objetivo
Eliminar toda evidencia de la actividad realizada y generar un
informe técnico completo.

### Sub-fases
- **Log manipulation**: Limpieza de syslog, auth.log, audit.log
- **Timestomp**: Manipulación de timestamps de archivos
- **Artefact removal**: Eliminación de herramientas, scripts, binarios
- **Reporting**: Informe ejecutivo + técnico con hallazgos

### Herramientas típicas
- `timestomp` - Manipulación de timestamps
- Log editing manual
- `shred` - Borrado seguro de archivos
- Plantillas de reporte

### Entregables
- Informe ejecutivo para stakeholders
- Informe técnico con hallazgos detallados
- PoCs y evidencia de cada vulnerabilidad
- Recomendaciones de remediación

## Estructura de datos

### feature_list.json
- Formato JSON estructurado con array de `features`.
- Cada feature tiene: `id`, `name`, `title`, `description`, `priority`, `acceptance`, `status`.
- Estados válidos: `pending`, `in_progress`, `done`, `blocked`.

### progress/current.md
- Plantilla de sesión actual.
- Se vacía al cerrar sesión y se mueve a `history.md`.

### agents/*.md
- Definición de rol, responsabilidades, herramientas y técnicas específicas.
- Un archivo por agente siguiendo patrón: `NN-rol.md`.

### specs/*/spec.md
- Contrato funcional de un módulo de hacking usando formato BDD (DADO/CUANDO/ENTONCES).
- Cada spec tiene estado: `draft`, `active`, o `deprecated`.
- Se complementa con `changelog.md` (delta funcional) y `decisions.md` (ADRs).

## Qué NO hacer

- No operar sin autorización escrita del objetivo.
- No usar rutas hardcodeadas a proyectos específicos.
- No mezclar múltiples fases en una misma sesión.
- No marcar `done` sin ejecutar `./init.sh` y ver tests verdes.
- No editar `progress/history.md` (solo append).
- No dejar archivos temporales, payloads, o credenciales en el repositorio público.
