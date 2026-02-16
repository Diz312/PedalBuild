# PedalBuild API Documentation

## Overview

PedalBuild backend REST API built with FastAPI. Provides endpoints for component inventory management, BOM validation, and CSV import.

**Base URL**: `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

---

## Quick Start

### 1. Setup Database
```bash
python3 scripts/setup-db.py
```

### 2. Install Dependencies
```bash
source .venv/bin/activate
uv pip install -e '.[dev]'
```

### 3. Start Server
```bash
# Development mode (auto-reload)
npm run dev:backend

# Or directly with uvicorn
uvicorn src.backend.main:app --reload --port 8000
```

### 4. Access API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## API Endpoints

### Health & Info

#### `GET /`
Root endpoint with API information.

**Response:**
```json
{
  "message": "PedalBuild API",
  "version": "0.1.0",
  "docs": "/docs",
  "health": "/health"
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": 1708095600.123
}
```

---

## Component Inventory API

Base path: `/api/inventory`

### List Components

#### `GET /api/inventory/`
List all components with optional type filter.

**Query Parameters:**
- `type` (optional): Filter by component type (resistor, capacitor, ic, etc.)

**Response:**
```json
{
  "components": [
    {
      "id": "resistor_10k_through_hole",
      "type": "resistor",
      "name": "Metal Film 10k",
      "value": "10k",
      "tolerance": "1%",
      "package": "through-hole",
      "quantity_in_stock": 50,
      "minimum_quantity": 10,
      "location": "Drawer A",
      "created_at": "2026-02-16T10:00:00",
      "updated_at": "2026-02-16T10:00:00"
    }
  ],
  "total": 1
}
```

**Example:**
```bash
curl http://localhost:8000/api/inventory/
curl http://localhost:8000/api/inventory/?type=resistor
```

### Search Components

#### `GET /api/inventory/search`
Search components by value, name, or part number.

**Query Parameters:**
- `q` (required): Search query string

**Response:**
```json
{
  "components": [...],
  "total": 5
}
```

**Example:**
```bash
curl "http://localhost:8000/api/inventory/search?q=10k"
```

### Get Component by ID

#### `GET /api/inventory/{component_id}`
Get detailed component information.

**Response:** Single component object

**Example:**
```bash
curl http://localhost:8000/api/inventory/resistor_10k_through_hole
```

### Low Stock Components

#### `GET /api/inventory/low-stock`
Get components where `quantity_in_stock <= minimum_quantity`.

**Response:**
```json
{
  "components": [...],
  "total": 3
}
```

### Inventory Statistics

#### `GET /api/inventory/stats`
Get inventory statistics grouped by type.

**Response:**
```json
{
  "total_types": 42,
  "total_units": 1250,
  "low_stock_count": 3,
  "out_of_stock_count": 1,
  "by_type": {
    "resistor": {
      "types": 15,
      "units": 450
    },
    "capacitor": {
      "types": 12,
      "units": 320
    }
  }
}
```

### Update Component Quantity

#### `PATCH /api/inventory/{component_id}/quantity`
Update component stock quantity (add or subtract).

**Request Body:**
```json
{
  "delta": 10  // Positive to add, negative to subtract
}
```

**Response:**
```json
{
  "success": true,
  "component_id": "resistor_10k_through_hole",
  "new_quantity": 60
}
```

**Example:**
```bash
# Add 10 units
curl -X PATCH http://localhost:8000/api/inventory/resistor_10k_through_hole/quantity \
  -H "Content-Type: application/json" \
  -d '{"delta": 10}'

# Subtract 5 units
curl -X PATCH http://localhost:8000/api/inventory/resistor_10k_through_hole/quantity \
  -H "Content-Type: application/json" \
  -d '{"delta": -5}'
```

---

## BOM Management API

Base path: `/api/bom`

### Get BOM

#### `GET /api/bom/{circuit_id}`
Get complete BOM for a circuit.

**Response:**
```json
{
  "circuit_id": "triangulum_overdrive",
  "items": [
    {
      "id": "triangulum_overdrive_resistor_10k_1",
      "circuit_id": "triangulum_overdrive",
      "component_type": "resistor",
      "component_value": "10k",
      "quantity": 2,
      "reference_designator": "R1,R2",
      "is_critical": true,
      "confidence_score": 0.95
    }
  ],
  "total": 24
}
```

### Get BOM by Type

#### `GET /api/bom/{circuit_id}/by-type`
Get BOM organized by component type.

**Response:**
```json
{
  "circuit_id": "triangulum_overdrive",
  "by_type": {
    "resistor": [...],
    "capacitor": [...],
    "ic": [...]
  },
  "total": 24
}
```

### Add BOM Item

#### `POST /api/bom/{circuit_id}/items`
Add a new item to the BOM.

**Request Body:**
```json
{
  "component_type": "ic",
  "component_value": "TL072",
  "quantity": 1,
  "reference_designator": "IC1",
  "is_critical": true,
  "confidence_score": 0.92
}
```

### Validate BOM

#### `GET /api/bom/{circuit_id}/validate`
Validate BOM against inventory to check component availability.

**Response:**
```json
{
  "total_items": 24,
  "available_count": 20,
  "missing_count": 4,
  "completeness": 0.833,
  "matches": [...],
  "missing": [...]
}
```

### Shopping List

#### `GET /api/bom/{circuit_id}/shopping-list`
Get list of missing components that need to be purchased.

**Response:**
```json
{
  "missing_items": [
    {
      "type": "capacitor",
      "value": "47uF",
      "quantity": 2,
      "references": ["C5", "C6"]
    }
  ],
  "total_missing": 4
}
```

### BOM Statistics

#### `GET /api/bom/{circuit_id}/stats`
Get BOM statistics.

**Response:**
```json
{
  "total_items": 24,
  "by_type": {
    "resistor": 8,
    "capacitor": 7,
    "ic": 2,
    "diode": 4,
    "transistor": 3
  },
  "critical_count": 5,
  "low_confidence_count": 2
}
```

### Export BOM to CSV

#### `GET /api/bom/{circuit_id}/export`
Export BOM as CSV file.

**Response:** CSV file download

**Example:**
```bash
curl http://localhost:8000/api/bom/triangulum_overdrive/export > bom.csv
```

---

## Import API

Base path: `/api/import`

### Import Inventory from CSV

#### `POST /api/import/inventory`
Import component inventory from CSV file.

**Query Parameters:**
- `preview` (optional): Set to `true` for preview mode (doesn't write to database)

**Request:** Multipart form-data with CSV file

**Response:**
```json
{
  "success": true,
  "total_components": 181,
  "inserted": 181,
  "skipped": 0,
  "by_type": {
    "resistor": 45,
    "capacitor": 38,
    "ic": 25
  },
  "message": "Successfully imported 181 components"
}
```

**Example:**
```bash
# Preview mode (no database changes)
curl -X POST http://localhost:8000/api/import/inventory?preview=true \
  -F "file=@myInventory.csv"

