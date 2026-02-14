#!/usr/bin/env python3
"""
Excel/CSV Inventory Importer
Import component inventory from user's custom CSV format into SQLite database
"""

import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import sys

# Add src to path for types
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
from models.types import ComponentType


class InventoryImporter:
    """Import inventory from CSV to database"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def normalize_type(self, category: str) -> str:
        """Normalize component type from CSV to database enum"""
        type_map = {
            'RESISTOR': 'resistor',
            'RESISTORS': 'resistor',
            'CAPACITOR': 'capacitor',
            'CAPACITORS': 'capacitor',
            'IC': 'ic',
            'ICS': 'ic',
            'IC ': 'ic',  # Handle trailing space
            'TRANSISTOR': 'transistor',
            'TRANSISTORS': 'transistor',
            'DIODE': 'diode',
            'DIODES': 'diode',
            'POT': 'potentiometer',
            'POTS': 'potentiometer',
            'POTENTIOMETER': 'potentiometer',
            'POTENTIOMETERS': 'potentiometer',
            'HARDWARE': 'hardware',
            'HARDWARE ': 'hardware',  # Handle trailing space
            'SWITCH': 'switch',
            'LED': 'led',
            'JACK': 'jack',
        }

        normalized = category.strip().upper()
        return type_map.get(normalized, 'other')

    def generate_component_id(self, comp_type: str, value: str, package: str) -> str:
        """Generate unique component ID"""
        def clean(s: str) -> str:
            return s.lower().replace(' ', '_').replace('/', '_').replace('-', '_').replace('.', '_')

        parts = [clean(comp_type)]
        if value:
            parts.append(clean(value))
        if package:
            parts.append(clean(package[:20]))  # Limit package length

        return '_'.join(parts)

    def create_component_name(self, subtype: str, value: str) -> str:
        """Create component name from SubType and Value"""
        if subtype and value:
            return f"{subtype.strip()} {value.strip()}"
        elif subtype:
            return subtype.strip()
        elif value:
            return value.strip()
        else:
            return "Unknown Component"

    def parse_csv(self, csv_path: str) -> pd.DataFrame:
        """Parse CSV file"""
        # Read CSV
        df = pd.read_csv(csv_path)

        # Remove completely empty rows
        df = df.dropna(how='all')

        # Required columns
        required = ['Category', 'HumanReadableValue', 'Quantity']
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Remove rows with missing required fields
        df = df.dropna(subset=required)

        return df

    def transform_row(self, row: pd.Series) -> Dict:
        """Transform CSV row to component data"""
        # Normalize type
        comp_type = self.normalize_type(row['Category'])

        # Create name
        subtype = str(row.get('SubType', '')) if pd.notna(row.get('SubType')) else ''
        value = str(row['HumanReadableValue'])
        name = self.create_component_name(subtype, value)

        # Generate ID
        package = str(row.get('Footprint', '')) if pd.notna(row.get('Footprint')) else ''
        comp_id = self.generate_component_id(comp_type, value, package)

        # Build component dict
        component = {
            'id': comp_id,
            'type': comp_type,
            'name': name,
            'value': value,
            'tolerance': None,  # Not in user's CSV
            'package': package if package else None,
            'manufacturer': None,  # Not in user's CSV
            'part_number': str(row.get('MfrPartNumber', '')) if pd.notna(row.get('MfrPartNumber')) else None,
            'datasheet_url': None,  # Not in user's CSV
            'quantity_in_stock': int(row['Quantity']),
            'minimum_quantity': int(row.get('ReorderLevel', 0)) if pd.notna(row.get('ReorderLevel')) else 0,
            'unit_price': None,  # Not in user's CSV
            'location': None,  # Not in user's CSV
            'voltage': str(row.get('Voltage', '')) if pd.notna(row.get('Voltage')) else None,
            'notes': self._build_notes(row),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        return component

    def _build_notes(self, row: pd.Series) -> Optional[str]:
        """Build notes field from CSV columns"""
        notes_parts = []

        # Add key notes (especially for ICs)
        if pd.notna(row.get('KeyNotes')):
            notes_parts.append(str(row['KeyNotes']))

        # Add related parts
        if pd.notna(row.get('RelatedPart')):
            notes_parts.append(f"Related: {row['RelatedPart']}")

        # Add vendor info
        if pd.notna(row.get('Vendor')):
            vendor = row['Vendor']
            sku = row.get('VendorSKU', '')
            if pd.notna(sku):
                notes_parts.append(f"Vendor: {vendor} (SKU: {sku})")
            else:
                notes_parts.append(f"Vendor: {vendor}")

        # Add numeric base value and unit for reference
        if pd.notna(row.get('NumericBaseValue')) and pd.notna(row.get('UnitType')):
            notes_parts.append(f"Numeric: {row['NumericBaseValue']} {row['UnitType']}")

        return "\n".join(notes_parts) if notes_parts else None

    def import_components(self, csv_path: str, preview: bool = False) -> Dict:
        """Import components from CSV"""
        print(f"📂 Parsing CSV file: {csv_path}")

        # Parse CSV
        df = self.parse_csv(csv_path)

        print(f"✓ Found {len(df)} components")

        # Transform rows
        components = [self.transform_row(row) for _, row in df.iterrows()]

        # Group by type for statistics
        type_counts = {}
        for comp in components:
            comp_type = comp['type']
            type_counts[comp_type] = type_counts.get(comp_type, 0) + 1

        # Print preview
        print("\n📊 Inventory Preview:")
        print("=" * 60)
        for comp_type, count in sorted(type_counts.items()):
            total_units = sum(c['quantity_in_stock'] for c in components if c['type'] == comp_type)
            print(f"  {comp_type.upper()}: {count} types ({total_units} total units)")

        if preview:
            print("\n⚠️  Preview mode - no changes made to database")
            return {
                'preview': True,
                'total_components': len(components),
                'by_type': type_counts
            }

        # Import to database
        print(f"\n💾 Importing to database: {self.db_path}")

        cursor = self.conn.cursor()
        inserted = 0
        skipped = 0

        for comp in components:
            try:
                # Check if exists
                cursor.execute("SELECT id FROM components WHERE id = ?", (comp['id'],))
                if cursor.fetchone():
                    print(f"  ⚠️  Skipped (exists): {comp['name']}")
                    skipped += 1
                    continue

                # Insert
                cursor.execute("""
                    INSERT INTO components (
                        id, type, name, value, tolerance, package, manufacturer,
                        part_number, datasheet_url, quantity_in_stock, minimum_quantity,
                        unit_price, location, voltage, notes, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    comp['id'], comp['type'], comp['name'], comp['value'],
                    comp['tolerance'], comp['package'], comp['manufacturer'],
                    comp['part_number'], comp['datasheet_url'], comp['quantity_in_stock'],
                    comp['minimum_quantity'], comp['unit_price'], comp['location'],
                    comp['voltage'], comp['notes'], comp['created_at'], comp['updated_at']
                ))
                inserted += 1

            except Exception as e:
                print(f"  ✗ Error importing {comp['name']}: {e}")

        self.conn.commit()

        print(f"\n✅ Import complete!")
        print(f"   Inserted: {inserted}")
        print(f"   Skipped: {skipped}")

        return {
            'preview': False,
            'inserted': inserted,
            'skipped': skipped,
            'total_components': len(components),
            'by_type': type_counts
        }


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Import component inventory from CSV')
    parser.add_argument('csv_file', help='Path to CSV file')
    parser.add_argument('--preview', action='store_true', help='Preview only, do not import')
    parser.add_argument('--db', default='data/db/pedalbuild.db', help='Database path')

    args = parser.parse_args()

    # Check file exists
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        sys.exit(1)

    # Import
    with InventoryImporter(args.db) as importer:
        result = importer.import_components(str(csv_path), preview=args.preview)

    sys.exit(0)


if __name__ == "__main__":
    main()
