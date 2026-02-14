# Python Tooling Decisions - PedalBuild

## Summary

All tooling decisions aligned before Phase 2 implementation. This document serves as the single source of truth for Python development setup.

---

## ✅ Decisions Made

### 1. Environment Management: **uv** ✅

**Decision**: Use `uv` instead of `pip`/`venv`

**Rationale**:
- 10-100x faster dependency resolution (Rust-based)
- Better dependency conflict detection
- Lock files for reproducible builds
- Compatible with existing Python workflows
- Single binary installation

**Setup**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install -e '.[dev]'
```

**npm script**: `npm run setup:venv`

---

### 2. Dependency Management: **pyproject.toml** ✅

**Decision**: Use `pyproject.toml` (PEP 621 standard) over `requirements.txt`

**Rationale**:
- Modern Python standard (3.11+)
- Single source of truth for all configuration
- Dependency groups (prod vs dev)
- Project metadata included
- Native uv support

**File**: [pyproject.toml](pyproject.toml)

**Migration**: Keep `requirements.txt` temporarily for backwards compatibility, but pyproject.toml is primary

---

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

**Command**: `npm run lint:py`

---

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

**Command**: `npm run lint:py` (includes mypy)

---

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

**Command**: `npm run format:py`

---

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

**Commands**:
- `npm test` - Run all tests
- `npm run test:coverage` - With coverage report

---

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

**File**: [.pre-commit-config.yaml](.pre-commit-config.yaml)

**Setup**: `npm run precommit:install`

---

### 8. Python Version: **3.11+** ✅

**Decision**: Require Python 3.11 or higher

**Rationale**:
- Better performance (10-25% faster than 3.10)
- Improved type hints (Self, LiteralString, etc.)
- Better error messages
- FastAPI/Pydantic fully compatible
- Modern standard

**Enforcement**: `pyproject.toml` requires-python = ">=3.11"

---

### 9. Type Synchronization: **Auto-generation** ✅

**Decision**: Generate TypeScript types from Python Pydantic models

**Rationale**:
- Single source of truth (Python)
- Prevents type drift between frontend/backend
- Automated in build process
- Validated in pre-commit hooks

**Script**: `scripts/generate-types.py`

**Commands**:
- `npm run generate:types` - Generate TypeScript
- `npm run validate:types` - Validate sync

**Output**: 551 lines of TypeScript auto-generated

---

### 10. Dependency Locking: **uv.lock** ✅

**Decision**: Use uv's built-in lock file mechanism

**Rationale**:
- Reproducible builds
- Pin exact versions
- Separate dev/prod dependencies
- Automatic with uv

**File**: `uv.lock` (generated automatically by uv)

---

## Other Decisions

### Line Length: **100 characters** ✅

**Decision**: Use 100-character line length (not 88 or 120)

**Rationale**:
- Balance between readability and screen space
- Modern displays support wider lines
- Common in modern Python projects
- Consistent across black, ruff, mypy

**Applied to**: black, ruff, all tools

---

### Import Organization: **Automatic (ruff)** ✅

**Decision**: Let ruff handle import sorting (isort replacement)

**Rationale**:
- ruff includes isort functionality
- Faster than standalone isort
- One less tool to configure
- Auto-fixes on pre-commit

**Configuration**: ruff select = ["I"] (import sorting)

---

### Code Complexity Limits: **Disabled** ✅

**Decision**: Disable complexity limits (McCabe)

**Rationale**:
- Focus on readability over metrics
- AI-generated code can be verbose
- Refactor when needed, not by metric
- ruff still catches actual issues

**Configuration**: ruff ignore = ["C901"] (complexity)

---

### Docstring Style: **Not enforced** ✅

**Decision**: No strict docstring requirements (yet)

**Rationale**:
- Focus on type hints first (more valuable)
- Add docstring enforcement in Phase 3
- Code is self-documenting with good names + types

**Future**: May add pydocstyle checks later

---

## Files Created

1. **pyproject.toml** - All configuration
2. **.pre-commit-config.yaml** - Pre-commit hooks
3. **PYTHON_SETUP.md** - Developer guide
4. **MIGRATION_GUIDE.md** - requirements.txt → pyproject.toml migration
5. **TOOLING_DECISIONS.md** - This file

---

## Commands Quick Reference

```bash
# Setup (first time)
uv venv && source .venv/bin/activate
uv pip install -e '.[dev]'
pre-commit install

# Development
npm run generate:types           # After changing Python models
npm run format:py                # Format code
npm run lint:py                  # Lint + type check
npm test                         # Run tests

# Git workflow
git add .
git commit -m "message"          # Pre-commit hooks run automatically
```

---

## Future Considerations

### Potential Changes (Phase 3+)

1. **pyright** over mypy
   - Faster type checking
   - Better VSCode integration
   - Evaluate if mypy becomes bottleneck

2. **Docstring enforcement**
   - Add pydocstyle to ruff config
   - Enforce Google or NumPy style
   - Only after core functionality complete

3. **Coverage requirements**
   - Require minimum test coverage (e.g., 80%)
   - Enforce in pre-commit or CI/CD
   - Add after more tests written

4. **Security scanning**
   - Add bandit for security checks
   - Scan dependencies with safety
   - Important for production deployment

5. **Performance profiling**
   - Add py-spy or scalene
   - Profile agent execution
   - Optimize bottlenecks

---

## Why These Decisions Matter

### Speed
- **uv**: 10-100x faster dependency resolution
- **ruff**: 10-100x faster linting
- **black**: Instant formatting
- **Total**: Significantly faster development cycle

### Reliability
- **Type safety**: Python (mypy) + TypeScript (auto-generated)
- **Pre-commit**: Catch issues before commit
- **Lock files**: Reproducible builds
- **Validation**: Auto-check type sync

### Developer Experience
- **Single config**: pyproject.toml for everything
- **Auto-formatting**: No style debates
- **Auto-fixing**: ruff fixes most issues
- **Clear errors**: mypy + pytest give good feedback

### Maintainability
- **Standard approach**: PEP 621 compliance
- **Future-proof**: Modern Python ecosystem
- **Less boilerplate**: Fewer config files
- **Clear separation**: Prod vs dev dependencies

---

## Alignment with Project Goals

### From CLAUDE.md

**User Preference**: "I prefer to use uv for venv management"
✅ **Implemented**: uv as primary environment manager

**Critical Requirements**:
- Type safety between frontend/backend
✅ **Implemented**: Auto-generate TypeScript from Python

- Fast iteration cycle
✅ **Implemented**: Fast tools (uv, ruff, black)

- Local-first architecture
✅ **Implemented**: All tools work offline

- Simplicity over abstraction
✅ **Implemented**: Single pyproject.toml, minimal config

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

**Status**: All tooling decisions finalized ✅
**Ready For**: Phase 2 - Next.js + FastAPI implementation

**Last Updated**: 2026-02-14
