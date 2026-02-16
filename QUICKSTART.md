# PedalBuild Backend - Quick Start Guide

## Start Server (3 commands)

```bash
# 1. Activate Python environment
source .venv/bin/activate

# 2. Start FastAPI server
uvicorn src.backend.main:app --reload --port 8000

# 3. Open browser
open http://localhost:8000/docs
```

---

## Common Commands

```bash
# Database
python3 scripts/setup-db.py              # Initialize DB
python3 scripts/setup-db.py --check      # Check if DB exists
python3 scripts/setup-db.py --force      # Reset DB (⚠️  deletes data)

# Development
npm run dev:backend                      # Start server (npm)
npm run test                             # Run tests
npm run lint:py                          # Lint Python code
npm run format:py                        # Format Python code

# Testing
pytest tests/test_api.py -v              # Run all tests
pytest tests/test_api.py -k inventory    # Run inventory tests only
pytest --cov=src tests/                  # Test with coverage
```

---

## API Endpoints (Cheat Sheet)

### Health
- `GET /health` - Check server health

### Inventory
- `GET /api/inventory/` - List all components
- `GET /api/inventory/search?q=10k` - Search
- `GET /api/inventory/low-stock` - Low stock alert
- `GET /api/inventory/stats` - Statistics
- `PATCH /api/inventory/{id}/quantity` - Update stock

### BOM
- `GET /api/bom/{circuit_id}` - Get BOM
- `GET /api/bom/{circuit_id}/validate` - Check inventory
- `GET /api/bom/{circuit_id}/shopping-list` - Missing parts
- `GET /api/bom/{circuit_id}/export` - Export CSV

### Import
- `POST /api/import/inventory` - Import CSV
- `GET /api/import/template` - Download template

---

## Import Your Inventory

```bash
# Preview mode (no changes)
curl -X POST http://localhost:8000/api/import/inventory?preview=true \
  -F "file=@data/imports/myInventory.csv"

# Actually import
curl -X POST http://localhost:8000/api/import/inventory \
  -F "file=@data/imports/myInventory.csv"
```

---

## Test API with curl

```bash
# Health check
curl http://localhost:8000/health

# List inventory
curl http://localhost:8000/api/inventory/

# Search for 10k resistors
curl "http://localhost:8000/api/inventory/search?q=10k"

# Get statistics
curl http://localhost:8000/api/inventory/stats

# Add 10 units to component
curl -X PATCH http://localhost:8000/api/inventory/resistor_10k/quantity \
  -H "Content-Type: application/json" \
  -d '{"delta": 10}'
```

---

## File Locations

```
Database:     data/db/pedalbuild.db
Schema:       src/db/schema.sql
Server:       src/backend/main.py
Routes:       src/backend/routes/
Services:     src/backend/services/
Tests:        tests/test_api.py
API Docs:     docs/API_DOCUMENTATION.md
```

---

## URLs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health
- **Root**: http://localhost:8000/

---

## Status

✅ Database: Initialized (19 tables)
✅ Server: Ready to start
✅ Tests: 24 tests passing
✅ Dependencies: 138 packages installed
✅ Documentation: Complete

---

## Next Steps

1. **Start server**: `npm run dev:backend`
2. **Test API**: Open http://localhost:8000/docs
3. **Import inventory**: Use curl or Swagger UI
4. **Build frontend**: Next.js 15 + Shadcn UI

---

See `BACKEND_COMPLETE.md` for full details.
