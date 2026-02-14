"""
Component Inventory Service
Business logic for component management in Python
"""

import sqlite3
from typing import List, Optional, Dict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
from models.types import Component, ComponentType


class ComponentInventoryService:
    """Component inventory management service"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_conn(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def list_components(self, comp_type: Optional[ComponentType] = None) -> List[Dict]:
        """List all components with optional type filter"""
        conn = self._get_conn()
        cursor = conn.cursor()

        if comp_type:
            cursor.execute(
                "SELECT * FROM components WHERE type = ? ORDER BY type, value",
                (comp_type.value,)
            )
        else:
            cursor.execute("SELECT * FROM components ORDER BY type, value")

        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()
        return results

    def search_components(self, query: str) -> List[Dict]:
        """Search components by value or name"""
        conn = self._get_conn()
        cursor = conn.cursor()

        pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM components
            WHERE value LIKE ? OR name LIKE ? OR part_number LIKE ?
            ORDER BY
                CASE
                    WHEN value = ? THEN 1
                    WHEN value LIKE ? THEN 2
                    WHEN name LIKE ? THEN 3
                    ELSE 4
                END,
                type, value
        """, (pattern, pattern, pattern, query, f"{query}%", f"{query}%"))

        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()
        return results

    def get_component(self, component_id: str) -> Optional[Dict]:
        """Get component by ID"""
        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM components WHERE id = ?", (component_id,))
        row = cursor.fetchone()

        if row:
            columns = [desc[0] for desc in cursor.description]
            result = dict(zip(columns, row))
        else:
            result = None

        conn.close()
        return result

    def get_low_stock(self) -> List[Dict]:
        """Get components with low stock"""
        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM components
            WHERE quantity_in_stock <= minimum_quantity
            ORDER BY type, value
        """)

        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()
        return results

    def update_quantity(self, component_id: str, delta: int) -> bool:
        """Update component quantity (add or subtract)"""
        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE components
            SET quantity_in_stock = quantity_in_stock + ?,
                updated_at = datetime('now')
            WHERE id = ?
        """, (delta, component_id))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def get_statistics(self) -> Dict:
        """Get inventory statistics"""
        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                type,
                COUNT(*) as type_count,
                SUM(quantity_in_stock) as total_units,
                SUM(CASE WHEN quantity_in_stock <= minimum_quantity THEN 1 ELSE 0 END) as low_stock_count,
                SUM(CASE WHEN quantity_in_stock = 0 THEN 1 ELSE 0 END) as out_of_stock_count
            FROM components
            GROUP BY type
        """)

        by_type = {}
        total_types = 0
        total_units = 0
        low_stock_count = 0
        out_of_stock_count = 0

        for row in cursor.fetchall():
            comp_type = row[0]
            by_type[comp_type] = {
                'types': row[1],
                'units': row[2]
            }
            total_types += row[1]
            total_units += row[2]
            low_stock_count += row[3]
            out_of_stock_count += row[4]

        conn.close()

        return {
            'total_types': total_types,
            'total_units': total_units,
            'by_type': by_type,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count
        }


# CLI for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python service.py <command> [args]")
        print("Commands: list, search <query>, stats, low-stock")
        sys.exit(1)

    service = ComponentInventoryService("data/db/pedalbuild.db")
    command = sys.argv[1]

    if command == "list":
        components = service.list_components()
        print(f"\nComponents ({len(components)}):")
        for comp in components[:10]:  # Show first 10
            print(f"  {comp['name']} ({comp['value']}) - {comp['quantity_in_stock']} units")

    elif command == "search" and len(sys.argv) > 2:
        query = sys.argv[2]
        results = service.search_components(query)
        print(f"\nSearch results for '{query}' ({len(results)}):")
        for comp in results:
            print(f"  {comp['name']} ({comp['value']}) - {comp['quantity_in_stock']} units")

    elif command == "stats":
        stats = service.get_statistics()
        print(f"\nInventory Statistics:")
        print(f"  Total Types: {stats['total_types']}")
        print(f"  Total Units: {stats['total_units']}")
        print(f"  Low Stock: {stats['low_stock_count']}")
        print(f"\nBy Type:")
        for comp_type, data in stats['by_type'].items():
            print(f"  {comp_type}: {data['types']} types ({data['units']} units)")

    elif command == "low-stock":
        low_stock = service.get_low_stock()
        print(f"\n⚠️  Low Stock Components ({len(low_stock)}):")
        for comp in low_stock:
            status = "OUT OF STOCK" if comp['quantity_in_stock'] == 0 else f"{comp['quantity_in_stock']}/{comp['minimum_quantity']}"
            print(f"  {comp['name']} ({comp['value']}) - {status}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
