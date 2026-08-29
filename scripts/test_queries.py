import sqlite3

DATABASE_PATH = "data/ecommerce.db"


def main():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    query = """
        SELECT
            c.name AS customer_name,
            SUM(o.total_amount) AS total_spending
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.customer_id
        ORDER BY total_spending DESC
        LIMIT 10;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    print("\n===== TOP 10 CUSTOMERS BY SPENDING =====\n")

    for rank, (name, spending) in enumerate(results, start=1):
        print(
            f"{rank}. {name} - ${spending:,.2f}"
        )

    connection.close()


if __name__ == "__main__":
    main()