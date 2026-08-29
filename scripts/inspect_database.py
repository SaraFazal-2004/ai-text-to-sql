import sqlite3

DATABASE_PATH = "data/ecommerce.db"


def main():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    print("\n===== TABLES =====")

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    for table in tables:
        print(f"- {table[0]}")

    print("\n===== RECORD COUNTS =====")

    for table in tables:
        table_name = table[0]

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        count = cursor.fetchone()[0]

        print(f"{table_name}: {count}")

    print("\n===== SAMPLE CUSTOMERS =====")

    cursor.execute("""
        SELECT customer_id, name, country, city
        FROM customers
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(row)

    print("\n===== SAMPLE PRODUCTS =====")

    cursor.execute("""
        SELECT product_id, name, price, rating
        FROM products
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(row)

    print("\n===== SAMPLE ORDERS =====")

    cursor.execute("""
        SELECT
            order_id,
            customer_id,
            order_date,
            status,
            total_amount
        FROM orders
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(row)

    connection.close()

    print("\nDatabase inspection complete!")


if __name__ == "__main__":
    main()