"""
PedalBuild Type Definitions
Complete type system for the application using Pydantic
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# ENUMS
# ============================================================================

class ComponentType(str, Enum):
    """Electronic component types"""
    RESISTOR = "resistor"
    CAPACITOR = "capacitor"
    IC = "ic"
    TRANSISTOR = "transistor"
    DIODE = "diode"
    POTENTIOMETER = "potentiometer"
    SWITCH = "switch"
    LED = "led"
    JACK = "jack"
    HARDWARE = "hardware"
    OTHER = "other"


class PedalCategory(str, Enum):
    """Pedal effect categories"""
    OVERDRIVE = "overdrive"
    DISTORTION = "distortion"
    FUZZ = "fuzz"
    DELAY = "delay"
    REVERB = "reverb"
    MODULATION = "modulation"
    FILTER = "filter"
    COMPRESSOR = "compressor"
    BOOST = "boost"
    OTHER = "other"


class DifficultyLevel(str, Enum):
    """Build difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class WorkflowStage(str, Enum):
    """10-stage workflow"""
    INSPIRATION = "inspiration"
    SPEC_DOWNLOAD = "spec_download"
    SCHEMATIC_ANALYSIS = "schematic_analysis"
    INVENTORY_CHECK = "inventory_check"
    BOM_GENERATION = "bom_generation"
    BREADBOARD_LAYOUT = "breadboard_layout"
    PROTOTYPE_TESTING = "prototype_testing"
    FINAL_ASSEMBLY = "final_assembly"
    GRAPHICS_DESIGN = "graphics_design"
    SHOWCASE = "showcase"


class ProjectStatus(str, Enum):
    """Project status"""
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class StageStatus(str, Enum):
    """Individual stage status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


# ============================================================================
# PEDALPCB CATALOG
# ============================================================================

class PedalPCBCatalogItem(BaseModel):
    """Pedal from PedalPCB.com catalog"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    url: str
    name: str
    category: PedalCategory
    description: Optional[str] = None
    original_pedal: Optional[str] = None  # e.g., "Ibanez TS808"
    difficulty_level: Optional[DifficultyLevel] = None
    price: Optional[float] = None
    build_doc_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    images_json: Optional[str] = None  # JSON array
    specifications_json: Optional[str] = None  # JSON object
    last_scraped: datetime
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class PedalPCBReview(BaseModel):
    """User review from PedalPCB.com"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    pedal_id: str
    author: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = None
    comment: str
    helpful_count: int = 0
    reply_count: int = 0
    posted_date: Optional[datetime] = None
    source_url: Optional[str] = None
    scraped_at: datetime


class ScrapingJob(BaseModel):
    """Scraping job tracking"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    job_type: Literal["catalog", "reviews", "build_docs"]
    status: Literal["pending", "running", "completed", "failed"]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    items_processed: int = 0
    items_failed: int = 0
    error_log: Optional[str] = None
    created_at: datetime


# ============================================================================
# COMPONENTS & INVENTORY
# ============================================================================

class Component(BaseModel):
    """Electronic component in inventory"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: ComponentType
    name: str
    value: Optional[str] = None  # e.g., "10k", "100nF", "TL072"
    tolerance: Optional[str] = None  # e.g., "5%", "10%"
    package: Optional[str] = None  # e.g., "DIP-8", "Axial 1/4W"
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    datasheet_url: Optional[str] = None
    quantity_in_stock: int = Field(default=0, ge=0)
    minimum_quantity: int = Field(default=0, ge=0)
    unit_price: Optional[float] = Field(None, ge=0)
    location: Optional[str] = None
    voltage: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ============================================================================
# CIRCUITS
# ============================================================================

class Circuit(BaseModel):
    """Circuit specification"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: Optional[str] = None
    category: PedalCategory
    difficulty_level: Optional[DifficultyLevel] = None
    source_url: Optional[str] = None
    pedalpcb_catalog_id: Optional[str] = None
    schematic_image_path: Optional[str] = None
    schematic_pdf_path: Optional[str] = None
    voltage_requirement: Optional[str] = None
    current_draw_ma: Optional[int] = None
    enclosure_size: Optional[str] = None
    estimated_build_time_hours: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CircuitBOMItem(BaseModel):
    """BOM item for a circuit"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    circuit_id: str
    component_type: ComponentType
    component_value: str
    quantity: int = Field(ge=1)
    reference_designator: Optional[str] = None  # "R1", "C2", "IC1"
    substitution_allowed: bool = False
    substitution_notes: Optional[str] = None
    is_critical: bool = False  # Affects tone significantly
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    confidence_score: float = Field(default=1.0, ge=0, le=1)


# ============================================================================
# PROJECTS & WORKFLOW
# ============================================================================

class Project(BaseModel):
    """User build project"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    circuit_id: str
    name: str
    current_stage: WorkflowStage
    status: ProjectStatus
    breadboard_platform: str = "dual_board_custom"
    enclosure_id: Optional[str] = None
    color_scheme: Optional[str] = None  # JSON
    notes: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    updated_at: datetime


