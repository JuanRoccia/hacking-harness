#!/usr/bin/env bash
# init.sh — Verificación e inicialización del Hacking Harness
#
# Este script verifica la integridad del harness de hacking y recopila
# información del objetivo antes de iniciar el workflow.
#
# Uso: bash init.sh

set -u
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; }
info()  { printf "${BLUE}[INFO]${NC}  %s\n" "$1"; }

EXIT_CODE=0
PY_TESTS=0
BASH_TESTS=0

echo "═══════════════════════════════════════════════════════════"
echo "  HACKING HARNESS - Inicialización del Entorno"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "── 1. Verificando estructura del harness ──────────────"

for dir in agents tasks skills tests qa prompts audits user tools; do
  if [ ! -d "$dir" ]; then
    fail "Falta directorio: $dir/"
    EXIT_CODE=1
  else
    ok "Directorio existe: $dir/"
  fi
done

echo ""
echo "── 2. Verificando archivos base del workflow ──────────"

for f in "AGENTS.md" "feature_list.json" "07-BUGS-REPORT.md" "TESTING-MANUAL.md"; do
  if [ ! -f "$f" ]; then
    warn "Falta archivo base: $f"
  else
    ok "Existe $f"
  fi
done

echo ""
echo "── 3. Verificando documentación (docs/) ──────────────"

for f in "docs/methodology.md" "docs/conventions.md" "docs/verification.md"; do
  if [ ! -f "$f" ]; then
    warn "Falta documento: $f"
  else
    ok "Existe $f"
  fi
done

echo ""
echo "── 4. Verificando agentes definidos ───────────────────"

AGENTS=("01-recon-agent.md" "02-scan-agent.md" "03-exploit-agent.md" "04-persist-agent.md" "05-cleanup-agent.md" "06-ghost.md" "07-qa-browser.md")
for agent in "${AGENTS[@]}"; do
  if [ ! -f "agents/$agent" ]; then
    warn "Falta definición de agente: $agent"
  else
    ok "Agente definido: $agent"
  fi
done

echo ""
echo "── 5. Verificando tareas por agente ───────────────────"

for task in "task-recon.md" "task-scan.md" "task-exploit.md" "task-persist.md" "task-cleanup.md" "task-ghost.md" "task-qa-browser.md"; do
  if [ ! -f "tasks/$task" ]; then
    warn "Falta tarea: tasks/$task"
  else
    ok "Tarea existe: $task"
  fi
done

echo ""
echo "── 6. Verificando herramientas de hacking ───────────"

HACKING_TOOLS=("nmap" "curl" "python3")
for tool in "${HACKING_TOOLS[@]}"; do
  if command -v "$tool" >/dev/null 2>&1; then
    ok "Herramienta disponible: $tool"
  else
    warn "Herramienta no encontrada: $tool (instalación recomendada)"
  fi
done

# Herramientas opcionales (no críticas)
OPTIONAL_TOOLS=("gobuster" "sqlmap" "msfconsole" "nikto" "whatweb" "dirsearch" "hydra" "john")
for tool in "${OPTIONAL_TOOLS[@]}"; do
  if command -v "$tool" >/dev/null 2>&1; then
    ok "Herramienta opcional disponible: $tool"
  fi
done

echo ""
echo "── 7. Verificando wrappers de herramientas (tools/) ──"

