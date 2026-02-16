"""
BOM Manager Service
Business logic for Bill of Materials management in Python
"""

import sqlite3
from typing import List, Dict, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
from models.types import ComponentType, CircuitBOMItem


class BOMManagerService:
    """BOM management service"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_conn(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def get_bom(self, circuit_id: str) -> List[Dict]:
        """Get BOM for a circuit"""
        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM circuit_bom WHERE circuit_id = ? ORDER BY component_type, component_value",
            (circuit_id,)
        )

        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()
        return results

    def get_bom_by_type(self, circuit_id: str) -> Dict[str, List[Dict]]:
        """Get BOM organized by component type"""
        bom_items = self.get_bom(circuit_id)

        by_type = {}
        for item in bom_items:
            comp_type = item['component_type']
            if comp_type not in by_type:
                by_type[comp_type] = []
            by_type[comp_type].append(item)

        return by_type

    def add_bom_item(self, circuit_id: str, item: Dict) -> bool:
        """Add item to BOM"""
        conn = self._get_conn()
        cursor = conn.cursor()

        # Generate ID
        item_id = f"{circuit_id}_{item['component_type']}_{item['component_value']}_{item['quantity']}"

        cursor.execute("""
            INSERT INTO circuit_bom (
                id, circuit_id, component_type, component_value, quantity,
                reference_designator, substitution_allowed, substitution_notes,
                is_critical, position_x, position_y, confidence_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id,
            circuit_id,
            item['component_type'],
            item['component_value'],
            item['quantity'],
            item.get('reference_designator'),
            item.get('substitution_allowed', False),
            item.get('substitution_notes'),
            item.get('is_critical', False),
            item.get('position_x'),
            item.get('position_y'),
            item.get('confidence_score', 1.0)
        ))

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        return success

    def validate_bom(self, circuit_id: str) -> Dict:
        """Validate BOM against inventory"""
        bom_items = self.get_bom(circuit_id)

        # Import component inventory service
        from .component_inventory import ComponentInventoryService

        inventory_service = ComponentInventoryService(self.db_path)

        matches = []
        missing = []
        available_count = 0

        for bom_item in bom_items:
            # Search for matching component
            search_results = inventory_service.search_components(bom_item['component_value'])

            # Filter by type
            matching = [
                c for c in search_results
                if c['type'] == bom_item['component_type']
            ]

            if matching and matching[0]['quantity_in_stock'] >= bom_item['quantity']:
                matches.append({
                    'bom_item': bom_item,
                    'component': matching[0],
                    'available': True,
                    'quantity_needed': bom_item['quantity'],
                    'quantity_available': matching[0]['quantity_in_stock']
                })
                available_count += 1
            else:
                missing.append({
                    'bom_item': bom_item,
                    'component': matching[0] if matching else None,
                    'available': False,
                    'quantity_needed': bom_item['quantity'],
                    'quantity_available': matching[0]['quantity_in_stock'] if matching else 0
                })

        completeness = available_count / len(bom_items) if bom_items else 0

        return {
            'total_items': len(bom_items),
            'available_count': available_count,
            'missing_count': len(missing),
            'completeness': completeness,
            'matches': matches,
            'missing': missing
        }

    def get_shopping_list(self, circuit_id: str) -> Dict:
        """Get shopping list of missing components"""
        validation = self.validate_bom(circuit_id)

        shopping_list = []
        for item in validation['missing']:
            shopping_list.append({
                'type': item['bom_item']['component_type'],
                'value': item['bom_item']['component_value'],
                'quantity': item['bom_item']['quantity'],
                'references': item['bom_item']['reference_designator'].split(',') if item['bom_item']['reference_designator'] else []
            })

        return {
            'missing_items': shopping_list,
            'total_missing': len(shopping_list)
        }

    def export_bom_csv(self, circuit_id: str) -> str:
        """Export BOM to CSV format"""
        bom_items = self.get_bom(circuit_id)

        lines = ["Type,Value,Quantity,Reference Designators,Critical,Confidence"]

        for item in bom_items:
            lines.append(
                f"{item['component_type']},"
                f"{item['component_value']},"
                f"{item['quantity']},"
                f"\"{item['reference_designator'] or ''}\","
                f"{'Yes' if item['is_critical'] else 'No'},"
                f"{item['confidence_score']:.2f}"
            )

        return "\n".join(lines)

    def get_statistics(self, circuit_id: str) -> Dict:
        """Get BOM statistics"""
        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                component_type,
                COUNT(*) as count,
                SUM(CASE WHEN is_critical = 1 THEN 1 ELSE 0 END) as critical_count,
                SUM(CASE WHEN confidence_score < 0.7 THEN 1 ELSE 0 END) as low_confidence_count
            FROM circuit_bom
            WHERE circuit_id = ?
            GROUP BY component_type
        """, (circuit_id,))

        by_type = {}
        total_items = 0
        critical_count = 0
        low_confidence_count = 0

        for row in cursor.fetchall():
            comp_type = row[0]
            by_type[comp_type] = row[1]
            total_items += row[1]
            critical_count += row[2]
            low_confidence_count += row[3]

        conn.close()

        return {
            'total_items': total_items,
            'by_type': by_type,
            'critical_count': critical_count,
            'low_confidence_count': low_confidence_count
        }


# CLI for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python service.py <command> <circuit_id>")
        print("Commands: show, validate, shopping-list, stats, export")
        sys.exit(1)

    service = BOMManagerService("data/db/pedalbuild.db")
    command = sys.argv[1]
    circuit_id = sys.argv[2]

    if command == "show":
        bom = service.get_bom(circuit_id)
        print(f"\nBOM for {circuit_id} ({len(bom)} items):")
        for item in bom:
            print(f"  {item['reference_designator']}: {item['component_value']} ({item['component_type']}) x{item['quantity']}")

    elif command == "validate":
        validation = service.validate_bom(circuit_id)
        print(f"\nBOM Validation for {circuit_id}:")
        print(f"  Total: {validation['total_items']}")
        print(f"  Available: {validation['available_count']} ({validation['completeness']*100:.0f}%)")
        print(f"  Missing: {validation['missing_count']}")

        if validation['missing']:
            print(f"\n  Missing Components:")
            for item in validation['missing']:
                print(f"    - {item['bom_item']['component_value']} ({item['bom_item']['component_type']}) x{item['bom_item']['quantity']}")

    elif command == "shopping-list":
        shopping = service.get_shopping_list(circuit_id)
        print(f"\nShopping List for {circuit_id}:")
        print(f"  Missing: {shopping['total_missing']} items\n")

        for item in shopping['missing_items']:
            refs = ', '.join(item['references']) if item['references'] else 'N/A'
            print(f"  [ ] {item['value']} ({item['type']}) x{item['quantity']}")
            print(f"      Refs: {refs}")

    elif command == "stats":
        stats = service.get_statistics(circuit_id)
        print(f"\nBOM Statistics for {circuit_id}:")
        print(f"  Total Items: {stats['total_items']}")
        print(f"  Critical Components: {stats['critical_count']}")
        print(f"  Low Confidence: {stats['low_confidence_count']}")
        print(f"\n  By Type:")
        for comp_type, count in stats['by_type'].items():
            print(f"    {comp_type}: {count}")

    elif command == "export":
        csv = service.export_bom_csv(circuit_id)
        print(csv)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
