# Claude Code Development Tools

This document lists all custom Claude Code skills and sub-agents created to accelerate PedalBuild development.

## Overview

**Universal Tools** (available in ALL projects): Skills and sub-agents in `~/.claude/`
**Project-Specific Tools**: Sub-agents in `PedalBuild/.claude/agents/`

---

## Universal Skills

Located in `~/.claude/skills/` - Available across all projects

### 1. test-runner
**Purpose**: Run pytest tests with coverage reporting

**Usage**:
```bash
python ~/.claude/skills/test-runner/run_tests.py
python ~/.claude/skills/test-runner/run_tests.py --coverage
python ~/.claude/skills/test-runner/run_tests.py tests/test_specific.py
```

**When to Use**: After writing any Python code, before committing

### 2. format-and-lint
**Purpose**: Format and lint Python code (black, ruff, mypy)

**Usage**:
```bash
python ~/.claude/skills/format-and-lint/format_lint.py
python ~/.claude/skills/format-and-lint/format_lint.py src/backend/
python ~/.claude/skills/format-and-lint/format_lint.py --check
```

**When to Use**: Before committing, when pre-commit hooks fail

### 3. db-inspector
**Purpose**: Interactive SQLite/PostgreSQL database inspector

**Usage**:
```bash
python ~/.claude/skills/db-inspector/inspect_db.py                    # Interactive
python ~/.claude/skills/db-inspector/inspect_db.py --tables           # List tables
python ~/.claude/skills/db-inspector/inspect_db.py --schema circuits  # Show schema
python ~/.claude/skills/db-inspector/inspect_db.py --query "SELECT * FROM circuits"
python ~/.claude/skills/db-inspector/inspect_db.py --export circuits --output circuits.csv
```

**When to Use**: Debugging data issues, verifying migrations, exploring schema

### 4. type-sync-validator
**Purpose**: Validate TypeScript types match Python Pydantic models (zero drift)

**Usage**:
```bash
python ~/.claude/skills/type-sync-validator/validate_types.py
python ~/.claude/skills/type-sync-validator/validate_types.py --regenerate
python ~/.claude/skills/type-sync-validator/validate_types.py --verbose
```

**When to Use**: After changing Pydantic models, before committing, in pre-commit hooks

---

## Universal Sub-Agents

Located in `~/.claude/agents/` - Available across all projects

### 1. framework-verifier
**Purpose**: Verify latest API patterns for frameworks before writing code

**Model**: haiku (fast)
**Tools**: WebSearch, WebFetch, Write, Read

**When to Use**:
- Before implementing Next.js 15 App Router code
- Before implementing FastAPI routes
- Before implementing Google ADK agents
- Before using any framework API (training cutoff: Jan 2025)

**Example**:
> "Use framework-verifier to verify the latest Next.js 15 route handler API before implementing /api/circuits endpoint"

**Output**: Verification report with API signature, code example, sources, confidence level

### 2. schema-designer
**Purpose**: Design database schemas and migrations for SQLite/PostgreSQL

**Model**: sonnet
**Tools**: Read, Write, Grep, Glob

**When to Use**:
- Before Phase 2 database setup
- When creating new database tables
- Planning schema migrations
- Optimizing existing schemas

**Example**:
> "Use schema-designer to design the database schema for circuits, components, inventory, and projects tables"

**Output**: schema.sql, migration script, design documentation

### 3. test-writer
**Purpose**: Write comprehensive pytest test cases for Python code

**Model**: sonnet
**Tools**: Read, Write, Grep, Glob

**When to Use**:
- After implementing services/repositories
- After implementing agents
- When test coverage is low
- Proactively for TDD

**Example**:
> "Use test-writer to create comprehensive tests for src/backend/services/component_inventory.py"

**Output**: test_[module].py with happy path, edge cases, error cases, integration tests

### 4. api-integrator
**Purpose**: Build FastAPI REST API routes with proper error handling and validation

**Model**: sonnet
**Tools**: Read, Write, Grep, Glob

**When to Use**:
- When implementing REST API layer
- Creating CRUD endpoints
- Adding API documentation

**Example**:
> "Use api-integrator to create FastAPI routes for circuit management (CRUD operations)"

**Output**: routes/[resource].py, models/[resource].py (Pydantic), API documentation

---

## Domain Knowledge Reference

### Electronics Reference for Application Agents

**Location**: [docs/ELECTRONICS_REFERENCE.md](docs/ELECTRONICS_REFERENCE.md)

