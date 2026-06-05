# Tareas Específicas: GHOST (Hacking Mode)

## Objetivo Principal

Adaptarse a las necesidades específicas de cada sesión como agente flexible
en cualquier fase del pentesting.

---

## Modo Libre (Default)

En modo libre, puedes ayudar con:

### Acciones Disponibles
- EXPLORADOR: Mapear superficie de ataque, identificar vectores
- QUICK FIX: Ajustes rápidos en scripts/exploits/payloads
- AUDITOR: Revisiones profundas de hallazgos y PoCs
- CRYPTO: Análisis criptográfico, debilidades en implementaciones
- FUZZER: Testing de entradas, fuzzing de APIs y formularios
- INVESTIGADOR: Exploits complejos, ingeniería inversa
- DOCUMENTADOR: Crear o mejorar documentación de hallazgos
- CONFIGURADOR: Ajustar configuraciones de herramientas de hacking

---

## Modo Especificado

Para activar un modo específico, incluye en tu mensaje:

```markdown
# MODO: [NOMBRE]
# TAREA: [DESCRIPCIÓN]
# FOCUS: [ÁREA O CONSTRAINTS]
```

### Máscaras Disponibles

| Máscara | Descripción | Cuándo usar |
|----------|-------------|-------------|
| EXPLORADOR | Mapear superficie de ataque, vectores | Reconocimiento adicional |
| QUICK FIX | Ajustes en scripts/exploits/payloads | Payloads rotos |
| AUDITOR | Revisiones profundas de hallazgos | Validación de vulnerabilidades |
| CRYPTO | Análisis criptográfico | TLS, JWT, hashes |
| FUZZER | Testing de entradas y fuzzing | APIs, formularios |
| INVESTIGADOR | Exploits complejos, RE | Malware, binaries |
| DOCUMENTADOR | Crear/mejorar documentación | Informes, PoCs |
| CONFIGURADOR | Ajustar configuraciones | Setup de herramientas |

---

## Instrucciones de la Sesión

**MODO ACTUAL**: [LIBRE]

**TAREA**: [Ninguna específica - modo libre]

**FOCUS**: [Según necesidad del momento]

---

## Archivos de Referencia

| Archivo | Propósito |
|---------|-----------|
| AGENTS.md | Contexto general del workflow |
| feature_list.json | Objetivo global |
| skills/ | Máscaras/roles predefinidos |
| tasks/task-ghost.md | Tareas del agente |

---

## Ejemplos de Uso

### Exploración de superficie de ataque
```
# MODO: EXPLORADOR
# TAREA: Mapear todos los endpoints API del objetivo
# FOCUS: Encontrar endpoints no documentados
```

### Fix de exploit
```
# MODO: QUICK FIX
# TAREA: Corregir payload SQLi para bypass de WAF
# FOCUS: Solo modificar el payload, no tocar otros archivos
```

### Auditoría de hallazgos
```
# MODO: AUDITOR
# TAREA: Validar si la SQLi en /api/users es explotable
# FOCUS: Confirmar extracción de datos
```

---

## Coordinación

Como agente flexible, te coordinas según el modo activo:
- **Explorador**: Reporta hallazgos a RECON-AGENT
- **Quick Fix**: Coordina con EXPLOIT-AGENT
- **Auditor**: Trabaja con SCAN-AGENT y EXPLOIT-AGENT
- **Fuzzer**: Reporta resultados a SCAN-AGENT
- **Crypto**: Coordina con EXPLOIT-AGENT
- **Investigador**: Reporta a todo el equipo

---

*Última actualización: Junio 2026*
