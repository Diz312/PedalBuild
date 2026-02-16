# PedalBuild Project Guide for Claude Code

> **📖 Universal Standards**: This project follows the universal coding standards defined in `~/.claude/CODING_STANDARDS.md`. For questions about tooling, architecture patterns, or best practices, consult the universal standards first, then this project-specific guide.

## Project Overview

PedalBuild is an intelligent end-to-end application for streamlining guitar pedal building from inspiration through final showcase. It combines Google's ADK framework for agentic workflows with Next.js 15 for the frontend and **Python (FastAPI) backend**, using local-first architecture (SQLite).

**Architecture**: Next.js (TypeScript) frontend + Python (FastAPI) backend with auto-generated TypeScript types

**Status**: Phase 2 Complete (Backend API + Database Foundation) ✅
**Next**: Phase 3 (Frontend Development - Next.js 15 + Shadcn UI)

> **📋 Quick Resume**: See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current status and how to continue

---

## Critical User Requirements ⚠️

These are NON-NEGOTIABLE requirements from the user:

### 1. PedalPCB.com Single Source
- **ONLY** PedalPCB.com for pedal inspiration (not multiple sites)
- Full catalog with ALL historical reviews stored locally
- Offline-first: Browse without internet after initial scrape
- Monthly scraping schedule
- Embedded content viewing (configurable: always/toggle/separate tab)

### 2. Schematic Analysis (CRITICAL)
- **Multi-pass AI vision** (3+ passes for confidence)
- **IMPERATIVE**: Components can be vertical OR horizontal orientation
- Confidence scoring (0-1 scale)
- Flag components with confidence < 0.7 for user review
- Extract: type, value, reference designator (R1, C2, IC1), connections

### 3. Dual-Board Breadboard Platform (CRITICAL)
User has a SPECIFIC custom breadboard platform that MUST be used:
```
2 boards side-by-side
63 columns × 10 rows (a-j) per section
2 sections per board (through-hole gap between)
4 power rails per board (2 positive, 2 negative)
6 potentiometer slots at top
Power jumpers: INPUT, GND, 3.3V, REF, 5V, 9V, -9V, 18V, OUTPUT
2× 1/4" jacks + effect bypass switch
```
Full specification in implementation plan.

### 4. Output Formats
- **Breadboard layouts**: Fritzing (.fzz) + PNG images
- **BOM**: Organized by component type (resistors, capacitors, ICs, etc.)
- **No vendor pricing**: User handles procurement themselves

### 5. Excel Inventory Import
- User has 181 components in custom 14-column CSV format
- Format: Category, SubType, HumanReadableValue, NumericBaseValue, UnitType, Footprint, Voltage, Quantity, etc.
- See `src/backend/services/excel_importer.py` for implementation

---

## Python Tooling Setup ⚙️

**IMPORTANT**: All Python development follows these standards:

### Environment & Dependencies
- **Environment Manager**: `uv` (10-100x faster than pip)
- **Dependencies**: `pyproject.toml` (PEP 621 standard, not requirements.txt)
- **Python Version**: 3.11+ required

### Code Quality Tools
- **Linting**: `ruff` (Rust-based, combines 10+ tools)
- **Type Checking**: `mypy` (industry standard, Pydantic plugin)
- **Formatting**: `black` (100 char lines)
- **Testing**: `pytest`
- **Pre-commit**: Automated hooks for type validation, formatting, linting

### Type Synchronization
- **Single Source of Truth**: Python Pydantic models in `src/models/types.py`
- **Auto-Generated TypeScript**: `scripts/generate-types.py` → `src/models/types.generated.ts`
- **Validation**: `scripts/validate-types.py` (runs in pre-commit hook)
- **Result**: 551 lines of TypeScript auto-generated, zero type drift possible

### Quick Start
```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e '.[dev]'
pre-commit install

# Development
npm run generate:types    # After changing Python models
npm run format:py         # Format code
npm run lint:py           # Lint + type check
npm test                  # Run tests
```

**See**:
- [PYTHON_DEVELOPMENT.md](PYTHON_DEVELOPMENT.md) - Complete Python guide (setup, tooling, decisions)
- [~/.claude/CODING_STANDARDS.md](~/.claude/CODING_STANDARDS.md) - Universal standards (Code Accuracy Protocol)

