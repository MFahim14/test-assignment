# DCC Plugin with Flask Server and PyQt UI

## Overview
This project integrates a Blender plugin, a Flask server, a SQLite database, and a PyQt UI to manage object transformations and inventory data efficiently. The plugin allows users to select objects and apply transformations while sending relevant data to the local server. The Flask server handles transformation requests and inventory management, while the PyQt UI provides an interactive way to view and modify inventory data.

## Project Structure
```
test-assignment
│── /server
│   │── app.py          # Flask server handling requests
│── /blender_plugin
│   │── __init__.py     # Plugin registration
│   │── operators.py    # Operators for transformations
│   │── ui.py           # Blender UI elements
│── /ui
│   │── ui.py           # PyQt UI for inventory management
│
│── main.py             # Entry point (if applicable)
│── requirements.txt    # Dependencies
│── inventory.db        # SQLite database file
│── README.md           # Project documentation
```

## Features
### Part 1: Blender Plugin
- Object selection within Blender.
- Transform controls for position, rotation, and scale.
- Endpoint dropdown to choose server functions.
- Submit button to send transform data to the server.
- Synchronization of UI fields when an object’s transform is updated.

### Part 2: Flask Server
- API Endpoints:
  - `/transform`: Receives full transformation data.
  - `/translation`: Receives only position data.
  - `/rotation`: Receives only rotation data.
  - `/scale`: Receives only scale data.
  - `/file-path`: Retrieves the DCC file path.
  - `/add-item`: Adds an inventory item.
  - `/remove-item`: Removes an inventory item.
  - `/update-quantity`: Updates an item’s quantity.
- Logs requests and responses.
- Introduces a 10-second delay to simulate real-world processing.
- Returns appropriate status codes.

### Part 3: SQLite Database
- Stores inventory items and quantities.
- Integrated with the Flask server for real-time updates.

### Part 4: PyQt UI
- Displays the inventory from the SQLite database.
- Buttons for purchasing and returning items.
- Non-blocking UI that remains responsive during server communication.

## Installation
### Prerequisites
- Blender 4.3.2
- Python 3.8+
- Flask
- SQLite
- PyQt5
- Requests

### Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the Flask server:
   ```sh
   python main.py
   ```
3. Install the Blender plugin:
   - Navigate to `Edit > Preferences > Add-ons > Install` in Blender.
   - Select the zipped `blender_plugin/` directory.
   - Enable the plugin.

## **Usage**

### **1. Transform Objects in Blender**
- Select an object
- Apply transformations (position, rotation, scale).
- Send transformation data to the Flask server.

### **2. Manage Inventory in PyQt UI**
- View inventory items.
- Perform operations (add-item, remove, update-item).

## **Code Explanation**

# **1. main.py**

## Overview
`main.py` is the entry point for the project. It is responsible for launching the Flask server and the PyQt UI while ensuring that they start in the correct order. The script handles process management and clean shutdowns.

## Code Breakdown

### Importing Required Modules
```python
import subprocess
import time
```
- `subprocess`: This module allows us to create and manage additional processes.
- `time`: Used to introduce a delay to ensure the Flask server starts properly before the UI launches.

### Starting the Flask Server
```python
flask_process = subprocess.Popen(["python", "server/app.py"])
```
- `subprocess.Popen()` starts the Flask server by running `app.py` inside the `server/` directory.
- This runs in the background, allowing the script to continue execution.

### Waiting for the Server to Start
```python
time.sleep(5)
```
- Introduces a 5-second delay to allow the Flask server to initialize before launching the UI.
- Ensures the UI does not attempt to connect to a server that hasn't started yet.

### Launching the PyQt UI
```python
ui_process = subprocess.Popen(["python", "ui/ui.py"])
```
- Starts the PyQt-based UI by running `ui.py` inside the `ui/` directory.
- This UI is used to manage inventory data and interact with the server.

### Keeping the Script Running
```python
try:
    flask_process.wait()
    ui_process.wait()
```
- Waits for both the Flask server and the UI process to complete execution.
- Ensures that the script does not exit immediately after starting the processes.

