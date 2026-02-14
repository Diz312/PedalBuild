/**
 * PedalBuild Type Definitions
 * Complete type system for the application
 */

// ============================================================================
// ENUMS
// ============================================================================

export enum ComponentType {
  RESISTOR = 'resistor',
  CAPACITOR = 'capacitor',
  IC = 'ic',
  TRANSISTOR = 'transistor',
  DIODE = 'diode',
  POTENTIOMETER = 'potentiometer',
  SWITCH = 'switch',
  LED = 'led',
  JACK = 'jack',
  HARDWARE = 'hardware',
  OTHER = 'other'
}

export enum PedalCategory {
  OVERDRIVE = 'overdrive',
  DISTORTION = 'distortion',
  FUZZ = 'fuzz',
  DELAY = 'delay',
  REVERB = 'reverb',
  MODULATION = 'modulation',
  FILTER = 'filter',
  COMPRESSOR = 'compressor',
  BOOST = 'boost',
  OTHER = 'other'
}

export enum DifficultyLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced'
}

export enum WorkflowStage {
  INSPIRATION = 'inspiration',
  SPEC_DOWNLOAD = 'spec_download',
  SCHEMATIC_ANALYSIS = 'schematic_analysis',
  INVENTORY_CHECK = 'inventory_check',
  BOM_GENERATION = 'bom_generation',
  BREADBOARD_LAYOUT = 'breadboard_layout',
  PROTOTYPE_TESTING = 'prototype_testing',
  FINAL_ASSEMBLY = 'final_assembly',
  GRAPHICS_DESIGN = 'graphics_design',
  SHOWCASE = 'showcase'
}

export enum ProjectStatus {
  ACTIVE = 'active',
  ON_HOLD = 'on_hold',
  COMPLETED = 'completed',
  ABANDONED = 'abandoned'
}

export enum StageStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  SKIPPED = 'skipped',
  BLOCKED = 'blocked'
}

// ============================================================================
// PEDALPCB CATALOG (NEW - for embedded content)
// ============================================================================