---

## Architecture Principles

### 1. Local-First
- SQLite for development (single file, easy backup)
- All files stored locally (no S3/cloud initially)
- Offline-first: App works without internet
- PostgreSQL migration path for production

### 2. Simplicity Over Abstraction
- Clear separation: Frontend ↔ API ↔ Agents ↔ Storage
- Minimal external dependencies
- Flat repository pattern (not over-engineered)
- Direct, readable code

### 3. Build Reusable Tools First
- Custom Claude Code skills and agents built BEFORE main app
- Reusable across other electronics projects
- Well-documented for future use

### 4. Deterministic Where Possible
- 5 out of 10 stages use deterministic orchestration
- LLM agents ONLY for tasks requiring reasoning/creativity
- Clear agent hierarchy

### 5. 12-Factor Principles
- Config via environment variables (.env)
- Stateless processes (state in database)
- Backing services abstracted (storage adapter pattern)
- Structured logging to database

---

## Project Structure

```
/PedalBuild/
├── .claude/
│   ├── agents/                    # Custom sub-agents (to be built)
│   │   ├── pedalpcb-scraper.md   # Catalog scraper
│   │   ├── schematic-analyzer.md  # Multi-pass vision AI
│   │   └── breadboard-layout.md   # Layout optimizer
│   └── skills/                    # Custom skills (Python)
│       ├── excel-importer/        # Import inventory from CSV
│       │   ├── SKILL.md          # Documentation
│       │   └── importer.py       # Python implementation (250 lines)
│       ├── component-inventory/   # Manage component stock
│       │   ├── SKILL.md          # Documentation
│       │   └── service.py        # Python implementation (200 lines)
│       └── bom-manager/           # Bill of materials management
│           ├── SKILL.md          # Documentation
│           └── service.py        # Python implementation (220 lines)
├── src/
│   ├── models/
│   │   ├── types.py              # Python Pydantic models (450 lines)
│   │   ├── types.generated.ts    # Auto-generated TypeScript (551 lines)
│   │   └── types.ts              # TypeScript copy (for frontend)
│   ├── db/
│   │   └── schema.sql            # Database schema (25+ tables)
│   ├── backend/                   # Python FastAPI + ADK (to be built)
│   └── frontend/                  # Next.js app (to be built)
├── scripts/
│   ├── generate-types.py         # Python → TypeScript type generator
│   └── validate-types.py         # Type sync validator
├── data/
│   ├── db/                        # SQLite database
│   ├── uploads/                   # PDFs, schematics, photos
│   └── exports/                   # Layouts, graphics
├── docs/                          # Documentation
├── pyproject.toml                 # Python dependencies & tool config
├── .pre-commit-config.yaml        # Pre-commit hooks
├── PYTHON_SETUP.md                # Python development guide
├── TOOLING_DECISIONS.md           # Tooling decisions log
└── README.md                      # Project overview
```

---

## Key File Locations

### Database & Types
- **Schema**: `src/db/schema.sql` (25+ tables)
- **Python Types**: `src/models/types.py` (Pydantic models, 450 lines)
- **TypeScript Types**: `src/models/types.generated.ts` (auto-generated, 551 lines)
- **Database**: `data/db/pedalbuild.db` (runtime)

### Application Services (Python)
- **Excel Importer**: `src/backend/services/excel_importer.py` (250 lines)
- **Component Inventory**: `src/backend/services/component_inventory.py` (200 lines)
- **BOM Manager**: `src/backend/services/bom_manager.py` (220 lines)
- **PedalPCB Scraper**: `src/backend/agents/pedalpcb_scraper.py` (to be built - Phase 3)
- **Schematic Analyzer**: `src/backend/agents/schematic_analyzer.py` (to be built - Phase 3)
- **Breadboard Layout**: `src/backend/agents/breadboard_layout.py` (to be built - Phase 3)

### Claude Code Development Tools
- **Universal Skills**: `~/.claude/skills/` (test-runner, format-and-lint, db-inspector, type-sync-validator)
- **Universal Sub-Agents**: `~/.claude/agents/` (framework-verifier, schema-designer, test-writer, api-integrator)
- **See**: [CLAUDE_CODE_TOOLS.md](CLAUDE_CODE_TOOLS.md) for complete documentation

