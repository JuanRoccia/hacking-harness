# Tutorial del Hacking Harness - Guía para el Usuario

**Hacking Harness** es un sistema de orquestación para agentes de IA
especializados en pentesting. Con esta guía aprenderás a usar todas las
funciones de forma simple y rápida.

---

## Paso 1: Iniciar Sesión

1. Abre una terminal en la raíz del proyecto
2. Ejecuta el script de inicialización:
   ```bash
   bash init.sh
   ```
3. Completa la información solicitada (nombre del objetivo, tipo, etc.)

> **Tip:** El script verifica que todo el harness esté correctamente configurado
> y detecta las herramientas de hacking disponibles.

---

## Paso 2: Conocer el Menú

En la pantalla verás las diferentes secciones:

| Ícono | Sección | Para qué sirve |
|-------|---------|----------------|
| AGENTS.md | Punto de entrada y contexto |
| feature_list.json | Lista de tareas y estados |
| docs/ | Documentación del harness |
| tasks/ | Tareas por agente/fase |
| skills/ | Habilidades de hacking especializadas |

---

## Paso 3: Configurar una Nueva Auditoría

1. Andá a **AGENTS.md**
2. Leé la sección "Antes de empezar"
3. Ejecuta `./init.sh` para verificar el entorno
4. Configurá:
   - **Nombre del objetivo**
   - **Tipo de objetivo** (web, red, api, mobile)
   - **¿Se subirá a GitHub?**

---

## Paso 4: Asignar Tareas a Agentes

Una vez configurado:

1. Andá a **feature_list.json**
2. Identificá tareas con estado `pending`
3. Asigná un agente según la fase:

| Agente | Cuándo usarlo | Fase |
|--------|--------------|------|
| RECON-AGENT | OSINT, footprinting, recolección de información | 1. Recon |
| SCAN-AGENT | Escaneo de puertos, enumeración web | 2. Scan |
| EXPLOIT-AGENT | SQLi, XSS, RCE, explotación | 3. Exploit |
| PERSIST-AGENT | Backdoors, escalada, movimiento lateral | 4. Persist |
| CLEANUP-AGENT | Limpieza de logs, informe final | 5. Cleanup |
| GHOST | Tareas flexibles en cualquier fase | Variable |
| QA-BROWSER | Validación de seguridad en navegador | Transversal |

---

## Paso 5: Ejecutar el Workflow

Cuando un agente trabaja:

1. Leé el archivo de tarea en `tasks/task-[rol].md`
2. El agente analiza el objetivo y aplica técnicas de hacking
3. El agente documenta en `progress/current.md`
4. Al finalizar:
   - Marcá la tarea como `done` en `feature_list.json`
   - Mové el resumen a `progress/history.md`
   - Vació `progress/current.md`

---

## Paso 6: Verificar Progreso

Para ver el estado general:

```bash
bash init.sh
```

El script te dirá:
- **[OK]** - Todo está bien
- **[WARN]** - Faltan archivos (no bloqueante)
- **[FAIL]** - Hay errores (debe arreglarse)

---

## Paso 7: Flujo Completo de Pentesting

```
FASE 1: RECON-AGENT → OSINT, footprinting, subdominios
    ↓
FASE 2: SCAN-AGENT → Puertos, servicios, vulnerabilidades
    ↓
FASE 3: EXPLOIT-AGENT → SQLi, XSS, RCE, shells
    ↓
FASE 4: PERSIST-AGENT → Backdoors, escalada, pivoting
    ↓
FASE 5: CLEANUP-AGENT → Logs, artefactos, informe final
    ↓
QA-BROWSER (transversal) → Validación en navegador
```

---

## Tips Rápidos

| Situación | Qué hacer |
|-----------|-----------|
| Quiero iniciar pentesting | Ejecuta `bash init.sh` y lee `AGENTS.md` |
| Un agente terminó su fase | Marcá `done` en `feature_list.json` |
| Hay un error en el harness | Ejecuta `bash init.sh` para diagnóstico |
| Necesito documentación | Andá a `docs/` (methodology, conventions, verification) |
| Quiero un agente flexible | Usa **GHOST** con diferentes máscaras |

---

## Cómo Finalizar una Sesión

1. Ejecuta `bash init.sh` — todo verde
2. Si la tarea está lista: marcá `status: "done"` en `feature_list.json`
3. Mové el resumen de `progress/current.md` al final de `progress/history.md`
4. Vació `progress/current.md` dejando solo la plantilla
5. No dejes archivos temporales, ni payloads, ni hallazgos sin documentar

---

*Tutorial del Hacking Harness - Versión 2.0 - Junio 2026*