# Import to database
curl -X POST http://localhost:8000/api/import/inventory \
  -F "file=@myInventory.csv"
```

### Download CSV Template

#### `GET /api/import/template`
Download CSV template with example data.

**Response:** CSV file download

**Example:**
```bash
curl http://localhost:8000/api/import/template > inventory_template.csv
```

### Get CSV Format Info

#### `GET /api/import/format`
Get detailed CSV format documentation.

**Response:**
```json
{
  "format": "CSV",
  "encoding": "UTF-8",
  "required_columns": ["Category", "HumanReadableValue", "Quantity"],
  "optional_columns": [...],
  "category_values": ["RESISTOR", "CAPACITOR", "IC", ...],
  "example_row": {...},
  "notes": [...]
}
```

---

## CSV Import Format

### Required Columns
1. **Category**: Component type (RESISTOR, CAPACITOR, IC, TRANSISTOR, DIODE, etc.)
2. **HumanReadableValue**: Component value (e.g., "10k", "100nF", "TL072")
3. **Quantity**: Quantity in stock (integer)

### Optional Columns
- **SubType**: Component subtype (e.g., "Metal Film", "Electrolytic")
- **NumericBaseValue**: Numeric value for sorting
- **UnitType**: Unit (ohm, F, etc.)
- **Footprint**: Package type (through-hole, DIP8, etc.)
- **Voltage**: Voltage rating (e.g., "16V", "50V")
- **ReorderLevel**: Minimum quantity threshold
- **MfrPartNumber**: Manufacturer part number
- **KeyNotes**: Notes
- **RelatedPart**: Related part information
- **Vendor**: Vendor name
- **VendorSKU**: Vendor SKU

### Example CSV
```csv
Category,SubType,HumanReadableValue,Quantity,ReorderLevel,Footprint,Voltage
RESISTOR,Metal Film,10k,50,10,through-hole,
CAPACITOR,Electrolytic,100uF,20,5,radial,25V
IC,Op-Amp,TL072,10,3,DIP8,
```

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": 1708095600.123
}
```

**HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found
- `500`: Internal Server Error

---

## Testing

### Run Tests
```bash
source .venv/bin/activate
pytest tests/test_api.py -v
```

### Test Coverage
```bash
pytest --cov=src tests/
```

### Manual API Testing

**Using curl:**
```bash
# Health check
curl http://localhost:8000/health

# List inventory
curl http://localhost:8000/api/inventory/

# Search components
curl "http://localhost:8000/api/inventory/search?q=10k"

# Get statistics
curl http://localhost:8000/api/inventory/stats
```

**Using HTTPie:**
```bash
# Health check
http :8000/health

# List inventory
http :8000/api/inventory/

# Update quantity
http PATCH :8000/api/inventory/resistor_10k_through_hole/quantity delta:=10
```

---

## Development

### Database Setup
```bash
# Initial setup
python3 scripts/setup-db.py

# Reset database (WARNING: deletes all data)
python3 scripts/setup-db.py --force

# Check database
python3 scripts/setup-db.py --check
```

### Run Development Server
```bash
# With auto-reload
npm run dev:backend

# Or with uvicorn directly
uvicorn src.backend.main:app --reload --port 8000 --log-level debug
```

### View Logs
Server logs are written to stdout with timestamps and request details:
```
2026-02-16 10:00:00 - INFO - GET /api/inventory/ - 200 - 15.23ms
```

---

## Architecture

### Components
- **FastAPI App** (`src/backend/main.py`): Main application
- **Database Layer** (`src/backend/db.py`): Connection management
- **Routes** (`src/backend/routes/`): API endpoint handlers
- **Services** (`src/backend/services/`): Business logic
- **Database** (`data/db/pedalbuild.db`): SQLite database

### Request Flow
```
Client Request
  ↓
FastAPI App
  ↓
Route Handler (validates request)
  ↓
Service Layer (business logic)
  ↓
Database (SQLite)
  ↓
Response (JSON)
```

---

## Type Safety

All API requests and responses use Pydantic models for validation.

Auto-generated TypeScript types are available at:
```
GET /api/types
```

---

## Next Steps

- [ ] Add authentication/authorization
- [ ] Implement circuit management endpoints
- [ ] Add project workflow endpoints
- [ ] Build PedalPCB scraper integration
- [ ] Add schematic analysis endpoints
- [ ] Implement breadboard layout endpoints

---

**Last Updated**: 2026-02-16
**API Version**: 0.1.0
