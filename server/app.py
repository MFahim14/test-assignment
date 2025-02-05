from flask import Flask, request, jsonify
import sqlite3
import logging
import time
import os

app = Flask(__name__)

DATABASE = os.path.abspath("inventory.db")
print(f"Using database at: {DATABASE}")


# Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Function to connect to SQLite
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Create database if not exists
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

# ✅ Home route
@app.route("/")
def home():
    return "Flask Server is Running!", 200

# ✅ Favicon route (Prevents unnecessary requests from browsers)
@app.route("/favicon.ico")
def favicon():
    return '', 204

# ✅ Fetch inventory
@app.route("/inventory", methods=["GET"])
def get_inventory():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity FROM inventory")
        rows = cursor.fetchall()
        inventory = [{"name": row["name"], "quantity": row["quantity"]} for row in rows]
    return jsonify(inventory), 200

# ✅ Add an item to inventory
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

# ✅ Remove an item
@app.route("/remove-item", methods=["POST"])
def remove_item():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE name = ?", (data["name"],))
        conn.commit()
    return jsonify({"message": "Item removed"}), 200

# ✅ Update item quantity
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

# ✅ Apply translation
@app.route("/translation", methods=["POST"])
def apply_translation():
    data = request.json
    logging.info(f"Received translation data: {data}")
    return jsonify({"message": "Translation applied", "position": data["translation"]}), 200

# ✅ Apply rotation
@app.route("/rotation", methods=["POST"])
def apply_rotation():
    data = request.json
    logging.info(f"Received rotation data: {data}")
    return jsonify({"message": "Rotation applied", "rotation": data["rotation"]}), 200

# ✅ Apply scale
@app.route("/scale", methods=["POST"])
def apply_scale():
    data = request.json
    logging.info(f"Received scale data: {data}")
    return jsonify({"message": "Scale applied", "scale": data["scale"]}), 200

# ✅ Apply full transformation
@app.route("/transform", methods=["POST"])
def transform():
    """Handles full transform data (position, rotation, scale)"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    time.sleep(10)  # Simulated delay
    app.logger.info(f"Received transform data: {data}")
    return jsonify({"message": "Transform data received", "data": data}), 200

# ✅ Initialize database
init_db()

if __name__ == "__main__":
    app.run(debug=True)
