from flask import Flask, request, jsonify
from database import get_user_by_username, get_all_suppliers, get_supplier_by_id, get_products_by_supplier, insert_order
from functools import wraps
import sqlite3

app = Flask(__name__)

# In-memory user sessions (for simplicity, not production-ready)
sessions = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token and token in sessions:
            kwargs['user_id'] = sessions[token]
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'Authentication required'}), 401
    return decorated_function

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Username and password required'}), 400

    user = get_user_by_username(data['username'])
    if user and user['password'] == data['password']:
        # For simplicity, we'll use a basic token
        token = f'session_{user["id"]}'
        sessions[token] = user['id']
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/suppliers', methods=['GET'])
@login_required
def list_suppliers(user_id):
    suppliers = get_all_suppliers()
    return jsonify([dict(row) for row in suppliers]), 200

@app.route('/suppliers/<int:supplier_id>', methods=['GET'])
@login_required
def get_supplier_details(user_id, supplier_id):
    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    products = get_products_by_supplier(supplier_id)
    return jsonify({
        'id': supplier['id'],
        'name': supplier['name'],
        'products': [dict(row) for row in products]
    }), 200

@app.route('/orders', methods=['POST'])
@login_required
def submit_order(user_id):
    data = request.get_json()
    if not data or 'order_items' not in data or not isinstance(data['order_items'], list):
        return jsonify({'message': 'Invalid order data'}), 400

    total_amount = 0
    order_items_data = []
    for item in data['order_items']:
        if 'product_id' not in item or 'quantity' not in item or 'price' not in item:
            return jsonify({'message': 'Invalid order item data'}), 400
        total_amount += item['quantity'] * item['price']
        order_items_data.append({
            'product_id': item['product_id'],
            'quantity': item['quantity'],
            'price': item['price']
        })

    try:
        order_id = insert_order(user_id, total_amount, order_items_data)
        return jsonify({'message': 'Order submitted successfully', 'order_id': order_id}), 201
    except sqlite3.Error as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)