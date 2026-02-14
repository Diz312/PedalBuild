---
name: component-inventory
description: Manage electronic component inventory with Python. CRUD operations, low-stock alerts, and search capabilities. Essential for tracking on-hand parts during pedal builds.
argument-hint: [command] [options]
---

# Component Inventory Management (Python)

Track and manage your electronic component inventory with comprehensive CRUD operations, intelligent search, and low-stock monitoring.

## Commands

### List Components
```bash
# List all components
python .claude/skills/component-inventory/service.py list

# Filter by type (in Python code)
from component_inventory.service import ComponentInventoryService
service = ComponentInventoryService("data/db/pedalbuild.db")
resistors = service.list_components(comp_type="resistor")
```

### Search
```bash
# Search by value or name
python .claude/skills/component-inventory/service.py search "10k"
python .claude/skills/component-inventory/service.py search "TL072"
```

### Low Stock
```bash
# Show components at or below minimum quantity
python .claude/skills/component-inventory/service.py low-stock
```

### Statistics
```bash
# Show inventory summary
python .claude/skills/component-inventory/service.py stats
```

## Python Usage

### Basic Operations
```python
from component_inventory.service import ComponentInventoryService

# Initialize service
service = ComponentInventoryService("data/db/pedalbuild.db")

# List all components
all_components = service.list_components()

# Filter by type
resistors = service.list_components(comp_type="resistor")

# Search
results = service.search_components("10k")

# Get specific component
component = service.get_component("resistor_10k_axial")

# Check low stock
low_stock = service.get_low_stock()

# Get statistics
stats = service.get_statistics()
print(f"Total: {stats['total_types']} types, {stats['total_units']} units")

# Update quantity
service.update_quantity("resistor_10k_axial", delta=-5)  # Use 5
service.update_quantity("resistor_10k_axial", delta=10)  # Add 10
```

## Features

### 1. Component Types
Supports all standard electronic components:
- **Resistors**: Carbon film, metal film, wire-wound
- **Capacitors**: Ceramic, electrolytic, film, tantalum
- **ICs**: Op-amps, regulators, logic, microcontrollers
- **Transistors**: BJT (NPN/PNP), JFET, MOSFET
- **Diodes**: Silicon, germanium, Schottky, Zener, LED
- **Potentiometers**: Linear, logarithmic, reverse log
- **Switches**: DPDT, 3PDT, footswitches
- **Jacks**: 1/4" mono/stereo, DC power
- **Hardware**: Enclosures, knobs, wire, solder

### 2. Intelligent Search
```python
# Find by exact value
results = service.search_components("10k")
# Results: 10k resistors, 10k pots, etc.

# Find by partial match
results = service.search_components("TL07")
# Results: TL071, TL072, TL074

# Results sorted by relevance:
# 1. Exact matches (value = "10k")
# 2. Starts with query (value LIKE "10k%")
# 3. Name matches (name LIKE "10k%")
# 4. Contains query (value LIKE "%10k%")
```

### 3. Low Stock Alerts
```python
low_stock = service.get_low_stock()

# Returns components where:
# quantity_in_stock <= minimum_quantity

for component in low_stock:
    if component['quantity_in_stock'] == 0:
        print(f"❌ OUT OF STOCK: {component['name']}")
    else:
        print(f"⚠️  LOW: {component['name']} ({component['quantity_in_stock']}/{component['minimum_quantity']})")
```

Output:
```
⚠️  Low Stock Components (5)
================================
Resistors:
  - 4.7k Metal Film (2/10 in stock)

Capacitors:
  - 100nF Ceramic (5/15 in stock)
  - 1µF Electrolytic (1/5 in stock)

ICs:
  - JRC4558D (0/2 in stock) - OUT OF STOCK
  - TL072CP (1/3 in stock)
```

### 4. Statistics & Reports
```python
stats = service.get_statistics()

# Returns:
# {
#     'total_types': 181,
#     'total_units': 2464,
#     'by_type': {
#         'resistor': {'types': 52, 'units': 1234},
#         'capacitor': {'types': 41, 'units': 612},
#         ...
#     },
#     'low_stock_count': 5,
#     'out_of_stock_count': 1
# }
```

## Data Model

