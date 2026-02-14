---
name: bom-manager
description: Create, validate, and manage Bills of Materials (BOM) for electronic circuits. Organizes components by type, validates against inventory, identifies substitutions.
argument-hint: [command] [options]
---

# BOM Manager

Comprehensive Bill of Materials management for electronic circuit builds. Create, validate, organize, and export BOMs with intelligent component matching and substitution suggestions.

## Commands

### Create BOM
```bash
# Create BOM for a circuit
/bom-manager create <circuit-id>

# Create from schematic analysis results
/bom-manager create <circuit-id> --from-schematic <analysis-json>

# Import from CSV
/bom-manager import <circuit-id> <bom-file.csv>
```

### View BOM
```bash
# Show BOM for circuit
/bom-manager show <circuit-id>

# Show organized by component type
/bom-manager show <circuit-id> --by-type

# Show with reference designators
/bom-manager show <circuit-id> --with-refs
```

### Validate BOM
```bash
# Check availability against inventory
/bom-manager validate <circuit-id>

# Show missing components only
/bom-manager validate <circuit-id> --missing-only

# Include substitution suggestions
/bom-manager validate <circuit-id> --suggest-subs
```

### Update BOM
```bash
# Add item to BOM
/bom-manager add-item <circuit-id> \
  --type resistor \
  --value "10k" \
  --quantity 3 \
  --refs "R1,R2,R3"

# Update item quantity
/bom-manager update-item <item-id> --quantity 5

# Remove item from BOM
/bom-manager remove-item <item-id>
```

### Export BOM
```bash
# Export to CSV
/bom-manager export <circuit-id> --format csv --output bom.csv

# Export organized by type
/bom-manager export <circuit-id> --format csv --by-type --output bom.csv

# Export shopping list (missing items only)
/bom-manager shopping-list <circuit-id> --output shopping.txt
```

## Features

### 1. BOM Creation from Multiple Sources

#### From Schematic Analysis
```bash
# After schematic vision analysis completes
/bom-manager create triangulum-overdrive --from-schematic analysis-results.json

Output:
Creating BOM from schematic analysis...
✓ Extracted 24 components
✓ Grouped by type (8 resistors, 7 capacitors, 2 ICs, 3 transistors, 4 diodes)
✓ Reference designators mapped
✓ Confidence scores recorded

BOM created: triangulum-overdrive (24 items)
```

#### From Manual Entry
```bash
/bom-manager create tube-screamer-clone
/bom-manager add-item tube-screamer-clone --type resistor --value "10k" --quantity 3 --refs "R1,R2,R3"
/bom-manager add-item tube-screamer-clone --type capacitor --value "100nF" --quantity 2 --refs "C1,C5"
/bom-manager add-item tube-screamer-clone --type ic --value "JRC4558D" --quantity 1 --refs "IC1"
```

#### From CSV Import
```csv
Type,Value,Quantity,Reference Designators,Notes
resistor,10k,3,"R1,R2,R3",Metal film 1%
resistor,4.7k,2,"R4,R5",
capacitor,100nF,4,"C1,C2,C3,C4",Ceramic
capacitor,1uF,2,"C5,C6",Electrolytic 25V
ic,JRC4558D,1,IC1,Dual op-amp
transistor,2N5088,2,"Q1,Q2",NPN BJT
```

### 2. Organization by Component Type

```bash
/bom-manager show triangulum-overdrive --by-type

BOM: Triangulum Overdrive (24 items)
====================================

RESISTORS (8):
  10k    × 3  [R1, R2, R3]          ✓ In stock (47 units)
  4.7k   × 2  [R4, R5]              ⚠️ Low stock (2 units)
  1k     × 1  [R6]                  ✓ In stock (25 units)
  100R   × 2  [R7, R8]              ✗ Out of stock

CAPACITORS (7):
  100nF  × 4  [C1, C2, C3, C4]      ✓ In stock (15 units)
  1µF    × 2  [C5, C6]              ✓ In stock (8 units)
  47nF   × 1  [C7]                  ✗ Out of stock

ICS (2):
  JRC4558D × 1  [IC1]               ✗ Out of stock
  → Substitute: TL072CP (3 in stock) - "TL072 is brighter/clearer"

TRANSISTORS (3):
  2N5088   × 2  [Q1, Q2]            ✓ In stock (5 units)
  2N3904   × 1  [Q3]                ✓ In stock (12 units)

DIODES (4):
  1N4148   × 2  [D1, D2]            ✓ In stock (20 units)
  1N5817   × 2  [D3, D4]            ✓ In stock (10 units)
```

