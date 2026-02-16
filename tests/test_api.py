"""
API Integration Tests

Tests for FastAPI endpoints.
"""

import io

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health check and root endpoints."""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "PedalBuild API"
        assert data["version"] == "0.1.0"

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "database" in data
        assert "timestamp" in data


class TestInventoryEndpoints:
    """Test component inventory endpoints."""

    def test_list_components_empty(self, client: TestClient):
        """Test listing components when inventory is empty."""
        response = client.get("/api/inventory/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["components"] == []

    def test_list_components_with_data(self, client: TestClient, sample_component: dict):
        """Test listing components with data."""
        response = client.get("/api/inventory/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["components"]) == 1
        assert data["components"][0]["id"] == sample_component["id"]

    def test_list_components_filtered_by_type(self, client: TestClient, sample_component: dict):
        """Test listing components filtered by type."""
        response = client.get("/api/inventory/?type=resistor")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1

        response = client.get("/api/inventory/?type=capacitor")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

    def test_search_components(self, client: TestClient, sample_component: dict):
        """Test component search."""
        response = client.get("/api/inventory/search?q=10k")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["components"][0]["value"] == "10k"

    def test_search_components_no_results(self, client: TestClient):
        """Test component search with no results."""
        response = client.get("/api/inventory/search?q=nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

    def test_get_component_by_id(self, client: TestClient, sample_component: dict):
        """Test getting component by ID."""
        response = client.get(f"/api/inventory/{sample_component['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_component["id"]
        assert data["type"] == sample_component["type"]
        assert data["value"] == sample_component["value"]

    def test_get_component_not_found(self, client: TestClient):
        """Test getting non-existent component."""
        response = client.get("/api/inventory/nonexistent")
        assert response.status_code == 404

    def test_get_low_stock(self, client: TestClient, sample_component: dict):
        """Test getting low stock components."""
        response = client.get("/api/inventory/low-stock")
        assert response.status_code == 200
        data = response.json()
        # Sample component has 50 units with min 10, so not low stock
        assert data["total"] == 0

    def test_get_statistics(self, client: TestClient, sample_component: dict):
        """Test inventory statistics."""
        response = client.get("/api/inventory/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_types"] == 1
        assert data["total_units"] == 50
        assert "by_type" in data

    def test_update_quantity(self, client: TestClient, sample_component: dict):
        """Test updating component quantity."""
        # Add 10 units
        response = client.patch(
            f"/api/inventory/{sample_component['id']}/quantity", json={"delta": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["new_quantity"] == 60

        # Subtract 20 units
        response = client.patch(
            f"/api/inventory/{sample_component['id']}/quantity", json={"delta": -20}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["new_quantity"] == 40


class TestBOMEndpoints:
    """Test BOM management endpoints."""

    def test_get_bom_empty(self, client: TestClient, sample_circuit: dict):
        """Test getting BOM for circuit with no items."""
        response = client.get(f"/api/bom/{sample_circuit['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    def test_get_bom_with_data(self, client: TestClient, sample_circuit: dict, sample_bom: list):
        """Test getting BOM with data."""
        response = client.get(f"/api/bom/{sample_circuit['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_get_bom_by_type(self, client: TestClient, sample_circuit: dict, sample_bom: list):
        """Test getting BOM organized by type."""
        response = client.get(f"/api/bom/{sample_circuit['id']}/by-type")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert "resistor" in data["by_type"]
        assert "capacitor" in data["by_type"]
        assert len(data["by_type"]["resistor"]) == 1
        assert len(data["by_type"]["capacitor"]) == 1

    def test_add_bom_item(self, client: TestClient, sample_circuit: dict):
        """Test adding BOM item."""
        new_item = {
            "component_type": "ic",
            "component_value": "TL072",
            "quantity": 1,
            "reference_designator": "IC1",
            "is_critical": True,
            "confidence_score": 0.92,
        }

        response = client.post(f"/api/bom/{sample_circuit['id']}/items", json=new_item)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # Verify item was added
        response = client.get(f"/api/bom/{sample_circuit['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1

    def test_validate_bom(
        self, client: TestClient, sample_circuit: dict, sample_bom: list, sample_component: dict
    ):
        """Test BOM validation."""
        response = client.get(f"/api/bom/{sample_circuit['id']}/validate")
        assert response.status_code == 200
        data = response.json()
        assert data["total_items"] == 2
        assert "completeness" in data
        assert "matches" in data
        assert "missing" in data

    def test_get_shopping_list(self, client: TestClient, sample_circuit: dict, sample_bom: list):
        """Test getting shopping list."""
        response = client.get(f"/api/bom/{sample_circuit['id']}/shopping-list")
        assert response.status_code == 200
        data = response.json()
        assert "missing_items" in data
        assert "total_missing" in data

    def test_get_bom_stats(self, client: TestClient, sample_circuit: dict, sample_bom: list):
        """Test BOM statistics."""
        response = client.get(f"/api/bom/{sample_circuit['id']}/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_items"] == 2
        assert data["critical_count"] == 1
        assert "by_type" in data

    def test_export_bom_csv(self, client: TestClient, sample_circuit: dict, sample_bom: list):
        """Test BOM CSV export."""
        response = client.get(f"/api/bom/{sample_circuit['id']}/export")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        csv_content = response.text
        assert "Type,Value,Quantity" in csv_content
        assert "10k" in csv_content


class TestImportEndpoints:
    """Test import endpoints."""

    def test_get_format_info(self, client: TestClient):
        """Test getting CSV format information."""
        response = client.get("/api/import/format")
        assert response.status_code == 200
        data = response.json()
        assert "format" in data
        assert "required_columns" in data
        assert "Category" in data["required_columns"]

    def test_download_template(self, client: TestClient):
        """Test downloading CSV template."""
        response = client.get("/api/import/template")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "Category,SubType,HumanReadableValue" in response.text

    def test_import_inventory_preview(self, client: TestClient):
        """Test importing inventory in preview mode."""
        # Create sample CSV
        csv_content = """Category,SubType,HumanReadableValue,NumericBaseValue,UnitType,Footprint,Voltage,Quantity,ReorderLevel,MfrPartNumber,KeyNotes,RelatedPart,Vendor,VendorSKU
RESISTOR,Metal Film,10k,10000,ohm,through-hole,,50,10,,,,,
CAPACITOR,Electrolytic,100uF,0.0001,F,radial,25V,20,5,,,,,
"""

        files = {"file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")}

        response = client.post("/api/import/inventory?preview=true", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["total_components"] == 2
        assert data["inserted"] == 0  # Preview mode
        assert "Preview complete" in data["message"]

    def test_import_inventory_invalid_file(self, client: TestClient):
        """Test importing with invalid file type."""
        files = {"file": ("test.txt", io.BytesIO(b"not a csv"), "text/plain")}

        response = client.post("/api/import/inventory", files=files)
        assert response.status_code == 400
        data = response.json()
        # Check if detail exists and contains the error message
        if "detail" in data and data["detail"]:
            assert "Only CSV files are supported" in data["detail"]
