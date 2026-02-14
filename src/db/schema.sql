-- PedalBuild SQLite Database Schema
-- Version: 1.0.0
-- Local-first architecture with offline support

-- ============================================================================
-- PEDALPCB.COM CATALOG & REVIEWS (NEW - for embedded content feature)
-- ============================================================================

-- Full pedal catalog from PedalPCB.com (scraped monthly)
CREATE TABLE pedalpcb_catalog (
    id TEXT PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,              -- fuzz, distortion, overdrive, delay, reverb, modulation, etc.
    description TEXT,
    original_pedal TEXT,                 -- e.g., "Ibanez TS808 Tube Screamer"
    difficulty_level TEXT,               -- beginner, intermediate, advanced
    price REAL,
    build_doc_url TEXT,                  -- Direct link to build documentation PDF
    thumbnail_url TEXT,
    images_json TEXT,                    -- JSON array of additional image URLs
    specifications_json TEXT,            -- JSON object with detailed specs
    last_scraped DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,         -- FALSE if pedal discontinued
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pedalpcb_catalog_category ON pedalpcb_catalog(category);
CREATE INDEX idx_pedalpcb_catalog_difficulty ON pedalpcb_catalog(difficulty_level);
CREATE INDEX idx_pedalpcb_catalog_original ON pedalpcb_catalog(original_pedal);
CREATE INDEX idx_pedalpcb_catalog_active ON pedalpcb_catalog(is_active);

-- User reviews and comments from PedalPCB.com (ALL historical reviews)
CREATE TABLE pedalpcb_reviews (
    id TEXT PRIMARY KEY,
    pedal_id TEXT NOT NULL,
    author TEXT,
    rating INTEGER,                      -- 1-5 stars (if available)
    title TEXT,
    comment TEXT NOT NULL,
    helpful_count INTEGER DEFAULT 0,
    reply_count INTEGER DEFAULT 0,
    posted_date DATE,
    source_url TEXT,                     -- Link to original review/comment
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedal_id) REFERENCES pedalpcb_catalog(id) ON DELETE CASCADE
);

CREATE INDEX idx_pedalpcb_reviews_pedal ON pedalpcb_reviews(pedal_id);
CREATE INDEX idx_pedalpcb_reviews_rating ON pedalpcb_reviews(rating);
CREATE INDEX idx_pedalpcb_reviews_date ON pedalpcb_reviews(posted_date);

-- Scraping job tracking (for monthly updates)
CREATE TABLE scraping_jobs (
    id TEXT PRIMARY KEY,
    job_type TEXT NOT NULL,              -- 'catalog', 'reviews', 'build_docs'
    status TEXT NOT NULL,                -- 'pending', 'running', 'completed', 'failed'
    started_at DATETIME,
    completed_at DATETIME,
    items_processed INTEGER DEFAULT 0,
    items_failed INTEGER DEFAULT 0,
    error_log TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scraping_jobs_type ON scraping_jobs(job_type);
CREATE INDEX idx_scraping_jobs_status ON scraping_jobs(status);

-- ============================================================================
-- CIRCUITS & COMPONENTS
-- ============================================================================

-- Circuit specifications (from PedalPCB or user-uploaded)
CREATE TABLE circuits (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,                       -- overdrive, distortion, fuzz, delay, reverb, modulation, filter, compressor, boost
    difficulty_level TEXT,               -- beginner, intermediate, advanced
    source_url TEXT,
    pedalpcb_catalog_id TEXT,            -- Link to PedalPCB catalog if applicable
    schematic_image_path TEXT,
    schematic_pdf_path TEXT,
    voltage_requirement TEXT,            -- e.g., '9V DC'
    current_draw_ma INTEGER,
    enclosure_size TEXT,                 -- '1590B', '1590BB', '125B', 'custom'
    estimated_build_time_hours REAL,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedalpcb_catalog_id) REFERENCES pedalpcb_catalog(id)
);

