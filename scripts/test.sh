#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Test Script for Production AI Engineering
# Runs pytest with coverage
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  Running Tests"
echo "=========================================="

# Default to running all tests with coverage
PYTEST_ARGS=("$@")

if [ ${#PYTEST_ARGS[@]} -eq 0 ]; then
    echo ""
    echo -e "${YELLOW}Running all tests with coverage...${NC}"
    pytest --cov=app --cov-report=term-missing --cov-report=html -v
else
    echo ""
    echo -e "${YELLOW}Running tests with custom arguments...${NC}"
    pytest "${PYTEST_ARGS[@]}"
fi

EXIT_CODE=$?

echo ""
echo "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}  All tests passed!${NC}"
else
    echo -e "${RED}  Some tests failed.${NC}"
fi
echo "=========================================="

echo ""
echo "Coverage report: open htmlcov/index.html"

exit $EXIT_CODE
