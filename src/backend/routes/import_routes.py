"""
Import API Routes

REST endpoints for importing inventory from CSV/Excel files.
"""

import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Query
from pydantic import BaseModel

from ..db import Database, get_db
from ..services.excel_importer import InventoryImporter

logger = logging.getLogger(__name__)

router = APIRouter()


# Response models
class ImportPreviewResponse(BaseModel):
    """Import preview response."""

    preview: bool
    total_components: int
    by_type: dict[str, int]
    message: str


class ImportResultResponse(BaseModel):
    """Import result response."""

    success: bool
    total_components: int
    inserted: int
    skipped: int
    by_type: dict[str, int]
    message: str


@router.post("/inventory", response_model=ImportResultResponse)
async def import_inventory(
    file: UploadFile = File(..., description="CSV file with inventory data"),
    preview: bool = Query(False, description="Preview mode - don't write to database"),
    db: Database = Depends(get_db),
):
    """
    Import component inventory from CSV file.

    Expected CSV format (user's 14-column format):
    - Category: Component category (e.g., 'RESISTOR', 'CAPACITOR', 'IC')
    - SubType: Component subtype (optional)
    - HumanReadableValue: Component value (e.g., '10k', '100nF', 'TL072')
    - NumericBaseValue: Numeric value (optional)
    - UnitType: Unit (optional, e.g., 'ohm', 'F')
    - Footprint: Package type (optional, e.g., 'DIP8', 'through-hole')
    - Voltage: Voltage rating (optional, e.g., '16V', '50V')
    - Quantity: Quantity in stock (required)
    - ReorderLevel: Minimum quantity threshold (optional)
    - MfrPartNumber: Manufacturer part number (optional)
    - KeyNotes: Notes (optional)
    - RelatedPart: Related part info (optional)
    - Vendor: Vendor name (optional)
    - VendorSKU: Vendor SKU (optional)

    Args:
        file: CSV file upload
        preview: If True, parse and validate but don't import
        db: Database dependency

    Returns:
        Import results with counts and statistics
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided",
        )

    if not file.filename.endswith((".csv", ".CSV")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are supported",
        )

    # Create temporary file
    try:
        # Read uploaded file
        contents = await file.read()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".csv", delete=False
        ) as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        logger.info(f"Saved uploaded file to temporary location: {temp_path}")

        # Import using InventoryImporter
        with InventoryImporter(str(db.db_path)) as importer:
            result = importer.import_components(temp_path, preview=preview)

        # Clean up temporary file
        Path(temp_path).unlink()

        # Format response
        if preview:
            return ImportResultResponse(
                success=True,
                total_components=result["total_components"],
                inserted=0,
                skipped=0,
                by_type=result["by_type"],
                message="Preview complete - no changes made to database",
            )
        else:
            return ImportResultResponse(
                success=True,
                total_components=result["total_components"],
                inserted=result.get("inserted", 0),
                skipped=result.get("skipped", 0),
                by_type=result["by_type"],
                message=f"Successfully imported {result.get('inserted', 0)} components",
            )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid CSV format: {str(e)}",
        )

    except Exception as e:
        logger.error(f"Import error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}",
        )


@router.get("/template")
async def download_template():
    """
    Download CSV template for inventory import.

    Returns:
        CSV template with example data
    """
    template_content = """Category,SubType,HumanReadableValue,NumericBaseValue,UnitType,Footprint,Voltage,Quantity,ReorderLevel,MfrPartNumber,KeyNotes,RelatedPart,Vendor,VendorSKU
RESISTOR,Metal Film,10k,10000,ohm,through-hole,,50,10,,,,,
CAPACITOR,Electrolytic,100uF,0.0001,F,radial,25V,20,5,,,,,
IC,Op-Amp,TL072,,,DIP8,,10,3,,Dual op-amp low noise,TL071,Mouser,595-TL072CP
DIODE,Germanium,1N34A,,,through-hole,,25,5,,Authentic NOS germanium diode,,,
TRANSISTOR,BJT NPN,2N3904,,,TO-92,,100,20,,,2N2222,,,
"""

    from fastapi.responses import PlainTextResponse

    return PlainTextResponse(
        content=template_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=inventory_template.csv"},
    )


@router.get("/format")
async def get_format_info():
    """
    Get information about CSV format requirements.

    Returns:
        CSV format documentation
    """
    return {
        "format": "CSV",
        "encoding": "UTF-8",
        "required_columns": [
            "Category",
            "HumanReadableValue",
            "Quantity",
        ],
        "optional_columns": [
            "SubType",
            "NumericBaseValue",
            "UnitType",
            "Footprint",
            "Voltage",
            "ReorderLevel",
            "MfrPartNumber",
            "KeyNotes",
            "RelatedPart",
            "Vendor",
            "VendorSKU",
        ],
        "category_values": [
            "RESISTOR",
            "CAPACITOR",
            "IC",
            "TRANSISTOR",
            "DIODE",
            "POTENTIOMETER",
            "SWITCH",
            "LED",
            "JACK",
            "HARDWARE",
        ],
        "example_row": {
            "Category": "RESISTOR",
            "SubType": "Metal Film",
            "HumanReadableValue": "10k",
            "NumericBaseValue": "10000",
            "UnitType": "ohm",
            "Footprint": "through-hole",
            "Voltage": "",
            "Quantity": "50",
            "ReorderLevel": "10",
            "MfrPartNumber": "",
            "KeyNotes": "",
            "RelatedPart": "",
            "Vendor": "",
            "VendorSKU": "",
        },
        "notes": [
            "CSV must be comma-separated",
            "First row must contain column headers",
            "Empty rows will be ignored",
            "Rows with missing required fields will be skipped",
            "Component IDs are auto-generated from type, value, and package",
            "Duplicate components (same ID) will be skipped",
        ],
    }
