# PedalBuild: Guitar Pedal Workflow Application

An intelligent end-to-end application for streamlining guitar pedal building from inspiration through final showcase, combining Google's ADK framework with Next.js.

## Overview

PedalBuild guides you through a 10-stage workflow:
1. **Inspiration** - Browse PedalPCB.com by pedal type
2. **Spec Download** - Extract build documentation PDFs
3. **Schematic Analysis** - AI vision analysis of schematics
4. **Inventory Check** - Match components against your inventory
5. **BOM Generation** - Organize components by type
6. **Breadboard Layout** - AI-optimized layout for your custom platform
7. **Prototype Testing** - Guided testing and validation
8. **Final Assembly** - Step-by-step enclosure assembly
9. **Graphics Design** - AI-assisted enclosure graphics
10. **Showcase** - Share your build with the community

## Features

- 🤖 **AI-Powered Agents**: Multi-pass schematic analysis, optimal breadboard layouts
- 📦 **Local-First**: SQLite database, no cloud dependencies
- 🔧 **Component Tracking**: Import from Excel, track inventory
- 🎨 **Custom Breadboard Platform**: Support for dual-board setup with power jumpers
- 📊 **Real-time Progress**: Live agent status updates during workflow
- 🎯 **PedalPCB Integration**: Direct browsing and PDF download
- 🖼️ **Fritzing Export**: Editable breadboard layouts + PNG images

## Quick Start

### Prerequisites