CREATE INDEX idx_circuits_category ON circuits(category);
CREATE INDEX idx_circuits_difficulty ON circuits(difficulty_level);
CREATE INDEX idx_circuits_pedalpcb ON circuits(pedalpcb_catalog_id);

-- Component library (user's personal component collection + standard parts)
CREATE TABLE components (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,                  -- resistor, capacitor, ic, transistor, diode, potentiometer, switch, led, jack, other
    name TEXT NOT NULL,
    value TEXT,                          -- e.g., '10k', '100nF', 'TL072'
    tolerance TEXT,                      -- e.g., '5%', '10%'
    package TEXT,                        -- e.g., 'DIP8', '0805', 'through-hole'
    manufacturer TEXT,
    part_number TEXT,
    datasheet_url TEXT,
    quantity_in_stock INTEGER DEFAULT 0,
    minimum_quantity INTEGER DEFAULT 0,  -- Alert when stock falls below this
    unit_price REAL,
    location TEXT,                       -- Storage location (drawer, bin, etc.)
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_components_type ON components(type);
CREATE INDEX idx_components_value ON components(value);
CREATE INDEX idx_components_stock ON components(quantity_in_stock);

-- Bill of Materials for each circuit
CREATE TABLE circuit_bom (
    id TEXT PRIMARY KEY,
    circuit_id TEXT NOT NULL,
    component_type TEXT NOT NULL,
    component_value TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    reference_designator TEXT,           -- e.g., 'R1', 'C2', 'IC1'
    substitution_allowed BOOLEAN DEFAULT 0,
    substitution_notes TEXT,
    is_critical BOOLEAN DEFAULT 0,       -- Component affects tone significantly
    position_x REAL,                     -- Position in schematic for reference
    position_y REAL,
    confidence_score REAL DEFAULT 1.0,   -- Confidence from schematic analysis (0-1)
    FOREIGN KEY (circuit_id) REFERENCES circuits(id) ON DELETE CASCADE
);

CREATE INDEX idx_circuit_bom_circuit ON circuit_bom(circuit_id);
CREATE INDEX idx_circuit_bom_component ON circuit_bom(component_type, component_value);
CREATE INDEX idx_circuit_bom_confidence ON circuit_bom(confidence_score);

-- ============================================================================
-- PROJECTS & WORKFLOW
-- ============================================================================

-- Build projects (user's active builds)
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    circuit_id TEXT NOT NULL,
    name TEXT NOT NULL,
    current_stage TEXT NOT NULL,         -- inspiration, spec_download, schematic_analysis, inventory_check, bom_generation, breadboard_layout, prototype_testing, final_assembly, graphics_design, showcase
    status TEXT NOT NULL,                -- active, on_hold, completed, abandoned
    breadboard_platform TEXT DEFAULT 'dual_board_custom',
    enclosure_id TEXT,
    color_scheme TEXT,                   -- JSON string with color preferences
    notes TEXT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (circuit_id) REFERENCES circuits(id),
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_projects_stage ON projects(current_stage);
CREATE INDEX idx_projects_status ON projects(status);

-- Workflow stage tracking
CREATE TABLE project_stages (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,                -- pending, in_progress, completed, skipped, blocked
    started_at DATETIME,
    completed_at DATETIME,
    data TEXT,                           -- JSON - stage-specific data
    notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX idx_project_stages_project ON project_stages(project_id);
CREATE INDEX idx_project_stages_stage ON project_stages(stage);

-- ============================================================================
-- BREADBOARD LAYOUTS
-- ============================================================================

-- Breadboard layouts (specific to user's dual-board platform)
CREATE TABLE breadboard_layouts (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    platform TEXT NOT NULL DEFAULT 'dual_board_custom',
    layout_data TEXT NOT NULL,           -- JSON with component positions, connections, power config
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT 1,
    fritzing_file_path TEXT,             -- .fzz file for editing
    png_image_path TEXT,                 -- PNG for quick reference
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX idx_breadboard_layouts_project ON breadboard_layouts(project_id);
CREATE INDEX idx_breadboard_layouts_active ON breadboard_layouts(is_active, project_id);

-- ============================================================================
-- ENCLOSURES & GRAPHICS
-- ============================================================================

-- Enclosure inventory
CREATE TABLE enclosures (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    size TEXT NOT NULL,                  -- 1590A, 1590B, 1590BB, 125B, custom
    width_mm REAL NOT NULL,
    height_mm REAL NOT NULL,
    depth_mm REAL NOT NULL,
    material TEXT,                       -- aluminum, plastic, steel
    color TEXT,
    manufacturer TEXT,
    quantity_in_stock INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_enclosures_size ON enclosures(size);
CREATE INDEX idx_enclosures_stock ON enclosures(quantity_in_stock);

-- Enclosure graphics designs
CREATE TABLE enclosure_graphics (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    enclosure_id TEXT NOT NULL,
    design_file_path TEXT,               -- SVG or design file
    preview_image_path TEXT,
    drill_template_path TEXT,            -- PDF for drilling
    drill_holes_json TEXT,               -- JSON array of drill hole specifications
    version INTEGER DEFAULT 1,
    is_final BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (enclosure_id) REFERENCES enclosures(id)
);

CREATE INDEX idx_enclosure_graphics_project ON enclosure_graphics(project_id);
CREATE INDEX idx_enclosure_graphics_final ON enclosure_graphics(is_final, project_id);

-- ============================================================================
-- TESTING & ASSEMBLY
-- ============================================================================

-- Test results (breadboard and final assembly)
CREATE TABLE test_results (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    test_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    stage TEXT,                          -- breadboard, final
    test_type TEXT,                      -- audio_test, voltage_test, signal_flow, tone_test
    passed BOOLEAN,
    measurements TEXT,                   -- JSON with voltage readings, frequency response, etc.
    audio_sample_path TEXT,
    notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX idx_test_results_project ON test_results(project_id);
CREATE INDEX idx_test_results_stage ON test_results(stage);

-- ============================================================================
-- SHOWCASE & COMMUNITY
-- ============================================================================

-- Showcase posts
CREATE TABLE showcase_posts (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    visibility TEXT DEFAULT 'public',    -- public, private, unlisted
    likes_count INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE INDEX idx_showcase_posts_visibility ON showcase_posts(visibility);
CREATE INDEX idx_showcase_posts_created ON showcase_posts(created_at);

-- Showcase images
CREATE TABLE showcase_images (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    image_path TEXT NOT NULL,
    caption TEXT,
    display_order INTEGER,
    FOREIGN KEY (post_id) REFERENCES showcase_posts(id) ON DELETE CASCADE
);

CREATE INDEX idx_showcase_images_post ON showcase_images(post_id);

-- ============================================================================
-- USER MANAGEMENT
-- ============================================================================

-- User profiles and preferences
CREATE TABLE user_profiles (
    user_id TEXT PRIMARY KEY,
    display_name TEXT,
    skill_level TEXT,                    -- beginner, intermediate, advanced
    preferred_breadboard TEXT DEFAULT 'dual_board_custom',
    preferred_vendors TEXT,              -- JSON array of preferred vendors
    ui_preferences TEXT,                 -- JSON with UI settings including embedded view preference
    notification_preferences TEXT,       -- JSON
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- ADK AGENT STATE MANAGEMENT
-- ============================================================================

-- Agent state storage (session/user/global scopes)
CREATE TABLE agent_state (
    id TEXT PRIMARY KEY,
    scope TEXT NOT NULL,                 -- session, user, global
    key TEXT NOT NULL,
    value TEXT NOT NULL,                 -- JSON serialized
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_agent_state_scope_key ON agent_state(scope, key);
CREATE INDEX idx_agent_state_expires ON agent_state(expires_at);

-- Workflow execution logs
CREATE TABLE workflow_logs (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    agent_name TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,                -- started, completed, failed
    input TEXT,                          -- JSON
    output TEXT,                         -- JSON
    error TEXT,
    duration_ms INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX idx_workflow_logs_project ON workflow_logs(project_id);
CREATE INDEX idx_workflow_logs_agent ON workflow_logs(agent_name);
CREATE INDEX idx_workflow_logs_status ON workflow_logs(status);

-- ============================================================================
-- COMPONENT ORDERING (Optional - for BOM tracking)
-- ============================================================================

-- Component orders
CREATE TABLE component_orders (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    vendor TEXT,
    order_number TEXT,
    total_amount REAL,
    status TEXT,                         -- draft, ordered, shipped, delivered, cancelled
    tracking_number TEXT,
    expected_delivery DATETIME,
    notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE INDEX idx_component_orders_project ON component_orders(project_id);
CREATE INDEX idx_component_orders_status ON component_orders(status);

-- Order items
CREATE TABLE order_items (
    id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    component_type TEXT NOT NULL,
    component_value TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL,
    matched_component_id TEXT,           -- Link to components table once received
    FOREIGN KEY (order_id) REFERENCES component_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (matched_component_id) REFERENCES components(id)
);

CREATE INDEX idx_order_items_order ON order_items(order_id);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Projects with circuit and pedal info
CREATE VIEW v_projects_full AS
SELECT
    p.id,
    p.name AS project_name,
    p.current_stage,
    p.status,
    c.name AS circuit_name,
    c.category,
    pc.name AS pedalpcb_name,
    pc.original_pedal,
    pc.url AS pedalpcb_url,
    p.started_at,
    p.updated_at
FROM projects p
LEFT JOIN circuits c ON p.circuit_id = c.id
LEFT JOIN pedalpcb_catalog pc ON c.pedalpcb_catalog_id = pc.id;

-- View: Pedals with review summaries
CREATE VIEW v_pedalpcb_with_reviews AS
SELECT
    pc.id,
    pc.name,
    pc.category,
    pc.original_pedal,
    pc.difficulty_level,
    pc.price,
    pc.url,
    COUNT(pr.id) AS review_count,
    AVG(pr.rating) AS avg_rating,
    MAX(pr.posted_date) AS latest_review_date
FROM pedalpcb_catalog pc
LEFT JOIN pedalpcb_reviews pr ON pc.id = pr.pedal_id
GROUP BY pc.id;

-- View: Low stock components
CREATE VIEW v_low_stock_components AS
SELECT
    id,
    type,
    name,
    value,
    quantity_in_stock,
    minimum_quantity,
    location
FROM components
WHERE quantity_in_stock <= minimum_quantity
ORDER BY type, value;

-- ============================================================================
-- TRIGGERS FOR AUTO-UPDATES
-- ============================================================================

-- Update timestamps on modifications
CREATE TRIGGER update_circuits_timestamp
AFTER UPDATE ON circuits
BEGIN
    UPDATE circuits SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_components_timestamp
AFTER UPDATE ON components
BEGIN
    UPDATE components SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_projects_timestamp
AFTER UPDATE ON projects
BEGIN
    UPDATE projects SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_user_profiles_timestamp
AFTER UPDATE ON user_profiles
BEGIN
    UPDATE user_profiles SET updated_at = CURRENT_TIMESTAMP WHERE user_id = NEW.user_id;
END;

CREATE TRIGGER update_pedalpcb_catalog_timestamp
AFTER UPDATE ON pedalpcb_catalog
BEGIN
    UPDATE pedalpcb_catalog SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Create default user profile
INSERT INTO user_profiles (user_id, display_name, skill_level, ui_preferences)
VALUES (
    'default_user',
    'Default User',
    'intermediate',
    '{"embedded_view_mode": "toggle", "theme": "dark", "compact_mode": false}'
);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
