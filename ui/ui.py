import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import QThread, pyqtSignal

SERVER_URL = "http://127.0.0.1:5000"

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Inventory & Transformation Management")
        self.setGeometry(100, 100, 600, 600)
        layout = QVBoxLayout()

        # -------- INVENTORY MANAGEMENT --------
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Quantity"])
        layout.addWidget(self.table)

        self.refresh_button = QPushButton("Refresh Inventory")
        self.refresh_button.clicked.connect(self.refresh_inventory)
        layout.addWidget(self.refresh_button)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        layout.addWidget(self.name_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        layout.addWidget(self.quantity_input)

        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        self.remove_name_input = QLineEdit()
        self.remove_name_input.setPlaceholderText("Item Name to Remove")
        layout.addWidget(self.remove_name_input)

        self.remove_button = QPushButton("Remove Item")
        self.remove_button.clicked.connect(self.remove_item)
        layout.addWidget(self.remove_button)

        self.update_name_input = QLineEdit()
        self.update_name_input.setPlaceholderText("Item Name to Update")
        layout.addWidget(self.update_name_input)

        self.update_quantity_input = QLineEdit()
        self.update_quantity_input.setPlaceholderText("New Quantity")
        layout.addWidget(self.update_quantity_input)

        self.update_button = QPushButton("Update Quantity")
        self.update_button.clicked.connect(self.update_item)
        layout.addWidget(self.update_button)

        # -------- TRANSFORMATION SECTION --------
        layout.addWidget(QLabel("Transformation Data"))

        # Translation
        translation_layout = QHBoxLayout()
        self.translation_x_input = QLineEdit()
        self.translation_x_input.setPlaceholderText("X")
        translation_layout.addWidget(self.translation_x_input)
        self.translation_y_input = QLineEdit()
        self.translation_y_input.setPlaceholderText("Y")
        translation_layout.addWidget(self.translation_y_input)
        self.translation_z_input = QLineEdit()
        self.translation_z_input.setPlaceholderText("Z")
        translation_layout.addWidget(self.translation_z_input)
        self.translation_button = QPushButton("Send Translation")
        self.translation_button.clicked.connect(self.send_translation)
        translation_layout.addWidget(self.translation_button)
        layout.addLayout(translation_layout)

        # Rotation
        rotation_layout = QHBoxLayout()
        self.rotation_x_input = QLineEdit()
        self.rotation_x_input.setPlaceholderText("X")
        rotation_layout.addWidget(self.rotation_x_input)
        self.rotation_y_input = QLineEdit()
        self.rotation_y_input.setPlaceholderText("Y")
        rotation_layout.addWidget(self.rotation_y_input)
        self.rotation_z_input = QLineEdit()
        self.rotation_z_input.setPlaceholderText("Z")
        rotation_layout.addWidget(self.rotation_z_input)
        self.rotation_button = QPushButton("Send Rotation")
        self.rotation_button.clicked.connect(self.send_rotation)
        rotation_layout.addWidget(self.rotation_button)
        layout.addLayout(rotation_layout)

        # Scale
        scale_layout = QHBoxLayout()
        self.scale_x_input = QLineEdit()
        self.scale_x_input.setPlaceholderText("X")
        scale_layout.addWidget(self.scale_x_input)
        self.scale_y_input = QLineEdit()
        self.scale_y_input.setPlaceholderText("Y")
        scale_layout.addWidget(self.scale_y_input)
        self.scale_z_input = QLineEdit()
        self.scale_z_input.setPlaceholderText("Z")
        scale_layout.addWidget(self.scale_z_input)
        self.scale_button = QPushButton("Send Scale")
        self.scale_button.clicked.connect(self.send_scale)
        scale_layout.addWidget(self.scale_button)
        layout.addLayout(scale_layout)

        self.setLayout(layout)
        self.refresh_inventory()

    # ------------- Inventory Functions -------------
    def refresh_inventory(self):
        self.worker = Worker(self.fetch_inventory)
        self.worker.result_signal.connect(self.update_table)
        self.worker.start()

    def fetch_inventory(self):
        try:
            response = requests.get(f"{SERVER_URL}/inventory")
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching inventory: {e}")
            return []

    def update_table(self, data):
        self.table.setRowCount(0)
        for item in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["quantity"])))

    def add_item(self):
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        if name and quantity.isdigit():
            self.worker = Worker(self.send_request, "add-item", {"name": name, "quantity": int(quantity)})
            self.worker.finished.connect(self.refresh_inventory)  # Refresh UI after adding
            self.worker.start()

    def remove_item(self):
        name = self.remove_name_input.text().strip()
        if name:
            self.worker = Worker(self.send_request, "remove-item", {"name": name})
            self.worker.finished.connect(self.refresh_inventory)  # Refresh UI after removing
            self.worker.start()

    def update_item(self):
        name = self.update_name_input.text().strip()
        quantity = self.update_quantity_input.text().strip()
        if name and quantity.isdigit():
            self.worker = Worker(self.send_request, "update-quantity", {"name": name, "quantity": int(quantity)})
            self.worker.finished.connect(self.refresh_inventory)  # Refresh UI after updating
            self.worker.start()


    # ------------- Transformation Functions -------------
    def send_translation(self):
        self.send_transformation("translation", ["translation_x_input", "translation_y_input", "translation_z_input"], "position")

    def send_rotation(self):
        self.send_transformation("rotation", ["rotation_x_input", "rotation_y_input", "rotation_z_input"], "rotation")

    def send_scale(self):
        self.send_transformation("scale", ["scale_x_input", "scale_y_input", "scale_z_input"], "scale")

    def send_transformation(self, endpoint, input_fields, key):
        data = {key: [float(getattr(self, field).text().strip() or 0) for field in input_fields]}
        self.worker = Worker(self.send_request, endpoint, data)
        self.worker.start()

    def send_request(self, endpoint, data):
        try:
            response = requests.post(f"{SERVER_URL}/{endpoint}", json=data)
            if response.status_code == 200:
                print(f"{endpoint.capitalize()} applied successfully: {response.json()}")
            else:
                print(f"Error applying {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"Error applying {endpoint}: {e}")

class Worker(QThread):
    result_signal = pyqtSignal(list)

    def __init__(self, func, *args):
        super().__init__()
        self.func, self.args = func, args

    def run(self):
        result = self.func(*self.args)
        self.result_signal.emit(result if result is not None else [])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())
