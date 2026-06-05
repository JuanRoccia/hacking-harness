# Tareas Específicas: RECON-AGENT

## Objetivo Principal

Footprinting y OSINT - Recolectar la máxima información posible sobre el
objetivo para mapear la superficie de ataque.

---

## Tareas Asignadas

### Fase 1A: OSINT Pasivo

#### 1.1 Google Dorking
**Objetivo**: Encontrar información expuesta mediante búsqueda avanzada.

**Queries a probar**:
- `site:target.com filetype:pdf`
- `site:target.com inurl:admin`
- `site:target.com ext:sql | ext:bak | ext:swp`
- `intitle:"index of" site:target.com`

#### 1.2 WHOIS y DNS
**Objetivo**: Mapear infraestructura DNS.

**Comandos**:
```bash
whois target.com
dig any target.com
nslookup target.com
```

#### 1.3 Subdominios
**Objetivo**: Descubrir todos los subdominios del objetivo.

**Herramientas**:
- `theHarvester -d target.com -b google,dns,bing`
- `amass enum -d target.com` (si está disponible)
- Certificate Transparency (crt.sh)

#### 1.4 Leaks y Credenciales
**Objetivo**: Encontrar credenciales filtradas.

**Fuentes**:
- Have I Been Pwned (API)
- DeHashed / IntelX
- GitHub dorking: `"target.com" password` `"target.com" secret`

---

### Fase 1B: OSINT Activo

#### 2.1 Fingerprinting de Tecnologías
**Objetivo**: Identificar stack tecnológico.

```bash
whatweb target.com
curl -I https://target.com
```

#### 2.2 Shodan/Censys
**Objetivo**: Encontrar dispositivos expuestos.

```bash
# Usando Shodan CLI (si instalado)
shodan search hostname:target.com
```

#### 2.3 Redes Sociales
**Objetivo**: Encontrar personal y relaciones.

- LinkedIn: empleados de la empresa objetivo
- Twitter: menciones, tech stack revelado
- GitHub: repositorios de empleados

---

## Checklist de Entregable

- [ ] Google Dorking completado
- [ ] WHOIS y DNS records obtenidos
- [ ] Subdominios enumerados
- [ ] Tecnologías identificadas
- [ ] Leaks y credenciales buscados
- [ ] OSINT en redes sociales realizado
- [ ] Reporte de reconocimiento generado
- [ ] Superficie de ataque documentada

---

## Coordinación con Otros Agentes

- **SCAN-AGENT**: Entregar superficie de ataque para escaneo
- **GHOST**: Soporte en tareas OSINT específicas
- **EXPLOIT-AGENT**: Proveer endpoints y tecnologías descubiertas

---

## Formato de Entrega a SCAN-AGENT

```markdown
## Handoff a SCAN-AGENT

### Dominios
- target.com (IP: X.X.X.X)

### Subdominios
- admin.target.com
- mail.target.com
- dev.target.com

### Puertos Conocidos
- 80 (HTTP), 443 (HTTPS), 22 (SSH)

### Tecnologías
- Apache 2.4.49
- PHP 8.0
- WordPress 5.8
```

---

*Última actualización: Junio 2026*
