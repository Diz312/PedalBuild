/**
 * PedalBuild Type Definitions
 * AUTO-GENERATED from Python Pydantic models
 * DO NOT EDIT MANUALLY - Run: npm run generate:types
 */

// ============================================================================
// ENUMS
// ============================================================================

export enum ComponentType {
  RESISTOR = "resistor",
  CAPACITOR = "capacitor",
  IC = "ic",
  TRANSISTOR = "transistor",
  DIODE = "diode",
  POTENTIOMETER = "potentiometer",
  SWITCH = "switch",
  LED = "led",
  JACK = "jack",
  HARDWARE = "hardware",
  OTHER = "other",
}

export enum PedalCategory {
  OVERDRIVE = "overdrive",
  DISTORTION = "distortion",
  FUZZ = "fuzz",
  DELAY = "delay",
  REVERB = "reverb",
  MODULATION = "modulation",
  FILTER = "filter",
  COMPRESSOR = "compressor",
  BOOST = "boost",
  OTHER = "other",
}

export enum DifficultyLevel {
  BEGINNER = "beginner",
  INTERMEDIATE = "intermediate",
  ADVANCED = "advanced",
}

export enum WorkflowStage {
  INSPIRATION = "inspiration",
  SPEC_DOWNLOAD = "spec_download",
  SCHEMATIC_ANALYSIS = "schematic_analysis",
  INVENTORY_CHECK = "inventory_check",
  BOM_GENERATION = "bom_generation",
  BREADBOARD_LAYOUT = "breadboard_layout",
  PROTOTYPE_TESTING = "prototype_testing",
  FINAL_ASSEMBLY = "final_assembly",
  GRAPHICS_DESIGN = "graphics_design",
  SHOWCASE = "showcase",
}

export enum ProjectStatus {
  ACTIVE = "active",
  ON_HOLD = "on_hold",
  COMPLETED = "completed",
  ABANDONED = "abandoned",
}

export enum StageStatus {
  PENDING = "pending",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
  SKIPPED = "skipped",
  BLOCKED = "blocked",
}

// ============================================================================
// INTERFACES
// ============================================================================

export interface APIResponse {
  success: boolean;
  data?: any;
  error?: any;
  warnings?: any;
}

export interface AgentState {
  id: string;
  scope: "session" | "user" | "global";
  key: string;
  value: string;
  expires_at?: any;
  created_at: Date;
  updated_at: Date;
}

export interface AgentUpdate {
  type: "started" | "progress" | "completed" | "error";
  agent_name: string;
  stage: WorkflowStage;
  progress?: any;
  message?: any;
  result?: any;
  error?: any;
}

export interface AssemblyStep {
  step_number: number;
  description: string;
  completed: boolean;
  photo_path?: any;
  notes?: any;
}

export interface AudioSample {
  id: string;
  file_path: string;
  description: string;
  settings: Record<string, number>;
  timestamp: Date;
}

export interface BOMGenerationData {
  type?: "bom_generation";
  items: Array<BOMItem>;
  organized_by_type: Record<string, Array<BOMItem>>;
  total_items: number;
  generated_at: Date;
}

export interface BOMItem {
  component_type: ComponentType;
  component_value: string;
  quantity: number;
  reference_designators: Array<string>;
  in_stock: boolean;
  notes?: any;
}

export interface BaseModel {
}

export interface BreadboardComponent {
  bom_item_id: string;
  component_id: string;
  reference_designator: string;
  board: 1 | 2;
  row: number;
  column: number;
  orientation: "horizontal" | "vertical";
  span: number;
}

export interface BreadboardConnection {
  from_component: string;
  from_pin: number;
  to_component: string;
  to_pin: number;
  wire_color?: any;
  board_crossing?: boolean;
}

export interface BreadboardLayoutData {
  type?: "breadboard_layout";
  layout_id: string;
  platform: string;
  components: Array<BreadboardComponent>;
  connections: Array<BreadboardConnection>;
  power_config: PowerRailConfig;
  fritzing_path?: any;
  png_path?: any;
  layout_notes?: any;
}