**Purpose**: Comprehensive electronics domain knowledge for implementing PedalBuild's Google ADK agents

**Content**:
- Electronic components (resistors, capacitors, transistors, op-amps, ICs)
- Schematic conventions (symbol recognition, orientations, reference designators)
- Guitar pedal circuit topology (overdrive, fuzz, delay, reverb)
- Breadboard layout principles (signal flow, power distribution, grounding)
- Component substitution rules (op-amps, transistors, capacitors)
- Common guitar pedal circuits (Tube Screamer, RAT, Big Muff, PT2399 delay)

**Used By**:
- Schematic Analyzer Agent (Google ADK)
- BOM Manager Service
- Breadboard Layout Agent (Google ADK)
- Component Inventory Service

**Note**: This is documentation for the APPLICATION's agents, not a Claude Code sub-agent.

---

## How Claude Code Uses These Tools

### During Development

**When Claude Code writes code**, it can:
1. **Spawn sub-agents** using the Task tool:
   ```
   Use framework-verifier to verify Next.js 15 API before implementation
   Use schema-designer to design database schema
   Use test-writer to write tests for component_inventory.py
   Use api-integrator to create FastAPI routes
   ```

2. **Invoke skills** using the Skill tool (once implemented):
   ```
   Run test-runner after implementing new service
   Run format-and-lint before committing
   Run type-sync-validator after changing Pydantic models
   Run db-inspector to debug data issues
   ```

3. **Reference documentation** for domain knowledge:
   ```
   Read docs/ELECTRONICS_REFERENCE.md for component specifications
   Read docs/ELECTRONICS_REFERENCE.md for schematic conventions
   Read docs/ELECTRONICS_REFERENCE.md for breadboard layout principles
   ```

### Workflow Example

**Scenario**: Implementing component inventory service

1. **Research** → Read `docs/ELECTRONICS_REFERENCE.md` for component categorization
2. **Design Schema** → Spawn `schema-designer` to design components table
3. **Implement** → Write component_inventory.py service
4. **Test** → Spawn `test-writer` to create comprehensive tests
5. **Validate** → Run `test-runner` skill to verify tests pass
6. **Format** → Run `format-and-lint` skill before committing
7. **Commit** → Pre-commit hooks run automatically

---

## Benefits of These Tools

### For Development Speed
- **Parallel Work**: Sub-agents research while Claude Code implements
- **No Context Pollution**: Research stays in sub-agent context
- **Reusable**: Universal tools work across all projects

### For Code Quality
- **Verified APIs**: framework-verifier ensures current best practices
- **Comprehensive Tests**: test-writer covers edge cases and errors
- **Type Safety**: type-sync-validator prevents Python/TypeScript drift
- **Clean Code**: format-and-lint ensures consistent style

### For Domain Knowledge
- **Electronics Reference**: Comprehensive documentation for guitar pedal building
- **Database Design**: schema-designer applies normalization and indexing best practices
- **API Design**: api-integrator follows REST conventions and FastAPI patterns

---

## Tool Statistics

**Total Claude Code Tools**: 8 (4 skills + 4 sub-agents)

**Universal Tools**: 8
- Skills: test-runner, format-and-lint, db-inspector, type-sync-validator
- Sub-agents: framework-verifier, schema-designer, test-writer, api-integrator

**Domain Documentation**: 1
- docs/ELECTRONICS_REFERENCE.md (for application agents, not Claude Code)

**Lines of Code**: ~3,000 lines across all Claude Code tools

---

## Next Steps

These tools are now available for use during Phase 2-6 implementation:
- Phase 2: Use schema-designer for database setup
- Phase 3: Use api-integrator for FastAPI routes, framework-verifier for Google ADK
- Phase 4: Use framework-verifier for Next.js 15, test-writer for all services
- Phase 5: Use test-runner for continuous testing
- All Phases: Reference docs/ELECTRONICS_REFERENCE.md for guitar pedal electronics knowledge

---

**Last Updated**: 2026-02-14

**See Also**:
- [CODING_STANDARDS.md](~/.claude/CODING_STANDARDS.md) - Universal coding standards
- [CLAUDE.md](CLAUDE.md) - Project-specific guidelines
- [ELECTRONICS_REFERENCE.md](docs/ELECTRONICS_REFERENCE.md) - Guitar pedal electronics domain knowledge
- [Implementation Plan](.claude/plans/sunny-stargazing-garden.md) - Complete Phase 1-6 plan