WRAPPER_COUNT=$(find tools/wrappers/ -name "*wrapper.py" 2>/dev/null | wc -l)
if [ "$WRAPPER_COUNT" -gt 0 ]; then
  ok "Wrappers disponibles: $WRAPPER_COUNT"
  for wrapper in tools/wrappers/*wrapper.py; do
    name=$(basename "$wrapper" .py)
    tool_name=$(echo "$name" | sed 's/-wrapper//')
    if command -v "$tool_name" >/dev/null 2>&1; then
      ok "  $name → $tool_name instalado"
    else
      warn "  $name → $tool_name no encontrado (wrapper presente pero herramienta ausente)"
    fi
  done
else
  warn "No hay wrappers en tools/wrappers/"
fi

if [ -f "tools/schemas/tool-output-schema.json" ]; then
  ok "Schema unificado de salida: tools/schemas/tool-output-schema.json"
else
  warn "Falta schema unificado: tools/schemas/tool-output-schema.json"
fi

echo ""
echo "── 8. Verificando QA Automation ─────────────────────"

for f in "qa/qa-runner.mjs" "qa/qa-security.mjs" "qa/setup-qa-local.sh" "qa/README.md"; do
  if [ ! -f "$f" ]; then
    warn "Falta archivo QA: $f"
  else
    ok "Existe $f"
  fi
done

echo ""
echo "── 9. Verificando skills disponibles ──────────────────"

SKILL_COUNT=$(find skills/ -type f 2>/dev/null | wc -l)
if [ "$SKILL_COUNT" -eq 0 ]; then
  warn "No hay skills definidos en skills/"
else
  ok "Skills disponibles: $SKILL_COUNT archivo(s)"
fi

echo ""
echo "── 10. Ejecutando tests del harness ──────────────────"

if [ "${WORKFLOW_TEST:-0}" -eq 1 ]; then
  info "Modo test detectado, omitiendo ejecución de tests"
else
  if [ -d "tests" ]; then
    if python3 -c "import sys; sys.exit(0)" >/dev/null 2>&1; then
      PY_TESTS=$(find tests/ -name "test_*.py" 2>/dev/null | wc -l)
      if [ "$PY_TESTS" -gt 0 ]; then
        if python3 -m unittest discover -s tests -v 2>&1; then
          ok "Todos los tests de Python pasan"
        else
          fail "Hay tests de Python rotos"
          EXIT_CODE=1
        fi
      fi
    else
      warn "Python no disponible, omitiendo tests de Python"
    fi

    BASH_TESTS=$(find tests/ -name "test_*.sh" 2>/dev/null | wc -l)
    if [ "$BASH_TESTS" -gt 0 ]; then
      echo "Encontrados $BASH_TESTS tests de Bash"
      for test in tests/test_*.sh; do
        if [ -x "$test" ]; then
          if bash "$test" 2>&1; then
            ok "Test $test pasó"
          else
            fail "Test $test falló"
            EXIT_CODE=1
          fi
        fi
      done
    fi

    if [ "$PY_TESTS" -eq 0 ] && [ "$BASH_TESTS" -eq 0 ]; then
      warn "No hay tests en tests/"
    fi
  else
    warn "Carpeta tests/ no existe todavía"
  fi
fi

echo ""
echo "── 11. Generando configuración inicial ─────────────────"

if [ -t 0 ]; then
  info "Para configurar el workflow, necesito información sobre el objetivo:"
  echo ""

  read -p "¿Cuál es el nombre del proyecto/objetivo? (ej: Auditoria-EmpresaX): " PROJECT_NAME
  read -p "¿Qué tipo de objetivo es? (web, red, api, mobile, red-interna): " PROJECT_TYPE
  read -p "¿Se subirá a GitHub? (y/n): " GITHUB_CHOICE

  if [[ "$GITHUB_CHOICE" =~ ^[Yy]$ ]]; then
    info "Se configurará .gitignore para excluir hallazgos sensibles"
    GITHUB_REPO=true
  else
    GITHUB_REPO=false
  fi
else
  PROJECT_NAME="Hacking Harness"
  PROJECT_TYPE="generic"
  GITHUB_REPO=false
  info "Modo no interactivo - usando valores por defecto"
fi

cat > .workflow-config.json <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_type": "$PROJECT_TYPE",
  "github_repo": $GITHUB_REPO,
  "initialized_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "harness_version": "2.0.0",
  "phases": {
    "1_recon": "pending",
    "2_scan": "pending",
    "3_exploit": "pending",
    "4_persist": "pending",
    "5_cleanup": "pending"
  }
}
EOF

ok "Configuración guardada en .workflow-config.json"

if [ "$GITHUB_REPO" = true ]; then
  if [ ! -f ".gitignore" ]; then
    cat > .gitignore <<EOF
# Hacking harness - archivos internos
/agents
/tasks
/skills
audits/
user/
*.md
!README.md

# Datos sensibles de auditorías
reports/
findings/
loot/
 screenshots/

# Dependencias
node_modules/
__pycache__/
*.pyc

# Entorno
.env
.DS_Store
EOF
    ok "Creado .gitignore inicial"
  else
    warn ".gitignore ya existe, no se sobrescribe"
  fi
fi

echo ""
echo "── 12. Verificando capa de specs ────────────────────"

if [ -d "specs" ]; then
  if [ -f "specs/_template.md" ]; then
    ok "Template de specs existe: _template.md"
  else
    warn "Falta _template.md en specs/"
  fi

  if [ -f "specs/_README.md" ]; then
    ok "Guía de specs existe: _README.md"
  else
    warn "Falta _README.md en specs/"
  fi

  ACTIVE_COUNT=0
  DRAFT_COUNT=0
  for dir in specs/*/; do
    if [ -f "${dir}spec.md" ]; then
      if grep -q "Estado.*active" "${dir}spec.md" 2>/dev/null; then
        ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
      elif grep -q "Estado.*draft" "${dir}spec.md" 2>/dev/null; then
        DRAFT_COUNT=$((DRAFT_COUNT + 1))
      fi
    fi
  done

  if [ "$ACTIVE_COUNT" -gt 0 ]; then
    ok "Specs activas: $ACTIVE_COUNT"
  else
    warn "No hay specs activas en specs/"
  fi
  if [ "$DRAFT_COUNT" -gt 0 ]; then
    warn "Specs en draft: $DRAFT_COUNT (promover a active cuando corresponda)"
  fi
else
  warn "Carpeta specs/ no existe (opcional para proyectos nuevos)"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  RESUMEN DE INICIALIZACIÓN"
echo "═══════════════════════════════════════════════════════════"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
  ok "Harness verificado correctamente. Puedes comenzar el pentesting."
  info "Objetivo: $PROJECT_NAME ($PROJECT_TYPE)"
  info "Fases disponibles: 5 (Recon → Scan → Exploit → Persist → Cleanup)"
  info "Configuración: .workflow-config.json"
else
  fail "Harness tiene problemas. Revisa los errores arriba."
fi

exit $EXIT_CODE