### Python Tooling
- **Dependencies**: `pyproject.toml` (PEP 621 standard)
- **Type Generator**: `scripts/generate-types.py`
- **Type Validator**: `scripts/validate-types.py`
- **Pre-commit Config**: `.pre-commit-config.yaml`

### Documentation
- **Universal Standards**: `~/.claude/CODING_STANDARDS.md` (all projects)
- **Python Setup**: `PYTHON_SETUP.md` (developer guide)
- **Tooling Decisions**: `TOOLING_DECISIONS.md` (all decisions logged)
- **Setup**: `README.md` (getting started)
- **Plan**: `.claude/plans/sunny-stargazing-garden.md` (implementation plan)

---

## Database Schema Patterns

### Key Tables
```sql
-- PedalPCB Integration
pedalpcb_catalog         -- Full pedal catalog
pedalpcb_reviews         -- ALL historical reviews
scraping_jobs           -- Scraping job tracking

-- Component Management
components              -- Component library with inventory
circuit_bom            -- BOM items with confidence scores

-- Project Workflow
projects               -- User build projects
project_stages        -- Workflow stage tracking (10 stages)
breadboard_layouts    -- Layout designs

-- State Management
agent_state           -- ADK session/user/global state
workflow_logs         -- Execution logs
```

### Important Fields
- `confidence_score` in `circuit_bom` - From schematic analysis (0-1)
- `voltage` in `components` - Added for user's inventory format
- `is_critical` in `circuit_bom` - Component affects tone significantly
- `images_json`, `specifications_json` in `pedalpcb_catalog` - JSON columns

---

## Type System

**Single Source of Truth**: Python Pydantic models in `src/models/types.py`

**Auto-Generated TypeScript**: `scripts/generate-types.py` → `src/models/types.generated.ts`

### Python Pydantic Models (Source)
```python
class ComponentType(str, Enum):
    RESISTOR = "resistor"
    CAPACITOR = "capacitor"
    IC = "ic"
    # ... 11 types total

class Component(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: ComponentType
    quantity_in_stock: int = Field(default=0, ge=0)  # Validation
    voltage: Optional[str] = None
    # ... 14 fields total
```

### TypeScript Types (Auto-Generated)
```typescript
export type ComponentType = "resistor" | "capacitor" | "ic" | ...;
export type PedalCategory = "fuzz" | "distortion" | "overdrive" | ...;
export type WorkflowStage = "inspiration" | "spec_download" | ...;

export interface Component {
  id: string;
  type: ComponentType;
  quantity_in_stock: number;
  voltage: string | null;
  // ...
}
```

### Discriminated Unions (Both Languages)
```python
# Python
class SchematicAnalysisData(BaseModel):
    type: Literal["schematic_analysis"] = "schematic_analysis"
    schematic_path: str
    components: List[SchematicComponent]
```

```typescript
// Auto-generated TypeScript
export interface SchematicAnalysisData {
  type: "schematic_analysis";
  schematic_path: string;
  components: SchematicComponent[];
}
```

### Key Models
- `Component` - Inventory item with stock tracking
- `CircuitBOMItem` - BOM with confidence & substitution info
- `Project` & `ProjectStage` - Workflow management
- `BreadboardLayoutData` - Dual-board platform layout
- `PedalPCBCatalogItem` - Pedal metadata with reviews

---

## Workflow Stages

1. **Inspiration** - Browse PedalPCB.com by type
2. **Spec Download** - Download build documentation PDF
3. **Schematic Analysis** - Multi-pass AI vision (NEW & CRITICAL)
4. **Inventory Check** - Match against local inventory
5. **BOM Generation** - Organize by component type
6. **Breadboard Layout** - AI-optimized dual-board layout
7. **Prototype Testing** - Guided testing and validation
8. **Final Assembly** - Enclosure assembly
9. **Graphics Design** - AI-assisted graphics
10. **Showcase** - Share with community

---

## REST API Endpoints (Phase 2 Complete) ✅

**Base URL**: http://localhost:8000 (when running `npm run dev:backend`)
**API Docs**: http://localhost:8000/docs (interactive Swagger UI)

