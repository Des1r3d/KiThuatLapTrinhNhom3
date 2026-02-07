# Project Documentation Charts

This document outlines key architectural and flow diagrams for the Pharmacy Management System, providing a visual overview of its structure and functionality. These diagrams are generated using Mermaid syntax, which can be rendered by many Markdown viewers and documentation tools.

---

### 1. Component Architecture Diagram

**Why it's needed:** This high-level diagram illustrates the main software components, their organization into layers (UI, Business Logic, Data), and their primary interactions. It helps developers quickly understand the overall design and interdependencies of the system.

```mermaid
graph TD
    subgraph "UI Layer (PyQt6)"
        A[MainWindow]
        B[InventoryView]
        C[Dashboard]
        D[Add/Edit Dialogs]
        E[Search Modal]
    end

    subgraph "Business Logic Layer (Core)"
        F[InventoryManager]
        G[SearchEngine]
        H[AlertSystem]
    end

    subgraph "Data Layer"
        I[StorageEngine]
        J[(medicines.json)]
    end

    %% --- Connections ---
    A & B & C & D & E --> F
    F --> G
    F --> H
    F --> I
    I --> J
```

---

### 2. Logic Flow / Sequence Diagram (for a Key Use Case)

**Why it's needed:** This diagram demonstrates the dynamic interaction between different components over time to complete a specific task. It's particularly useful for detailing "How the code runs" for a key feature, such as adding a new medicine, showing the sequence of calls between the UI, business logic, and data layers.

```mermaid
sequenceDiagram
    actor User
    participant D as AddMedicineDialog
    participant IM as InventoryManager
    participant SE as StorageEngine

    User->>D: Clicks "Save" on Add Medicine form
    activate D
    D->>D: Validate user input
    D->>IM: add_medicine(new_medicine_data)
    activate IM
    IM->>IM: Validate business rules (e.g., qty >= 0)
    IM->>SE: save_data(updated_inventory_list)
    activate SE
    SE->>SE: Perform atomic write to medicines.json
    SE-->>IM: Return Success
    deactivate SE
    IM-->>D: Return Success
    deactivate IM
    D-->>User: Close dialog, UI updates
    deactivate D
```

---

### 3. Class Diagram

**Why it's needed:** A class diagram describes the static structure of the project's data models. It defines the core objects (classes) like `Medicine` and `Shelf`, their attributes (properties), their methods (functions), and the relationships (associations, aggregations) between them. This serves as a blueprint for the data and object-oriented design.

```mermaid
classDiagram
    direction LR

    class Medicine {
        +id: str
        +name: str
        +quantity: int
        +expiry_date: date
        +shelf_id: str
        +is_expired(): bool
        +days_until_expiry(): int
        +to_dict(): dict
    }

    class Shelf {
        +id: str
        +row: str
        +column: str
        +to_dict(): dict
    }

    class InventoryManager {
        -medicines: List~Medicine~
        +add_medicine(medicine)
        +remove_medicine(id)
        +update_medicine(id, changes)
        +check_expiry(days): List~Medicine~
        +check_low_stock(threshold): List~Medicine~
    }

    InventoryManager "1" o-- "*" Medicine : manages
    Shelf "1" -- "*" Medicine : "stores"
```

---

### 4. File Structure Diagram

**Why it's needed:** This diagram provides a visual representation of the project's directory and file organization. It's crucial for understanding where different parts of the code and data reside, aiding navigation and maintenance. It also clarifies the separation of concerns within the project.

```mermaid
graph TD
    A[KiThuatLapTrinhNhom3/]
    B[src/]
    C[docs/]
    D[data/]

    A --> B
    A --> C
    A --> D

    subgraph "src/"
        B1[models.py]
        B2[storage.py]
        B3[inventory_manager.py]
        B4[search_engine.py]
        B5[alerts.py]
        B6[main.py]
        B7[ui/]
    end

    B --> B1
    B --> B2
    B --> B3
    B --> B4
    B --> B5
    B --> B6
    B --> B7

    subgraph "src/ui/"
        B7_1[main_window.py]
        B7_2[inventory_view.py]
        B7_3[dialogs.py]
        B7_4[dashboard.py]
        B7_5[search_modal.py]
    end

    B7 --> B7_1
    B7 --> B7_2
    B7 --> B7_3
    B7 --> B7_4
    B7 --> B7_5

    subgraph "docs/"
        C1[classflow.md]
        C2[tickets.md]
        C3[classDiagram.drawio.png]
        C4[project_charts.md]
    end

    C --> C1
    C --> C2
    C --> C3
    C --> C4

    subgraph "data/"
        D1[medicines.json]
        D2[shelves.json]
    end

    D --> D1
    D --> D2
```