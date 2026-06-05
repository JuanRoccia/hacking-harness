#!/usr/bin/env bash
# test_init.sh - Validate that hackings init.sh works correctly

set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; exit 1; }

echo "═══════════════════════════════════════════════════════"
echo "  TEST INIT.SH (HACKING HARNESS)"
echo "═══════════════════════════════════════════════════════"
echo ""

echo "Test 1: init.sh exists and is executable"
if [ ! -f "init.sh" ]; then
  fail "init.sh does not exist"
fi
if [ ! -x "init.sh" ]; then
  echo "  Warning: init.sh not executable, making it executable..."
  chmod +x init.sh
fi
ok "init.sh exists and is executable"

echo ""
echo "Test 2: Syntax check for init.sh"
if bash -n init.sh 2>/dev/null; then
  ok "init.sh syntax is valid"
else
  fail "init.sh has syntax errors"
fi

echo ""
echo "Test 3: Execution of init.sh (non-interactive mode)"
output=$(WORKFLOW_TEST=1 bash init.sh 2>&1)
if echo "$output" | grep -q "\[FAIL\]"; then
  fail "init.sh reports errors"
fi
ok "init.sh executes without fatal errors"

echo ""
echo "Test 4: Verify init.sh checks hacking agent files"
if grep -q "01-recon-agent.md" init.sh && \
   grep -q "02-scan-agent.md" init.sh && \
   grep -q "03-exploit-agent.md" init.sh; then
  ok "init.sh verifies hacking agent files"
else
  fail "init.sh does not verify all hacking agent files"
fi

echo ""
echo "Test 5: Verify init.sh checks hacking tools"
if grep -q "nmap" init.sh && \
   grep -q "curl" init.sh && \
   grep -q "python3" init.sh; then
  ok "init.sh checks hacking tools (nmap, curl, python3)"
else
  fail "init.sh missing expected hacking tool checks"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ALL INIT.SH TESTS PASSED"
echo "═══════════════════════════════════════════════════════"