class ProjectStage(BaseModel):
    """Individual workflow stage for a project"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    stage: WorkflowStage
    status: StageStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    data: Optional[str] = None  # JSON - stage-specific data
    notes: Optional[str] = None


# ============================================================================
# STAGE DATA (for JSON storage)
# ============================================================================

class InspirationData(BaseModel):
    """Data for inspiration stage"""
    type: Literal["inspiration"] = "inspiration"
    selected_pedal_ids: List[str]
    search_criteria: Optional[str] = None
    notes: Optional[str] = None


class SpecDownloadData(BaseModel):
    """Data for spec download stage"""
    type: Literal["spec_download"] = "spec_download"
    source_url: str
    pdf_path: Optional[str] = None
    extraction_method: Literal["manual", "ocr", "pdf_parse"]
    extracted_bom: Optional[List[Dict[str, Any]]] = None
    schematic_images: Optional[List[str]] = None


class SchematicComponent(BaseModel):
    """Component extracted from schematic"""
    id: str
    type: ComponentType
    value: str
    reference_designator: str
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    orientation: Literal["horizontal", "vertical"]
    confidence: float = Field(ge=0, le=1)


class SchematicConnection(BaseModel):
    """Connection between components"""
    from_component: str
    from_pin: str
    to_component: str
    to_pin: str
    confidence: float = Field(ge=0, le=1)


class SchematicAnalysisData(BaseModel):
    """Data for schematic analysis stage"""
    type: Literal["schematic_analysis"] = "schematic_analysis"
    schematic_path: str
    analysis_passes: int
    components: List[SchematicComponent]
    connections: List[SchematicConnection]
    low_confidence_components: List[str]
    analysis_notes: Optional[str] = None


class ComponentMatch(BaseModel):
    """Inventory match result"""
    bom_item_id: str
    component_id: str
    quantity_needed: int
    quantity_available: int
    is_exact_match: bool


class MissingComponent(BaseModel):
    """Missing component from inventory"""
    bom_item_id: str
    component_type: ComponentType
    component_value: str
    quantity_needed: int
    estimated_price: Optional[float] = None
    suggested_vendors: Optional[List[str]] = None


class SubstitutionSuggestion(BaseModel):
    """Component substitution suggestion"""
    bom_item_id: str
    original_value: str
    substitute_component_id: str
    substitute_value: str
    reason: str
    impact_on_tone: Literal["none", "minimal", "moderate", "significant"]


class InventoryCheckData(BaseModel):
    """Data for inventory check stage"""
    type: Literal["inventory_check"] = "inventory_check"
    matches: List[ComponentMatch]
    missing_components: List[MissingComponent]
    substitution_suggestions: List[SubstitutionSuggestion]
    completeness: float = Field(ge=0, le=1)


class BOMItem(BaseModel):
    """BOM item for generation stage"""
    component_type: ComponentType
    component_value: str
    quantity: int
    reference_designators: List[str]
    in_stock: bool
    notes: Optional[str] = None


class BOMGenerationData(BaseModel):
    """Data for BOM generation stage"""
    type: Literal["bom_generation"] = "bom_generation"
    items: List[BOMItem]
    organized_by_type: Dict[str, List[BOMItem]]
    total_items: int
    generated_at: datetime


class BreadboardComponent(BaseModel):
    """Component placement on breadboard"""
    bom_item_id: str
    component_id: str
    reference_designator: str
    board: Literal[1, 2]
    row: int = Field(ge=0, le=9)  # a-j (0-9)
    column: int = Field(ge=1, le=63)
    orientation: Literal["horizontal", "vertical"]
    span: int  # Number of holes


class BreadboardConnection(BaseModel):
    """Wire connection on breadboard"""
    from_component: str
    from_pin: int
    to_component: str
    to_pin: int
    wire_color: Optional[str] = None
    board_crossing: bool = False


class PowerRailConfig(BaseModel):
    """Power rail configuration"""
    voltage: float
    jumper_connections: Dict[str, bool]
    potentiometer_slots: List[Dict[str, Any]]


class BreadboardLayoutData(BaseModel):
    """Data for breadboard layout stage"""
    type: Literal["breadboard_layout"] = "breadboard_layout"
    layout_id: str
    platform: str
    components: List[BreadboardComponent]
    connections: List[BreadboardConnection]
    power_config: PowerRailConfig
    fritzing_path: Optional[str] = None
    png_path: Optional[str] = None
    layout_notes: Optional[str] = None


class TestResult(BaseModel):
    """Test result"""
    test_id: str
    test_type: Literal["power", "audio", "signal_flow", "tone"]
    passed: bool
    timestamp: datetime
    notes: str


class AudioSample(BaseModel):
    """Audio sample recording"""
    id: str
    file_path: str
    description: str
    settings: Dict[str, float]
    timestamp: datetime


class Measurement(BaseModel):
    """Measurement result"""
    measurement_type: str
    location: str
    expected_value: str
    actual_value: str
    within_tolerance: bool


class Issue(BaseModel):
    """Build issue"""
    id: str
    severity: Literal["critical", "major", "minor"]
    description: str
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None


class PrototypeTestingData(BaseModel):
    """Data for prototype testing stage"""
    type: Literal["prototype_testing"] = "prototype_testing"
    test_results: List[TestResult]
    audio_samples: List[AudioSample]
    measurements: List[Measurement]
    issues: List[Issue]
    is_fully_functional: bool


class AssemblyStep(BaseModel):
    """Assembly step"""
    step_number: int
    description: str
    completed: bool
    photo_path: Optional[str] = None
    notes: Optional[str] = None


class FinalAssemblyData(BaseModel):
    """Data for final assembly stage"""
    type: Literal["final_assembly"] = "final_assembly"
    enclosure_id: str
    drill_template: Optional[str] = None
    assembly_steps: List[AssemblyStep]
    completion_photos: List[str]
    final_test_passed: bool


class DrillHole(BaseModel):
    """Drill hole specification"""
    x: float
    y: float
    diameter: float
    purpose: Literal["potentiometer", "switch", "led", "jack", "dc", "other"]
    label: Optional[str] = None


class EnclosureDimensions(BaseModel):
    """Enclosure dimensions"""
    width: float
    height: float
    depth: float
    unit: Literal["mm", "inches"]


class ColorScheme(BaseModel):
    """Color scheme for graphics"""
    base_color: str
    text_color: str
    accent_color: Optional[str] = None
    finish: Optional[Literal["matte", "glossy", "textured"]] = None


class GraphicsDesignData(BaseModel):
    """Data for graphics design stage"""
    type: Literal["graphics_design"] = "graphics_design"
    design_id: str
    design_file_path: str
    preview_image_path: str
    drill_holes: List[DrillHole]
    dimensions: EnclosureDimensions
    color_scheme: ColorScheme
    is_final: bool


class ShowcaseImage(BaseModel):
    """Showcase image"""
    id: str
    path: str
    caption: Optional[str] = None
    display_order: int


class ShowcaseData(BaseModel):
    """Data for showcase stage"""
    type: Literal["showcase"] = "showcase"
    post_id: str
    title: str
    description: str
    images: List[ShowcaseImage]
    published_at: datetime
    visibility: Literal["public", "private", "unlisted"]


# ============================================================================
# ENCLOSURES
# ============================================================================

class Enclosure(BaseModel):
    """Enclosure inventory item"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    size: str  # '1590A', '1590B', '125B', etc.
    width_mm: float
    height_mm: float
    depth_mm: float
    material: Optional[str] = None
    color: Optional[str] = None
    manufacturer: Optional[str] = None
    quantity_in_stock: int = Field(default=0, ge=0)
    created_at: datetime


