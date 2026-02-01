# Development Tickets

## Phase 1: Foundation & Core Logic

### T-101: Project Setup & Repository Initialization
-   **Description:** Initialize the Python project structure.
-   **Tasks:**
    -   Create virtual environment.
    -   Install dependencies: `PyQt6`, `pandas`, `thefuzz`, `matplotlib`.
    -   Set up folder structure: `src/`, `data/`, `tests/`, `assets/`.
    -   Create `README.md` and `.gitignore`.

### T-102: Implement Data Models (Dataclasses)
-   **Description:** Define the core data structures using Python `dataclasses`.
-   **Files:** `src/models.py`
-   **Requirements:**
    -   `Medicine` class: `id`, `name`, `qty`, `expiry`, `shelf_id`.
    -   `Shelf` class.
    -   Include helper methods: `to_dict()`, `from_dict()`.

### T-103: Storage Engine (JSON I/O)
-   **Description:** Create a robust generic JSON handler.
-   **Files:** `src/storage.py`
-   **Requirements:**
    -   Atomic writes (write to temp then rename) to prevent corruption.
    -   Error handling for missing/corrupt files.
    -   Unit tests for load/save operations.

## Phase 2: Business Logic

### T-201: Inventory Manager Logic
-   **Description:** Implement the controller for inventory operations.
-   **Files:** `src/inventory_manager.py`
-   **Requirements:**
    -   `add_item()`, `remove_item()`, `update_item()`.
    -   Validations (e.g., negative quantity not allowed).
    -   Auto-generate IDs if not provided.

### T-202: Expiry & Stock Alert System
-   **Description:** Logic to filter items needing attention.
-   **Requirements:**
    -   `get_expiring_soon(days=30)`: Returns list of items.
    -   `get_low_stock(threshold=5)`: Returns list of low stock items.

### T-203: Fuzzy Search Engine
-   **Description:** Implement search functionality using `thefuzz` or `process` from `rapidfuzz`.
-   **Requirements:**
    -   Cache/Index the medicine names for speed.
    -   Return top 5 matches with scores.

## Phase 3: UI Implementation (PyQt6)

### T-301: Main Window Layout & Navigation
-   **Description:** Create the shell of the application.
-   **Requirements:**
    -   Sidebar with navigation buttons.
    -   `QStackedWidget` for switching views (Dashboard, Inventory, Settings).
    -   `Ctrl+K` for global search.

### T-302: Inventory Table View
-   **Description:** Display all medicines in a sortable/filterable table.
-   **Requirements:**
    -   Use `QTableView` with a custom `QAbstractTableModel` (powered by Pandas/Polars).
    -   Columns: Name, Qty, Expiry, Shelf, Status (Color-coded).

### T-303: Add/Edit Medicine Dialog
-   **Description:** Form to input medicine details.
-   **Requirements:**
    -   Date picker for expiry.
    -   Dropdown for Shelf selection.
    -   Validation before submit.

### T-304: Dashboard & Matplotlib Integration
-   **Description:** Landing page with charts.
-   **Requirements:**
    -   Embed `FigureCanvasQTAgg`.
    -   Plot: Pie chart of Expiry status.
    -   Plot: Bar chart of Stock levels.

### T-305: Dark/Light Mode Toggle
-   **Description:** Implement theming.
-   **Requirements:**
    -   Use a stylesheet (QSS) loader.
    -   Toggle button `Ctrl+D`.
    -   Persist preference in `settings.json`.
