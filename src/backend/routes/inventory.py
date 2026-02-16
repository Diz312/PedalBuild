"""
Component Inventory API Routes

REST endpoints for component inventory management.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from ..db import Database, get_db, DatabaseError
from ..services.component_inventory import ComponentInventoryService

logger = logging.getLogger(__name__)

router = APIRouter()


# Request/Response models
class ComponentResponse(BaseModel):
    """Component response model."""

    id: str
    type: str
    name: str
    value: Optional[str] = None
    tolerance: Optional[str] = None
    package: Optional[str] = None
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    datasheet_url: Optional[str] = None
    quantity_in_stock: int
    minimum_quantity: int
    unit_price: Optional[float] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    updated_at: str


class ComponentListResponse(BaseModel):
    """List of components response."""

    components: list[dict]
    total: int


class InventoryStatsResponse(BaseModel):
    """Inventory statistics response."""

    total_types: int
    total_units: int
    low_stock_count: int
    out_of_stock_count: int
    by_type: dict[str, dict]


class UpdateQuantityRequest(BaseModel):
    """Request to update component quantity."""

    delta: int = Field(..., description="Quantity change (positive to add, negative to subtract)")


class UpdateQuantityResponse(BaseModel):
    """Response for quantity update."""

    success: bool
    component_id: str
    new_quantity: int


def get_inventory_service(db: Database = Depends(get_db)) -> ComponentInventoryService:
    """Get inventory service instance."""
    return ComponentInventoryService(str(db.db_path))


@router.get("/", response_model=ComponentListResponse)
async def list_components(
    type: Optional[str] = Query(None, description="Filter by component type"),
    service: ComponentInventoryService = Depends(get_inventory_service),
):
    """
    List all components with optional type filter.

    Args:
        type: Component type filter (resistor, capacitor, ic, etc.)
        service: Inventory service dependency

    Returns:
        List of components
    """
    try:
        from ...models.types import ComponentType

        comp_type = None
        if type:
            try:
                comp_type = ComponentType(type)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid component type: {type}",
                )

        components = service.list_components(comp_type)

        return ComponentListResponse(
            components=components,
            total=len(components),
        )

    except Exception as e:
        logger.error(f"Error listing components: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/search", response_model=ComponentListResponse)
async def search_components(
    q: str = Query(..., min_length=1, description="Search query"),
    service: ComponentInventoryService = Depends(get_inventory_service),
):
    """
    Search components by value, name, or part number.

    Args:
        q: Search query string
        service: Inventory service dependency

    Returns:
        Matching components
    """
    try:
        components = service.search_components(q)

        return ComponentListResponse(
            components=components,
            total=len(components),
        )

    except Exception as e:
        logger.error(f"Error searching components: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/low-stock", response_model=ComponentListResponse)
async def get_low_stock(
    service: ComponentInventoryService = Depends(get_inventory_service),
):
    """
    Get components with low stock.

    Returns:
        Components where quantity_in_stock <= minimum_quantity
    """
    try:
        components = service.get_low_stock()

        return ComponentListResponse(
            components=components,
            total=len(components),
        )

    except Exception as e:
        logger.error(f"Error getting low stock: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/stats", response_model=InventoryStatsResponse)
async def get_statistics(
    service: ComponentInventoryService = Depends(get_inventory_service),
):
    """
    Get inventory statistics.

    Returns:
        Statistics grouped by component type
    """
    try:
        stats = service.get_statistics()
        return InventoryStatsResponse(**stats)

    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{component_id}", response_model=ComponentResponse)
async def get_component(
    component_id: str,
    service: ComponentInventoryService = Depends(get_inventory_service),
):
    """
    Get component by ID.

    Args:
        component_id: Component ID
        service: Inventory service dependency

    Returns:
        Component details
    """
    try:
        component = service.get_component(component_id)

        if not component:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Component not found: {component_id}",
            )

        return ComponentResponse(**component)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting component: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/{component_id}/quantity", response_model=UpdateQuantityResponse)
async def update_quantity(
    component_id: str,
    request: UpdateQuantityRequest,
    service: ComponentInventoryService = Depends(get_inventory_service),
):
    """
    Update component quantity.

    Args:
        component_id: Component ID
        request: Quantity update request (delta can be positive or negative)
        service: Inventory service dependency

    Returns:
        Update result with new quantity
    """
    try:
        # First check if component exists
        component = service.get_component(component_id)
        if not component:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Component not found: {component_id}",
            )

        # Update quantity
        success = service.update_quantity(component_id, request.delta)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update quantity",
            )

        # Get updated component
        updated_component = service.get_component(component_id)

        return UpdateQuantityResponse(
            success=True,
            component_id=component_id,
            new_quantity=updated_component["quantity_in_stock"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating quantity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
