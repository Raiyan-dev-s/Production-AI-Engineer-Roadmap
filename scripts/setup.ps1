# =============================================================================
# Setup Script for Production AI Engineering (Windows PowerShell)
# =============================================================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Production AI Engineering - Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check Python version
Write-Host ""
Write-Host "Checking Python version..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python not found" }
} catch {
    Write-Host "Error: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.12+ from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Parse version
$versionMatch = [regex]::Match($pythonVersion, '(\d+)\.(\d+)\.(\d+)')
$major = [int]$versionMatch.Groups[1].Value
$minor = [int]$versionMatch.Groups[2].Value

if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
    Write-Host "Error: Python 3.12+ is required. Found $pythonVersion." -ForegroundColor Red
    exit 1
}

Write-Host "Python $major.$minor found." -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "Setting up virtual environment..." -ForegroundColor Yellow

if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "Created .venv" -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
Write-Host "Activated .venv" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
pip install --upgrade pip --quiet
Write-Host "pip upgraded." -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -e ".[all]" --quiet
Write-Host "Dependencies installed." -ForegroundColor Green

# Copy .env.example to .env
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example" -ForegroundColor Green
    Write-Host "Please edit .env with your configuration." -ForegroundColor Yellow
} else {
    Write-Host ".env already exists." -ForegroundColor Green
}

# Run checks
Write-Host ""
Write-Host "Running linter..." -ForegroundColor Yellow

ruff check . --quiet 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Linting passed." -ForegroundColor Green
} else {
    Write-Host "Linting found issues. Run 'ruff check .' to see details." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Running type checker..." -ForegroundColor Yellow

mypy . --quiet 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Type checking passed." -ForegroundColor Green
} else {
    Write-Host "Type checking found issues. Run 'mypy .' to see details." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Running tests..." -ForegroundColor Yellow

pytest --tb=short -q 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Tests passed." -ForegroundColor Green
} else {
    Write-Host "Some tests failed. Run 'pytest' to see details." -ForegroundColor Yellow
}

# Done
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Edit .env with your configuration"
Write-Host "  2. Run '.\.venv\Scripts\Activate.ps1' to activate the venv"
Write-Host "  3. Run 'uvicorn app.main:app --reload' to start the server"
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  ruff check .          # Lint code"
Write-Host "  ruff format .         # Format code"
Write-Host "  mypy .                # Type check"
Write-Host "  pytest                # Run tests"
Write-Host "  pytest --cov=app      # Run tests with coverage"
