"""
Pytest configuration and fixtures.
"""

import sqlite3
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.backend.db import Database
from src.backend.main import app


@pytest.fixture
def test_db() -> Generator[Database, None, None]:
    """
    Create a temporary test database.

    Yields:
        Database instance with test data
    """
    # Create temporary database
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_path = Path(temp_file.name)
    temp_file.close()

    # Read schema
    schema_path = Path(__file__).parent.parent / "src" / "db" / "schema.sql"
    schema_sql = schema_path.read_text()

    # Initialize database
    conn = sqlite3.connect(str(temp_path))
    conn.executescript(schema_sql)
    conn.close()

    # Create Database instance
    db = Database(temp_path)

    yield db

    # Cleanup
    temp_path.unlink()


@pytest.fixture
def client(test_db: Database) -> TestClient:
    """
    Create FastAPI test client with test database.

    Args:
        test_db: Test database fixture

    Returns:
        Test client
    """
    # Override database dependency
    def override_get_db():
        yield test_db

    from src.backend.db import get_db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    yield client

    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture
def sample_component(test_db: Database) -> dict:
    """
    Insert a sample component for testing.

    Args:
        test_db: Test database

    Returns:
        Component data
    """
    component = {
        "id": "resistor_10k_through_hole",
        "type": "resistor",
        "name": "Metal Film 10k",
        "value": "10k",
        "tolerance": "1%",
        "package": "through-hole",
        "manufacturer": None,
        "part_number": None,
        "datasheet_url": None,
        "quantity_in_stock": 50,
        "minimum_quantity": 10,
        "unit_price": None,
        "location": "Drawer A",
        "voltage": None,
        "notes": None,
    }

    with test_db.transaction() as cursor:
        cursor.execute(
            """
            INSERT INTO components (
                id, type, name, value, tolerance, package, manufacturer,
                part_number, datasheet_url, quantity_in_stock, minimum_quantity,
                unit_price, location, voltage, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                component["id"],
                component["type"],
                component["name"],
                component["value"],
                component["tolerance"],
                component["package"],
                component["manufacturer"],
                component["part_number"],
                component["datasheet_url"],
                component["quantity_in_stock"],
                component["minimum_quantity"],
                component["unit_price"],
                component["location"],
                component["voltage"],
                component["notes"],
            ),
        )

    return component


@pytest.fixture
def sample_circuit(test_db: Database) -> dict:
    """
    Insert a sample circuit for testing.

    Args:
        test_db: Test database

    Returns:
        Circuit data
    """
    circuit = {
        "id": "test_overdrive",
        "name": "Test Overdrive",
        "description": "Test circuit for BOM testing",
        "category": "overdrive",
    }

    with test_db.transaction() as cursor:
        cursor.execute(
            """
            INSERT INTO circuits (id, name, description, category)
            VALUES (?, ?, ?, ?)
        """,
            (circuit["id"], circuit["name"], circuit["description"], circuit["category"]),
        )

    return circuit


@pytest.fixture
def sample_bom(test_db: Database, sample_circuit: dict, sample_component: dict) -> list[dict]:
    """
    Insert sample BOM items for testing.

    Args:
        test_db: Test database
        sample_circuit: Circuit fixture
        sample_component: Component fixture

    Returns:
        List of BOM items
    """
    bom_items = [
        {
            "id": "test_overdrive_resistor_10k_1",
            "circuit_id": sample_circuit["id"],
            "component_type": "resistor",
            "component_value": "10k",
            "quantity": 2,
            "reference_designator": "R1,R2",
            "is_critical": True,
            "confidence_score": 0.95,
        },
        {
            "id": "test_overdrive_capacitor_100nf_1",
            "circuit_id": sample_circuit["id"],
            "component_type": "capacitor",
            "component_value": "100nF",
            "quantity": 3,
            "reference_designator": "C1,C2,C3",
            "is_critical": False,
            "confidence_score": 0.88,
        },
    ]

    with test_db.transaction() as cursor:
        for item in bom_items:
            cursor.execute(
                """
                INSERT INTO circuit_bom (
                    id, circuit_id, component_type, component_value, quantity,
                    reference_designator, is_critical, confidence_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    item["id"],
                    item["circuit_id"],
                    item["component_type"],
                    item["component_value"],
                    item["quantity"],
                    item["reference_designator"],
                    item["is_critical"],
                    item["confidence_score"],
                ),
            )

    return bom_items
