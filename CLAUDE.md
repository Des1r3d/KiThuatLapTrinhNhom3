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

> For detailed class flows and method sequences, see [docs/classflow.md](docs/classflow.md)

### Medicine
```python
@dataclass
class Medicine:
    id: str
    name: str
    quantity: int
    expiry_date: date
    shelf_id: str
    price: float

    def is_expired() -> bool      # True if expiry_date < today
    def days_until_expiry() -> int  # Negative if expired
    def to_dict() -> dict         # JSON serialization
    @staticmethod
    def from_dict(data: dict) -> Medicine  # Deserialize from JSON
```

**Medicine State Transitions:**
```
[New] → [Valid] → [In Inventory]
           ↓
      [Expired] (when expiry_date < today)
           ↓
      [Low Stock] (when quantity < threshold)
```

### Shelf
```python
@dataclass
class Shelf:
    id: str
    row: str
    column: str
    capacity: str

    def to_dict() -> dict
    @staticmethod
    def from_dict(data: dict) -> Shelf
```

## Critical Implementation Details

### StorageEngine (`src/storage.py`)
- **Atomic writes required:** Write to `.tmp` file first, then rename to prevent data corruption
- **Error handling:** Handle missing files and malformed JSON gracefully
- **Validation:** Always validate JSON structure on load
- **Backup mechanism:** Create backup before write, restore on failure

**Key Methods:**
```python
def read_json(filepath: str) -> dict   # Raises FileNotFoundError, JSONDecodeError
def write_json(filepath: str, data: dict)  # Atomic: backup → temp → rename
```

### InventoryManager (`src/inventory_manager.py`)
Central controller for all inventory operations.

**Key Methods:**
```python
def load_data()                                    # Load medicines from JSON
def save_data()                                    # Persist to JSON
def add_medicine(medicine: Medicine)               # Validate & add
def remove_medicine(medicine_id: str)              # Find & remove
def update_medicine(medicine_id: str, changes: dict)  # Immutable update
def check_expiry(days_threshold: int = 30) -> List[Medicine]
def check_low_stock(threshold: int = 5) -> List[Medicine]
```

**Validation Rules:**
- **No negative quantities:** Validate qty >= 0 before save
- **Auto-generate IDs:** If Medicine.id is empty, generate unique ID
- **Date validation:** Expiry date must be future date for new entries

### SearchEngine (`src/search_engine.py`)
- **Fuzzy matching threshold:** 80% minimum score using TheFuzz
- **Index caching:** Cache medicine names for faster repeated searches
- **Return top 5 results** with scores

**Key Methods:**
```python
def index_data(medicines: List[Medicine])  # Build search index
def search(query: str, limit: int = 5) -> List[Tuple[Medicine, int]]
```

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

### UI Components

**MainWindow (`src/ui/main_window.py`):**
- QStackedWidget for page switching (Dashboard, InventoryView, Settings)
- Keyboard shortcuts: Ctrl+K (search), Ctrl+N (add), Ctrl+D (theme)
- Emits signals on navigation changes

**InventoryView (`src/ui/inventory_view.py`):**
- QTableView with custom QAbstractTableModel
- Pandas DataFrame as backend
- Double-click → Edit dialog, Right-click → Context menu

**Dashboard (`src/ui/dashboard.py`):**
- FigureCanvasQTAgg for Matplotlib integration
- Refresh button reloads charts from InventoryManager

**Add/Edit Dialog (`src/ui/dialogs.py`):**
- QLineEdit (Name, Ingredient, Price), QSpinBox (Qty), QDateEdit, QComboBox (Shelf)
- Validation before save, emits signal on success

### Integration Flow Example

```
User clicks "Add Medicine" (Ctrl+N)
    ↓
AddMedicineDialog opens
    ↓
User fills form → clicks Save
    ↓
Dialog validates → creates Medicine object
    ↓
InventoryManager.add_medicine() validates & appends
    ↓
InventoryManager.save_data() → StorageEngine.write_json()
    ↓
StorageEngine: backup → write .tmp → rename
    ↓
InventoryManager emits 'medicine_added' signal
    ↓
InventoryView receives signal → reloads DataFrame
    ↓
Table updates, Dialog closes
```

## Important Notes

- This is a **desktop-only** application (no web/mobile)
- Target users are **internal pharmacists** (not public-facing)
- All data persists in **JSON files only** (no SQL database)
- Settings stored in `data/settings.json` (theme preference, alert thresholds)
- Use **immutable patterns** when updating medicine objects (create new object, don't mutate)

## Error Handling Strategy

**Data Layer Errors:**
- `FileNotFoundError` → Check for backup, initialize empty list if none
- `JSONDecodeError` → Load backup if exists, show error dialog if not
- Write failure → Rollback from backup, keep in-memory state

**Business Logic Errors:**
- Invalid data → Raise `ValueError` with message, dialog shows error
- Duplicate ID → Auto-generate new ID, retry

**UI Layer Errors:**
- Invalid form input → Inline error, disable Save button
- Search no results → Display "No results found" message

## Ticket Cross-Reference

| Ticket | Component | Description |
|--------|-----------|-------------|
| T-101 | Project Setup | Infrastructure |
| T-102 | Data Models | Medicine, Shelf classes |
| T-103 | Storage Engine | JSON read/write |
| T-201 | Inventory Manager | CRUD operations |
| T-202 | Alert System | Expiry/low stock checks |
| T-203 | Search Engine | Fuzzy search |
| T-301 | Main Window | Navigation, shortcuts |
| T-302 | Inventory View | Table display |
| T-303 | Add/Edit Dialog | Form dialogs |
| T-304 | Dashboard | Charts |
| T-305 | Theme Toggle | Dark/Light mode |
