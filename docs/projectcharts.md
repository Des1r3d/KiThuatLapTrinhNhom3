# Project Charts: Pharmacy Management System

This document outlines key architectural and flow diagrams for the Pharmacy Management System, providing a visual overview of its structure and functionality. These diagrams are generated using Mermaid syntax, which can be rendered by many Markdown viewers and documentation tools.

---

## 1. Component Architecture Diagram

This diagram illustrates the high-level organization of the Pharmacy Management System into distinct layers and components, showing their primary relationships and dependencies.

```mermaid
graph TD
    App[Main Application] --> UI[UI Layer (PyQt6)]

    UI --> Logic[Business Logic]
    Logic --> Data[Data Access Layer]

    UI --> Dashboard[Dashboard View]
    UI --> InventoryView[Inventory View]
    UI --> SearchBar[Global Search (Ctrl+K)]
    UI --> Reports[Reports (Matplotlib)]

    Logic --> InvMgr[Inventory Manager]
    Logic --> SearchEng[Search Engine]
    Logic --> AlertSys[Expiry Alert System]

    Data --> JSON_Store[JSON Storage Engine]
    Data --> Models[Data Models]

    InvMgr --> Models
    SearchEng --> Models
    JSON_Store --> Files[(JSON Files)]
```

### Explanation:
-   **Main Application:** Đóng vai trò khởi tạo (bootstrap) hệ thống.
-   **UI Layer (PyQt6):** Xử lý tương tác người dùng và hiển thị thông tin. Gọi các chức năng từ lớp Business Logic. Gồm các chế độ xem như Dashboard, Inventory View, Global Search và Reports.
-   **Business Logic Layer:** Chứa các quy tắc nghiệp vụ và hoạt động cốt lõi, được quản lý bởi Inventory Manager, Search Engine và Alert System.
-   **Data Access Layer:** Chịu trách nhiệm về việc lưu trữ và truy cập dữ liệu, bao gồm JSON Storage Engine và các Data Models (Medicine, Shelf).
-   **Dependencies:** Các mũi tên chỉ ra luồng điều khiển hoặc dữ liệu. Cụ thể, `UI Layer` gọi `Business Logic`, và `Business Logic` gọi `Data Access Layer` khi cần thiết. Ví dụ, `InventoryManager` phụ thuộc vào `Data Models` và `StorageEngine`.

---

## 2. Logic Flow / Sequence Diagram (for a Key Use Case: Add Medicine)

This sequence diagram details the interaction between the user and various system components during the process of adding a new medicine entry.

```mermaid
sequenceDiagram
    participant User
    participant UI as UI Layer
    participant IM as InventoryManager
    participant SE as StorageEngine

    User->>UI: Clicks "Add Medicine"
    UI->>UI: MainWindow opens AddMedicineDialog
    User->>UI: Fills form & Clicks Save
    UI->>UI: Dialog validates input
    activate UI
    UI->>IM: Creates Medicine object & Calls add_medicine()
    activate IM
    IM->>IM: Validates medicine data (ID, quantity, shelf_id)
    IM->>IM: Appends medicine to list
    IM->>SE: Calls save_data() (indirectly via IM)
    activate SE
    SE->>SE: Converts medicines to dicts
    SE->>SE: Performs atomic write (backup, .tmp, rename)
    deactivate SE
    IM-->>UI: Emits 'medicine_added' signal
    deactivate IM
    UI->>UI: InventoryView reloads data
    UI->>UI: Table updates with new medicine
    UI->>UI: Status bar shows updated count
    UI->>UI: Dialog closes
    deactivate UI
```

### Explanation:
-   Biểu đồ này theo dõi quy trình "Thêm thuốc" từ khi người dùng khởi tạo đến khi cập nhật UI và lưu trữ dữ liệu.
-   **Người dùng và UI:** Người dùng tương tác với giao diện đồ họa.
-   **Xác thực ở UI:** UI thực hiện xác thực đầu vào cơ bản (UX-level validation) trước khi chuyển dữ liệu.
-   **UI gọi InventoryManager:** UI chuyển dữ liệu thuốc đã được xác thực sơ bộ cho `InventoryManager`.
-   **Vai trò của InventoryManager:** Xử lý logic nghiệp vụ, bao gồm xác thực quy tắc nghiệp vụ (business rule validation) chi tiết hơn và cập nhật danh sách thuốc nội bộ.
-   **InventoryManager gọi StorageEngine:** `InventoryManager` ủy quyền việc lưu trữ dữ liệu cho `StorageEngine` để lưu các thay đổi vào tệp JSON.
-   **Ghi dữ liệu nguyên tử của StorageEngine:** `StorageEngine` đảm bảo tính toàn vẹn dữ liệu bằng cách sử dụng tệp tạm thời và thao tác đổi tên nguyên tử.
-   **Phản hồi về UI:** Sau khi lưu thành công, `InventoryManager` phát tín hiệu để UI làm mới hiển thị, cập nhật bảng kho và thanh trạng thái.

---

## 3. Class Diagram

This diagram presents the core classes of the system, their attributes, key methods, and the relationships between them.

