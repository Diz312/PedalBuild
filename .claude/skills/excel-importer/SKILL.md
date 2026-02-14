---
name: excel-importer
description: Import component inventory from Excel/CSV files into PedalBuild database. Handles user's specific CSV format with Category, SubType, HumanReadableValue, NumericBaseValue, Footprint, Voltage, and Quantity columns.
argument-hint: [csv-file-path]
---

# Excel Inventory Importer

Import your existing component inventory from CSV/Excel into the PedalBuild database.

## Supported Format

Your CSV file with columns:
- **Category** - Component type (Resistor, Capacitor, IC, Transistor, Diode, Pot, Hardware)
- **SubType** - Specific subtype (Metal Film, Ceramic, JFET N-Channel, etc.)
- **HumanReadableValue** - Display value (10K, 100n, 2N5088, TL072CP, etc.)
- **NumericBaseValue** - Numeric value for calculations
- **UnitType** - Unit (Ohms, pF, N/A)
- **Footprint** - Package type (Axial 1/4W, DIP-8, TO-92, etc.)
- **Voltage** - Voltage rating (50V, ±18V / 36V, etc.)
- **Quantity** - Current stock quantity
- **ReorderLevel** - (optional) Minimum stock alert
- **RelatedPart** - (optional) Related components
- **MfrPartNumber** - (optional) Manufacturer part number
- **Vendor** - (optional) Supplier name
- **VendorSKU** - (optional) Supplier SKU
- **KeyNotes** - Detailed notes (especially for ICs)

## Usage

### Command Line
```bash
# Import from CSV
/excel-importer path/to/myInventory.csv

# With preview (dry-run)
/excel-importer path/to/myInventory.csv --preview

# Force overwrite existing components
/excel-importer path/to/myInventory.csv --force
```

### From Code
```typescript
import { importInventory } from '.claude/skills/excel-importer/parsers/csv-parser';

const result = await importInventory('myInventory.csv', {
  preview: false,
  skipDuplicates: true
});

console.log(`Imported: ${result.imported}, Skipped: ${result.skipped}`);
```

## Column Mapping

CSV Column → Database Field:
- `Category` → `components.type` (normalized: resistor, capacitor, ic, transistor, diode, potentiometer, hardware, other)
- `SubType` → Included in `components.name` (e.g., "Metal Film 10K", "Dual Op-Amp JRC4558")
- `HumanReadableValue` → `components.value`
- `NumericBaseValue` + `UnitType` → Stored in notes for reference
- `Footprint` → `components.package`
- `Voltage` → `components.voltage` (add to schema if needed)
- `Quantity` → `components.quantity_in_stock`
- `ReorderLevel` → `components.minimum_quantity`
- `KeyNotes` → `components.notes`
- `MfrPartNumber` → `components.part_number`
- `Vendor` → Stored in notes

## Features

### 1. Duplicate Detection
- Checks for existing components by `type` + `value` + `package`
- Options: skip, overwrite, or merge (add quantities)

### 2. Data Validation
- Ensures required fields (Category, HumanReadableValue, Quantity)
- Validates quantity is numeric and >= 0
- Normalizes component types to match database enum

### 3. Data Cleaning
- Trims whitespace
- Handles quoted fields with commas
- Skips empty rows (many in your CSV)
- Normalizes voltage formats

### 4. Import Preview
```
Preview Mode - No changes will be made
=======================================
✓ 52 Resistors (Metal Film)
✓ 41 Capacitors (15 Ceramic, 8 Electrolytic, 18 Film)
✓ 18 ICs (Op-Amps, Regulators, Power Amps)
✓ 7 Transistors (JFET, BJT NPN)
✓ 11 Diodes (Germanium, Silicon, Schottky, Zener)
✓ 31 Potentiometers (Logarithmic, Linear, Reverse Log)
✓ 21 Hardware (Footswitches, Jacks, LEDs, Enclosures)

Total: 181 components
Duplicates found: 0
Missing required fields: 0
```

### 5. Import Report
```
Import Complete
===============
✓ 181 components imported
✗ 0 skipped (duplicates)
⚠ 0 warnings

Inventory by Type:
- Resistors: 52 (1,234 total units)
- Capacitors: 41 (612 total units)
- ICs: 18 (61 total units)
- Transistors: 7 (54 total units)
- Diodes: 11 (119 total units)
- Potentiometers: 31 (166 total units)
- Hardware: 21 (218 total units)

Database updated: data/db/pedalbuild.db
Backup created: data/backups/inventory_backup_2026-02-14.db
```

