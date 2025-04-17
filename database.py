import sqlite3
import os

# Always use absolute path to avoid permission issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'data.db')
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn
DATABASE = 'data.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, args)
    results = cursor.fetchall()
    conn.close()
    return (results[0] if results else None) if one else results

def execute_db(query, args=()):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    conn.close()

def get_user_by_username(username):
    return query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)

def get_all_suppliers():
    return query_db("SELECT id, name FROM suppliers")

def get_supplier_by_id(supplier_id):
    return query_db("SELECT id, name FROM suppliers WHERE id = ?", (supplier_id,), one=True)

def get_products_by_supplier(supplier_id):
    return query_db("SELECT id, name, price FROM products WHERE supplier_id = ?", (supplier_id,))

def insert_order(user_id, total_amount, order_items_data):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", (user_id, total_amount))
        order_id = cursor.lastrowid
        for item in order_items_data:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)",
                (order_id, item['product_id'], item['quantity'], item['price'])
            )
        conn.commit()
        return order_id
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()