### Handling Shutdown Gracefully
```python
except KeyboardInterrupt:
    print("Shutting down...")
    flask_process.terminate()
    ui_process.terminate()
```
- Detects when the user interrupts execution (e.g., by pressing `Ctrl+C`).
- Terminates both the Flask server and UI processes to ensure a clean shutdown.

# **2. app.py**

## Overview
This Flask-based server manages object transformations and inventory data. It provides endpoints for handling transformations (position, rotation, scale), inventory management, and basic API operations.

## Dependencies
- Flask: Web framework for building APIs.
- SQLite: Lightweight database for inventory storage.
- Logging: To log API requests and debug information.
- OS: To handle file paths and ensure the database is accessible.
- Time: Simulated delay for API responses.

## Code Breakdown

### 1. Initial Setup
```python
from flask import Flask, request, jsonify
import sqlite3
import logging
import time
import os
```
- **Flask**: Imports necessary functions for creating API endpoints.
- **SQLite3**: Used for handling inventory database operations.
- **Logging**: Configured to record API interactions.
- **Time**: Introduces artificial delays to mimic real-world processing time.
- **OS**: Determines the absolute path for the SQLite database file.

```python
app = Flask(__name__)
DATABASE = os.path.abspath("inventory.db")
print(f"Using database at: {DATABASE}")
```
- Initializes the Flask application.
- Defines the path to the database file and prints it for debugging purposes.

### 2. Database Connection
```python
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
```
- Establishes a connection to the SQLite database.
- Configures the connection to return rows as dictionaries.

### 3. Database Initialization
```python
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            quantity INTEGER
        )
        """)
        conn.commit()
```
- Ensures the `inventory` table exists before the server starts.
- The table contains an ID, name, and quantity field.

### 4. API Endpoints
#### Home Route
```python
@app.route("/")
def home():
    return "Flask Server is Running!", 200
```
- A simple route that confirms the server is active.

#### Prevent Unnecessary Requests
```python
@app.route("/favicon.ico")
def favicon():
    return '', 204
```
- Avoids redundant browser requests for the favicon.

#### Fetch Inventory
```python
@app.route("/inventory", methods=["GET"])
def get_inventory():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity FROM inventory")
        rows = cursor.fetchall()
        inventory = [{"name": row["name"], "quantity": row["quantity"]} for row in rows]
    return jsonify(inventory), 200
```
- Retrieves and returns all inventory items from the database.

#### Add Item
```python
@app.route("/add-item", methods=["POST"])
def add_item():
    data = request.json
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (data["name"], data["quantity"]))
            conn.commit()
        return jsonify({"message": "Item added"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Item already exists"}), 400
```
- Adds a new item to the inventory.
- Ensures duplicate items are not allowed.

#### Remove Item
```python
@app.route("/remove-item", methods=["POST"])
def remove_item():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE name = ?", (data["name"],))
        conn.commit()
    return jsonify({"message": "Item removed"}), 200
```
- Removes an item based on the provided name.

#### Update Item Quantity
```python
@app.route("/update-quantity", methods=["POST"])
def update_quantity():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET quantity = ? WHERE name = ?", (data["quantity"], data["name"]))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Quantity updated"}), 200
```
- Updates the quantity of an existing item.
- Returns an error if the item is not found.

### 5. Object Transformations
#### Apply Translation
```python
@app.route("/translation", methods=["POST"])
def apply_translation():
    data = request.json
    logging.info(f"Received translation data: {data}")
    return jsonify({"message": "Translation applied", "position": data["translation"]}), 200
```
- Accepts and logs translation data.

#### Apply Rotation
```python
@app.route("/rotation", methods=["POST"])
def apply_rotation():
    data = request.json
    logging.info(f"Received rotation data: {data}")
    return jsonify({"message": "Rotation applied", "rotation": data["rotation"]}), 200
```
- Accepts and logs rotation data.

#### Apply Scale
```python
@app.route("/scale", methods=["POST"])
def apply_scale():
    data = request.json
    logging.info(f"Received scale data: {data}")
    return jsonify({"message": "Scale applied", "scale": data["scale"]}), 200
```
- Accepts and logs scale data.