export interface Circuit {
  id: string;
  name: string;
  description?: any;
  category: PedalCategory;
  difficulty_level?: any;
  source_url?: any;
  pedalpcb_catalog_id?: any;
  schematic_image_path?: any;
  schematic_pdf_path?: any;
  voltage_requirement?: any;
  current_draw_ma?: any;
  enclosure_size?: any;
  estimated_build_time_hours?: any;
  notes?: any;
  created_at: Date;
  updated_at: Date;
}

export interface CircuitBOMItem {
  id: string;
  circuit_id: string;
  component_type: ComponentType;
  component_value: string;
  quantity: number;
  reference_designator?: any;
  substitution_allowed?: boolean;
  substitution_notes?: any;
  is_critical?: boolean;
  position_x?: any;
  position_y?: any;
  confidence_score?: number;
}

export interface ColorScheme {
  base_color: string;
  text_color: string;
  accent_color?: any;
  finish?: any;
}

export interface Component {
  id: string;
  type: ComponentType;
  name: string;
  sub_type?: any;
  value?: any;
  tolerance?: any;
  package?: any;
  manufacturer?: any;
  part_number?: any;
  datasheet_url?: any;
  quantity_in_stock?: number;
  minimum_quantity?: number;
  unit_price?: any;
  location?: any;
  voltage?: any;
  alternatives_json?: any;
  notes?: any;
  created_at: Date;
  updated_at: Date;
}

export interface ComponentMatch {
  bom_item_id: string;
  component_id: string;
  quantity_needed: number;
  quantity_available: number;
  is_exact_match: boolean;
}

export interface DrillHole {
  x: number;
  y: number;
  diameter: number;
  purpose: "potentiometer" | "switch" | "led" | "jack" | "dc" | "other";
  label?: any;
}

export interface Enclosure {
  id: string;
  name: string;
  size: string;
  width_mm: number;
  height_mm: number;
  depth_mm: number;
  material?: any;
  color?: any;
  manufacturer?: any;
  quantity_in_stock?: number;
  created_at: Date;
}

export interface EnclosureDimensions {
  width: number;
  height: number;
  depth: number;
  unit: "mm" | "inches";
}

export interface FinalAssemblyData {
  type?: "final_assembly";
  enclosure_id: string;
  drill_template?: any;
  assembly_steps: Array<AssemblyStep>;
  completion_photos: Array<string>;
  final_test_passed: boolean;
}

export interface GraphicsDesignData {
  type?: "graphics_design";
  design_id: string;
  design_file_path: string;
  preview_image_path: string;
  drill_holes: Array<DrillHole>;
  dimensions: EnclosureDimensions;
  color_scheme: ColorScheme;
  is_final: boolean;
}

export interface InspirationData {
  type?: "inspiration";
  selected_pedal_ids: Array<string>;
  search_criteria?: any;
  notes?: any;
}

export interface InventoryCheckData {
  type?: "inventory_check";
  matches: Array<ComponentMatch>;
  missing_components: Array<MissingComponent>;
  substitution_suggestions: Array<SubstitutionSuggestion>;
  completeness: number;
}

export interface Issue {
  id: string;
  severity: "critical" | "major" | "minor";
  description: string;
  resolution?: any;
  resolved_at?: any;
}

export interface Measurement {
  measurement_type: string;
  location: string;
  expected_value: string;
  actual_value: string;
  within_tolerance: boolean;
}

export interface MissingComponent {
  bom_item_id: string;
  component_type: ComponentType;
  component_value: string;
  quantity_needed: number;
  estimated_price?: any;
  suggested_vendors?: any;
}

export interface PaginatedResponse {
  items: Array<Any>;
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
}

