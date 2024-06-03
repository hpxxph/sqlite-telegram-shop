import sqlite3

def create_tables():
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'Pending',
            delivery_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            review_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            discount_percentage REAL CHECK(discount_percentage >= 0 AND discount_percentage <= 100),
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_users():
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()

    users_data = [
        ('Nazar', 'nazar@gmail.com'),
        ('Hpx', 'hpx@gmail.com'),
    ]
    cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users_data)

    conn.commit()
    conn.close()

def insert_categories():
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()

    categories_data = [
        ('Electronics',),
        ('Home Appliances',),
        ('Books',),
        ('Clothing',),
    ]
    cursor.executemany('INSERT INTO categories (name) VALUES (?)', categories_data)

    conn.commit()
    conn.close()

def insert_products():
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()

    products_data = [
        ('Laptop', 1200.0, 10, 1),
        ('Mouse', 25.0, 100, 1),
        ('Keyboard', 45.0, 50, 1),
        ('Monitor', 300.0, 20, 1),
        ('Blender', 150.0, 30, 2),
        ('Toaster', 60.0, 40, 2),
        ('Python Programming Book', 35.0, 200, 3),
        ('T-Shirt', 20.0, 150, 4),
    ]
    cursor.executemany('INSERT INTO products (name, price, stock, category_id) VALUES (?, ?, ?, ?)', products_data)

    conn.commit()
    conn.close()

def initialize_database():
    create_tables()
    insert_users()
    insert_categories()
    insert_products()

def get_users():
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_categories():
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_products():
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

def create_order(user_id, items, delivery_address):
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO orders (user_id, total, delivery_address) VALUES (?, ?, ?)', (user_id, 0, delivery_address))
    order_id = cursor.lastrowid

    for product_id, quantity in items:
        cursor.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)', (order_id, product_id, quantity))
        cursor.execute('UPDATE products SET stock = stock - ? WHERE id = ?', (quantity, product_id))

    cursor.execute('''
        UPDATE orders SET total = (
            SELECT SUM(products.price * order_items.quantity)
            FROM order_items
            JOIN products ON order_items.product_id = products.id
            WHERE order_items.order_id = ?
        ) WHERE id = ?
    ''', (order_id, order_id))

    conn.commit()
    conn.close()

def add_review(user_id, product_id, rating, comment):
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (?, ?, ?, ?)',
                   (user_id, product_id, rating, comment))

    conn.commit()
    conn.close()

def apply_discount(product_id, discount_percentage, start_date, end_date):
    conn = sqlite3.connect('full_shop.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO discounts (product_id, discount_percentage, start_date, end_date) VALUES (?, ?, ?, ?)',
                   (product_id, discount_percentage, start_date, end_date))

    conn.commit()
    conn.close()
