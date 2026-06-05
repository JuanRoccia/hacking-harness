# BUGS-REPORT.md — Plantilla de Reporte de Vulnerabilidades

> Este archivo es una plantilla para documentar vulnerabilidades y hallazgos
> de seguridad descubiertos durante el pentesting.

---

## Formato de Reporte de Vulnerabilidad

```markdown
### VULN-[NUMERO] - [Título Breve]

**Fecha**: [YYYY-MM-DD]
**Severidad**: 🔴 Crítica / 🟠 Alta / 🟡 Media / 🟢 Baja
**CVSS**: [Score (ej: 9.1)] / [Vector (ej: AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N)]
**CVE**: [CVE-XXXX-XXXX si aplica / N/A]
**Fase**: Recon / Scan / Exploit / Persist / Cleanup
**Agente**: [Rol que encontró la vulnerabilidad]
**Estado**: Pending / Confirmed / Fixed / Won't Fix / False Positive

#### Descripción
[Descripción clara de la vulnerabilidad]

#### Impacto
[Qué puede hacer un atacante con esto]

#### Pasos para Reproducir
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

#### Prueba de Concepto (PoC)
```bash
[Comandos, payloads, requests necesarios para demostrar la vulnerabilidad]
```

#### Comportamiento Esperado
[Qué debería pasar si está correctamente implementado]

#### Comportamiento Actual
[Qué está pasando (la vulnerabilidad)]

#### Ubicación
- **URL/Endpoint**: [ruta/al/endpoint]
- **Parámetro**: [nombre del parámetro]
- **Método**: [GET/POST/PUT/DELETE]

#### Evidencia
```
[Logs, screenshots, outputs, request/response]
```

#### Causa Raíz (si se identificó)
[Explicación de la causa técnica]

#### Recomendación de Remediación
[Descripción de cómo arreglarlo]

#### Referencias
- [OWASP: SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CVE Details](https://www.cvedetails.com/)
```

---

## Vulnerabilidades Reportadas

### VULN-EJEMPLO - SQL Injection en endpoint de usuarios

**Fecha**: 2026-06-01
**Severidad**: 🔴 Crítica
**CVSS**: 9.1 / AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
**CVE**: N/A
**Fase**: Exploit
**Agente**: EXPLOIT-AGENT
**Estado**: Pending

#### Descripción
El endpoint `/api/users/search` es vulnerable a SQL Injection en el parámetro
`q`. Un atacante no autenticado puede extraer toda la base de datos.

#### Impacto
Exposición completa de la base de datos incluyendo credenciales de usuarios,
datos personales y configuraciones del sistema.

#### Pasos para Reproducir
1. Enviar request con payload malicioso
2. Verificar respuesta con datos de la base de datos

#### PoC
```bash
curl "https://target.com/api/users/search?q=test' UNION SELECT 1,2,3,4,5,@@version--"
```

#### Evidencia
```
Response contiene: 1,2,3,4,5,MySQL 8.0.28
```

#### Recomendación de Remediación
- Usar prepared statements / ORM parameterized queries
- Validar y sanitizar entrada de usuario
- Implementar WAF con reglas de SQLi

---

## Formato para Actualización de Estado

```markdown
### VULN-[NUMERO] - [Título Breve] - ACTUALIZACIÓN

**Fecha**: [YYYY-MM-DD]
**Estado**: Fixed / In Progress / Won't Fix / False Positive
**Agente que verificó**: [Rol]
**Comprobación**: [Descripción de cómo se verificó]

#### Resolución
[Descripción de cómo se arregló o por qué no aplica]

#### Verificación
- [ ] Vulnerabilidad ya no es reproducible
- [ ] Prueba de regresión pasada
- [ ] Remediación validada por QA-BROWSER
```

---

*Plantilla de reporte de vulnerabilidades para hacking-harness*
