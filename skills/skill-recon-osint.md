# Skill: Reconocimiento y OSINT

## Descripción
Técnicas de recolección de información pasiva y activa para la fase de
reconocimiento en pentesting.

## Google Dorking

### Operadores básicos
| Operador | Uso | Ejemplo |
|----------|-----|---------|
| `site:` | Limitar a dominio | `site:target.com` |
| `filetype:` | Tipo de archivo | `filetype:pdf confidential` |
| `inurl:` | Palabra en URL | `inurl:admin` |
| `intitle:` | Palabra en título | `intitle:"index of"` |
| `intext:` | Palabra en cuerpo | `intext:password` |
| `cache:` | Versión cacheada | `cache:target.com` |

### Dorks útiles para pentesting
```
site:target.com inurl:admin
site:target.com intitle:login
site:target.com filetype:sql | filetype:bak | filetype:swp
site:target.com ext:php intitle:phpinfo
site:target.com "index of" /backup
site:target.com inurl:wp- | inurl:plugin
site:"*.target.com" -www
site:target.com intitle:"Dashboard" inurl:dashboard
```

## WHOIS y DNS

### Consultas WHOIS
```bash
whois target.com
whois X.X.X.X
```

### Consultas DNS
```bash
# Registros A
dig target.com A

# Registros MX (mail servers)
dig target.com MX

# Registros NS (name servers)
dig target.com NS

# Registros TXT (SPF, DKIM, DMARC)
dig target.com TXT

# Todos los registros
dig target.com ANY

# Transferencia de zona (raro pero posible)
dig axfr @ns1.target.com target.com

# Reverse DNS
dig -x X.X.X.X
```

## Subdomain Discovery

### Certificate Transparency
```bash
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u
```

### Amass (if installed)
```bash
amass enum -d target.com
```

### Subfinder (if installed)
```bash
subfinder -d target.com
```

## Tecnologías

### Fingerprinting web
```bash
whatweb target.com
```
### Headers HTTP
```bash
curl -sI https://target.com
```

## Herramientas OSINT
- **theHarvester**: `theHarvester -d target.com -b google,dns,bing,linkedin`
- **Shodan**: `shodan search hostname:target.com`
- **Have I Been Pwned**: API para leaks de credenciales

## Referencias
- Google Hacking Database: https://www.exploit-db.com/google-hacking-database
- OWASP Recon Guide
- OSINT Framework: https://osintframework.com/