### Component Schema (from Pydantic)
```python
from models.types import Component, ComponentType

class Component(BaseModel):
    id: str                    # Unique identifier
    type: ComponentType        # resistor, capacitor, ic, etc.
    name: str                  # Display name
    value: Optional[str]       # Component value (10k, 100nF, TL072)
    tolerance: Optional[str]   # ±1%, ±5%, etc.
    package: Optional[str]     # Footprint (DIP-8, Axial 1/4W)
    manufacturer: Optional[str]
    part_number: Optional[str]
    datasheet_url: Optional[str]
    quantity_in_stock: int     # Current quantity
    minimum_quantity: int      # Reorder threshold
    unit_price: Optional[float]
    location: Optional[str]    # Storage location
    voltage: Optional[str]     # Voltage rating
    notes: Optional[str]       # Additional information
    created_at: datetime
    updated_at: datetime
```

## Integration with Workflow

### Stage 4: Inventory Check
During the Inventory Check workflow stage, this skill is used to:
1. Match each BOM item against inventory
2. Identify exact matches
3. Suggest substitutions for missing components
4. Calculate completeness percentage
5. Generate shopping list for missing items

### Stage 6: Breadboard Layout
Before generating layout, verify all components are available:
```python
from bom_manager.service import BOMManagerService

bom_service = BOMManagerService("data/db/pedalbuild.db")
validation = bom_service.validate_bom(circuit_id)

if validation['completeness'] < 1.0:
    print(f"⚠️  Missing {validation['missing_count']} components")
```

### Stage 8: Final Assembly
Track component usage during assembly:
```python
# Deduct components used in build
for bom_item in bom_items:
    service.update_quantity(
        bom_item['component_id'],
        delta=-bom_item['quantity']
    )
```

## Examples

### Complete Workflow
```python
from component_inventory.service import ComponentInventoryService

service = ComponentInventoryService("data/db/pedalbuild.db")

# 1. Check current stock
stats = service.get_statistics()
print(f"Total: {stats['total_types']} types ({stats['total_units']} units)")

# 2. Search for specific part
results = service.search_components("JRC4558")
if results:
    print(f"Found: {results[0]['name']} - {results[0]['quantity_in_stock']} in stock")

# 3. Check low stock
low_stock = service.get_low_stock()
print(f"⚠️  {len(low_stock)} components need reordering")

# 4. Update quantity after building
success = service.update_quantity("resistor_10k_axial", delta=-3)
if success:
    print("✓ Updated: 10k Resistor (47 → 44 units)")
```

### BOM Validation
```python
from bom_manager.service import BOMManagerService

bom_service = BOMManagerService("data/db/pedalbuild.db")

# Validate circuit BOM
validation = bom_service.validate_bom("triangulum-overdrive")

print(f"\nBOM Validation: Triangulum Overdrive")
print(f"Total Items: {validation['total_items']}")
print(f"✓ Available: {validation['available_count']} ({validation['completeness']*100:.0f}%)")
print(f"⚠️  Missing: {validation['missing_count']}")

# Show missing components
if validation['missing']:
    print("\nMissing Components:")
    for item in validation['missing']:
        bom_item = item['bom_item']
        print(f"  ✗ {bom_item['component_value']} ({bom_item['component_type']}) x{bom_item['quantity']}")
```

## File Structure

```
.claude/skills/component-inventory/
├── SKILL.md                      # This file
└── service.py                    # Python service implementation
```

## Testing

```bash
# Run CLI commands
python .claude/skills/component-inventory/service.py list
python .claude/skills/component-inventory/service.py search "10k"
python .claude/skills/component-inventory/service.py stats
python .claude/skills/component-inventory/service.py low-stock
```

## Performance

- **Search**: O(n) full-text search with SQLite LIKE
- **Low Stock**: O(n) with WHERE clause, indexed on quantity
- **Statistics**: O(n) with GROUP BY, efficient aggregation

## Integration with Excel Importer

The Component Inventory integrates seamlessly with the Excel Importer:

```python
# Import inventory from CSV
from excel_importer.importer import InventoryImporter

with InventoryImporter("data/db/pedalbuild.db") as importer:
    result = importer.import_components("myInventory.csv")

# Verify import
from component_inventory.service import ComponentInventoryService

service = ComponentInventoryService("data/db/pedalbuild.db")
stats = service.get_statistics()
print(f"✓ Imported: {stats['total_types']} types")
```

## Future Enhancements

- [ ] Barcode/QR code scanning for component lookup
- [ ] Auto-reordering integration with vendors (Mouser, DigiKey)
- [ ] Price tracking and cost analysis
- [ ] Component usage history and analytics
- [ ] Multi-location inventory (multiple storage areas)
- [ ] Component photos/images
- [ ] Component lifecycle tracking (expiration dates)

---

**Status**: ✅ Complete (Python implementation)

**Dependencies**:
- Database: SQLite with `components` table
- Python: 3.9+
- Pydantic: For type validation

**Last Updated**: 2026-02-14
