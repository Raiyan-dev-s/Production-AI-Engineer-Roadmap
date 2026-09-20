#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Lint Script for Production AI Engineering
# Runs ruff check, ruff format, and mypy
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

EXIT_CODE=0

echo "=========================================="
echo "  Running Linting & Type Checking"
echo "=========================================="

# Ruff Check
echo ""
echo -e "${YELLOW}Running ruff check...${NC}"
if ruff check .; then
    echo -e "${GREEN}ruff check passed.${NC}"
else
    echo -e "${RED}ruff check failed.${NC}"
    EXIT_CODE=1
fi

# Ruff Format Check
echo ""
echo -e "${YELLOW}Running ruff format check...${NC}"
if ruff format --check .; then
    echo -e "${GREEN}ruff format check passed.${NC}"
else
    echo -e "${RED}ruff format check failed. Run 'ruff format .' to fix.${NC}"
    EXIT_CODE=1
fi

# Mypy
echo ""
echo -e "${YELLOW}Running mypy...${NC}"
if mypy .; then
    echo -e "${GREEN}mypy passed.${NC}"
else
    echo -e "${RED}mypy failed.${NC}"
    EXIT_CODE=1
fi

echo ""
echo "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}  All checks passed!${NC}"
else
    echo -e "${RED}  Some checks failed.${NC}"
fi
echo "=========================================="

exit $EXIT_CODE
