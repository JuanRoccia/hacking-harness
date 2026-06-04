# Bitácora histórica (append-only)

> Cada vez que se cierra una sesión, su resumen se añade aquí.
> No edites entradas anteriores. Solo añades al final.

---

## 2026-05-01 — Inicialización del workflow-harness
- **Agente:** humano (Juan Manuel)
- **Cambios:** creación inicial de la estructura del harness (AGENTS.md, init.sh, feature_list.json, progress/).
- **Resultado:** entorno base listo. Pendiente limpieza de referencias específicas de proyectos.

---

## 2026-05-04 — Limpieza y Generización del Harness
- **Agente:** humano (Juan Manuel)
- **Cambios:**
  - Eliminado `00-INICIO.md` (reemplazado por AGENTS.md)
  - Eliminado `09-TODO.md` (reemplazado por feature_list.json)
  - Movido `07-BUGS-REPORT.md` a `audits/`
  - Adaptado `08-LOOP.md` a genérico
  - Task 7 (tests_structure) completada
  - Creados tests en `tests/` (test_feature_list.py, test_structure.py, test_init.sh)
  - Actualizado `init.sh` para ejecutar tests automáticamente
  - Eliminado `skill-gsap.txt` (solo un link a GitHub)
  - Eliminado `skill-business-logic.md` (DIROCCO específico)
  - `audit.md` y `auditoria.md` convertidos a plantillas genéricas
  - `user/TUTORIAL.md` convertido a guía genérica del harness
  - `07-BUGS-REPORT.md` renombrado (plantilla genérica)
  - Task 6 (skills_audit) completada
  - Task 3 (clean_project_references) completada
  - `init.sh` actualizado para modo no interactivo
  - Arreglado `test_init.sh` (sintaxis)
  - Task 4 (progress_structure) completada
  - Task 5 (docs_structure) completada
  - Task 2 (agents_md_entrypoint) completada
  - Task 1 (init_script) completada

- **Resultado:** ✅ Harness completamente genérico y projectless. Todas las tareas en `feature_list.json` marcadas como `done`.

---

*Última actualización: 2026-05-04*

---

## 2026-06-04 — Sistema de Prompts Reutilizables (Feature #11)
- **Agente:** big-pickle
- **Cambios:**
  - Creado `prompts/prompt-template.md` con template estándar de 6 secciones (orden de lectura, contexto, tarea técnica, restricciones, criterios de éxito, cierre de sesión)
  - Feature #11 agregada a `feature_list.json` y marcada como `done`
  - AGENTS.md actualizado — agregada entrada `prompts/` al mapa del repositorio
  - `init.sh` actualizado — verifica existencia de `prompts/`
  - `init.sh` → todo verde
- **Resultado:** ✅ Metodología de prompts formalizada como componente del harness.