## Special Handling

### IC Op-Amps
Your inventory has detailed IC notes (JRC4558, TL072, LM833, etc.). The importer:
- Preserves all KeyNotes in the `notes` field
- Creates searchable entries for substitutions
- Links related parts (e.g., JRC4558 ↔ RC4558P)

### Potentiometers
Multi-line footprint specs are preserved:
```
Diameter: 16mm
Pins: Right-Angle
Shaft: 15mm Smooth
Mounting Hole: 6.8mm
```

### Hardware
Enclosures are imported with full dimensions (125B, 1590B, 1590BB).

## Error Handling

### Common Issues
1. **Missing CSV file**: Provides clear path error
2. **Invalid format**: Shows line number and expected format
3. **Duplicate components**: Lists conflicts and suggests resolution
4. **Type mismatch**: Shows validation errors with suggestions

### Rollback
If import fails midway:
```bash
# Restore from automatic backup
sqlite3 data/db/pedalbuild.db < data/backups/inventory_backup_YYYY-MM-DD.db
```

## Advanced Options

### Merge Mode
```bash
# Add quantities to existing components instead of skipping
/excel-importer myInventory.csv --merge
```

### Selective Import
```bash
# Import only resistors and capacitors
/excel-importer myInventory.csv --types resistor,capacitor

# Import only items with quantity > 0
/excel-importer myInventory.csv --min-quantity 1
```

### Update Mode
```bash
# Update quantities for existing components
/excel-importer myInventory.csv --update-quantities-only
```

## Implementation Notes

### Parser (`parsers/csv-parser.ts`)
- Uses `papaparse` or native CSV parsing
- Handles quoted fields with embedded commas
- Skips rows with all empty fields
- Preserves multi-line cell content

### Mapper (`mappers/column-mapper.ts`)
- Maps your CSV columns to database schema
- Normalizes component types
- Generates composite names (SubType + Value)
- Handles voltage format variations

### Validator (`validators/component-validator.ts`)
- Validates required fields
- Checks data types
- Ensures referential integrity
- Flags suspicious values (e.g., quantity > 10000)

## Example Output

After running `/excel-importer myInventory.csv`:

```
Parsing CSV file: myInventory.csv
✓ Found 270 rows (89 empty, 181 components)

Validating data...
✓ All required fields present
✓ No invalid quantities
✓ Component types recognized

Checking for duplicates...
✓ No duplicates found in database

Importing to database...
[========================================] 100% (181/181)

✓ Import complete in 2.3 seconds

Summary:
  Resistors: 52 items (1,234 total units)
  Capacitors: 41 items (612 total units)
  ICs: 18 items (61 total units)
  Transistors: 7 items (54 total units)
  Diodes: 11 items (119 total units)
  Potentiometers: 31 items (166 total units)
  Hardware: 21 items (218 total units)

Next steps:
  1. View inventory: /component-inventory list
  2. Check low stock: /component-inventory low-stock
  3. Start building: Select circuit from PedalPCB.com
```

## Testing

Test with your actual inventory:
```bash
# Preview first (no changes)
/excel-importer myInventory.csv --preview

# If preview looks good, import
/excel-importer myInventory.csv

# Verify import
sqlite3 data/db/pedalbuild.db "SELECT type, COUNT(*), SUM(quantity_in_stock) FROM components GROUP BY type;"
```

## Database Schema Requirements

Ensure `components` table has these fields:
- `id` TEXT PRIMARY KEY
- `type` TEXT NOT NULL
- `name` TEXT NOT NULL
- `value` TEXT
- `package` TEXT (maps to Footprint)
- `voltage` TEXT (add if not present)
- `quantity_in_stock` INTEGER
- `minimum_quantity` INTEGER
- `part_number` TEXT
- `notes` TEXT
- `created_at` DATETIME
- `updated_at` DATETIME

## Reusability

This importer is designed for your specific CSV format but can be adapted:
- Modify column mapping in `mappers/column-mapper.ts`
- Adjust validation rules in `validators/component-validator.ts`
- Support Excel (.xlsx) by adding `xlsx` library

---

**Status**: ✅ Ready for use with your myInventory.csv

**Last Updated**: 2026-02-14