#### Apply Full Transformation
```python
@app.route("/transform", methods=["POST"])
def transform():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    time.sleep(10)  # Simulated delay
    app.logger.info(f"Received transform data: {data}")
    return jsonify({"message": "Transform data received", "data": data}), 200
```
- Handles full transformation data, including position, rotation, and scale.
- Introduces a 10-second delay to simulate real-world processing time.

### 6. Run the Server
```python
if __name__ == "__main__":
    app.run(debug=True)
```
- Starts the Flask server in debug mode.

# **3. ui.py (PyQt UI for Inventory Management)**

## Overview
The `ui.py` file implements a PyQt5-based graphical user interface for managing inventory. It allows users to:
- View current inventory items.
- Add new items with a specified quantity.
- Remove existing items from inventory.
- Update the quantity of an existing item.
- (Commented Out) Transformation-related functionality, such as translation, rotation, and scaling.

This UI interacts with the local Flask server (`app.py`) via HTTP requests.

---

## Code Breakdown

### 1. **Imports and Setup**
```python
import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import QThread, pyqtSignal
```
- **PyQt5 Modules**: Used to create the UI components.
- **Requests Module**: Handles HTTP requests to communicate with the Flask server.
- **QThread & pyqtSignal**: Allows running tasks in a separate thread to prevent UI freezing.

### 2. **Defining the Server URL**
```python
SERVER_URL = "http://127.0.0.1:5000"
```
- The UI connects to a locally running Flask server.

### 3. **Creating the `InventoryApp` Class**
```python
class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
```
- The `InventoryApp` class extends `QWidget`, which provides the main application window.
- The `init_ui` function initializes the UI components.

### 4. **Building the UI Layout**
```python
layout = QVBoxLayout()
```
- Uses a vertical layout (`QVBoxLayout`) to arrange UI elements from top to bottom.

#### **Inventory Table**
```python
self.table = QTableWidget()
self.table.setColumnCount(2)
self.table.setHorizontalHeaderLabels(["Name", "Quantity"])
layout.addWidget(self.table)
```
- Displays inventory items in a table with two columns: "Name" and "Quantity".

#### **Buttons & Inputs**
- `Refresh Inventory`
- `Add Item`
- `Remove Item`
- `Update Quantity`

Each button triggers a function that interacts with the Flask API.

### 5. **Fetching and Displaying Inventory Data**
```python
def refresh_inventory(self):
    self.worker = Worker(self.fetch_inventory)
    self.worker.result_signal.connect(self.update_table)
    self.worker.start()
```
- Uses a separate thread to fetch data from the server (`Worker` class).
- Calls `fetch_inventory`, which makes a GET request to `/inventory`.

```python
def update_table(self, data):
    self.table.setRowCount(0)
    for item in data:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
        self.table.setItem(row, 1, QTableWidgetItem(str(item["quantity"])))
```
- Updates the table with the fetched inventory data.

### 6. **Adding, Removing, and Updating Items**
- Each function sends a POST request to the corresponding API endpoint.

```python
def add_item(self):
    name = self.name_input.text().strip()
    quantity = self.quantity_input.text().strip()
    if name and quantity.isdigit():
        self.worker = Worker(self.send_request, "add-item", {"name": name, "quantity": int(quantity)})
        self.worker.finished.connect(self.refresh_inventory)
        self.worker.start()
```
- Retrieves user input and sends a request to the `/add-item` endpoint.
- Calls `refresh_inventory` after completion to update the table.

### 7. **Background Threading with `Worker`**
```python
class Worker(QThread):
    result_signal = pyqtSignal(list)

    def __init__(self, func, *args):
        super().__init__()
        self.func, self.args = func, args

    def run(self):
        result = self.func(*self.args)
        self.result_signal.emit(result if result is not None else [])
```
- Runs API requests in a background thread to prevent UI lag.
- Emits results back to the main thread using `result_signal`.

### 8. **Running the Application**
```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())
```
- Initializes and runs the PyQt application.

---
# **4. __init__.py (Blender)**

This module initializes the DCC Plugin for Blender, allowing it to send object transformation data to a Flask server.

## Plugin Information

```python
bl_info = {
    "name": "DCC Plugin",
    "blender": (4, 3, 2),
    "category": "Object",
    "author": "Mohammed Fahim A",
    "version": (1, 0),
    "location": "View3D > Sidebar > DCC Plugin",
    "description": "Send object transformation data to a Flask server",
    "support": "COMMUNITY"
}
```

