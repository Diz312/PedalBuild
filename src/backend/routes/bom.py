"""
BOM (Bill of Materials) API Routes

REST endpoints for BOM management and validation.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from ..db import Database, get_db
from ..services.bom_manager import BOMManagerService

logger = logging.getLogger(__name__)

router = APIRouter()


# Request/Response models
class BOMItemResponse(BaseModel):
    """BOM item response model."""

    id: str
    circuit_id: str
    component_type: str
    component_value: str
    quantity: int
    reference_designator: Optional[str] = None
    substitution_allowed: bool
    substitution_notes: Optional[str] = None
    is_critical: bool
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    confidence_score: float


class BOMResponse(BaseModel):
    """BOM list response."""

    circuit_id: str
    items: list[dict]
    total: int


class BOMByTypeResponse(BaseModel):
    """BOM organized by type response."""

    circuit_id: str
    by_type: dict[str, list[dict]]
    total: int


class ValidationResponse(BaseModel):
    """BOM validation response."""

    total_items: int
    available_count: int
    missing_count: int
    completeness: float
    matches: list[dict]
    missing: list[dict]


class ShoppingListResponse(BaseModel):
    """Shopping list response."""

    missing_items: list[dict]
    total_missing: int


class BOMStatsResponse(BaseModel):
    """BOM statistics response."""

    total_items: int
    by_type: dict[str, int]
    critical_count: int
    low_confidence_count: int


class AddBOMItemRequest(BaseModel):
    """Request to add BOM item."""

    component_type: str
    component_value: str
    quantity: int = Field(gt=0)
    reference_designator: Optional[str] = None
    substitution_allowed: bool = False
    substitution_notes: Optional[str] = None
    is_critical: bool = False
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)


def get_bom_service(db: Database = Depends(get_db)) -> BOMManagerService:
    """Get BOM service instance."""
    return BOMManagerService(str(db.db_path))


@router.get("/{circuit_id}", response_model=BOMResponse)
async def get_bom(
    circuit_id: str,
    service: BOMManagerService = Depends(get_bom_service),
):
    """
    Get BOM for a circuit.

    Args:
        circuit_id: Circuit ID
        service: BOM service dependency

    Returns:
        Complete BOM for the circuit
    """
    try:
        items = service.get_bom(circuit_id)

        if not items:
            # Check if circuit exists by trying to get it
            # For now, just return empty BOM
            logger.warning(f"No BOM items found for circuit: {circuit_id}")

        return BOMResponse(
            circuit_id=circuit_id,
            items=items,
            total=len(items),
        )

    except Exception as e:
        logger.error(f"Error getting BOM: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{circuit_id}/by-type", response_model=BOMByTypeResponse)
async def get_bom_by_type(
    circuit_id: str,
    service: BOMManagerService = Depends(get_bom_service),
):
    """
    Get BOM organized by component type.

    Args:
        circuit_id: Circuit ID
        service: BOM service dependency

    Returns:
        BOM grouped by component type (resistors, capacitors, etc.)
    """
    try:
        by_type = service.get_bom_by_type(circuit_id)
        total = sum(len(items) for items in by_type.values())

        return BOMByTypeResponse(
            circuit_id=circuit_id,
            by_type=by_type,
            total=total,
        )

    except Exception as e:
        logger.error(f"Error getting BOM by type: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/{circuit_id}/items")
async def add_bom_item(
    circuit_id: str,
    request: AddBOMItemRequest,
    service: BOMManagerService = Depends(get_bom_service),
):
    """
    Add item to BOM.

    Args:
        circuit_id: Circuit ID
        request: BOM item to add
        service: BOM service dependency

    Returns:
        Success status
    """
    try:
        item_dict = request.model_dump()
        success = service.add_bom_item(circuit_id, item_dict)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add BOM item",
            )

        return {"success": True, "circuit_id": circuit_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding BOM item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{circuit_id}/validate", response_model=ValidationResponse)
async def validate_bom(
    circuit_id: str,
    service: BOMManagerService = Depends(get_bom_service),
):
    """
    Validate BOM against inventory.

    Checks which components are available in stock and which are missing.

    Args:
        circuit_id: Circuit ID
        service: BOM service dependency

    Returns:
        Validation results with matches and missing components
    """
    try:
        validation = service.validate_bom(circuit_id)
        return ValidationResponse(**validation)

    except Exception as e:
        logger.error(f"Error validating BOM: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{circuit_id}/shopping-list", response_model=ShoppingListResponse)
async def get_shopping_list(
    circuit_id: str,
    service: BOMManagerService = Depends(get_bom_service),
):
    """
    Get shopping list of missing components.

    Returns only components that are not available in inventory.

    Args:
        circuit_id: Circuit ID
        service: BOM service dependency

    Returns:
        List of components to purchase
    """
    try:
        shopping_list = service.get_shopping_list(circuit_id)
        return ShoppingListResponse(**shopping_list)

    except Exception as e:
        logger.error(f"Error getting shopping list: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{circuit_id}/stats", response_model=BOMStatsResponse)
async def get_bom_stats(
    circuit_id: str,
    service: BOMManagerService = Depends(get_bom_service),
):
    """
    Get BOM statistics.

    Args:
        circuit_id: Circuit ID
        service: BOM service dependency

    Returns:
        Statistics including component counts, critical components, and low confidence items
    """
    try:
        stats = service.get_statistics(circuit_id)
        return BOMStatsResponse(**stats)

    except Exception as e:
        logger.error(f"Error getting BOM stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{circuit_id}/export", response_class=PlainTextResponse)
async def export_bom_csv(
    circuit_id: str,
    service: BOMManagerService = Depends(get_bom_service),
):
    """
    Export BOM to CSV format.

    Args:
        circuit_id: Circuit ID
        service: BOM service dependency

    Returns:
        CSV file as plain text
    """
    try:
        csv_content = service.export_bom_csv(circuit_id)

        if not csv_content or csv_content.count("\n") <= 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No BOM found for circuit: {circuit_id}",
            )

        return PlainTextResponse(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=bom_{circuit_id}.csv"
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting BOM: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
