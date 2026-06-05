# Tareas Específicas: SCAN-AGENT

## Objetivo Principal

Escaneo de puertos, enumeración de servicios y detección de vulnerabilidades
en la infraestructura del objetivo.

---

## Tareas Asignadas

### Fase 2A: Escaneo de Puertos

#### 1.1 Nmap - Escaneo Inicial
**Objetivo**: Identificar puertos abiertos y servicios.

```bash
# Escaneo rápido de top 1000 puertos
nmap -sS -T4 -A target.com

# Escaneo completo de todos los puertos TCP
nmap -sS -p- -T4 target.com

# Escaneo de puertos UDP comunes
nmap -sU --top-ports 100 target.com
```

#### 1.2 Nmap - Version Detection
**Objetivo**: Obtener versiones exactas de servicios.

```bash
nmap -sV -p 80,443,22,3306 target.com
nmap -sV --version-intensity 9 -p 80,443 target.com
```

#### 1.3 Nmap - Scripts de Enumeración
**Objetivo**: Enumeración adicional con scripts NSE.

```bash
# Enumeración HTTP
nmap --script http-enum -p 80,443 target.com

# Enumeración DNS
nmap --script dns-brute -p 53 target.com

# Detección de vulnerabilidades
nmap --script vuln -p 80,443 target.com
```

---

### Fase 2B: Enumeración Web

#### 2.1 Directorios Ocultos
**Objetivo**: Descubrir rutas y archivos en servidores web.

```bash
# gobuster (recomendado)
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt

# dirsearch (alternativa)
dirsearch -u https://target.com
```

#### 2.2 Nikto - Web Vulnerability Scanner
**Objetivo**: Detectar vulnerabilidades web comunes.

```bash
nikto -h https://target.com
```

#### 2.3 Headers de Seguridad
**Objetivo**: Verificar configuración de seguridad HTTP.

```bash
curl -sI https://target.com | grep -iE "strict-transport-security|x-frame-options|x-content-type-options|content-security-policy"
```

---

### Fase 2C: Detección de Vulnerabilidades

#### 3.1 Búsqueda de CVEs
**Objetivo**: Encontrar exploits conocidos para versiones detectadas.

- Searchsploit: `searchsploit apache 2.4.49`
- CVE Details: `https://www.cvedetails.com/`
- NVD: `https://nvd.nist.gov/`

#### 3.2 SSL/TLS Scan
**Objetivo**: Detectar problemas en configuración SSL.

```bash
nmap --script ssl-enum-ciphers -p 443 target.com
```

---

## Checklist de Entregable

- [ ] Escaneo TCP completo de puertos
- [ ] Escaneo de puertos UDP comunes
- [ ] Version detection en servicios abiertos
- [ ] Enumeración web (directorios ocultos)
- [ ] Nikto scan completado
- [ ] Headers de seguridad verificados
- [ ] Búsqueda de CVEs por versión
- [ ] SSL/TLS scan realizado
- [ ] Reporte de escaneo generado

---

## Coordinación con Otros Agentes

- **RECON-AGENT**: Recibe superficie de ataque
- **EXPLOIT-AGENT**: Entrega vulnerabilidades detectadas

---

## Formato de Entrega a EXPLOIT-AGENT

```markdown
## Handoff a EXPLOIT-AGENT

### Vulnerabilidades Críticas
| Puerto | Servicio | Versión | CVE | Riesgo |
|--------|----------|---------|-----|--------|
| 80     | Apache   | 2.4.49  | CVE-2021-41773 | Remoto |

### Rutas Web Sensibles
- /admin (login panel)
- /wp-admin (WordPress)
- /backup/ (directory listing)

### Configuraciones Erróneas
- Directory listing en /backup/
- Missing X-Frame-Options header
- SSL weak ciphers
```
---

*Última actualización: Junio 2026*
