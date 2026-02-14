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
git clone https://github.com/Diz312/PedalBuild
cd PedalBuild

# Setup Python environment
uv venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e '.[dev]'

# Install Node dependencies
npm install

# Setup pre-commit hooks
pre-commit install

# Generate TypeScript types
npm run generate:types

# Setup environment
cp .env.example .env
nano .env  # Add your API keys

# Initialize database
npm run setup:db

# Start development servers
npm run dev
```

### First Steps

1. **Import your component inventory**: `python src/backend/services/excel_importer.py myInventory.csv`
2. **Browse PedalPCB circuits**: Visit http://localhost:3000
3. **Start building**: Follow the 10-stage workflow

## Documentation

### For Developers
- **[PYTHON_DEVELOPMENT.md](PYTHON_DEVELOPMENT.md)** - Complete Python setup, tooling, decisions, and workflow
- **[CLAUDE.md](CLAUDE.md)** - Project guidelines for Claude Code development
- **[CLAUDE_CODE_TOOLS.md](CLAUDE_CODE_TOOLS.md)** - Claude Code development tools
- **[docs/ELECTRONICS_REFERENCE.md](docs/ELECTRONICS_REFERENCE.md)** - Guitar pedal electronics knowledge

### For Users
- **[User Guide](docs/USER_GUIDE.md)** - How to use the application (to be created)
- **[Architecture](docs/ARCHITECTURE.md)** - Technical architecture overview (to be created)
- **[API Reference](docs/API.md)** - API endpoints documentation (to be created)

## Technology Stack

**Frontend:**
- Next.js 15 (App Router), React 18, Shadcn UI, TailwindCSS
- TypeScript (auto-generated from Python models)

**Backend:**
- Python 3.11+ with FastAPI
- Google ADK (Agent Development Kit)
- Pydantic v2 (type system, single source of truth)

**Database:**
- SQLite (development)
- PostgreSQL-ready (production migration path)

**Python Tooling:**
- uv (environment & dependencies)
- ruff (linting), mypy (type checking), black (formatting)
- pytest (testing), pre-commit (automated quality checks)

**AI Models:**
- Claude (Anthropic) - Schematic analysis, layout generation
- Gemini (Google) - Agent orchestration

## Development

### Common Commands

```bash
# Python development
npm run generate:types    # Generate TypeScript types from Python models
npm run format:py         # Format and lint Python code
npm run lint:py           # Run linting and type checking
npm test                  # Run pytest tests

# Application
npm run dev               # Run both frontend and backend
npm run dev:frontend      # Run Next.js only
npm run dev:backend       # Run FastAPI only

# Database
npm run setup:db          # Initialize database
npm run migrate           # Run migrations (to be implemented)
```

**For detailed Python development guide, see [PYTHON_DEVELOPMENT.md](PYTHON_DEVELOPMENT.md)**

### Project Structure

```
PedalBuild/
├── src/
│   ├── backend/          # Python FastAPI + Google ADK agents
│   │   ├── agents/       # Google ADK agents
│   │   └── services/     # Business logic services
│   ├── frontend/         # Next.js application
│   │   └── app/          # App Router pages
│   ├── models/           # TypeScript types (auto-generated)
│   └── db/               # Database schema & migrations
├── data/                 # Local storage
│   ├── db/               # SQLite database
│   ├── uploads/          # PDFs, schematics, photos
│   └── exports/          # Generated layouts & graphics
├── docs/                 # Documentation
└── tests/                # Test suites
```

## Status

**Phase**: 1/6 Complete ✅

**Phase 1 Completed**:
- ✅ Python backend architecture established
- ✅ Pydantic models with auto-generated TypeScript (551 lines)
- ✅ Python tooling setup (uv, pyproject.toml, ruff, mypy, black, pytest)
- ✅ 3 application services (Excel Importer, Component Inventory, BOM Manager)
- ✅ 8 Claude Code development tools (skills + sub-agents)
- ✅ Pre-commit hooks for automated quality checks
- ✅ Type synchronization system (zero drift)
- ✅ Comprehensive documentation

**Next (Phase 2)**:
- Initialize Next.js 15 project
- Create FastAPI backend server
- Setup SQLite database with schema
- Build Google ADK orchestrator
- Implement core workflow agents

**Version**: 0.1.0-alpha

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for development guidelines (to be created).

## License

Private repository for personal use.

## Acknowledgments

- PedalPCB.com for pedal specifications
- Google ADK team for the agentic framework
- DIY pedal building community

---

**Repository**: https://github.com/Diz312/PedalBuild

For questions or support, open an issue on GitHub.