export interface PedalPCBCatalogItem {
  id: string;
  url: string;
  name: string;
  category: PedalCategory;
  description?: any;
  original_pedal?: any;
  difficulty_level?: any;
  price?: any;
  build_doc_url?: any;
  thumbnail_url?: any;
  images_json?: any;
  specifications_json?: any;
  last_scraped: Date;
  is_active?: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface PedalPCBReview {
  id: string;
  pedal_id: string;
  author?: any;
  rating?: any;
  title?: any;
  comment: string;
  helpful_count?: number;
  reply_count?: number;
  posted_date?: any;
  source_url?: any;
  scraped_at: Date;
}

export interface PowerRailConfig {
  voltage: number;
  jumper_connections: Record<string, boolean>;
  potentiometer_slots: Array<Record<string, Any>>;
}

export interface Project {
  id: string;
  user_id: string;
  circuit_id: string;
  name: string;
  current_stage: WorkflowStage;
  status: ProjectStatus;
  breadboard_platform?: string;
  enclosure_id?: any;
  color_scheme?: any;
  notes?: any;
  started_at: Date;
  completed_at?: any;
  updated_at: Date;
}

export interface ProjectStage {
  id: string;
  project_id: string;
  stage: WorkflowStage;
  status: StageStatus;
  started_at?: any;
  completed_at?: any;
  data?: any;
  notes?: any;
}

export interface PrototypeTestingData {
  type?: "prototype_testing";
  test_results: Array<TestResult>;
  audio_samples: Array<AudioSample>;
  measurements: Array<Measurement>;
  issues: Array<Issue>;
  is_fully_functional: boolean;
}

export interface SchematicAnalysisData {
  type?: "schematic_analysis";
  schematic_path: string;
  analysis_passes: number;
  components: Array<SchematicComponent>;
  connections: Array<SchematicConnection>;
  low_confidence_components: Array<string>;
  analysis_notes?: any;
}

export interface SchematicComponent {
  id: string;
  type: ComponentType;
  value: string;
  reference_designator: string;
  position_x?: any;
  position_y?: any;
  orientation: "horizontal" | "vertical";
  confidence: number;
}

export interface SchematicConnection {
  from_component: string;
  from_pin: string;
  to_component: string;
  to_pin: string;
  confidence: number;
}

export interface ScrapingJob {
  id: string;
  job_type: "catalog" | "reviews" | "build_docs";
  status: "pending" | "running" | "completed" | "failed";
  started_at?: any;
  completed_at?: any;
  items_processed?: number;
  items_failed?: number;
  error_log?: any;
  created_at: Date;
}

export interface ShowcaseData {
  type?: "showcase";
  post_id: string;
  title: string;
  description: string;
  images: Array<ShowcaseImage>;
  published_at: Date;
  visibility: "public" | "private" | "unlisted";
}

export interface ShowcaseImage {
  id: string;
  path: string;
  caption?: any;
  display_order: number;
}

export interface SpecDownloadData {
  type?: "spec_download";
  source_url: string;
  pdf_path?: any;
  extraction_method: "manual" | "ocr" | "pdf_parse";
  extracted_bom?: any;
  schematic_images?: any;
}

export interface SubstitutionSuggestion {
  bom_item_id: string;
  original_value: string;
  substitute_component_id: string;
  substitute_value: string;
  reason: string;
  impact_on_tone: "none" | "minimal" | "moderate" | "significant";
}

export interface TestResult {
  test_id: string;
  test_type: "power" | "audio" | "signal_flow" | "tone";
  passed: boolean;
  timestamp: Date;
  notes: string;
}

export interface UIPreferences {
  embedded_view_mode: "always" | "toggle" | "separate_tab";
  theme: "light" | "dark";
  compact_mode: boolean;
}

export interface UserProfile {
  user_id: string;
  display_name?: any;
  skill_level: DifficultyLevel;
  preferred_breadboard?: string;
  preferred_vendors?: any;
  ui_preferences?: any;
  notification_preferences?: any;
  created_at: Date;
  updated_at: Date;
}

export interface WorkflowLog {
  id: string;
  project_id?: any;
  agent_name: string;
  stage: WorkflowStage;
  status: "started" | "completed" | "failed";
  input?: any;
  output?: any;
  error?: any;
  duration_ms?: any;
  created_at: Date;
}

export interface WorkflowProgress {
  project_id: string;
  current_stage: WorkflowStage;
  completed_stages: Array<WorkflowStage>;
  active_agent?: any;
  progress_percent: number;
  estimated_time_remaining?: any;
}

// ============================================================================
// UNION TYPES
// ============================================================================

export type StageData =
  | InspirationData
  | SpecDownloadData
  | SchematicAnalysisData
  | InventoryCheckData
  | BOMGenerationData
  | BreadboardLayoutData
  | PrototypeTestingData
  | FinalAssemblyData
  | GraphicsDesignData
  | ShowcaseData;