```mermaid
classDiagram
    class Medicine {
        +str id
        +str name
        +int quantity
        +date expiry_date
        +str shelf_id
        +float price
        +is_expired() bool
        +days_until_expiry() int
        +to_dict() dict
        +from_dict(dict) Medicine
    }

    class Shelf {
        +str id
        +str row
        +str column
        +str capacity
        +to_dict() dict
        +from_dict(dict) Shelf
    }

    class StorageEngine {
        +write_json(filepath, data)
        +read_json(filepath) dict
    }

    class InventoryManager {
        -List[Medicine] medicines
        -List[Shelf] shelves
        -StorageEngine storage
        +load_data()
        +save_data()
        +add_medicine(Medicine) Medicine
        +remove_medicine(str id) Medicine
        +update_medicine(str id, dict changes) Medicine
        +get_medicine(str id) Medicine
        +get_all_medicines() List~Medicine~
        +add_shelf(Shelf) Shelf
        +get_shelf(str id) Shelf
        +get_all_shelves() List~Shelf~
    }

    class SearchEngine {
        -List[Medicine] medicines
        -Dict~str, str~ name_index
        +index_data(List~Medicine~)
        +search(str query, int limit) List~Tuple~
        +get_suggestions(str partial_query, int limit) List~str~
        +clear_index()
        +update_index(List~Medicine~)
    }

    class AlertType {
        <<enum>>
        EXPIRED
        EXPIRING_SOON
        LOW_STOCK
        OUT_OF_STOCK
    }

    class Alert {
        +Medicine medicine
        +AlertType alert_type
        +str message
        +int severity
    }

    class AlertSystem {
        +int expiry_threshold
        +int low_stock_threshold
        +check_expiry(List~Medicine~) List~Medicine~
        +check_low_stock(List~Medicine~) List~Medicine~
        +check_expired(List~Medicine~) List~Medicine~
        +check_out_of_stock(List~Medicine~) List~Medicine~
        +generate_alerts(List~Medicine~) List~Alert~
        +get_alert_summary(List~Medicine~) dict
    }

    InventoryManager "1" *-- "many" Medicine
    InventoryManager "1" *-- "many" Shelf
    InventoryManager -- StorageEngine : uses >
    AlertSystem -- Medicine : checks >
    AlertSystem -- AlertType : uses >
    Alert --> Medicine : references
    Alert "1" *-- "1" AlertType : has
    SearchEngine -- Medicine : indexes >
```

### Explanation:
-   **Medicine & Shelf:** These are dataclasses representing the fundamental data entities, with methods for validation and serialization.
-   **StorageEngine:** Encapsulates the logic for reading and writing JSON data to files, ensuring data integrity.
-   **InventoryManager:** The central business logic component for managing `Medicine` and `Shelf` objects, performing CRUD operations and interacting with the `StorageEngine` for persistence.
-   **SearchEngine:** Provides fuzzy search capabilities for medicines using `TheFuzz` library, indexing medicine names for efficient querying.
-   **AlertType & Alert:** `AlertType` is an enumeration for different alert categories, and `Alert` is a dataclass representing a specific alert for a medicine.
-   **AlertSystem:** Monitors medicine inventory for expiry dates and stock levels, generating `Alert` objects based on defined thresholds.
    -   **Relationships:**
        -   `InventoryManager` aggregates `Medicine` và `Shelf` objects (được biểu thị bằng `*--`).
        -   `InventoryManager` sử dụng `StorageEngine` (được biểu thị bằng `-->`).
        -   `AlertSystem` và `SearchEngine` tương tác với các đối tượng `Medicine`.
        -   `Alert` objects `tham chiếu` đến `Medicine` (thay vì sở hữu), và được `kết hợp` với `AlertType`.
        -   *Lưu ý:* Thuộc tính `capacity` của `Shelf` hiện đang là kiểu `str` trong mã nguồn, nhưng nên được cân nhắc thay đổi thành `int` để đảm bảo tính toàn vẹn dữ liệu tốt hơn.
---

## 4. File Structure Diagram

This diagram provides a visual representation of the project's directory and file organization, highlighting the main modules.

```mermaid
graph TD
    A[Pharmacy Management System] --> B[src/]
    A --> C[tests/]
    A --> D[data/]
    A --> E[docs/]
    A --> F[.gitignore]
    A --> G[CLAUDE.md]
    A --> H[README.md]
    A --> I[requirements.txt]

    B --> B1[__init__.py]
    B --> B2[models.py]
    B --> B3[storage.py]
    B --> B4[inventory_manager.py]
    B --> B5[alerts.py]
    B --> B6[search_engine.py]

    C --> C1[__init__.py]
    C --> C2[test_alerts.py]
    C --> C3[test_inventory.py]
    C --> C4[test_models.py]
    C --> C5[test_search.py]
    C --> C6[test_storage.py]

    D --> D1[.gitkeep]

    E --> E1[classDiagram.drawio.png]
    E --> E2[classflow.md]
    E --> E3[design_docs.md]
    E --> E4[PROGRESS.md]
```

### Explanation:
-   **Root Directory:** Contains project-level files like `.gitignore`, `README.md`, and `requirements.txt`.
-   **`src/`:** Houses the main source code of the application, logically separated into modules for data models, storage, inventory management, alerts, and search.
-   **`tests/`:** Contains unit tests for each corresponding module in the `src/` directory, ensuring code quality and functionality.
-   **`data/`:** Intended for storing application data, such as JSON files for persistence (e.g., `medicines.json`, `shelves.json`).
-   **`docs/`:** Holds documentation files, including design documents, progress reports, and now, these project charts.