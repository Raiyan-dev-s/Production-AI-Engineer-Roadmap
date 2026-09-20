# Local Development Environment Setup

Step-by-step guide to setting up this project on your machine.

## Prerequisites

### Python 3.12+

```bash
# Check if Python is installed
python --version
# Should show Python 3.12.x or higher

# If not installed, download from https://www.python.org/downloads/
# On Windows, check "Add Python to PATH" during installation
```

### Git

```bash
# Check if Git is installed
git --version
```

## Setup Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-production-kit
```

### 2. Create a Virtual Environment

```bash
# Using venv (built-in)
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all dependencies (core + dev + AI)
pip install -e ".[all]"

# Or just core dependencies
pip install -e .
```

### 4. Set Up Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and fill in your values
# At minimum, set a SECRET_KEY for development
```

### 5. Verify Installation

```bash
# Run linter
ruff check .

# Run type checker
mypy .

# Run tests
pytest
```

## IDE Configuration

### VS Code

Install these extensions:
- Python (ms-python.python)
- Ruff (charliermarsh.ruff)
- Pylance (ms-python.vscode-pylance)

Recommended `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": ".venv/Scripts/python.exe",
    "python.testing.pytestEnabled": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        }
    }
}
```

### PyCharm

1. Open the project folder
2. Set Python interpreter to `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (macOS/Linux)
3. Enable "Run with Python Console"

## Common Issues

### "python not found"

Python is not in your PATH. Reinstall Python with "Add to PATH" checked, or add it manually.

### "pip not found"

```bash
python -m pip install --upgrade pip
```

### Import errors

Make sure your virtual environment is activated:
```bash
# Check which Python you're using
which python
# Should point to .venv/Scripts/python or .venv/bin/python
```

### mypy errors about missing stubs

```bash
pip install types-requests
```

## Quick Start Script

Run the setup script for automated setup:
```bash
# macOS/Linux
bash scripts/setup.sh

# Windows
.\scripts\setup.ps1
```
