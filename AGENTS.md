# AGENTS.md — Mapa de navegación para agentes de IA (Hacking Harness)

> Este archivo es el **punto de entrada** para cualquier agente que trabaje en este
> repositorio. NO es una biblia de reglas: es un **mapa**. Lee solo lo que
> necesites cuando lo necesites (divulgación progresiva).

---

## 0. Directrices de Comportamiento (Karpathy)

Follow these behavioral guidelines to reduce common LLM coding mistakes. These bias toward caution over speed; use judgment for trivial tasks.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 1. Antes de empezar (obligatorio)

1. Ejecuta `./init.sh` y verifica que termina sin errores. Si falla, **para**
   y resuelve el entorno antes de tocar código.
2. Lee `progress/current.md` para entender en qué estado quedó la última sesión.
3. Si existe `specs/[módulo-relevante]/spec.md`, léela antes de tocar ese módulo.
4. Lee `TODO.md` y elige **una** tarea con estado `pending`. No
   trabajes en más de una a la vez.

## 2. Mapa del repositorio

| Archivo / carpeta            | Qué contiene                                              | Cuándo leerlo |
|------------------------------|-----------------------------------------------------------|---------------|
| `TODO.md`                    | Lista de tareas con estado (pending / in_progress / done)  | Siempre, al empezar |
| `progress/current.md`        | Estado de la sesión actual                                | Siempre, al empezar |
| `progress/history.md`        | Bitácora append-only de sesiones anteriores               | Si necesitas contexto histórico |
| `agents/`                    | Definiciones de roles de agentes (recon, scan, exploit, etc) | Al asumir un rol específico |
| `tasks/`                     | Tareas específicas por agente                             | Al ejecutar tarea de un rol |
| `skills/`                    | Skills especializados (OSINT, scanning, explotación, etc.)| Según necesidad técnica |
| `TASK-PRINCIPAL.md`          | Objetivo global del workflow de hacking                   | Para entender el propósito general |
| `TESTING-MANUAL.md`          | Guía de pentesting manual                                 | Antes de validar cambios |
| `BUGS-REPORT.md`             | Plantilla para reportar vulnerabilidades                  | Al encontrar un hallazgo |
| `specs/`                     | Contratos funcionales de cada módulo de hacking           | Antes de tocar cualquier módulo |
| `audits/`                    | Auditorías de seguridad y hallazgos                       | Para revisar resultados previos |
| `tests/`                     | Tests automáticos del harness                             | Para verificar integridad |
| `qa/`                        | Scripts de validación de seguridad (Playwright)           | Antes de marcar tarea como `done` |
| `prompts/`                   | Templates de prompts reutilizables (6-sección)            | Al planificar una nueva fase |
| `user/`                      | Documentación para usuarios del harness                   | Referencia externa |
| `tools/`                     | Wrappers unificados para herramientas externas (nmap, msf, burp, caido, sqlmap, ffuf) | Al integrar herramientas externas |
| `init.sh`                    | Script de verificación de entorno de hacking              | Al iniciar sesión |

## 3. Reglas duras (no negociables)

- **Una sola tarea a la vez.** No mezcles cambios de varias tareas en la misma sesión.
- **No declares una tarea `done` sin pruebas verdes.** Ejecuta `./init.sh` y
  asegúrate de que el bloque de tests pasa al 100%.
- **Documenta lo que haces** en `progress/current.md` mientras trabajas, no al final.
- **Deja el repositorio limpio** antes de cerrar la sesión (ver §5).
- **Si modificás comportamiento de un módulo que tiene spec, actualizá el
  changelog.md de esa spec con el delta funcional.**
- **Si no sabes algo, busca en `docs/`** antes de inventarlo.

## 4. Cómo elegir una tarea

```
1. Abre feature_list.json
2. Filtra por status == "pending"
3. Coge la de mayor prioridad (menor "id")
4. Cambia su status a "in_progress" y guarda
5. Anota en progress/current.md: tarea, hora de inicio, plan breve
```

## 5. Cierre de sesión (lifecycle)

Antes de terminar:

1. Ejecuta `./init.sh` — todo verde.
2. Si la tarea está acabada: marca `status: "done"` en `TODO.md`.
3. Mueve el resumen de `progress/current.md` al final de `progress/history.md`.
4. Vacía `progress/current.md` dejando solo la plantilla.
5. No dejes archivos temporales, ni `print()` de debug, ni TODOs sin contexto.

## 6. Si te bloqueas

- Relee la sección relevante de `agents/` o `docs/`.
- Si la herramienta no hace lo que esperas, **no inventes un workaround**:
  documenta el bloqueo en `progress/current.md` y para la sesión.

---

## 7. Roles disponibles

| Rol | Archivo | Responsabilidad | Fase de Hacking |
|-----|---------|-----------------|-----------------|
| **RECON-AGENT** | `agents/01-recon-agent.md` | Footprinting, OSINT, recolección de información | 1. Reconocimiento |
| **SCAN-AGENT** | `agents/02-scan-agent.md` | Escaneo de puertos, enumeración, detección de vulnerabilidades | 2. Escaneo y Enumeración |
| **EXPLOIT-AGENT** | `agents/03-exploit-agent.md` | Explotación de vulnerabilidades, obtención de acceso | 3. Obtención de Acceso |
| **PERSIST-AGENT** | `agents/04-persist-agent.md` | Persistencia, backdoors, movimiento lateral | 4. Mantenimiento de Acceso |
| **CLEANUP-AGENT** | `agents/05-cleanup-agent.md` | Borrado de huellas, manipulación de logs, forense | 5. Borrado de Huellas |
| **GHOST** | `agents/06-ghost.md` | Agente flexible para tareas variables en cualquier fase | Multi-fase |
| **QA-BROWSER** | `agents/07-qa-browser.md` | Validación de seguridad en navegador, tests de payloads | Validación transversal |

---

*Este archivo sirve como punto de entrada del workflow de hacking.*