### Overview
- **Registers** operators for applying transformations (Translation, Rotation, Scale, and Full Transform) to objects.
- **Creates** a UI panel in Blender’s sidebar for easy access.
- **Interacts** with a Flask server by sending transformation data.

## Code Explanation

### Imports
```python
import bpy
from .operators import (
    TransformOperator, TranslationOperator, RotationOperator, ScaleOperator
)
from .ui import DCC_PT_Panel  # Import the UI panel
```
- `bpy`: Blender’s Python API for registering classes and handling transformations.
- `operators`: Custom transformation operators (handled in `operators.py`).
- `ui`: UI panel class (from `ui.py`).

### Class Registration
```python
classes = [
    TransformOperator, TranslationOperator, RotationOperator, ScaleOperator,
    DCC_PT_Panel  # Add UI panel here
]
```
- Stores all classes that need to be registered in Blender.

### Register & Unregister Functions
```python
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```
- `register()`: Registers each class in Blender when the plugin is loaded.
- `unregister()`: Unregisters classes when the plugin is disabled.

### Main Execution
```python
if __name__ == "__main__":
    register()
```
- Ensures the plugin is registered when executed directly.

# **5. ui.py (Blender UI)**

## Overview
This script defines the UI panel for the Blender plugin, allowing users to apply transformations (translation, rotation, scale) directly from the Blender UI. It is implemented using the Blender Python API.

## Code Explanation

```python
import bpy
```
This imports Blender's Python API, `bpy`, which is necessary to interact with Blender’s UI and operations.

### Creating the UI Panel
```python
class DCC_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport sidebar"""
    bl_label = "DCC Plugin"
    bl_idname = "DCC_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DCC Plugin"
```
- Defines a custom panel called `DCC_PT_Panel`.
- `bl_label`: Name of the panel displayed in Blender.
- `bl_idname`: Internal identifier for the panel.
- `bl_space_type`: Specifies that the panel appears in the 3D Viewport.
- `bl_region_type`: Indicates it will be shown in the UI sidebar.
- `bl_category`: Defines the tab name in the sidebar where the panel appears.

### Adding UI Elements
```python
    def draw(self, context):
        layout = self.layout
        layout.operator("object.apply_transform", text="Apply Transform")
        layout.operator("object.apply_translation", text="Apply Translation")
        layout.operator("object.apply_rotation", text="Apply Rotation")
        layout.operator("object.apply_scale", text="Apply Scale")
```
- `draw(self, context)`: This function defines how the panel is drawn.
- `layout.operator()`: Adds buttons for different transformation actions.
- Each button calls a corresponding operator (defined in `operators.py`) when clicked.

### Registering the UI Panel in Blender
```python
# Blender Registration
def register():
    bpy.utils.register_class(DCC_PT_Panel)

def unregister():
    bpy.utils.unregister_class(DCC_PT_Panel)
```
- `register()`: Registers the panel so it appears in Blender.
- `unregister()`: Removes the panel when the plugin is disabled.

# **5. operators.py**

# Operators for Blender DCC Plugin

## Overview
This script provides a set of **Blender Operators** that send object transformation data (translation, rotation, scale) to an external **Flask server**. Additionally, it supports basic inventory management operations such as **adding, removing, and updating items**.

## Features
- **Send transformation data** (position, rotation, scale) to a Flask server.
- **UI integration**: Operators can be accessed through Blender’s interface.
- **Inventory management**: Supports add, remove, and update item operations.

---

## Code Explanation

### 1. Import Required Modules
```python
import bpy
import requests
```
- `bpy`: Blender's Python API to interact with objects in the scene.
- `requests`: Used to send HTTP requests to the Flask server.

---

### 2. Define Flask Server URL
```python
FLASK_SERVER_URL = "http://127.0.0.1:5000"  # Update if hosted elsewhere
```
- Defines the **Flask server** URL where transformation data will be sent.

---

### 3. Function to Send HTTP Requests
```python
def send_request(endpoint, data):
    """Sends a request to the Flask server."""
    url = f"{FLASK_SERVER_URL}/{endpoint}"
    try:
        response = requests.post(url, json=data)
        print(f"Response from {endpoint}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send request: {e}")
```
- `send_request(endpoint, data)`: Sends **POST requests** to the Flask server with JSON data.
- Handles exceptions if the request fails.

