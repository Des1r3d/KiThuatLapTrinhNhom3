### **To: UI/UX Design Team**
### **From: Development Team**
### **Subject: Design Brief for Pharmacy Management System**

This document provides a detailed breakdown of the required user interface components and user experience flows for the new Pharmacy Management System. The application should be modern, clean, and intuitive for pharmacists.

### **1. Core Design Principles & Application Shell**

-   **Technology:** The front-end will be built entirely using **PyQt6**.
-   **Aesthetic:** A modern, flat design is preferred. Please provide style guidelines (QSS/CSS) for both a **Light Theme** and a **Dark Theme**.
-   **Main Window Layout:** The application will have a standard three-part layout:
    1.  **Sidebar (Left):** A `QListWidget` or similar for primary navigation.
    2.  **Main Area (Center):** A `QStackedWidget` that displays the active view based on the sidebar selection.
    3.  **Status Bar (Bottom):** A bar to show persistent information like total medicine count and important alerts.

-   **Navigation:** The sidebar should contain the following items:
    -   **Dashboard** (Default view)
    -   **Inventory**
    -   **Reports** (Future Scope)
    -   **Settings** (Future Scope)

-   **Keyboard Shortcuts:** The following global shortcuts must be supported:
    -   `Ctrl+K`: Opens the **Global Search Modal**.
    -   `Ctrl+N`: Opens the **Add Medicine Dialog**.
    -   `Ctrl+D`: Toggles between **Light and Dark themes**.

### **2. View 1: The Dashboard (Primary Surface)**

**Purpose:** To provide a high-level, "at-a-glance" overview of the inventory's status. This is the first screen the user sees and should immediately highlight critical information.

**Required Components:**

#### **A. Key Performance Indicator (KPI) Cards**
A set of prominent, easy-to-read summary cards at the top of the view. Each card should have a large number and a clear label.
-   **Total Inventory:** Total count of unique medicine types.
-   **Expiring Soon:** Count of medicines expiring within the next 30 days. This card should have a **yellow** accent color.
-   **Expired Medicines:** Count of already expired medicines. This card should have a **red** accent color.
-   **Low Stock:** Count of medicines with quantity below a threshold (e.g., 5 units). This card should have an **orange** or **yellow** accent color.

#### **B. Charts & Visualizations (Matplotlib Integration)**
The dashboard will feature two primary charts embedded within the PyQt6 UI.

1.  **Expiry Status Distribution (Pie Chart):**
    -   **Purpose:** To show the proportion of the inventory based on expiry status.
    -   **Slices/Data:**
        -   `Normal` (In date): Represents medicines not expiring within 30 days. (Suggested color: **Green**)
        -   `Expiring Soon` (0-30 days): (Suggested color: **Yellow**)
        -   `Expired` (< 0 days): (Suggested color: **Red**)
    -   **Labels:** Each slice should be clearly labeled with the category and percentage.

2.  **Top 10 Medicines by Stock (Bar Chart):**
    -   **Purpose:** To quickly identify the most abundant items in the inventory.
    -   **X-Axis:** Medicine Names.
    -   **Y-Axis:** Quantity.
    -   **Design:** A simple vertical bar chart, sorted in descending order of quantity.

#### **C. Actionable Lists**
Two small list/table widgets to provide direct access to critical items without needing to navigate to the full inventory view.
1.  **"Approaching Expiry" List:**
    -   Displays the top 5-10 medicines closest to their expiry date.
    -   **Columns:** Medicine Name, Expiry Date, Days Left.
    -   **Interaction:** Clicking an item should navigate to and highlight it in the main `Inventory View`.

2.  **"Low Stock Items" List:**
    -   Displays the top 5-10 medicines with the lowest quantity.
    -   **Columns:** Medicine Name, Quantity, Shelf Location.
    -   **Interaction:** Clicking an item should navigate to and highlight it in the main `Inventory View`.

#### **D. Controls**
-   **Refresh Button:** A button to manually reload all dashboard data and charts.

---

### **3. View 2: Inventory Management**

**Purpose:** The primary workspace for viewing, adding, editing, and deleting medicine records.

**Required Components:**

-   **Main Component:** A full-featured table (`QTableView`).
-   **Table Columns:** The table must display:
    -   `Name`
    -   `Quantity`
    -   `Expiry Date`
    -   `Shelf` (Location ID)
    -   `Price`
    -   `Status` (A derived field, e.g., "Expired", "Low Stock")
-   **Sorting & Filtering:** All columns should be sortable. A search/filter bar above the table to filter by name is required.
-   **Conditional Formatting:** Table rows must be color-coded for quick identification:
    -   **Red Row:** Medicine is expired.
    -   **Yellow Row:** Medicine is expiring soon (within 30 days).
    -   **Default Row:** Normal status.
-   **Interaction:**
    -   **Double-Click** on a row opens the **Edit Medicine Dialog** for that item.
    -   **Right-Click** on a row opens a context menu with `Edit` and `Delete` options.
    -   An **"Add Medicine" button** (`+` icon) should be present on this view to open the Add Medicine Dialog.

---

### **4. Component: Add/Edit Medicine Dialog**

**Purpose:** A modal form (`QDialog`) for data entry.

**Required Fields:**
-   **Name:** `QLineEdit`
-   **Quantity:** `QSpinBox` (non-negative values).
-   **Expiry Date:** `QDateEdit` with a calendar pop-up.
-   **Shelf:** `QComboBox` populated with available shelf locations.
-   **Price:** `QLineEdit` or `QDoubleSpinBox`.
-   **Buttons:** `Save` and `Cancel`. The `Save` button should be disabled until all required fields are valid.

---

### **5. Component: Global Search Modal**

**Purpose:** A fast, system-wide search accessible from anywhere via `Ctrl+K`.

**Required Components:**
-   **Layout:** A simple, non-blocking modal (`QDialog`) with a single `QLineEdit` at the top and a `QListWidget` below it.
-   **Behavior:**
    -   When the user types into the `QLineEdit`, the `QListWidget` immediately updates with fuzzy search results.
    -   Each result item should display the **Medicine Name** and the **match score** (e.g., "Paracetamol 500mg (95%)").
    -   Selecting a result from the list closes the modal, switches the main view to **Inventory**, and highlights the selected medicine in the table.
