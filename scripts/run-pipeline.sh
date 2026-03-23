#!/bin/bash
#
# =============================================================================
#  GITHUB ACTIONS BASICS - LOCAL PIPELINE SIMULATOR
# =============================================================================
#
#  This script runs the same checks locally that GitHub Actions would run
#  in the cloud. Use it to verify your code BEFORE pushing to GitHub.
#
#  The Pipeline Stages:
#
#   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
#   │ 1.FILES  │──>│ 2.DEPS   │──>│ 3.UNIT   │──>│ 4.INTEG  │──>│ 5.DONE   │
#   │ (verify) │   │(install) │   │ (tests)  │   │ (tests)  │   │(summary) │
#   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
#
#  KEY CONCEPT: If ANY stage fails, the pipeline STOPS immediately.
#  This prevents broken code from being pushed to GitHub.
#
#  Usage:
#    chmod +x scripts/run-pipeline.sh
#    ./scripts/run-pipeline.sh
#
# =============================================================================

set -e  # EXIT IMMEDIATELY if any command fails (this is critical for pipelines!)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Track timing
PIPELINE_START=$(date +%s)

# Ensure we're in the project root
cd "$(dirname "$0")/.."
PROJECT_DIR=$(pwd)

# ===========================================================================
# HELPER FUNCTIONS
# ===========================================================================

stage_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${CYAN}  STAGE: $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

pass() {
    echo -e "  ${GREEN}✓ PASSED${NC}: $1"
}

fail() {
    echo -e "  ${RED}✗ FAILED${NC}: $1"
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  PIPELINE FAILED at stage: $2${NC}"
    echo -e "${RED}  The pipeline STOPPED. No further stages will run.${NC}"
    echo -e "${RED}  Fix the issue and run the pipeline again.${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
}

# ===========================================================================
# PIPELINE START
# ===========================================================================

echo ""
echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${CYAN}║     GitHub Actions Basics - Local Pipeline Starting...  ║${NC}"
echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Project:   ${PROJECT_DIR}"
echo -e "  Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "  Python:    $(python3 --version 2>/dev/null || python --version 2>/dev/null || echo 'NOT FOUND')"

# ===========================================================================
# STAGE 1: Verify Project Structure
# ===========================================================================

stage_header "1/5 - FILES (Verify Project Structure)"
echo "  Checking that all required files exist..."

REQUIRED_FILES=(
    "app/__init__.py"
    "app/greeter.py"
    "app/api.py"
    "tests/unit/test_greeter.py"
    "tests/integration/test_api.py"
    "requirements.txt"
    ".github/workflows/lab1-hello-world.yml"
    ".github/workflows/lab2-scheduled.yml"
    ".github/workflows/lab3-multi-trigger.yml"
)

ALL_FOUND=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "    ${GREEN}✓${NC} $file"
    else
        echo -e "    ${RED}✗${NC} $file  ${RED}(MISSING!)${NC}"
        ALL_FOUND=false
    fi
done

if [ "$ALL_FOUND" = true ]; then
    pass "All source files present"
else
    fail "Missing required files" "FILES"
fi

# ===========================================================================
# STAGE 2: Install Dependencies
# ===========================================================================

stage_header "2/5 - DEPS (Install Dependencies)"
echo "  Installing Python dependencies from requirements.txt..."
echo ""

# Detect python command
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

if $PYTHON_CMD -m pip install -r requirements.txt --quiet 2>&1; then
    pass "Dependencies installed successfully"
else
    fail "Failed to install dependencies" "DEPS"
fi

# ===========================================================================
# STAGE 3: Unit Tests
# ===========================================================================
#
#  Unit tests check individual functions in greeter.py.
#  They are FAST and run WITHOUT starting a server.
#  If these fail, integration tests are SKIPPED (fail fast!).
#

stage_header "3/5 - UNIT TESTS (fast, isolated)"
echo "  Running unit tests against greeter.py..."
echo "  These test individual functions WITHOUT starting a server."
echo ""

UNIT_START=$(date +%s)

if $PYTHON_CMD -m pytest tests/unit/ -v --tb=short 2>&1; then
    UNIT_END=$(date +%s)
    UNIT_TIME=$((UNIT_END - UNIT_START))
    echo ""
    pass "Unit tests passed (${UNIT_TIME}s)"
else
    UNIT_END=$(date +%s)
    UNIT_TIME=$((UNIT_END - UNIT_START))
    echo ""
    echo -e "  ${YELLOW}Hint: A unit test failed. Look at the FAILED line above.${NC}"
    echo -e "  ${YELLOW}      Check greeter.py -- did you change a function?${NC}"
    fail "Unit tests failed (${UNIT_TIME}s)" "UNIT TESTS"
fi

# ===========================================================================
# STAGE 4: Integration Tests
# ===========================================================================
#
#  Integration tests check the API endpoints.
#  They use Flask's test client to make real HTTP requests.
#  These are SLOWER but catch "wiring" bugs.
#

stage_header "4/5 - INTEGRATION TESTS (API endpoints)"
echo "  Running integration tests against the API endpoints..."
echo "  These test the full request/response cycle using Flask test client."
echo ""

INT_START=$(date +%s)

if $PYTHON_CMD -m pytest tests/integration/ -v --tb=short 2>&1; then
    INT_END=$(date +%s)
    INT_TIME=$((INT_END - INT_START))
    echo ""
    pass "Integration tests passed (${INT_TIME}s)"
else
    INT_END=$(date +%s)
    INT_TIME=$((INT_END - INT_START))
    echo ""
    echo -e "  ${YELLOW}Hint: Integration test failed. The API endpoint is broken.${NC}"
    echo -e "  ${YELLOW}      Check api.py -- is the routing or response correct?${NC}"
    fail "Integration tests failed (${INT_TIME}s)" "INTEGRATION TESTS"
fi

# ===========================================================================
# STAGE 5: Summary
# ===========================================================================

PIPELINE_END=$(date +%s)
TOTAL_TIME=$((PIPELINE_END - PIPELINE_START))

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                          ║${NC}"
echo -e "${GREEN}║       ✓  ALL CHECKS PASSED - READY TO PUSH!  ✓         ║${NC}"
echo -e "${GREEN}║                                                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Total time: ${TOTAL_TIME}s"
echo ""
echo -e "  ${BOLD}Pipeline Summary:${NC}"
echo -e "    ${GREEN}✓${NC} Files       - Project structure verified"
echo -e "    ${GREEN}✓${NC} Deps        - Dependencies installed"
echo -e "    ${GREEN}✓${NC} Unit Tests  - All greeter functions working correctly"
echo -e "    ${GREEN}✓${NC} Int. Tests  - All API endpoints responding correctly"
echo ""
echo -e "  ${BOLD}Next Steps:${NC}"
echo -e "    ${CYAN}1.${NC} Push to GitHub:  git add . && git commit -m 'feat: add greeter app' && git push"
echo -e "    ${CYAN}2.${NC} Watch Actions:   Go to GitHub > Actions tab"
echo -e "    ${CYAN}3.${NC} See workflows:   lab1-hello-world, lab2-scheduled, lab3-multi-trigger"
echo ""