### Component Inventory API (`/api/inventory`)
- `GET /` - List all components (with optional type filter)
- `GET /search?q=` - Search by value/name/part number
- `GET /{component_id}` - Get component by ID
- `GET /low-stock` - Get low stock components
- `GET /stats` - Inventory statistics
- `PATCH /{component_id}/quantity` - Update quantity (delta)

### BOM Management API (`/api/bom`)
- `GET /{circuit_id}` - Get complete BOM
- `GET /{circuit_id}/by-type` - BOM organized by type
- `POST /{circuit_id}/items` - Add BOM item
- `GET /{circuit_id}/validate` - Validate against inventory
- `GET /{circuit_id}/shopping-list` - Missing components
- `GET /{circuit_id}/stats` - BOM statistics
- `GET /{circuit_id}/export` - Export to CSV

### CSV Import API (`/api/import`)
- `POST /inventory?preview=true` - Import CSV (preview mode)
- `GET /template` - Download CSV template
- `GET /format` - CSV format documentation

**Full API Reference**: See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

---

## Custom Tools Usage (Python)

### Component Inventory
```bash
# CLI usage (Python)
python src/backend/services/component_inventory.py list
python src/backend/services/component_inventory.py search "10k"
python src/backend/services/component_inventory.py low-stock
python src/backend/services/component_inventory.py stats
```

```python
# Python code usage
from component_inventory.service import ComponentInventoryService

service = ComponentInventoryService("data/db/pedalbuild.db")
components = service.search_components("10k")
stats = service.get_statistics()
low_stock = service.get_low_stock()
```

### BOM Manager
```bash
# CLI usage (Python)
python src/backend/services/bom_manager.py show <circuit-id>
python src/backend/services/bom_manager.py validate <circuit-id>
python src/backend/services/bom_manager.py shopping-list <circuit-id>
python src/backend/services/bom_manager.py stats <circuit-id>
python src/backend/services/bom_manager.py export <circuit-id>  # CSV output
```

```python
# Python code usage
from bom_manager.service import BOMManagerService

service = BOMManagerService("data/db/pedalbuild.db")
validation = service.validate_bom("triangulum-overdrive")
shopping = service.get_shopping_list("triangulum-overdrive")
```

### Excel Importer
```bash
# CLI usage (Python)
python src/backend/services/excel_importer.py myInventory.csv --preview
python src/backend/services/excel_importer.py myInventory.csv --db data/db/pedalbuild.db
```

```python
# Python code usage
from excel_importer.importer import InventoryImporter

with InventoryImporter("data/db/pedalbuild.db") as importer:
    result = importer.import_components("myInventory.csv")
    print(f"Imported: {result['inserted']} components")
```

---

## Important Patterns

### Component Matching Intelligence
The inventory system has domain knowledge:
- **IC Substitutions**: JRC4558 ↔ TL072 (with tone impact notes)
- **Resistor Tolerance**: 1% matches 5% requirement (better)
- **Value Normalization**: 100n = 100nF = 0.1uF
- **IC Families**: TL07x series recognition

### Multi-Pass Schematic Analysis
1. **Pass 1**: Symbol identification (30-40% confidence)
2. **Pass 2**: Value extraction (60-75% confidence)
3. **Pass 3**: Connection mapping (80-95% confidence)
4. **Pass 4**: Low-confidence flagging (<0.7)

### Breadboard Layout Optimization
1. **Phase 1**: Component grouping by function
2. **Phase 2**: Placement (left-to-right signal flow)
3. **Phase 3**: Wire routing (minimize crossings)
4. **Phase 4**: Fritzing export (.fzz)
5. **Phase 5**: PNG export (300 DPI)

---

## Data Flow Example

### Building a Pedal (Complete Flow)
```
1. User selects "Overdrive" category
   → Query: SELECT * FROM pedalpcb_catalog WHERE category='overdrive'

2. User selects "Triangulum" pedal
   → Download build doc PDF to data/uploads/specs/

3. Schematic Vision Analyzer (Multi-pass AI)
   → Extract components with confidence scores
   → Output: JSON with 24 components
   → Flag 2 low-confidence items for user review

4. BOM Manager
   → Create BOM from schematic analysis
   → Store in circuit_bom table

5. Inventory Check
   → Match against components table
   → Result: 18/24 available, 6 missing
   → Suggest TL072 substitute for JRC4558

6. BOM Generation
   → Organize by type: 8 resistors, 7 caps, 2 ICs, 3 transistors, 4 diodes
   → Generate shopping list for missing items

7. Breadboard Layout Agent
   → Optimize for dual-board platform
   → Place ICs, route wires, assign pots to top 6 slots
   → Output: .fzz + .png + .json + assembly.md

8. User assembles on breadboard following layout

9. Test, assemble in enclosure, design graphics, showcase
```

