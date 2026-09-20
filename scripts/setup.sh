#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Setup Script for Production AI Engineering
# Works on Linux and macOS
# =============================================================================

echo "=========================================="
echo "  Production AI Engineering - Setup"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo ""
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3.12 or higher from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]); then
    echo -e "${RED}Error: Python 3.12+ is required. Found Python ${PYTHON_VERSION}.${NC}"
    exit 1
fi

echo -e "${GREEN}Python ${PYTHON_VERSION} found.${NC}"

# Check if venv exists, create if not
echo ""
echo -e "${YELLOW}Setting up virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}Created .venv${NC}"
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate venv
echo ""
echo -e "${YELLOW}Activating virtual environment...${NC}"
# shellcheck disable=SC1091
source .venv/bin/activate
echo -e "${GREEN}Activated .venv${NC}"

# Upgrade pip
echo ""
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}pip upgraded.${NC}"

# Install dependencies
echo ""
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -e ".[all]" --quiet
echo -e "${GREEN}Dependencies installed.${NC}"

# Copy .env.example to .env if .env doesn't exist
echo ""
echo -e "${YELLOW}Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}Created .env from .env.example${NC}"
    echo -e "${YELLOW}Please edit .env with your configuration.${NC}"
else
    echo -e "${GREEN}.env already exists.${NC}"
fi

# Run initial checks
echo ""
echo -e "${YELLOW}Running linter...${NC}"
if ruff check . --quiet; then
    echo -e "${GREEN}Linting passed.${NC}"
else
    echo -e "${YELLOW}Linting found issues. Run 'ruff check .' to see details.${NC}"
fi

echo ""
echo -e "${YELLOW}Running type checker...${NC}"
if mypy . --quiet; then
    echo -e "${GREEN}Type checking passed.${NC}"
else
    echo -e "${YELLOW}Type checking found issues. Run 'mypy .' to see details.${NC}"
fi

echo ""
echo -e "${YELLOW}Running tests...${NC}"
if pytest --tb=short -q; then
    echo -e "${GREEN}Tests passed.${NC}"
else
    echo -e "${YELLOW}Some tests failed. Run 'pytest' to see details.${NC}"
fi

# Done
echo ""
echo "=========================================="
echo -e "${GREEN}  Setup complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your configuration"
echo "  2. Run 'source .venv/bin/activate' to activate the venv"
echo "  3. Run 'uvicorn app.main:app --reload' to start the server"
echo ""
echo "Useful commands:"
echo "  ruff check .          # Lint code"
echo "  ruff format .         # Format code"
echo "  mypy .                # Type check"
echo "  pytest                # Run tests"
echo "  pytest --cov=app      # Run tests with coverage"
