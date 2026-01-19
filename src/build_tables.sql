PRAGMA foreign_keys = ON;

CREATE TABLE part_categories (
    id   INTEGER PRIMARY KEY,
    name VARCHAR(200)
);

CREATE TABLE parts (
    part_num      VARCHAR(20) PRIMARY KEY,
    name          VARCHAR(250),
    part_cat_id   INTEGER,
    part_material VARCHAR(20), -- added
    FOREIGN KEY (part_cat_id) REFERENCES part_categories(id)
);

CREATE TABLE colors (
    id        INTEGER PRIMARY KEY,
    name      VARCHAR(200),
    rgb       VARCHAR(6),
    is_trans  BOOLEAN,
    num_parts INTEGER, -- added
    num_sets  INTEGER, -- added
    y1        VARCHAR(4), -- added
    y2        VARCHAR(4) -- added
);

CREATE TABLE inventories (
    id       INTEGER PRIMARY KEY,
    version  INTEGER,
    set_num  VARCHAR(20)  -- references sets.set_num or minifigs.fig_num
);

CREATE TABLE inventory_parts (
    inventory_id INTEGER,
    part_num     VARCHAR(20),
    color_id     INTEGER,
    quantity     INTEGER,
    is_spare     BOOLEAN,
    img_url      VARCHAR(200), -- added

    PRIMARY KEY (inventory_id, part_num, color_id),

    FOREIGN KEY (inventory_id) REFERENCES inventories(id),
    FOREIGN KEY (part_num)     REFERENCES parts(part_num),
    FOREIGN KEY (color_id)     REFERENCES colors(id)
);

CREATE TABLE elements (
    element_id VARCHAR(10) PRIMARY KEY,
    part_num   VARCHAR(20),
    color_id   INTEGER,
    design_id  VARCHAR(20), -- added

    FOREIGN KEY (part_num) REFERENCES parts(part_num),
    FOREIGN KEY (color_id) REFERENCES colors(id)
);

CREATE TABLE part_relationships (
    rel_type        VARCHAR(1),
    child_part_num  VARCHAR(20),
    parent_part_num VARCHAR(20),

    PRIMARY KEY (rel_type, child_part_num, parent_part_num),

    FOREIGN KEY (child_part_num)  REFERENCES parts(part_num),
    FOREIGN KEY (parent_part_num) REFERENCES parts(part_num)
);

CREATE TABLE themes (
    id        INTEGER PRIMARY KEY,
    name      VARCHAR(40),
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES themes(id)
);

CREATE TABLE sets (
    set_num    VARCHAR(20) PRIMARY KEY,
    name       VARCHAR(256),
    year       INTEGER,
    theme_id   INTEGER,
    num_parts  INTEGER,
    img_url    VARCHAR(200), -- added

    FOREIGN KEY (theme_id)  REFERENCES themes(id)
);

CREATE TABLE inventory_sets (
    inventory_id INTEGER,
    set_num      VARCHAR(20),
    quantity     INTEGER,

    PRIMARY KEY (inventory_id, set_num),

    FOREIGN KEY (inventory_id) REFERENCES inventories(id),
    FOREIGN KEY (set_num)      REFERENCES sets(set_num)
);

CREATE TABLE minifigs (
    fig_num   VARCHAR(20) PRIMARY KEY,
    name      VARCHAR(256),
    num_parts INTEGER,
    img_url   VARCHAR(200) -- added
);

CREATE TABLE inventory_minifigs (
    inventory_id INTEGER,
    fig_num      VARCHAR(20),
    quantity     INTEGER,

    PRIMARY KEY (inventory_id, fig_num),

    FOREIGN KEY (inventory_id) REFERENCES inventories(id),
    FOREIGN KEY (fig_num)       REFERENCES minifigs(fig_num)
);

-- Lookup by part
CREATE INDEX idx_inventory_parts_part
ON inventory_parts (part_num);

-- Lookup by color
CREATE INDEX idx_inventory_parts_color
ON inventory_parts (color_id);

-- Lookup by inventory
CREATE INDEX idx_inventory_parts_inventory
ON inventory_parts (inventory_id);

-- Composite index for part + color queries
CREATE INDEX idx_inventory_parts_part_color
ON inventory_parts (part_num, color_id);

-- Count / filter elements by part
CREATE INDEX idx_elements_part
ON elements (part_num);

-- Count / filter elements by color
CREATE INDEX idx_elements_color
ON elements (color_id);

-- Fast part + color lookups
CREATE INDEX idx_elements_part_color
ON elements (part_num, color_id);

-- Parts
CREATE INDEX idx_parts_category
ON parts (part_cat_id);

-- Colours
CREATE INDEX idx_colors_is_trans
ON colors (is_trans);

-- Sets + themes
CREATE INDEX idx_sets_theme
ON sets (theme_id);

-- Inventories
CREATE INDEX idx_inventories_set
ON inventories (set_num);

-- Inventory sets
CREATE INDEX idx_inventory_sets_set
ON inventory_sets (set_num);

-- Inventory minifigs
CREATE INDEX idx_inventory_minifigs_fig
ON inventory_minifigs (fig_num);