---

## Technology Stack

### Current (Phase 1 Complete)
- **Backend Language**: Python 3.11+ (FastAPI)
- **Frontend Language**: TypeScript (Next.js 15)
- **Type System**: Pydantic (Python) → Auto-generated TypeScript
- **Database**: SQLite with comprehensive schema
- **Skills**: 3 custom Python skills (Excel, Inventory, BOM)
- **Tooling**: uv, pyproject.toml, ruff, mypy, black, pytest, pre-commit

### Python Backend Stack
- **Framework**: FastAPI (API server)
- **Type Validation**: Pydantic v2
- **Database**: sqlite3 (Python standard library)
- **Data Processing**: pandas (CSV parsing)
- **Vision**: OpenCV + Pillow (schematic analysis)
- **Web Scraping**: BeautifulSoup4
- **Testing**: pytest
- **AI**: Google ADK (Python)

### TypeScript Frontend Stack (To Build - Phase 2)
- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 18
- **Components**: Shadcn UI
- **Styling**: Tailwind CSS
- **Type Safety**: Auto-generated from Python

### Agents (To Build - Phase 2)
- **3 CRITICAL agents**: PedalPCB Scraper, Schematic Analyzer, Breadboard Layout
- **Framework**: Google ADK (Python)
- **AI Models**: Claude (Anthropic), Gemini (Google)
- **Tools**: Fritzing (layouts), SQLite (storage)

---

## Development Guidelines

### When Working on Python Backend
- **Always activate venv first**: `source .venv/bin/activate`
- **Type hints required**: All functions must have type annotations
- **Pydantic models**: Single source of truth for types
- **After changing types**: Run `npm run generate:types`
- **Code style**: Use `black` (auto-format) and `ruff` (lint)
- **Testing**: Write pytest tests for all business logic
- **ADK agents**: Follow hierarchy (Root → Sequential → Parallel → LLM)
- **Tools**: Clear name, description, inputSchema, execute()

### When Working on Frontend
- Use Next.js 15 App Router (not Pages Router)
- Server Components by default, Client Components when needed
- Shadcn UI for components
- Type-safe with auto-generated TypeScript types
- **Never manually edit types.generated.ts**

### When Working with Database
- Always use parameterized queries (SQL injection prevention)
- JSON columns for flexible nested data
- Timestamps auto-update via triggers
- Foreign keys with CASCADE for data integrity
- **Python**: Use sqlite3 with context managers

### When Writing Agents (Python)
- LLM agents for reasoning/creativity only
- Deterministic agents (Sequential, Parallel) for workflow
- Clear tool descriptions for agent understanding
- Context files provide domain knowledge
- State management: session (temp), user (persistent), global (shared)
- AG-UI protocol for streaming updates to frontend

### Type Synchronization
- **Python models are source of truth**
- **Auto-generate TypeScript**: `npm run generate:types`
- **Validate sync**: `npm run validate:types`
- **Pre-commit hook**: Validates types automatically
- **Never manually edit**: `types.generated.ts` or `types.ts`

---

## Git Workflow

### What to Commit
- Source code (src/)
- Configuration files (.env.example, tsconfig.json)
- Documentation (docs/, README.md, CLAUDE.md)
- Database schema (src/db/schema.sql)
- Custom tools (.claude/)