# ============================================================================
# USER PROFILES
# ============================================================================

class UIPreferences(BaseModel):
    """UI preferences"""
    embedded_view_mode: Literal["always", "toggle", "separate_tab"]
    theme: Literal["light", "dark"]
    compact_mode: bool


class UserProfile(BaseModel):
    """User profile"""
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    display_name: Optional[str] = None
    skill_level: DifficultyLevel
    preferred_breadboard: str = "dual_board_custom"
    preferred_vendors: Optional[str] = None  # JSON array
    ui_preferences: Optional[UIPreferences] = None
    notification_preferences: Optional[str] = None  # JSON
    created_at: datetime
    updated_at: datetime


# ============================================================================
# AGENT STATE
# ============================================================================

class AgentState(BaseModel):
    """Agent state storage"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    scope: Literal["session", "user", "global"]
    key: str
    value: str  # JSON serialized
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class WorkflowLog(BaseModel):
    """Workflow execution log"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: Optional[str] = None
    agent_name: str
    stage: WorkflowStage
    status: Literal["started", "completed", "failed"]
    input: Optional[str] = None  # JSON
    output: Optional[str] = None  # JSON
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    created_at: datetime


# ============================================================================
# API TYPES
# ============================================================================

class APIResponse(BaseModel):
    """Generic API response"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    warnings: Optional[List[str]] = None


class PaginatedResponse(BaseModel):
    """Paginated response"""
    items: List[Any]
    total: int
    page: int
    page_size: int
    has_next: bool


class WorkflowProgress(BaseModel):
    """Workflow progress"""
    project_id: str
    current_stage: WorkflowStage
    completed_stages: List[WorkflowStage]
    active_agent: Optional[str] = None
    progress_percent: float = Field(ge=0, le=100)
    estimated_time_remaining: Optional[int] = None  # seconds


class AgentUpdate(BaseModel):
    """Agent update message"""
    type: Literal["started", "progress", "completed", "error"]
    agent_name: str
    stage: WorkflowStage
    progress: Optional[float] = Field(None, ge=0, le=100)
    message: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