---

### 4. Get Active Object in Blender
```python
def get_active_object():
    """Returns the active Blender object."""
    obj = bpy.context.active_object
    if obj is None:
        print("No active object selected.")
    return obj
```
- Retrieves the currently selected object in Blender.
- If no object is selected, it prints a warning message.

---

### 5. Refresh Blender UI
```python
def refresh_ui():
    """Forces Blender's UI to update."""
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
```
- Ensures the Blender UI updates after an operation.

---

### 6. Transformation Operators

#### Apply Transform
```python
class TransformOperator(bpy.types.Operator):
    """Send Transform Data"""
    bl_idname = "object.apply_transform"
    bl_label = "Apply Transform"

    def execute(self, context):
        obj = get_active_object()
        if not obj:
            return {'CANCELLED'}
        
        transform_data = {
            "position": list(obj.location),
            "rotation": list(obj.rotation_euler),
            "scale": list(obj.scale)
        }
        
        send_request("transform", transform_data)
        refresh_ui()
        return {'FINISHED'}
```
- **Captures the object's** position, rotation, and scale.
- Sends the data to the Flask server using `send_request()`.
- Updates the Blender UI.

#### Apply Translation
```python
class TranslationOperator(bpy.types.Operator):
    """Send Position Data"""
    bl_idname = "object.apply_translation"
    bl_label = "Apply Translation"
```
- **Sends only the object's position** to the Flask server.

#### Apply Rotation
```python
class RotationOperator(bpy.types.Operator):
    """Send Rotation Data"""
    bl_idname = "object.apply_rotation"
    bl_label = "Apply Rotation"
```
- **Sends only the object's rotation** to the Flask server.

#### Apply Scale
```python
class ScaleOperator(bpy.types.Operator):
    """Send Scale Data"""
    bl_idname = "object.apply_scale"
    bl_label = "Apply Scale"
```
- **Sends only the object's scale** to the Flask server.

---

### 7. Inventory Management Operators

#### Add Item
```python
class AddItemOperator(bpy.types.Operator):
    """Send Add Item Request"""
    bl_idname = "object.add_item"
    bl_label = "Add Item"
```
- Sends the object's **name and position** to the server to add it to inventory.

#### Remove Item
```python
class RemoveItemOperator(bpy.types.Operator):
    """Send Remove Item Request"""
    bl_idname = "object.remove_item"
    bl_label = "Remove Item"
```
- Sends the object's **name** to remove it from inventory.

#### Update Item
```python
class UpdateItemOperator(bpy.types.Operator):
    """Send Update Item Request"""
    bl_idname = "object.update_item"
    bl_label = "Update Item"
```
- Sends the object's **updated position** to the server.

---

### 8. Registering Operators in Blender
```python
def register():
    bpy.utils.register_class(TransformOperator)
    bpy.utils.register_class(TranslationOperator)
    bpy.utils.register_class(RotationOperator)
    bpy.utils.register_class(ScaleOperator)
    bpy.utils.register_class(AddItemOperator)
    bpy.utils.register_class(RemoveItemOperator)
    bpy.utils.register_class(UpdateItemOperator)
```
- Registers all the operators so they can be used in Blender.

```python
def unregister():
    bpy.utils.unregister_class(TransformOperator)
    bpy.utils.unregister_class(TranslationOperator)
    bpy.utils.unregister_class(RotationOperator)
    bpy.utils.unregister_class(ScaleOperator)
    bpy.utils.unregister_class(AddItemOperator)
    bpy.utils.unregister_class(RemoveItemOperator)
    bpy.utils.unregister_class(UpdateItemOperator)
```
- Unregisters all the operators.

```python
if __name__ == "__main__":
    register()
```
- Runs `register()` when the script is executed.

---

## How to Use
1. **Ensure the Flask server is running**:
   ```sh
   python server.py
   ```
2. **Load the script in Blender** and register the operators.
3. **Use the Blender UI** (`View3D > Sidebar > DCC Plugin`) to apply transformations and manage inventory.

---