### 3. Inventory Validation

```bash
/bom-manager validate triangulum-overdrive

BOM Validation: Triangulum Overdrive
====================================
Total Items: 24
✓ Available: 18 (75%)
⚠️ Low Stock: 2 (8%)
✗ Missing: 4 (17%)

Overall Completeness: 75%

READY TO BUILD:
  ✓ 10k resistors (need 3, have 47)
  ✓ 1k resistors (need 1, have 25)
  ✓ 100nF capacitors (need 4, have 15)
  ✓ 1µF capacitors (need 2, have 8)
  ✓ 2N5088 transistors (need 2, have 5)
  ✓ 2N3904 transistors (need 1, have 12)
  ✓ 1N4148 diodes (need 2, have 20)
  ✓ 1N5817 diodes (need 2, have 10)

LOW STOCK (reorder soon):
  ⚠️ 4.7k resistors (need 2, have 2) - exact match
  ⚠️ 2N5088 transistors (need 2, have 5) - will be low after build

MISSING COMPONENTS:
  ✗ 100R resistors × 2
  ✗ 47nF capacitors × 1
  ✗ JRC4558D × 1 (can substitute TL072CP)
  ✗ 15k resistors × 1

SUBSTITUTION SUGGESTIONS:
  JRC4558D → TL072CP
    Reason: Compatible dual op-amp (TL072 is brighter/clearer than JRC4558)
    Impact: Moderate (affects tone character)
    In Stock: 3 units
    Confidence: 85%
```

### 4. Shopping List Generation

```bash
/bom-manager shopping-list triangulum-overdrive

Shopping List: Triangulum Overdrive
====================================
Missing components to purchase:

RESISTORS:
  [ ] 100Ω × 2  (Metal film, 1/4W, 1%)
  [ ] 15kΩ × 1  (Metal film, 1/4W, 1%)

CAPACITORS:
  [ ] 47nF × 1  (Ceramic, 50V)

ICS:
  [ ] JRC4558D × 1  (DIP-8, Dual Op-Amp)
      Alternative: TL072CP (currently in stock)

REORDER SOON (low stock):
  [ ] 4.7kΩ × 5  (Metal film, 1/4W, 1%) - currently 2, need buffer

Total Missing Items: 5
Estimated Cost: $2.50 (excluding IC)

Notes:
- Can substitute TL072CP for JRC4558D (tone will be brighter)
- 4.7k resistors will be depleted after this build
```

### 5. Component Matching Intelligence

The BOM Manager uses intelligent matching from the Component Inventory skill:

```bash
# Exact match
BOM: "10k resistor"
Inventory: "Metal Film Resistor 10k (±1%)"
Result: ✓ Exact match

# Tolerance matching
BOM: "10k resistor (±5%)"
Inventory: "10k resistor (±1%)"
Result: ✓ Match (better tolerance available)

# Value normalization
BOM: "100n capacitor"
Inventory: "100nF Ceramic Capacitor"
Result: ✓ Match (normalized values)

# IC substitution
BOM: "JRC4558D"
Inventory: "TL072CP"
Result: ⚠️ Substitute available (compatible dual op-amp)

# Package variants
BOM: "TL072"
Inventory: "TL072CP (DIP-8)"
Result: ✓ Match (same IC, specific package)
```

### 6. Critical Component Flagging

```bash
/bom-manager show triangulum-overdrive --critical

CRITICAL COMPONENTS (affect tone significantly):
  ⚠️ JRC4558D (IC1) - Core tone-shaping op-amp
     Substitution impact: MODERATE
     Alternative: TL072CP (brighter, less warm)

  ⚠️ 1N4148 Diodes (D1, D2) - Clipping circuit
     Substitution impact: SIGNIFICANT
     Alternative: 1N914 (nearly identical)

  ✓ 10k Resistors (R1, R2, R3) - Gain staging
     Substitution impact: MINIMAL
     Tolerance: ±1% preferred, ±5% acceptable
```

## Data Model

### BOM Item Schema
```typescript
interface CircuitBOMItem {
  id: string;
  circuit_id: string;
  component_type: ComponentType;
  component_value: string;
  quantity: number;
  reference_designator?: string;    // "R1" or "R1,R2,R3"
  substitution_allowed: boolean;
  substitution_notes?: string;
  is_critical: boolean;             // Affects tone significantly
  position_x?: number;              // Schematic position
  position_y?: number;
  confidence_score: number;         // From schematic analysis (0-1)
}
```