- **Python 3.11+** (required for backend)
- **Node.js 18+** (required for frontend)
- **uv** (Python package manager) - [Install](https://astral.sh/uv)
- Git

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd PedalBuild

# 1. Setup Python environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install Python dependencies
uv pip install -e '.[dev]'

# 3. Install Node dependencies
npm install

# 4. Setup pre-commit hooks (optional but recommended)
pre-commit install

# 5. Generate TypeScript types from Python models
npm run generate:types

# 6. Copy environment template
cp .env.local .env

# 7. Edit .env with your API keys (Anthropic, Google Gemini, etc.)
nano .env

# 8. Set up database
npm run setup:db

# 9. Start development servers (Python FastAPI + Next.js)
npm run dev
```

## Project Structure

```
/PedalBuild/
├── .claude/              # Custom Claude Code agents & skills
├── src/
│   ├── backend/          # Google ADK agents & API
│   ├── frontend/         # Next.js application
│   ├── models/           # TypeScript data models
│   ├── db/               # Database schema & migrations
│   └── shared/           # Shared types
├── data/                 # Local data storage
│   ├── db/              # SQLite database
│   ├── uploads/         # PDFs, schematics, photos
│   └── exports/         # Generated layouts & graphics
├── docs/                 # Documentation
└── tests/                # Test suites
```

## Development

### Running the Application

```bash
# Run development servers (Python FastAPI + Next.js)
npm run dev

# Run backend only (Python FastAPI with uvicorn)
npm run dev:backend

# Run frontend only (Next.js)
npm run dev:frontend
```

### Python Development

```bash
# ALWAYS activate venv first
source .venv/bin/activate

# Generate TypeScript types from Python models (run after changing Python types)
npm run generate:types

# Validate type synchronization
npm run validate:types

# Format Python code (black)
npm run format:py

# Lint + type check (ruff + mypy)
npm run lint:py

# Run Python tests (pytest)
npm test

# Run tests with coverage
npm run test:coverage
```

### Database

```bash
# Initialize SQLite database
npm run setup:db

# Run migrations (to be implemented)
npm run migrate
```

### Building for Production

```bash
# Build frontend (includes type generation)
npm run build
```

### Pre-commit Hooks

Pre-commit hooks automatically run:
- Code formatting (black)
- Linting (ruff)
- Type checking (mypy)
- Type validation (TypeScript ↔ Python sync)

```bash
# Install hooks (one-time)
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Documentation

### Python Development
- [PYTHON_SETUP.md](PYTHON_SETUP.md) - **START HERE** - Comprehensive Python development guide
- [TOOLING_DECISIONS.md](TOOLING_DECISIONS.md) - All tooling decisions explained and logged

### Project Documentation
- [CLAUDE.md](CLAUDE.md) - **Main project guide** for Claude Code (critical requirements, architecture, patterns)
- [Setup Guide](docs/SETUP.md) - Detailed installation instructions (to be created)
- [Architecture](docs/ARCHITECTURE.md) - Technical architecture overview (to be created)
- [API Reference](docs/API.md) - API endpoints documentation (to be created)
- [Agents Guide](docs/AGENTS.md) - Custom agent documentation (to be created)
- [User Guide](docs/USER_GUIDE.md) - How to use the application (to be created)

### Implementation
- [Implementation Plan](.claude/plans/sunny-stargazing-garden.md) - Complete Phase 1-6 plan

## Custom Claude Code Tools

This project includes reusable Claude Code sub-agents and skills (all in **Python**):

### Skills (`.claude/skills/` - Python)
- **excel-importer** ([importer.py](/.claude/skills/excel-importer/importer.py)) - Import inventory from CSV (250 lines)
  ```bash
  python .claude/skills/excel-importer/importer.py myInventory.csv --preview
  ```
- **component-inventory** ([service.py](/.claude/skills/component-inventory/service.py)) - Manage component stock (200 lines)
  ```bash
  python .claude/skills/component-inventory/service.py search "10k"
  python .claude/skills/component-inventory/service.py stats
  ```
- **bom-manager** ([service.py](/.claude/skills/bom-manager/service.py)) - Bill of materials management (220 lines)
  ```bash
  python .claude/skills/bom-manager/service.py validate <circuit-id>
  python .claude/skills/bom-manager/service.py shopping-list <circuit-id>
  ```

### Sub-Agents (`.claude/agents/` - To Be Built)
- **pedalpcb-scraper** - PedalPCB.com pedal browser (Python)
- **schematic-analyzer** - Multi-pass AI vision for schematics (Python + OpenCV)
- **breadboard-layout** - Optimal layout generation (Python + Fritzing export)

**Reusability**: These tools work with any electronics project!

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **UI**: React 18, Shadcn UI, TailwindCSS
- **Language**: TypeScript (auto-generated from Python models)
- **Type Safety**: Zero drift - types auto-generated from Python

### Backend (Python 3.11+)
- **Framework**: FastAPI (API server)
- **Agents**: Google ADK (Agent Development Kit)
- **Type System**: Pydantic v2 (single source of truth)
- **Data Processing**: pandas, BeautifulSoup4
- **Vision AI**: OpenCV, Pillow (schematic analysis)
- **Testing**: pytest
- **Web Search**: Brave Search API (for application agents)

### Database
- **Development**: SQLite
- **Production**: PostgreSQL (migration-ready)

### Python Tooling
- **Environment**: uv (10-100x faster than pip)
- **Dependencies**: pyproject.toml (PEP 621 standard)
- **Linting**: ruff (Rust-based, combines 10+ tools)
- **Type Checking**: mypy (Pydantic support)
- **Formatting**: black (100 char lines)
- **Pre-commit**: Automated quality checks

### AI Models
- **Claude** (Anthropic) - Schematic analysis, layout generation
- **Gemini** (Google) - Agent orchestration

### Additional Tools
- **Fritzing** - Breadboard layout export (.fzz + PNG)

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for development guidelines.

## License

[Your License Here]

## Acknowledgments

- PedalPCB.com for pedal specifications
- Google ADK team for the agentic framework
- DIY pedal building community

---

## Status

**Phase**: 1/6 Complete ✅

**Phase 1 Completed**:
- ✅ Python backend architecture established
- ✅ Pydantic models with auto-generated TypeScript (551 lines)
- ✅ Python tooling setup (uv, pyproject.toml, ruff, mypy, black, pytest)
- ✅ 3 custom Python skills (Excel Importer, Component Inventory, BOM Manager)
- ✅ Pre-commit hooks for automated quality checks
- ✅ Type synchronization system (zero drift)

**Next (Phase 2)**:
- Initialize Next.js 15 project
- Create FastAPI backend server
- Setup SQLite database with schema
- Build Google ADK orchestrator
- Implement 3 critical agents (PedalPCB Scraper, Schematic Analyzer, Breadboard Layout)

**Version**: 0.1.0-alpha

**Architecture**: Next.js (TypeScript) frontend + Python (FastAPI) backend with auto-generated types

For questions or support, open an issue on GitHub.
