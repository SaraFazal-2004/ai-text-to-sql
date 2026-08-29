import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATABASE_PATH = "data/ecommerce.db"

NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 500
NUM_ORDERS = 5000

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Books",
    "Sports",
    "Beauty",
    "Toys",
    "Grocery",
    "Furniture",
    "Accessories"
]

COUNTRIES = [
    "Pakistan",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany",
    "France",
    "UAE",
    "Saudi Arabia",
    "India"
]

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "Cash on Delivery",
    "Bank Transfer"
]

ORDER_STATUSES = [
    "Completed",
    "Pending",
    "Cancelled",
    "Shipped",
    "Processing"
]


# --------------------------------------------------
# Database setup
# --------------------------------------------------

def create_tables(cursor):

    cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL,
            signup_date DATE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            rating REAL NOT NULL,
            FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            status TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            shipping_country TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            discount REAL NOT NULL,
            FOREIGN KEY (order_id)
                REFERENCES orders(order_id),
            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)


# --------------------------------------------------
# Generate categories
# --------------------------------------------------

def generate_categories(cursor):

    for category_id, category in enumerate(CATEGORIES, start=1):

        cursor.execute("""
            INSERT INTO categories (category_id, name)
            VALUES (?, ?)
        """, (category_id, category))


# --------------------------------------------------
# Generate customers
# --------------------------------------------------

def generate_customers(cursor):

    for customer_id in range(1, NUM_CUSTOMERS + 1):

        name = fake.name()
        email = f"user{customer_id}@example.com"

        country = random.choice(COUNTRIES)
        city = fake.city()

        signup_date = fake.date_between(
            start_date="-3y",
            end_date="today"
        )

        cursor.execute("""
            INSERT INTO customers
            (
                customer_id,
                name,
                email,
                country,
                city,
                signup_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            name,
            email,
            country,
            city,
            signup_date
        ))


# --------------------------------------------------
# Generate products
# --------------------------------------------------

def generate_products(cursor):

    product_names = [
        "Laptop",
        "Smartphone",
        "Tablet",
        "Headphones",
        "Keyboard",
        "Mouse",
        "Monitor",
        "Smart Watch",
        "Camera",
        "Backpack",
        "T-Shirt",
        "Jeans",
        "Jacket",
        "Sneakers",
        "Novel",
        "Programming Book",
        "Coffee Maker",
        "Blender",
        "Office Chair",
        "Desk",
        "Football",
        "Cricket Bat",
        "Yoga Mat",
        "Perfume",
        "Skincare Set",
        "Toy Car",
        "Board Game",
        "Chocolate",
        "Protein Bar",
        "Wallet"
    ]

    for product_id in range(1, NUM_PRODUCTS + 1):

        base_name = random.choice(product_names)

        product_name = f"{base_name} {fake.word().title()}"

        category_id = random.randint(1, len(CATEGORIES))

        price = round(
            random.uniform(10, 1500),
            2
        )

        stock = random.randint(0, 500)

        rating = round(
            random.uniform(2.5, 5.0),
            1
        )

        cursor.execute("""
            INSERT INTO products
            (
                product_id,
                name,
                category_id,
                price,
                stock,
                rating
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            product_id,
            product_name,
            category_id,
            price,
            stock,
            rating
        ))


# --------------------------------------------------
# Generate orders and order items
# --------------------------------------------------

def generate_orders(cursor):

    order_item_id = 1

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 8, 1)

    days_difference = (
        end_date - start_date
    ).days

    for order_id in range(1, NUM_ORDERS + 1):

        customer_id = random.randint(
            1,
            NUM_CUSTOMERS
        )

        order_date = (
            start_date +
            timedelta(
                days=random.randint(
                    0,
                    days_difference
                )
            )
        ).date()

        status = random.choices(
            ORDER_STATUSES,
            weights=[
                60,
                10,
                8,
                15,
                7
            ]
        )[0]

        payment_method = random.choice(
            PAYMENT_METHODS
        )

        shipping_country = random.choice(
            COUNTRIES
        )

        # Number of products in this order
        number_of_items = random.randint(1, 5)

        order_total = 0

        items = []

        for _ in range(number_of_items):

            product_id = random.randint(
                1,
                NUM_PRODUCTS
            )

            quantity = random.randint(1, 4)

            cursor.execute("""
                SELECT price
                FROM products
                WHERE product_id = ?
            """, (product_id,))

            result = cursor.fetchone()

            unit_price = result[0]

            discount = round(
                random.uniform(0, 0.30),
                2
            )

            discounted_price = (
                unit_price *
                (1 - discount)
            )

            item_total = (
                discounted_price *
                quantity
            )

            order_total += item_total

            items.append((
                product_id,
                quantity,
                unit_price,
                discount
            ))

        order_total = round(
            order_total,
            2
        )

        cursor.execute("""
            INSERT INTO orders
            (
                order_id,
                customer_id,
                order_date,
                status,
                payment_method,
                shipping_country,
                total_amount
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id,
            customer_id,
            order_date,
            status,
            payment_method,
            shipping_country,
            order_total
        ))

        for product_id, quantity, unit_price, discount in items:

            cursor.execute("""
                INSERT INTO order_items
                (
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    discount
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                order_item_id,
                order_id,
                product_id,
                quantity,
                unit_price,
                discount
            ))

            order_item_id += 1


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("Creating e-commerce database...")

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    # Enable foreign keys
    cursor.execute(
        "PRAGMA foreign_keys = ON"
    )

    create_tables(cursor)

    print("Generating categories...")
    generate_categories(cursor)

    print("Generating customers...")
    generate_customers(cursor)

    print("Generating products...")
    generate_products(cursor)

    print("Generating orders...")
    generate_orders(cursor)

    connection.commit()

    connection.close()

    print()
    print("Database created successfully!")
    print(f"Location: {DATABASE_PATH}")
    print()
    print("Records generated:")
    print(f"Customers: {NUM_CUSTOMERS}")
    print(f"Products: {NUM_PRODUCTS}")
    print(f"Orders: {NUM_ORDERS}")
    print("Order items: 10,000+")
    print()
    print("You are ready for the Text-to-SQL project!")


if __name__ == "__main__":
    main()