import sqlite3

DATABASE = 'data.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create suppliers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
    ''')

    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create order_items table (for many-to-many relationship between orders and products)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Insert dummy users
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('user1', 'pass1'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('user2', 'pass2'))

    # Insert dummy suppliers
    cursor.execute("INSERT OR IGNORE INTO suppliers (name) VALUES (?)", ('Supplier A',))
    cursor.execute("INSERT OR IGNORE INTO suppliers (name) VALUES (?)", ('Supplier B',))

    # Insert dummy products
    cursor.execute("INSERT OR IGNORE INTO products (supplier_id, name, price) VALUES (?, ?, ?)", (1, 'Product A1', 10.99))
    cursor.execute("INSERT OR IGNORE INTO products (supplier_id, name, price) VALUES (?, ?, ?)", (1, 'Product A2', 25.50))
    cursor.execute("INSERT OR IGNORE INTO products (supplier_id, name, price) VALUES (?, ?, ?)", (2, 'Product B1', 5.75))
    cursor.execute("INSERT OR IGNORE INTO products (supplier_id, name, price) VALUES (?, ?, ?)", (2, 'Product B2', 12.00))
    cursor.execute("INSERT OR IGNORE INTO products (supplier_id, name, price) VALUES (?, ?, ?)", (2, 'Product B3', 30.00))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")