# Python Development Guide

**Purpose**: Comprehensive guide for Python development in PedalBuild - covering setup, tooling, decisions, and daily workflow.

**Last Updated**: 2026-02-14

---

## Table of Contents

1. [Overview](#overview)
2. [Tooling Stack & Decisions](#tooling-stack--decisions)
3. [Initial Setup](#initial-setup)
4. [Development Workflow](#development-workflow)
5. [Tool Configuration](#tool-configuration)
6. [Pre-commit Hooks](#pre-commit-hooks)
7. [Dependency Management](#dependency-management)
8. [Troubleshooting](#troubleshooting)
9. [Why These Tools](#why-these-tools)

---

## Overview

PedalBuild uses modern Python tooling for optimal developer experience and code quality.

**Stack:**
- **Environment**: `uv` (10-100x faster than pip)
- **Dependencies**: `pyproject.toml` (PEP 621 standard)
- **Linting**: `ruff` (Rust-based, combines 10+ tools)
- **Type Checking**: `mypy` (industry standard, Pydantic support)
- **Formatting**: `black` (opinionated, 100 char lines)
- **Testing**: `pytest` (modern, powerful)
- **Pre-commit**: Automated quality checks

### Type Synchronization
- **Single Source of Truth**: Python Pydantic models
- **Auto-Generated TypeScript**: 551 lines, zero drift possible
- **Validation**: Runs in pre-commit hook

---

## Tooling Stack & Decisions

All tooling decisions are documented with rationale. This section explains WHY we chose each tool.

### 1. Environment Management: **uv** ✅

**Decision**: Use `uv` instead of `pip`/`venv`

**Rationale**:
- 10-100x faster dependency resolution (Rust-based)
- Better dependency conflict detection
- Lock files for reproducible builds
- Compatible with existing Python workflows
- Single binary installation
- User preference (explicitly requested)

**Alternatives Considered**: pip, pipenv, poetry

### 2. Dependency Management: **pyproject.toml** ✅

**Decision**: Use `pyproject.toml` (PEP 621 standard) over `requirements.txt`

**Rationale**:
- Modern Python standard (3.11+)
- Single source of truth for all configuration
- Dependency groups (prod vs dev)
- Project metadata included
- Native uv support
- Future-proof

**Migration**: Removed requirements.txt, pyproject.toml is primary

### 3. Linting: **ruff** ✅

**Decision**: Use `ruff` as primary linter

**Rationale**:
- 10-100x faster than flake8/pylint (Rust-based)
- Combines 10+ tools (flake8, isort, pydocstyle, etc.)
- Auto-fix capabilities
- Easy configuration in pyproject.toml
- Active development, modern

**Configuration**:
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
```

**What it checks:**
- Code style violations
- Unused imports/variables
- Buggy patterns
- Import organization
- Outdated syntax

### 4. Type Checking: **mypy** ✅

**Decision**: Use `mypy` for static type checking

**Rationale**:
- Industry standard
- Excellent Pydantic support (via plugin)
- Mature ecosystem
- Good error messages
- Enforces type safety across codebase

**Alternative Considered**: `pyright` (faster, better VSCode integration)
- Could switch later if needed
- mypy sufficient for now

**Configuration**:
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]
```

**What it enforces:**
- All functions must have type hints
- Pydantic models are type-checked
- Return types must be annotated

### 5. Code Formatting: **black** ✅

**Decision**: Use `black` for auto-formatting

**Rationale**:
- Opinionated (no configuration debates)
- Industry standard
- Fast, deterministic
- Low maintenance
- Consistent output

**Configuration**:
```toml
[tool.black]
line-length = 100
target-version = ['py311']
```

**Why 100 characters?**
- Modern displays support wider lines
- Reduces vertical scrolling
- More code visible at once
- Common in modern Python projects

### 6. Testing: **pytest** ✅

**Decision**: Use `pytest` for all testing

**Rationale**:
- Modern, powerful
- Great plugin ecosystem
- Fixtures for reusable test setup
- Parametrization for data-driven tests
- Excellent error output

**Configuration**:
```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
pythonpath = ["src"]
```

### 7. Pre-commit Hooks: **pre-commit** ✅

**Decision**: Use `pre-commit` framework for automated checks

**Rationale**:
- Catches issues before commit
- Consistent across team
- Runs multiple checks (formatting, linting, type checking)
- Custom hook for type validation

**Hooks Configured**:
1. Trailing whitespace removal
2. End-of-file fixer
3. YAML/JSON/TOML validation
4. Large file check (>1MB blocked)
5. **black** - Auto-format Python
6. **ruff** - Lint and auto-fix
7. **mypy** - Type check
8. **validate-types** - Ensure TypeScript ↔ Python type sync

### 8. Python Version: **3.11+** ✅

**Decision**: Require Python 3.11 or higher

**Rationale**:
- Better performance (10-25% faster than 3.10)
- Improved type hints (Self, LiteralString, etc.)
- Better error messages
- FastAPI/Pydantic fully compatible
- Modern standard

**Enforcement**: `pyproject.toml` requires-python = ">=3.11"

### 9. Line Length: **100 characters** ✅

**Decision**: Use 100-character line length (not 88 or 120)

**Rationale**:
- Balance between readability and screen space
- Modern displays support wider lines
- Common in modern Python projects
- Consistent across black, ruff, mypy

**Applied to**: black, ruff, all tools

### 10. Import Organization: **Automatic (ruff)** ✅

**Decision**: Let ruff handle import sorting (isort replacement)

**Rationale**:
- ruff includes isort functionality
- Faster than standalone isort
- One less tool to configure
- Auto-fixes on pre-commit

**Configuration**: ruff select = ["I"] (import sorting)

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

### Using Services CLI

All Python services have CLI interfaces for testing:

#### Component Inventory
```bash
python src/backend/services/component_inventory.py list
python src/backend/services/component_inventory.py search "10k"
python src/backend/services/component_inventory.py low-stock
python src/backend/services/component_inventory.py stats
```

#### BOM Manager
```bash
python src/backend/services/bom_manager.py show <circuit-id>
python src/backend/services/bom_manager.py validate <circuit-id>
python src/backend/services/bom_manager.py shopping-list <circuit-id>
python src/backend/services/bom_manager.py export <circuit-id>
```

#### Excel Importer
```bash
# Preview import (no changes)
python src/backend/services/excel_importer.py myInventory.csv --preview

# Actual import
python src/backend/services/excel_importer.py myInventory.csv --db data/db/pedalbuild.db
```

---

## Tool Configuration

All tools are configured in `pyproject.toml` for consistency.

### Complete Configuration

```toml
[project]
name = "pedalbuild"
version = "0.1.0"
requires-python = ">=3.11"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"

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

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
pythonpath = ["src"]
```

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

**Configuration**: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic]

  - repo: local
    hooks:
      - id: validate-types
        name: Validate TypeScript/Python type synchronization
        entry: python scripts/validate-types.py
        language: system
        files: 'src/models/types\.py$'
```

---

## Dependency Management

### Adding Dependencies

```bash
# Add a production dependency
uv pip install <package>

# Then update pyproject.toml manually:
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
- **User preference** (explicitly requested)

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

**Note**: pyright is also excellent (especially with VSCode). Consider switching if you prefer faster checks and better IDE integration.

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

## Decision Log

| Date | Decision | Rationale | Status |
|------|----------|-----------|--------|
| 2026-02-14 | Use uv | User preference, 10-100x faster | ✅ Implemented |
| 2026-02-14 | pyproject.toml | Modern standard, single config | ✅ Implemented |
| 2026-02-14 | ruff | Fast, combines multiple tools | ✅ Implemented |
| 2026-02-14 | mypy | Industry standard, Pydantic support | ✅ Implemented |
| 2026-02-14 | black | Opinionated, consistent | ✅ Implemented |
| 2026-02-14 | pytest | Modern, powerful | ✅ Implemented |
| 2026-02-14 | pre-commit | Automated quality checks | ✅ Implemented |
| 2026-02-14 | Python 3.11+ | Performance, modern features | ✅ Implemented |
| 2026-02-14 | 100 char lines | Modern displays, readability | ✅ Implemented |

---

## See Also

- **Universal Standards**: `~/.claude/CODING_STANDARDS.md` - Code Accuracy Protocol and universal patterns
- **Project Guide**: `CLAUDE.md` - Project-specific guidelines for Claude Code
- **Quick Start**: `README.md` - Getting started with PedalBuild
- **Tools**: `CLAUDE_CODE_TOOLS.md` - Claude Code development tools

---

**Status**: All tooling finalized ✅
**Ready For**: Phase 2 - Next.js + FastAPI implementation

**Last Updated**: 2026-02-14