### What NOT to Commit
- Database files (data/db/*.db)
- Environment secrets (.env.local)
- Uploads (data/uploads/)
- Generated files (data/exports/)
- Node modules (node_modules/)

---

## Testing Strategy

### Unit Tests
- Component matching algorithms
- BOM validation logic
- State transformations

### Integration Tests
- ADK agent → Repository → SQLite
- Frontend → API → ADK workflow
- File upload → Storage → Database

### End-to-End Test
Complete workflow with real PedalPCB pedal:
1. Import inventory from user's CSV
2. Scrape Triangulum Overdrive from PedalPCB
3. Analyze schematic (multi-pass vision)
4. Validate BOM against inventory
5. Generate breadboard layout
6. Verify .fzz and .png outputs

---

## Common Commands

```bash
# Initial Setup
uv venv                       # Create virtual environment
source .venv/bin/activate     # Activate venv
uv pip install -e '.[dev]'    # Install all dependencies
pre-commit install            # Setup pre-commit hooks

# Development
npm run dev                    # Start frontend + backend
npm run dev:backend           # Python FastAPI backend (uvicorn)
npm run dev:frontend          # Next.js frontend

# Python Development
npm run generate:types        # Generate TypeScript from Python models
npm run validate:types        # Validate type sync
npm run format:py             # Format Python code (black)
npm run lint:py               # Lint + type check (ruff + mypy)
npm test                      # Run pytest tests
npm run test:coverage         # Pytest with coverage

# Database
npm run setup:db              # Initialize SQLite database

# Python Skills CLI
python src/backend/services/excel_importer.py myInventory.csv --preview
python src/backend/services/component_inventory.py list
python src/backend/services/component_inventory.py search "10k"
python src/backend/services/component_inventory.py stats
python src/backend/services/component_inventory.py low-stock
python src/backend/services/bom_manager.py show <circuit-id>
python src/backend/services/bom_manager.py validate <circuit-id>
```

---

## User Preferences

- **Permission**: Full autonomy to write files, run commands (no asking)
- **Communication**: Concise, no emojis unless requested
- **Commits**: Only when explicitly asked
- **Approach**: Build autonomously per implementation plan
- **Priority**: Functionality over polish, MVP first

---

## Phase 2 Complete ✅

**Backend API Foundation - Completed 2026-02-16**:
1. ✅ SQLite database initialized (19 tables, 3 views, 5 triggers)
2. ✅ FastAPI backend server with CORS, logging, error handling
3. ✅ Database connection utilities (pooling, transactions)
4. ✅ 16 REST API endpoints (inventory, BOM, CSV import)
5. ✅ 24 integration tests (all passing)
6. ✅ Complete API documentation

**Backend Ready**: http://localhost:8000 (start with `npm run dev:backend`)
**API Docs**: http://localhost:8000/docs (Swagger UI)

---

## Next Steps (Phase 3 - Frontend)

1. Initialize Next.js 15 project with App Router
2. Setup Shadcn UI component library
3. Create layout and navigation
4. Build inventory management UI (list, search, edit)
5. Build BOM management UI (validate, shopping list)
6. Build CSV import UI (upload, preview)
7. Integrate with FastAPI backend
8. Test complete user workflow

**After Phase 3**: Google ADK agents (Phase 4) - PedalPCB scraper, schematic analyzer, layout optimizer

---

## Useful References

### Implementation & Planning
- **Implementation Plan**: `.claude/plans/sunny-stargazing-garden.md`
- **Universal Standards**: `~/.claude/CODING_STANDARDS.md` (Code Accuracy Protocol, all standards)

### Type System & Database
- **Python Types**: `src/models/types.py` (Pydantic models, source of truth)
- **TypeScript Types**: `src/models/types.generated.ts` (auto-generated)
- **Database Schema**: `src/db/schema.sql`
- **User's Inventory**: `data/imports/myInventory.csv` (181 components)

### Python Development
- **Development Guide**: `PYTHON_DEVELOPMENT.md` (setup, tooling, decisions, workflow)
- **Code Accuracy**: Follow `~/.claude/CODING_STANDARDS.md` - use WebSearch/WebFetch to verify current patterns before coding

### Configuration
- **Python Dependencies**: `pyproject.toml` (PEP 621 standard)
- **Pre-commit Hooks**: `.pre-commit-config.yaml`
- **Package Scripts**: `package.json`

---

**Last Updated**: 2026-02-16 (Phase 2 Complete - Backend API + Database Foundation)
**Phase**: 2/6 Complete ✅
**Architecture**: Next.js (TypeScript) + Python (FastAPI) with auto-generated types
**Backend**: 16 REST API endpoints, 24 tests passing, SQLite initialized
**Ready For**: Phase 3 - Frontend Development (Next.js 15 + Shadcn UI)

> **📋 See [PROJECT_STATUS.md](PROJECT_STATUS.md) for detailed status and resume guide**