export interface PedalPCBCatalogItem {
  id: string;
  url: string;
  name: string;
  category: PedalCategory;
  description?: string;
  original_pedal?: string; // e.g., "Ibanez TS808"
  difficulty_level?: DifficultyLevel;
  price?: number;
  build_doc_url?: string;
  thumbnail_url?: string;
  images_json?: string; // JSON array
  specifications_json?: string; // JSON object
  last_scraped: Date;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface PedalPCBReview {
  id: string;
  pedal_id: string;
  author?: string;
  rating?: number; // 1-5
  title?: string;
  comment: string;
  helpful_count: number;
  reply_count: number;
  posted_date?: Date;
  source_url?: string;
  scraped_at: Date;
}

export interface ScrapingJob {
  id: string;
  job_type: 'catalog' | 'reviews' | 'build_docs';
  status: 'pending' | 'running' | 'completed' | 'failed';
  started_at?: Date;
  completed_at?: Date;
  items_processed: number;
  items_failed: number;
  error_log?: string;
  created_at: Date;
}

// ============================================================================
// COMPONENTS & INVENTORY
// ============================================================================

export interface Component {
  id: string;
  type: ComponentType;
  name: string;
  value?: string; // e.g., "10k", "100nF", "TL072"
  tolerance?: string; // e.g., "5%", "10%"
  package?: string; // e.g., "DIP-8", "Axial 1/4W"
  manufacturer?: string;
  part_number?: string;
  datasheet_url?: string;
  quantity_in_stock: number;
  minimum_quantity: number;
  unit_price?: number;
  location?: string; // Storage location
  voltage?: string; // NEW - from user's CSV
  notes?: string;
  created_at: Date;
  updated_at: Date;
}

// ============================================================================
// CIRCUITS
// ============================================================================

export interface Circuit {
  id: string;
  name: string;
  description?: string;
  category: PedalCategory;
  difficulty_level?: DifficultyLevel;
  source_url?: string;
  pedalpcb_catalog_id?: string; // Link to PedalPCB catalog
  schematic_image_path?: string;
  schematic_pdf_path?: string;
  voltage_requirement?: string;
  current_draw_ma?: number;
  enclosure_size?: string;
  estimated_build_time_hours?: number;
  notes?: string;
  created_at: Date;
  updated_at: Date;
}

export interface CircuitBOMItem {
  id: string;
  circuit_id: string;
  component_type: ComponentType;
  component_value: string;
  quantity: number;
  reference_designator?: string; // R1, C2, IC1, etc.
  substitution_allowed: boolean;
  substitution_notes?: string;
  is_critical: boolean; // Affects tone significantly
  position_x?: number; // Schematic position
  position_y?: number;
  confidence_score: number; // From schematic analysis (0-1)
}

// ============================================================================
// PROJECTS & WORKFLOW
// ============================================================================

export interface Project {
  id: string;
  user_id: string;
  circuit_id: string;
  name: string;
  current_stage: WorkflowStage;
  status: ProjectStatus;
  breadboard_platform: string;
  enclosure_id?: string;
  color_scheme?: string; // JSON
  notes?: string;
  started_at: Date;
  completed_at?: Date;
  updated_at: Date;
}

export interface ProjectStage {
  id: string;
  project_id: string;
  stage: WorkflowStage;
  status: StageStatus;
  started_at?: Date;
  completed_at?: Date;
  data?: StageData; // Discriminated union
  notes?: string;
}

// ============================================================================
// STAGE DATA (Discriminated Unions)
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

export interface InspirationData {
  type: 'inspiration';
  selected_pedal_ids: string[]; // PedalPCB catalog IDs
  search_criteria?: string;
  notes?: string;
}

export interface SpecDownloadData {
  type: 'spec_download';
  source_url: string;
  pdf_path?: string;
  extraction_method: 'manual' | 'ocr' | 'pdf_parse';
  extracted_bom?: CircuitBOMItem[];
  schematic_images?: string[];
}

export interface SchematicAnalysisData {
  type: 'schematic_analysis';
  schematic_path: string;
  analysis_passes: number;
  components: SchematicComponent[];
  connections: SchematicConnection[];
  low_confidence_components: string[]; // IDs flagged for review
  analysis_notes?: string;
}

export interface SchematicComponent {
  id: string;
  type: ComponentType;
  value: string;
  reference_designator: string;
  position_x: number;
  position_y: number;
  orientation: 'horizontal' | 'vertical';
  confidence: number; // 0-1
}

export interface SchematicConnection {
  from_component: string;
  from_pin: string;
  to_component: string;
  to_pin: string;
  confidence: number;
}

export interface InventoryCheckData {
  type: 'inventory_check';
  matches: ComponentMatch[];
  missing_components: MissingComponent[];
  substitution_suggestions: SubstitutionSuggestion[];
  completeness: number; // 0-1
}

export interface ComponentMatch {
  bom_item_id: string;
  component_id: string;
  quantity_needed: number;
  quantity_available: number;
  is_exact_match: boolean;
}

export interface MissingComponent {
  bom_item_id: string;
  component_type: ComponentType;
  component_value: string;
  quantity_needed: number;
  estimated_price?: number;
  suggested_vendors?: string[];
}

export interface SubstitutionSuggestion {
  bom_item_id: string;
  original_value: string;
  substitute_component_id: string;
  substitute_value: string;
  reason: string;
  impact_on_tone: 'none' | 'minimal' | 'moderate' | 'significant';
}

export interface BOMGenerationData {
  type: 'bom_generation';
  items: BOMItem[];
  organized_by_type: Record<string, BOMItem[]>;
  total_items: number;
  generated_at: Date;
}

export interface BOMItem {
  component_type: ComponentType;
  component_value: string;
  quantity: number;
  reference_designators: string[];
  in_stock: boolean;
  notes?: string;
}

export interface BreadboardLayoutData {
  type: 'breadboard_layout';
  layout_id: string;
  platform: string; // 'dual_board_custom'
  components: BreadboardComponent[];
  connections: BreadboardConnection[];
  power_config: PowerRailConfig;
  fritzing_path?: string;
  png_path?: string;
  layout_notes?: string;
}

export interface BreadboardComponent {
  bom_item_id: string;
  component_id: string;
  reference_designator: string;
  board: 1 | 2; // Which board (1 or 2)
  row: number; // a-j (0-9)
  column: number; // 1-63
  orientation: 'horizontal' | 'vertical';
  span: number; // Number of holes
}

export interface BreadboardConnection {
  from_component: string;
  from_pin: number;
  to_component: string;
  to_pin: number;
  wire_color?: string;
  board_crossing?: boolean; // Crosses between boards
}

export interface PowerRailConfig {
  voltage: number; // e.g., 9V
  jumper_connections: {
    input: boolean;
    ground: boolean;
    v3_3: boolean;
    ref: boolean;
    v5: boolean;
    v9: boolean;
    v9_neg: boolean;
    v18: boolean;
    output: boolean;
  };
  potentiometer_slots: Array<{
    slot: number; // 1-6
    component_id?: string;
    function?: string; // "Gain", "Tone", "Volume"
  }>;
}

export interface PrototypeTestingData {
  type: 'prototype_testing';
  test_results: TestResult[];
  audio_samples: AudioSample[];
  measurements: Measurement[];
  issues: Issue[];
  is_fully_functional: boolean;
}

export interface TestResult {
  test_id: string;
  test_type: 'power' | 'audio' | 'signal_flow' | 'tone';
  passed: boolean;
  timestamp: Date;
  notes: string;
}

export interface AudioSample {
  id: string;
  file_path: string;
  description: string;
  settings: Record<string, number>; // Knob positions
  timestamp: Date;
}

export interface Measurement {
  measurement_type: string;
  location: string;
  expected_value: string;
  actual_value: string;
  within_tolerance: boolean;
}

export interface Issue {
  id: string;
  severity: 'critical' | 'major' | 'minor';
  description: string;
  resolution?: string;
  resolved_at?: Date;
}

export interface FinalAssemblyData {
  type: 'final_assembly';
  enclosure_id: string;
  drill_template?: string;
  assembly_steps: AssemblyStep[];
  completion_photos: string[];
  final_test_passed: boolean;
}

export interface AssemblyStep {
  step_number: number;
  description: string;
  completed: boolean;
  photo_path?: string;
  notes?: string;
}

export interface GraphicsDesignData {
  type: 'graphics_design';
  design_id: string;
  design_file_path: string;
  preview_image_path: string;
  drill_holes: DrillHole[];
  dimensions: EnclosureDimensions;
  color_scheme: ColorScheme;
  is_final: boolean;
}

export interface DrillHole {
  x: number;
  y: number;
  diameter: number;
  purpose: 'potentiometer' | 'switch' | 'led' | 'jack' | 'dc' | 'other';
  label?: string;
}

export interface EnclosureDimensions {
  width: number;
  height: number;
  depth: number;
  unit: 'mm' | 'inches';
}

export interface ColorScheme {
  base_color: string;
  text_color: string;
  accent_color?: string;
  finish?: 'matte' | 'glossy' | 'textured';
}

export interface ShowcaseData {
  type: 'showcase';
  post_id: string;
  title: string;
  description: string;
  images: ShowcaseImage[];
  published_at: Date;
  visibility: 'public' | 'private' | 'unlisted';
}

export interface ShowcaseImage {
  id: string;
  path: string;
  caption?: string;
  display_order: number;
}

// ============================================================================
// ENCLOSURES
// ============================================================================

export interface Enclosure {
  id: string;
  name: string;
  size: string; // '1590A', '1590B', '125B', etc.
  width_mm: number;
  height_mm: number;
  depth_mm: number;
  material?: string;
  color?: string;
  manufacturer?: string;
  quantity_in_stock: number;
  created_at: Date;
}

export interface EnclosureGraphics {
  id: string;
  project_id: string;
  enclosure_id: string;
  design_file_path?: string;
  preview_image_path?: string;
  drill_template_path?: string;
  drill_holes_json?: string; // JSON array
  version: number;
  is_final: boolean;
  created_at: Date;
}

// ============================================================================
// USER PROFILES
// ============================================================================

export interface UserProfile {
  user_id: string;
  display_name?: string;
  skill_level: DifficultyLevel;
  preferred_breadboard: string;
  preferred_vendors?: string; // JSON array
  ui_preferences?: UIPreferences;
  notification_preferences?: string; // JSON
  created_at: Date;
  updated_at: Date;
}

export interface UIPreferences {
  embedded_view_mode: 'always' | 'toggle' | 'separate_tab';
  theme: 'light' | 'dark';
  compact_mode: boolean;
}

// ============================================================================
// AGENT STATE
// ============================================================================

export interface AgentState {
  id: string;
  scope: 'session' | 'user' | 'global';
  key: string;
  value: string; // JSON serialized
  expires_at?: Date;
  created_at: Date;
  updated_at: Date;
}

export interface WorkflowLog {
  id: string;
  project_id?: string;
  agent_name: string;
  stage: WorkflowStage;
  status: 'started' | 'completed' | 'failed';
  input?: string; // JSON
  output?: string; // JSON
  error?: string;
  duration_ms?: number;
  created_at: Date;
}

// ============================================================================
// API TYPES
// ============================================================================

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  warnings?: string[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
}

// ============================================================================
// WORKFLOW TYPES
// ============================================================================

export interface WorkflowProgress {
  project_id: string;
  current_stage: WorkflowStage;
  completed_stages: WorkflowStage[];
  active_agent?: string;
  progress_percent: number;
  estimated_time_remaining?: number; // seconds
}

export interface AgentUpdate {
  type: 'started' | 'progress' | 'completed' | 'error';
  agent_name: string;
  stage: WorkflowStage;
  progress?: number; // 0-100
  message?: string;
  result?: any;
  error?: string;
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
