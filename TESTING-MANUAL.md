# TESTING-MANUAL.md — Guía de Pentesting Manual

> Este documento proporciona una guía genérica para realizar pentesting manual
> siguiendo las 5 fases del hacking ético estructurado.

---

## Objetivo

Documentar el proceso de pentesting manual para validar la seguridad de un
objetivo antes de marcar una fase como `done`.

---

## Preparación

### 1. Verificar Entorno
```bash
./init.sh
```
Debe terminar sin errores.

### 2. Leer Documentación
- `AGENTS.md` - Entender el workflow de hacking
- `tasks/task-[rol].md` - Tareas asignadas por fase
- `docs/methodology.md` - Metodología de pentesting

### 3. Preparar Herramientas
- Asegurar que las herramientas necesarias estén instaladas
- Configurar IP atacante y puertos de escucha
- Preparar wordlists y payloads

---

## Flujo de Pentesting Manual

### Fase 1: Reconocimiento
- [ ] Google Dorking completado
- [ ] WHOIS y DNS records obtenidos
- [ ] Subdominios enumerados
- [ ] Tecnologías identificadas
- [ ] OSINT en redes sociales

### Fase 2: Escaneo y Enumeración
- [ ] Nmap scan completo (TCP/UDP)
- [ ] Enumeración web (directorios ocultos)
- [ ] Nikto / vulnerabilidad web scan
- [ ] Headers de seguridad verificados
- [ ] Búsqueda de CVEs

### Fase 3: Explotación
- [ ] SQL Injection probada
- [ ] XSS probado (reflejado/almacenado/DOM)
- [ ] RCE probado
- [ ] LFI/RFI probado
- [ ] Metasploit ejecutado
- [ ] Brute force probado

### Fase 4: Persistencia
- [ ] Webshell instalada
- [ ] Cron job / scheduled task creado
- [ ] Escalada de privilegios
- [ ] Movimiento lateral

### Fase 5: Limpieza
- [ ] Logs limpiados
- [ ] Artefactos removidos
- [ ] Timestamps restaurados
- [ ] Informe generado

---

## Matriz de Hallazgos

| ID | Vulnerabilidad | Fase | Severidad | PoC | Estado |
|----|----------------|------|-----------|-----|--------|
| VULN-001 | [Nombre] | Recon/Scan/Exploit/Persist | Critica/Alta/Media/Baja | [link] | Pending/Fixed |

---

## Formato de Reporte de Hallazgo

```markdown
## VULN-001 - [Título]

**Severidad**: 🔴 Crítica
**Fase**: Exploit
**URL**: https://target.com/api/endpoint
**PoC**: [Comando o payload]
**Evidencia**: [Screenshot o log]
**Remediación**: [Qué hacer para arreglarlo]
```

---

## Checklist de Cierre

Antes de marcar una fase como `done`:

- [ ] Todos los hallazgos documentados con PoC
- [ ] Vulnerabilidades críticas reportadas
- [ ] Se actualizó `progress/current.md`
- [ ] Se ejecutó `./init.sh` sin errores
- [ ] No hay artefactos temporales en el sistema objetivo
- [ ] Informe técnico generado

---

## Herramientas Recomendadas

- **nmap** - Escaneo de puertos
- **Burp Suite / ZAP** - Proxy de interceptación
- **sqlmap** - SQL Injection automation
- **Metasploit** - Exploitation framework
- **gobuster/dirsearch** - Enumeración web
- **nikto** - Web vulnerability scanner
- **hydra** - Brute force
- **john/hashcat** - Password cracking
- **curl** - Peticiones HTTP desde terminal

---

*Guía de pentesting manual adaptada para hacking-harness*
