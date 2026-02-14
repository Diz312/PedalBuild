# Python Development Setup Guide

## Overview

PedalBuild uses modern Python tooling for optimal developer experience and code quality.

**Stack:**
- **Environment**: `uv` (fast, modern package installer)
- **Dependencies**: `pyproject.toml` (PEP 621 standard)
- **Linting**: `ruff` (Rust-based, 10-100x faster than flake8)
- **Formatting**: `black` (opinionated, consistent)
- **Type Checking**: `mypy` (industry standard)
- **Testing**: `pytest` (modern, powerful)
- **Pre-commit**: Automated checks before commits

---

## Initial Setup

### 1. Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### 2. Create Virtual Environment

```bash
# Create .venv using uv
uv venv

# Activate venv
source .venv/bin/activate

# On Windows (Git Bash)
source .venv/Scripts/activate
```

### 3. Install Dependencies

```bash
# Install all dependencies (including dev dependencies)
uv pip install -e '.[dev]'

# This installs:
# - Core deps: fastapi, pydantic, pandas, etc.
# - Dev deps: pytest, black, ruff, mypy, pre-commit
```

### 4. Setup Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Test hooks (optional)
pre-commit run --all-files
```

---

## Development Workflow

### Generate TypeScript Types

```bash
# Generate TypeScript types from Python Pydantic models
npm run generate:types

# Output: src/models/types.generated.ts (551 lines)
```

### Validate Types

```bash
# Ensure TypeScript types match Python models
npm run validate:types

# This runs automatically in pre-commit hook when types.py changes
```

### Code Formatting

```bash
# Format Python code (black + ruff)
npm run format:py

# Or manually:
black src/
ruff check --fix src/
```

### Linting

```bash
# Lint Python code
npm run lint:py

# This runs:
# 1. ruff check (fast linter)
# 2. mypy (type checker)
```

### Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
pytest tests/test_component_inventory.py

# Run with verbose output
pytest -v
```

---

## Using Skills CLI

All Python skills have CLI interfaces for testing:

### Component Inventory

```bash
# List all components
python .claude/skills/component-inventory/service.py list

# Search for components
python .claude/skills/component-inventory/service.py search "10k"

# Show low stock
python .claude/skills/component-inventory/service.py low-stock

# Show statistics
python .claude/skills/component-inventory/service.py stats
```

### Excel Importer

```bash
# Preview import (no changes)
python .claude/skills/excel-importer/importer.py myInventory.csv --preview

# Actual import
python .claude/skills/excel-importer/importer.py myInventory.csv --db data/db/pedalbuild.db
```

### BOM Manager

```bash
# Show BOM for circuit
python .claude/skills/bom-manager/service.py show triangulum-overdrive

# Validate BOM against inventory
python .claude/skills/bom-manager/service.py validate triangulum-overdrive

# Generate shopping list
python .claude/skills/bom-manager/service.py shopping-list triangulum-overdrive

# Export BOM as CSV
python .claude/skills/bom-manager/service.py export triangulum-overdrive
```

---

## Tool Configuration

All tools are configured in `pyproject.toml` for consistency.

### Black (Code Formatter)

```toml
[tool.black]
line-length = 100
target-version = ['py311']
```

**Why 100 characters?**
- Modern displays support wider lines
- Reduces vertical scrolling
- More code visible at once

### Ruff (Linter)

```toml
[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort (import sorting)
    "B",   # flake8-bugbear (bug detection)
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade (modern Python syntax)
]
```

**What it checks:**
- Code style violations
- Unused imports/variables
- Buggy patterns
- Import organization
- Outdated syntax