## Integration with Workflow

### Stage 3: Schematic Analysis → BOM Generation
```bash
# After schematic vision analysis completes
/bom-manager create <circuit-id> --from-schematic <analysis-json>

# Automatically extracts:
- Component types and values
- Reference designators (R1, C2, IC1, etc.)
- Confidence scores from vision analysis
- Component positions on schematic
```

### Stage 4: Inventory Check
```bash
# Validate BOM against current inventory
/bom-manager validate <circuit-id>

# Outputs:
- Available components (ready to build)
- Missing components (need to order)
- Low stock warnings
- Substitution suggestions
```

### Stage 5: Component Procurement
```bash
# Generate shopping list
/bom-manager shopping-list <circuit-id>

# User handles ordering from preferred vendors
# (No automatic vendor integration per user requirements)
```

### Stage 6: Breadboard Layout
```bash
# Export organized BOM for layout agent
/bom-manager export <circuit-id> --format json --by-type

# Layout agent uses organized BOM to:
- Group components by function
- Place components logically on breadboard
- Minimize wire crossings
```

## Usage from Code

### TypeScript Integration
```typescript
import { BOMManagerService } from '.claude/skills/bom-manager/service';

const service = new BOMManagerService(db);

// Create BOM from schematic analysis
const bom = await service.createFromSchematic(circuitId, analysisResults);

// Validate against inventory
const validation = await service.validateBOM(circuitId);

// Export organized by type
const organized = await service.exportOrganized(circuitId);
```

### ADK Agent Integration
```typescript
import { BOMManagerTool } from '.claude/skills/bom-manager/tools';

const tool = new BOMManagerTool(db);

const agent = new LlmAgent({
  name: 'BOMGenerationAgent',
  tools: [tool],
  model: 'gemini-2.0-flash-exp'
});
```

## Export Formats

### CSV Format
```csv
Type,Value,Quantity,Reference Designators,In Stock,Notes
resistor,10k,3,"R1,R2,R3",Yes,Metal film 1%
resistor,4.7k,2,"R4,R5",Low Stock (2),
capacitor,100nF,4,"C1,C2,C3,C4",Yes,Ceramic
ic,JRC4558D,1,IC1,No,Substitute: TL072CP
```

### JSON Format
```json
{
  "circuit_id": "triangulum-overdrive",
  "circuit_name": "Triangulum Overdrive",
  "total_items": 24,
  "by_type": {
    "resistor": [
      {
        "value": "10k",
        "quantity": 3,
        "reference_designators": ["R1", "R2", "R3"],
        "in_stock": true,
        "available_quantity": 47
      }
    ],
    "capacitor": [ ... ],
    "ic": [ ... ]
  },
  "completeness": 0.75,
  "missing_components": [ ... ],
  "substitutions": [ ... ]
}
```

## File Structure

```
.claude/skills/bom-manager/
├── SKILL.md                      # This file
├── service.ts                    # Core business logic
├── repository.ts                 # Database operations
├── tools.ts                      # ADK tool implementations
├── cli.ts                        # Command-line interface
├── parser.ts                     # Parse BOM from various formats
├── export.ts                     # Export functionality
└── tests/
    ├── service.test.ts
    ├── parser.test.ts
    └── fixtures/
        ├── sample-bom.csv
        └── schematic-analysis.json
```

## Testing

```bash
# Test with sample data
/bom-manager import tube-screamer tests/fixtures/sample-bom.csv
/bom-manager validate tube-screamer
/bom-manager shopping-list tube-screamer
```

## Best Practices

1. **Always validate before building**: Check inventory availability
2. **Flag critical components**: Mark tone-affecting parts
3. **Document substitutions**: Note impact on tone/functionality
4. **Track confidence scores**: Review low-confidence items from schematic analysis
5. **Keep BOMs organized**: Use reference designators consistently

## Future Enhancements

- [ ] BOM versioning (track changes over time)
- [ ] Cost tracking and optimization
- [ ] Vendor price comparison (when vendor APIs integrated)
- [ ] Component lifecycle tracking (obsolescence warnings)
- [ ] BOM templates for common circuit blocks
- [ ] Multi-project BOM consolidation
- [ ] Alternative component suggestions from community

---

**Status**: ✅ Ready for use

**Dependencies**:
- Database: SQLite with `circuit_bom` table
- Component Inventory: For validation and matching
- Schematic Analyzer: For automatic BOM extraction

**Last Updated**: 2026-02-14
