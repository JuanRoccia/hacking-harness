# 🎯 TAREA PRINCIPAL DEL WORKFLOW

## Contexto del Proyecto

**Workflow Harness** - Sistema de orquestación de agentes de IA para desarrollo de proyectos.

### Stack Tecnológico Típico
- **Frontend**: React/Vue/Angular + TypeScript + Vite/Next.js (según proyecto)
- **Backend**: Express/Django/Spring + TypeScript/Python/Java (según proyecto)
- **Database**: PostgreSQL/MySQL/MongoDB (según proyecto)
- **Auth**: JWT/OAuth/Passport (según proyecto)
- **Payments**: Stripe/PayPal (si aplica)

### Estado Actual del Harness

| Área | Estado |
|------|--------|
| Estructura base | ✅ Funcional |
| Agentes definidos | ✅ 7 roles |
| Tasks por agente | ✅ Definidas |
| Documentación | ⚠️ En proceso |
| QA Automation | ✅ Scripts + agente definidos |
| Seguridad | ⚠️ Por validar |
| Tests | ⚠️ Por implementar |

---

## 🎯 Objetivo Global del Workflow

Proporcionar un **sistema de orquestación genérico** que permita a múltiples agentes de IA trabajar de forma coordinada en cualquier proyecto de software, manteniendo calidad, trazabilidad y buenas prácticas.

---

## 📋 Tareas Asignadas por Agente

### 1. ARQUITECTO (big-pickle)
**Ubicación**: `tasks/task-arquitecto.md`

**Responsabilidad principal**: Análisis arquitectónico de alto nivel y resolución de problemas técnicos críticos.

**Tareas específicas**:
- Revisión y remediación de vulnerabilidades de seguridad
- Análisis de sistemas críticos (pagos, auth, etc.)
- Optimización de la arquitectura de datos
- Diseño de APIs y contratos

---

### 2. CODE REVIEWER (glm-4.7-free)
**Ubicación**: `tasks/task-code-reviewer.md`

**Responsabilidad principal**: Asegurar la calidad del código, detectar bugs y anti-patterns.

**Tareas específicas**:
- Revisión completa del codebase
- Detección de code smells y deuda técnica
- Validación de buenas prácticas
- Sugerencias de refactoring

---

### 3. TESTER/DEBUGGER (kimi-k2.5-free)
**Ubicación**: `tasks/task-tester.md`

**Responsabilidad principal**: Testing, debugging y documentación técnica.

**Tareas específicas**:
- Análisis de cobertura de tests
- Identificación de edge cases
- Documentación de funciones y componentes
- Debugging de problemas

---

### 4. FRONTEND/UI (minimax-m2.1-free)
**Ubicación**: `tasks/task-frontend.md`

**Responsabilidad principal**: Mejora de componentes, UI/UX y experiencia de usuario.

**Tareas específicas**:
- Revisión de componentes y páginas
- Mejoras de diseño responsive
- Optimización de rendimiento frontend
- Mejoras de accesibilidad

---

### 5. BACKEND (big-pickle)
**Ubicación**: `tasks/task-backend.md`

**Responsabilidad principal**: APIs, base de datos, integración con servicios externos.

**Tareas específicas**:
- Revisión y mejora de endpoints API
- Optimización de queries
- Mejora de sistemas de pagos/integraciones
- Implementación de features pendientes

---

### 6. GHOST (big-pickle)
**Ubicación**: `tasks/task-ghost.md`

**Responsabilidad principal**: Agente flexible para tareas variables.

**Modos disponibles**:
- 🕵️ Explorador: Mapear estructura
- 🔧 Quick Fix: Bug fixing
- 📊 Auditor: Revisiones profundas
- 🎨 Designer: Diseño UI
- 🧪 Tester: Validar flujos
- 🔍 Investigador: Análisis específico

---

### 7. QA BROWSER (big-pickle)
**Ubicación**: `tasks/task-qa-browser.md`

**Responsabilidad principal**: Testing E2E en navegador real para validar flujos de usuario.

**Tareas específicas**:
- Smoke test de landing y health endpoint
- Registro y login completos
- CRUD de entidad principal
- Testing mobile (375px)
- Regresión post-deploy

---

## 🔄 Flujo de Trabajo Recomendado

```
1. ARQUITECTO (big-pickle)
   └─> Identifica prioridades técnicas y vulnerabilidades

2. CODE REVIEWER (glm-4.7-free)
   └─> Analiza código en las áreas prioritarias

3. BACKEND (big-pickle)
   └─> Implementa mejoras en backend/APIs

4. FRONTEND/UI (minimax-m2.1-free)
   └─> Implementa mejoras en frontend

5. TESTER/DEBUGGER (kimi-k2.5-free)
   └─> Valida cambios y documenta

6. QA BROWSER (big-pickle)
   └─> Testea en navegador real (E2E)

---

## 📁 Estructura de Archivos

```
workflow-harness/
├── AGENTS.md                 # Punto de entrada (este archivo es referencia)
├── init.sh                   # Script de inicialización
├── feature_list.json         # Lista de tareas
├── agents/                   # Definiciones de roles
│   ├── 01-arquitecto.md
│   ├── 02-code-reviewer.md
│   ├── 03-tester-debugger.md
│   ├── 04-frontend-ui.md
│   ├── 05-backend.md
│   ├── 06-ghost.md
│   └── 07-qa-browser.md
├── tasks/                    # Tareas por agente
│   ├── task-arquitecto.md
│   ├── task-code-reviewer.md
│   ├── task-tester.md
│   ├── task-frontend.md
│   ├── task-backend.md
│   ├── task-ghost.md
│   └── task-qa-browser.md
├── skills/                   # Skills especializados
│   └── [skills según necesidad]
├── docs/                     # Documentación del harness
│   ├── architecture.md
│   ├── conventions.md
│   └── verification.md
├── progress/                 # Seguimiento de sesiones
│   ├── current.md
│   ├── history.md
│   └── [informes de sesión]
├── qa/                       # Tests E2E (Playwright)
│   ├── qa-runner.mjs
│   ├── qa-register.mjs
│   ├── setup-qa-local.sh
│   └── qa-reports/
└── tests/                    # Tests automáticos
```

---

## 🚀 Inicio del Workflow

Para comenzar el workflow:

1. Ejecuta `./init.sh` para verificar el entorno
2. Lee `AGENTS.md` para entender el sistema
3. Lee tu archivo de tarea en `tasks/task-[rol].md`
4. Analiza el proyecto y comienza a trabajar

**Nota**: Cada agente debe leer primero la documentación relevante antes de comenzar su trabajo.

---

*Documento adaptado para workflow-harness genérico*
*Fecha: Mayo 2026*
