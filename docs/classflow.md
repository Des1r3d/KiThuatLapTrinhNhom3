# ClassFlow Documentation - Pharmacy Management System

This document describes the detailed flow and interaction patterns for each class in the Pharmacy Management System.

## Table of Contents
1. [Medicine Class Flow](#1-medicine-class-flow)
2. [Shelf Class Flow](#2-shelf-class-flow)
3. [InventoryManager Flow](#3-inventorymanager-flow)
4. [StorageEngine Flow](#4-storageengine-flow)
5. [SearchEngine Flow](#5-searchengine-flow)
6. [UI Components Flow](#6-ui-components-flow)
7. [Integration Flows](#7-integration-flows)
8. [Error Handling Flow](#8-error-handling-flow)

---

## 1. Medicine Class Flow

### Purpose
Core data model representing a medicine item in inventory.

### Attributes
- `id: str` - Unique identifier (auto-generated if empty)
- `name: str` - Medicine name
- `quantity: int` - Stock quantity (must be >= 0)
- `expiry_date: date` - Expiration date
- `shelf_id: str` - Reference to storage location
- `price: float` - Unit price

### Method Flow

#### `is_expired() -> bool`
```
START
  ↓
Get current date
  ↓
Compare expiry_date with today
  ↓
Return True if expiry_date < today
  ↓
END
```

#### `days_until_expiry() -> int`
```
START
  ↓
Get current date
  ↓
Calculate delta = expiry_date - today
  ↓
Return delta.days (negative if expired)
  ↓
END
```

#### `to_dict() -> dict`
```
START
  ↓
Create empty dictionary
  ↓
For each attribute:
  - Convert to JSON-serializable type
  - Handle date → ISO string conversion
  ↓
Return dictionary
  ↓
END
```

#### `from_dict(data: dict) -> Medicine`
```
START
  ↓
Validate required fields exist
  ↓
Parse date string → date object
  ↓
Create Medicine instance
  ↓
Validate constraints (qty >= 0)
  ↓
Return Medicine object
  ↓
END
```

### State Transitions
```
[New] → [Valid] → [In Inventory]
           ↓
      [Expired] (when expiry_date < today)
           ↓
      [Low Stock] (when quantity < threshold)
```

---

## 2. Shelf Class Flow

### Purpose
Represents physical storage location in pharmacy.

### Attributes
- `id: str` - Shelf identifier
- `row: str` - Row position
- `column: str` - Column position
- `capacity: str` - Maximum capacity

### Method Flow

#### `to_dict() -> dict`
```
START
  ↓
Convert all attributes to dictionary
  ↓
Return dictionary
  ↓
END
```

#### `from_dict(data: dict) -> Shelf`
```
START
  ↓
Validate required fields
  ↓
Create Shelf instance
  ↓
Return Shelf object
  ↓
END
```

### Usage in System
```
User selects shelf (Dropdown in Add/Edit Dialog)
  ↓
InventoryManager validates shelf_id exists
  ↓
Medicine.shelf_id references Shelf.id
  ↓
Display location in Inventory Table
```

---

## 3. InventoryManager Flow

### Purpose
Central controller for all inventory operations. Manages CRUD operations and business logic.

### Dependencies
- `StorageEngine` - For persistence
- `Medicine` - Data model
- `SearchEngine` - For search operations

### Method Flows

#### `load_data()`
```
START
  ↓
Call StorageEngine.read_json('medicines.json')
  ↓
Get list of dictionaries
  ↓
For each dict:
  - Medicine.from_dict(dict)
  - Add to self.medicines list
  ↓
Handle FileNotFoundError → Initialize empty list
  ↓
Handle JSONDecodeError → Log error, use backup
  ↓
END
```

#### `save_data()`
```
START
  ↓
For each Medicine in self.medicines:
  - Call medicine.to_dict()
  - Collect into list
  ↓
Call StorageEngine.write_json('medicines.json', data)
  ↓
Handle errors → Rollback to previous state
  ↓
END
```

#### `add_medicine(medicine: Medicine)`
```
START
  ↓
Validate medicine data
  ↓
Check if medicine.id is empty
  ↓
  YES → Generate unique ID (UUID or timestamp-based)
  ↓
Validate quantity >= 0
  ↓
Validate expiry_date >= today (warning if past)
  ↓
Validate shelf_id exists
  ↓
Append to self.medicines
  ↓
Call save_data()
  ↓
Emit signal → UI updates table
  ↓
END
```

#### `remove_medicine(medicine_id: str)`
```
START
  ↓
Find medicine by ID in self.medicines
  ↓
  NOT FOUND → Raise ValueError
  ↓
Remove from list
  ↓
Call save_data()
  ↓
Emit signal → UI updates table
  ↓
END
```

#### `update_medicine(medicine_id: str, changes: dict)`
```
START
  ↓
Find medicine by ID
  ↓
  NOT FOUND → Raise ValueError
  ↓
Create new Medicine object (immutable pattern)
  ↓
Apply changes to new object
  ↓
Validate new object
  ↓
Replace old object in list
  ↓
Call save_data()
  ↓
Emit signal → UI updates
  ↓
END
```

#### `check_expiry(days_threshold: int = 30) -> List[Medicine]`
```
START
  ↓
Initialize empty result list
  ↓
For each medicine in self.medicines:
  - Calculate days_until_expiry()
  - If days <= days_threshold:
    → Add to result list
  ↓
Sort by expiry_date (soonest first)
  ↓
Return result list
  ↓
END
```

#### `check_low_stock(threshold: int = 5) -> List[Medicine]`
```
START
  ↓
Initialize empty result list
  ↓
For each medicine in self.medicines:
  - If quantity <= threshold:
    → Add to result list
  ↓
Sort by quantity (lowest first)
  ↓
Return result list
  ↓
END
```

---

## 4. StorageEngine Flow

### Purpose
Handles atomic JSON file operations with error handling.

### Method Flows

#### `read_json(filepath: str) -> dict`
```
START
  ↓
Check if file exists
  ↓
  NO → Raise FileNotFoundError
  ↓
Open file in read mode
  ↓
Try: json.load(file)
  ↓
  JSONDecodeError → Check for backup file
    ↓
    Backup exists? → Load backup
    ↓
    No backup → Raise error
  ↓
Return parsed data
  ↓
END
```

#### `write_json(filepath: str, data: dict)`
```
START
  ↓
Create backup of existing file (if exists)
  ↓
Generate temp filename: filepath + '.tmp'
  ↓
Open temp file in write mode
  ↓
json.dump(data, file, indent=2)
  ↓
Close temp file
  ↓
Atomic rename: temp → filepath
  ↓
  SUCCESS → Delete backup
  ↓
  FAILURE → Restore from backup, raise error
  ↓
END
```

### Error Handling
```
Write Operation:
  ↓
Create backup → Write to .tmp → Rename
  ↓               ↓               ↓
  FAIL          FAIL            FAIL
  ↓               ↓               ↓
Log error    Restore backup  Restore backup
  ↓               ↓               ↓
Raise       Raise           Raise
```

---

## 5. SearchEngine Flow

### Purpose
Fuzzy search implementation using TheFuzz library.

### Dependencies
- `thefuzz` library (fuzzy matching)
- `Medicine` list from InventoryManager

### Method Flows

#### `index_data(medicines: List[Medicine])`
```
START
  ↓
Clear existing index
  ↓
For each medicine:
  - Extract name
  - Store in index dict: {id: name}
  ↓
Cache index for fast lookup
  ↓
END
```

#### `search(query: str, limit: int = 5) -> List[Tuple[Medicine, int]]`
```
START
  ↓
Normalize query (lowercase, strip whitespace)
  ↓
Initialize results list
  ↓
For each medicine in index:
  - Calculate fuzzy score for name (fuzz.ratio)
  - Use name_score
  ↓
Filter results: score >= 80
  ↓
Sort by score (descending)
  ↓
Take top 'limit' results
  ↓
Return List[(Medicine object, score)]
  ↓
END
```

### Fuzzy Matching Algorithm
```
Input: query = "paracetamol"
  ↓
For medicine.name = "Paracetamol 500mg":
  - fuzz.ratio("paracetamol", "paracetamol 500mg") → 85
  ↓
For medicine.name = "Aspirin":
  - fuzz.ratio("paracetamol", "aspirin") → 30
  ↓
Filter: Keep only score >= 80
  ↓
Result: [("Paracetamol 500mg", 85)]
```

---

## 6. UI Components Flow

### 6.1 MainWindow Flow

#### Initialization
```
START
  ↓
Create QMainWindow
  ↓
Setup sidebar navigation (QListWidget)
  ↓
Create QStackedWidget for main area
  ↓
Add pages: Dashboard, InventoryView, Settings
  ↓
Setup keyboard shortcuts:
  - Ctrl+K → Open search modal
  - Ctrl+N → Open add medicine dialog
  - Ctrl+D → Toggle theme
  ↓
Connect signals:
  - Sidebar item clicked → Change page
  - Menu actions → Open dialogs
  ↓
Load user settings (theme, window size)
  ↓
Show window
  ↓
END
```

### 6.2 Dashboard Flow

#### Purpose
Display overview statistics and charts using Matplotlib.

#### Initialization Flow
```
START
  ↓
Create Dashboard widget
  ↓
Get data from InventoryManager
  ↓
Create FigureCanvasQTAgg (Matplotlib canvas)
  ↓
Generate charts:
  - Pie chart: Expiry distribution
  - Bar chart: Top 10 medicines by quantity
  ↓
Embed canvas in QVBoxLayout
  ↓
Add refresh button → Reload charts
  ↓
END
```

#### Chart Generation Flow
```
Get medicines from InventoryManager
  ↓
Categorize:
  - Expired (days_until_expiry < 0)
  - Expiring soon (0 <= days <= 30)
  - Normal (days > 30)
  ↓
Create Matplotlib Figure
  ↓
Add subplot: Pie chart
  - Data: [expired_count, expiring_count, normal_count]
  - Labels: ["Hết hạn", "Sắp hết hạn", "Bình thường"]
  - Colors: [red, yellow, green]
  ↓
Add subplot: Bar chart
  - Sort medicines by quantity (descending)
  - Take top 10
  - X-axis: Medicine names
  - Y-axis: Quantities
  ↓
canvas.draw()
  ↓
END
```

### 6.3 InventoryView Flow

#### Purpose
Display medicines in sortable/filterable table.

#### Initialization Flow
```
START
  ↓
Create QTableView
  ↓
Create custom QAbstractTableModel
  ↓
Load medicines from InventoryManager
  ↓
Convert to Pandas DataFrame
  ↓
Set DataFrame as model backend
  ↓
Configure columns:
  - Name, Quantity, Expiry Date, Shelf, Status
  ↓
Enable sorting
  ↓
Setup color coding:
  - Red row if expired
  - Yellow row if expiring soon
  - Green row if normal
  ↓
Connect signals:
  - Double-click → Open edit dialog
  - Right-click → Context menu (Edit/Delete)
  ↓
END
```

#### Data Update Flow
```
InventoryManager emits signal (medicine added/updated/deleted)
  ↓
InventoryView receives signal
  ↓
Reload DataFrame from InventoryManager.medicines
  ↓
Call model.layoutChanged()
  ↓
QTableView refreshes display
  ↓
Reapply sorting/filtering
  ↓
Update status bar (total count)
  ↓
END
```

### 6.4 Add/Edit Dialog Flow

#### Purpose
Form for creating/editing medicine entries.

#### Initialization Flow
```
START
  ↓
Create QDialog
  ↓
Create form fields:
  - QLineEdit: Name, Active Ingredient, Price
  - QSpinBox: Quantity
  - QDateEdit: Expiry Date
  - QComboBox: Shelf (populate from shelves.json)
  ↓
If EDIT mode:
  - Pre-fill fields with existing medicine data
  ↓
Connect validators:
  - Quantity >= 0
  - Price >= 0
  - Date is valid
  ↓
Connect buttons:
  - Save → validate_and_save()
  - Cancel → close()
  ↓
END
```

#### Save Flow
```
User clicks Save button
  ↓
Validate all fields
  ↓
  INVALID → Show error message, return
  ↓
Create Medicine object from form data
  ↓
If ADD mode:
  - Call InventoryManager.add_medicine()
  ↓
If EDIT mode:
  - Call InventoryManager.update_medicine()
  ↓
InventoryManager saves to JSON
  ↓
InventoryManager emits signal
  ↓
Dialog closes
  ↓
InventoryView updates automatically
  ↓
END
```

### 6.5 Global Search Modal Flow

#### Purpose
Quick search accessible via Ctrl+K.

#### Activation Flow
```
User presses Ctrl+K
  ↓
Create/Show search modal (QDialog)
  ↓
Focus on QLineEdit
  ↓
User types query
  ↓
On text changed:
  - Call SearchEngine.search(query)
  - Display results in QListWidget
  - Show score for each result
  ↓
User selects result
  ↓
Navigate to InventoryView
  ↓
Highlight selected medicine in table
  ↓
Close modal
  ↓
END
```

---

## 7. Integration Flows

### 7.1 Complete Add Medicine Flow (All Layers)

```
[UI Layer]
User clicks "Add Medicine" button (Ctrl+N)
  ↓
MainWindow opens AddMedicineDialog
  ↓
User fills form and clicks Save
  ↓
Dialog validates input
  ↓

[Business Logic Layer]
Dialog creates Medicine object
  ↓
Calls InventoryManager.add_medicine(medicine)
  ↓
InventoryManager validates:
  - Auto-generate ID if empty
  - Check quantity >= 0
  - Validate shelf_id exists
  ↓
InventoryManager appends to medicines list
  ↓

[Data Layer]
InventoryManager calls save_data()
  ↓
Converts medicines to list of dicts
  ↓
Calls StorageEngine.write_json()
  ↓
StorageEngine performs atomic write:
  - Create backup
  - Write to .tmp file
  - Rename .tmp → medicines.json
  ↓

[Back to UI Layer]
InventoryManager emits 'medicine_added' signal
  ↓
InventoryView receives signal
  ↓
InventoryView reloads data
  ↓
Table updates with new medicine
  ↓
Status bar shows updated count
  ↓
Dialog closes
  ↓
END
```

### 7.2 Search Flow (All Layers)

```
[UI Layer]
User presses Ctrl+K
  ↓
SearchModal opens
  ↓
User types "paracet"
  ↓
SearchModal text changed event
  ↓

[Business Logic Layer]
Calls SearchEngine.search("paracet")
  ↓
SearchEngine performs fuzzy matching:
  - Compare against all medicine names
  - Calculate scores
  - Filter score >= 80
  - Sort by score
  ↓
Returns List[(Medicine, score)]
  ↓

[Back to UI Layer]
SearchModal displays results:
  - "Paracetamol 500mg (95%)"
  - "Paracetamol Extra (88%)"
  ↓
User selects first result
  ↓
SearchModal emits 'medicine_selected' signal
  ↓
MainWindow switches to InventoryView
  ↓
InventoryView highlights selected medicine
  ↓
SearchModal closes
  ↓
END
```

### 7.3 Dashboard Refresh Flow

```
[UI Layer]
Dashboard widget shown
  ↓
Dashboard requests data
  ↓

[Business Logic Layer]
Calls InventoryManager.check_expiry(30)
  ↓
Returns list of expiring medicines
  ↓
Calls InventoryManager.check_low_stock(5)
  ↓
Returns list of low stock medicines
  ↓

[Back to UI Layer]
Dashboard processes data:
  - Count expired, expiring, normal
  - Get top 10 by quantity
  ↓
Dashboard generates Matplotlib charts
  ↓
Embeds charts in canvas
  ↓
Display to user
  ↓
END
```

---

## 8. Error Handling Flow

### 8.1 Data Layer Errors

#### File Not Found
```
StorageEngine.read_json('medicines.json')
  ↓
FileNotFoundError raised
  ↓
Check for backup file
  ↓
  Backup exists? → Load backup, warn user
  ↓
  No backup? → Return empty list, log warning
  ↓
InventoryManager initializes with empty medicines list
  ↓
UI displays "No medicines found" message
```

#### JSON Decode Error
```
StorageEngine.read_json('medicines.json')
  ↓
JSONDecodeError raised (corrupted file)
  ↓
Check for backup file
  ↓
  Backup exists? → Load backup, warn user
  ↓
  No backup? → Show error dialog, exit gracefully
  ↓
Log error with stack trace
```

#### Write Error
```
StorageEngine.write_json()
  ↓
IOError during write (disk full, permission denied)
  ↓
Rollback: Restore from backup
  ↓
Show error dialog to user
  ↓
Log error details
  ↓
Keep current in-memory state (don't lose changes)
```

### 8.2 Business Logic Errors

#### Invalid Medicine Data
```
InventoryManager.add_medicine(medicine)
  ↓
Validation fails (quantity < 0)
  ↓
Raise ValueError with message
  ↓
Dialog catches exception
  ↓
Show error message to user: "Quantity must be >= 0"
  ↓
Focus on invalid field
  ↓
User corrects and retries
```

#### Duplicate ID
```
InventoryManager.add_medicine(medicine)
  ↓
Check if medicine.id already exists
  ↓
  EXISTS → Raise ValueError("Duplicate ID")
  ↓
Dialog shows error
  ↓
Auto-generate new ID
  ↓
Retry
```

### 8.3 UI Layer Errors

#### Invalid Form Input
```
User enters invalid date
  ↓
QDateEdit validation fails
  ↓
Show inline error message
  ↓
Disable Save button until fixed
```

#### Search No Results
```
SearchEngine.search(query)
  ↓
Returns empty list (no matches >= 80%)
  ↓
SearchModal displays: "No results found"
  ↓
Suggest user to try different keywords
```

---

## 9. State Machine Diagrams

### 9.1 Application State
```
[Startup]
  ↓
[Loading Data] → FAIL → [Error State] → [Recovery]
  ↓                                         ↓
[Ready]                                 [Loading Data]
  ↓
[Idle] ←→ [Searching] ←→ [Displaying Results]
  ↓
[Editing] → [Saving] → FAIL → [Error Dialog] → [Editing]
  ↓           ↓
[Idle]     SUCCESS
              ↓
           [Idle]
```

### 9.2 Medicine Object State
```
[New] → [Validated] → [Persisted]
                          ↓
                      [In Inventory]
                          ↓
                    [Normal Status]
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
        [Expiring Soon]          [Low Stock]
              ↓                       ↓
          [Expired]              [Out of Stock]
              ↓                       ↓
          [Removed]              [Removed]
```

---

## 10. File Structure and Class Mapping

### Planned File Organization
```
src/
├── models.py
│   ├── Medicine (T-102)
│   └── Shelf (T-102)
│
├── storage.py
│   └── StorageEngine (T-103)
│
├── inventory_manager.py
│   └── InventoryManager (T-201)
│
├── search_engine.py
│   └── SearchEngine (T-203)
│
├── alerts.py
│   └── AlertSystem (T-202)
│
├── main.py
│   └── Application entry point
│
└── ui/
    ├── main_window.py
    │   └── MainWindow (T-301)
    │
    ├── inventory_view.py
    │   ├── InventoryTableModel
    │   └── InventoryView (T-302)
    │
    ├── dialogs.py
    │   ├── AddMedicineDialog (T-303)
    │   └── EditMedicineDialog (T-303)
    │
    ├── dashboard.py
    │   └── Dashboard (T-304)
    │
    └── search_modal.py
        └── SearchModal (Global search)
```

---

## 11. Cross-Reference with Tickets

| Ticket | Component | ClassFlow Section |
|--------|-----------|-------------------|
| T-101 | Project Setup | N/A (Infrastructure) |
| T-102 | Data Models | 1. Medicine Class, 2. Shelf Class |
| T-103 | Storage Engine | 4. StorageEngine Flow |
| T-201 | Inventory Manager | 3. InventoryManager Flow |
| T-202 | Alert System | 3. InventoryManager (check_expiry, check_low_stock) |
| T-203 | Search Engine | 5. SearchEngine Flow |
| T-301 | Main Window | 6.1 MainWindow Flow |
| T-302 | Inventory View | 6.3 InventoryView Flow |
| T-303 | Add/Edit Dialog | 6.4 Add/Edit Dialog Flow |
| T-304 | Dashboard | 6.2 Dashboard Flow |
| T-305 | Theme Toggle | 6.1 MainWindow (keyboard shortcuts) |

---

## Summary

This ClassFlow document provides:
1. ✅ Detailed flow for each class
2. ✅ Input/Output specifications
3. ✅ Dependencies and interactions
4. ✅ Method execution sequences
5. ✅ State transitions
6. ✅ Error handling strategies
7. ✅ Integration flows across all three layers
8. ✅ Mapping to actual file structure and tickets

This documentation should be used as a blueprint during implementation phases to ensure all components follow the designed flow patterns.