### Mypy (Type Checker)

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]
```

**What it enforces:**
- All functions must have type hints
- Pydantic models are type-checked
- Return types must be annotated

### Pytest (Testing)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

**Features:**
- Auto-discovers tests in `tests/` directory
- Imports work correctly with `src` layout

---

## Pre-commit Hooks

When you `git commit`, these checks run automatically:

1. **Trailing whitespace** - Removes trailing spaces
2. **End of file fixer** - Ensures newline at EOF
3. **YAML/JSON/TOML checks** - Validates file syntax
4. **Large files check** - Prevents committing files >1MB
5. **Black** - Auto-formats Python code
6. **Ruff** - Lints and auto-fixes issues
7. **Mypy** - Type checks Python code
8. **Type validation** - Ensures TypeScript types match Python models

**Skip hooks (emergency only):**
```bash
git commit --no-verify -m "message"
```

---

## Dependency Management

### Adding Dependencies

```bash
# Add a production dependency
uv pip install <package>

# Then update pyproject.toml manually or:
uv pip freeze | grep <package> >> requirements.txt

# Better: Edit pyproject.toml directly
# [project]
# dependencies = [
#     "new-package>=1.0.0",
# ]

# Then reinstall
uv pip install -e '.[dev]'
```

### Updating Dependencies

```bash
# Update all packages
uv pip install --upgrade -e '.[dev]'

# Update specific package
uv pip install --upgrade <package>
```

### Lock Files

uv automatically creates `uv.lock` for reproducible builds:

```bash
# Lock current dependencies
uv pip compile pyproject.toml -o requirements.lock

# Install from lock file
uv pip install -r requirements.lock
```

---

## Common Commands Cheat Sheet

```bash
# Setup (first time)
uv venv && source .venv/bin/activate
uv pip install -e '.[dev]'
pre-commit install

# Daily workflow
npm run generate:types           # After changing Python models
npm run format:py                # Format code
npm run lint:py                  # Check for issues
npm test                         # Run tests

# Before committing
git add .
git commit -m "message"          # Pre-commit hooks run automatically

# If hooks fail, fix issues and retry:
npm run format:py
npm run lint:py
git add .
git commit -m "message"
```

---

## Troubleshooting

### "ModuleNotFoundError" when running Python scripts

**Solution**: Ensure venv is activated
```bash
source .venv/bin/activate
```

### "command not found: uv"

**Solution**: Install uv or add to PATH
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Add to PATH if needed
export PATH="$HOME/.cargo/bin:$PATH"
```

### Pre-commit hooks failing

**Solution**: Run checks manually to see detailed errors
```bash
black src/
ruff check --fix src/
mypy src/
python scripts/validate-types.py
```

### Type generation fails

**Solution**: Ensure Pydantic is installed
```bash
uv pip install pydantic
python scripts/generate-types.py
```

### Tests can't find modules

**Solution**: Install package in editable mode
```bash
uv pip install -e .
```

---

## Why These Tools?

### uv over pip/venv
- **10-100x faster** dependency resolution
- **Better conflict detection**
- **Reproducible builds** with lock files
- **Single binary** (no Python required)
- **Compatible** with existing workflows

### pyproject.toml over requirements.txt
- **PEP 621 standard** (modern Python)
- **Single source of truth** for all tools
- **Dependency groups** (dev vs prod)
- **Project metadata** included
- **Future-proof** (Python 3.11+)

### ruff over flake8/pylint
- **10-100x faster** (Rust-based)
- **Combines 10+ tools** (flake8, isort, pydocstyle, etc.)
- **Auto-fix** capabilities
- **Easy configuration**
- **Active development**

### black over other formatters
- **Opinionated** (no debates)
- **Consistent** (deterministic output)
- **Fast**
- **Industry standard**
- **Low configuration**

### mypy over pyright
- **Industry standard**
- **Excellent Pydantic support**
- **Mature ecosystem**
- **Better error messages**

Note: **pyright** is also excellent (especially with VSCode). Consider switching if you prefer faster checks and better IDE integration.

---

## Next Steps

1. ✅ Environment setup complete
2. ✅ Dependencies installed
3. ✅ Pre-commit hooks configured
4. ✅ Type generation working

**Ready for Phase 2:**
- Initialize Next.js 15 project
- Create FastAPI backend server
- Setup SQLite database
- Build Google ADK orchestrator

---

**Last Updated**: 2026-02-14
