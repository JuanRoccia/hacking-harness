# Skill: Escaneo y Enumeración

## Descripción
Técnicas de escaneo de puertos, enumeración de servicios y detección de
vulnerabilidades para la fase de escaneo en pentesting.

## Nmap

### Escaneos básicos
```bash
# SYN stealth (requiere root)
nmap -sS -T4 target.com

# TCP connect (sin root)
nmap -sT -T4 target.com

# UDP scan
nmap -sU --top-ports 100 target.com

# Todos los puertos TCP
nmap -sS -p- -T4 target.com

# Version detection
nmap -sV -p 80,443,22 target.com

# OS detection
nmap -O target.com

# Agresivo (OS + version + scripts + traceroute)
nmap -A target.com
```

### Scripts NSE útiles
```bash
# Enumeración HTTP
nmap --script http-enum -p 80,443 target.com

# Enumeración DNS
nmap --script dns-brute -p 53 target.com

# Detección de vulnerabilidades
nmap --script vuln -p 80,443 target.com

# SSL/TLS
nmap --script ssl-enum-ciphers -p 443 target.com

# SMB enumeration
nmap --script smb-enum-shares -p 445 target.com
```

### Output
```bash
nmap -oN scan.txt target.com              # Normal
nmap -oX scan.xml target.com              # XML
nmap -oG scan.gnmap target.com            # Greppable
nmap -oA scan target.com                  # Todos los formatos
```

## Enumeración Web

### Gobuster
```bash
# Directorios
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt

# Subdominios
gobuster dns -d target.com -w /usr/share/wordlists/dns/subdomains.txt
```

### Nikto
```bash
nikto -h https://target.com

# Con autenticación
nikto -h https://target.com -id admin:password

# SSL
nikto -h https://target.com -ssl
```

### curl para web enum
```bash
# Headers
curl -sI https://target.com

# Métodos HTTP permitidos
curl -X OPTIONS https://target.com -v

# POST data
curl -X POST https://target.com/login -d "user=admin&pass=test"
```

## Detección de Vulnerabilidades

### Searchsploit
```bash
searchsploit apache 2.4.49
searchsploit wordpress 5.8
searchsploit -m 12345   # Mirror exploit to current dir
```

### Verificación manual
```bash
# Directory listing
curl -s https://target.com/backup/

# Path traversal
curl -s https://target.com/page?file=../../../etc/passwd

# Headers de seguridad
curl -sI https://target.com | grep -i "server\|x-powered-by\|x-frame-options"
```

## Referencias
- Nmap Documentation: https://nmap.org/docs.html
- NSE Scripts: https://nmap.org/nsedoc/
- OWASP Testing Guide
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings
