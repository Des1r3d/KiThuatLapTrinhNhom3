# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Pharmacy Management System (Hệ thống Quản lý Kho Thuốc)** - A desktop application for pharmacists to manage medicine inventory, track expiry dates, and perform intelligent searches.

**Tech Stack:**
- Python 3.9+ with PyQt6 for GUI
- Pandas for data processing
- Pure JSON storage (no database)
- TheFuzz for fuzzy search
- Matplotlib for charts and reports

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
python src/main.py
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_storage.py

# Run with coverage
python -m pytest --cov=src tests/
```

## Architecture

### Three-Layer Structure

```
UI Layer (PyQt6)
    ↓
Business Logic Layer
    ↓
Data Access Layer (JSON)
```

**UI Layer Components:**
- `Dashboard`: Overview with charts (Matplotlib integration)
- `InventoryView`: Table view for medicine list (QTableView with custom model)
- `SearchBar`: Global search modal (Ctrl+K)
- `Reports`: Statistical visualizations

**Business Logic:**
- `InventoryManager`: CRUD operations for medicine inventory
- `SearchEngine`: Fuzzy search with TheFuzz (80%+ match threshold)
- `AlertSystem`: Check for expiring medicines and low stock

**Data Layer:**
- `StorageEngine`: Atomic JSON read/write operations
- `Models`: Python dataclasses (`Medicine`, `Shelf`)

### Key Design Patterns

**Repository Pattern:** StorageEngine abstracts JSON file operations from business logic.

**Model-View Pattern:** QTableView + QAbstractTableModel for inventory display with Pandas backend.

**Atomic Writes:** JSON files written to temporary file first, then renamed to prevent corruption.

## Data Models

### Medicine
```python
@dataclass
class Medicine:
    id: str
    name: str
    active_ingredient: str
    quantity: int
    expiry_date: date
    shelf_id: str
    price: float

    def is_expired() -> bool
    def days_until_expiry() -> int
```

### Shelf
```python
@dataclass
class Shelf:
    id: str
    row: str
    column: str
    capacity: str
```

## Critical Implementation Details

### JSON Storage (`src/storage.py`)
- **Atomic writes required:** Write to `.tmp` file first, then rename to prevent data corruption
- **Error handling:** Handle missing files and malformed JSON gracefully
- **Validation:** Always validate JSON structure on load

### Search Engine (`src/inventory_manager.py` or dedicated file)
- **Fuzzy matching threshold:** 80% minimum score using TheFuzz
- **Index caching:** Cache medicine names for faster repeated searches
- **Return top 5 results** with scores

### Inventory Manager Validation
- **No negative quantities:** Validate qty >= 0 before save
- **Auto-generate IDs:** If Medicine.id is empty, generate unique ID
- **Date validation:** Expiry date must be future date for new entries

### UI Keyboard Shortcuts
- `Ctrl+K`: Global search modal
- `Ctrl+N`: Add new medicine dialog
- `Ctrl+D`: Toggle Dark/Light mode

### Alert System Thresholds
- **Expiring soon:** Default 30 days threshold
- **Low stock:** Default 5 units threshold
- Both configurable in settings.json

## File Structure

```
src/
├── models.py              # Data classes (Medicine, Shelf)
├── storage.py             # JSON read/write engine
├── inventory_manager.py   # Business logic for inventory
├── search_engine.py       # Fuzzy search implementation
├── main.py               # Application entry point
└── ui/
    ├── main_window.py    # Main window with sidebar navigation
    ├── dashboard.py      # Dashboard with Matplotlib charts
    ├── inventory_view.py # Medicine table view
    └── dialogs.py        # Add/Edit medicine dialogs

data/
├── medicines.json        # Medicine inventory data
├── shelves.json          # Shelf configuration
└── settings.json         # User preferences (theme, thresholds)

tests/
├── test_storage.py       # JSON operations tests
├── test_inventory.py     # Business logic tests
└── test_models.py        # Data model tests
```

## Development Phases (from docs/tickets.md)

**Phase 1 (T-101 to T-103):** Foundation - Project setup, data models, storage engine
**Phase 2 (T-201 to T-203):** Business logic - Inventory manager, alerts, search
**Phase 3 (T-301 to T-305):** UI implementation - Main window, table view, dashboard, theme toggle

## UI/UX Guidelines

**Theme:** Modern flat design using Breeze or Qt-Material (customized via QSS)

**Layout:**
- Sidebar navigation (left)
- Main content area (QStackedWidget for view switching)
- Status bar (bottom) showing total medicines and alerts

**Color Coding in Tables:**
- Red: Expired medicines
- Yellow: Expiring within 30 days
- Green: Normal stock

**Charts (Matplotlib embedded in PyQt6):**
1. Pie chart: Expiry distribution (Good / Near expiry / Expired)
2. Bar chart: Top 10 medicines by quantity
3. Optional heatmap: Shelf capacity visualization

## Important Notes

- This is a **desktop-only** application (no web/mobile)
- Target users are **internal pharmacists** (not public-facing)
- All data persists in **JSON files only** (no SQL database)
- Settings stored in `data/settings.json` (theme preference, alert thresholds)
- Use **immutable patterns** when updating medicine objects (create new object, don't mutate)
