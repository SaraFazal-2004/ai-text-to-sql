import sqlite3
import json


DATABASE_PATH = "data/ecommerce.db"
OUTPUT_PATH = "evaluation/expected_results.json"


GROUND_TRUTH_QUERIES = {

    1: """
        SELECT SUM(total_amount)
        FROM orders
    """,

    2: """
        SELECT COUNT(*)
        FROM customers
    """,

    3: """
        SELECT COUNT(*)
        FROM orders
        WHERE strftime('%Y', order_date) = '2025'
    """,

    4: """
        SELECT
            c.customer_id,
            c.name,
            SUM(o.total_amount) AS total_spent
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        GROUP BY
            c.customer_id,
            c.name
        ORDER BY
            total_spent DESC
        LIMIT 1
    """,

    9: """
        SELECT
            cat.category_id,
            cat.name AS category,
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount)
            ) AS revenue
        FROM categories cat
        JOIN products p
            ON cat.category_id = p.category_id
        JOIN order_items oi
            ON p.product_id = oi.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE strftime('%Y', o.order_date) = '2025'
        GROUP BY
            cat.category_id,
            cat.name
        ORDER BY
            revenue DESC
    """,

    10: """
        SELECT
            country,
            COUNT(*) AS customer_count
        FROM customers
        GROUP BY country
        ORDER BY customer_count DESC
        LIMIT 1
    """,

    11: """
        SELECT AVG(total_amount)
        FROM orders
    """,

    12: """
        SELECT
            product_id,
            name,
            rating
        FROM products
        ORDER BY rating DESC
    """,

    14: """
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Completed'
        AND payment_method = 'Credit Card'
    """,

    15: """
        SELECT
            c.customer_id,
            c.name,
            COUNT(o.order_id) AS order_count
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        GROUP BY
            c.customer_id,
            c.name
        ORDER BY
            order_count DESC
    """
}


def main():

    print("=" * 70)
    print("              GENERATING GROUND TRUTH")
    print("=" * 70)

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    expected_results = []

    for question_id, query in GROUND_TRUTH_QUERIES.items():

        print(
            f"\nQUESTION {question_id}"
        )

        try:

            cursor = connection.cursor()

            cursor.execute(query)

            results = cursor.fetchall()

            # Convert SQLite tuples into lists
            results = [
                list(row)
                for row in results
            ]

            expected_results.append({
                "id": question_id,
                "expected_result": results
            })

            print(
                f"Result: {results}"
            )

            print(
                "✓ Ground truth generated."
            )

        except Exception as error:

            print(
                f"❌ Error for question "
                f"{question_id}: {error}"
            )

    connection.close()

    # ==========================================
    # Save as LIST of objects
    # ==========================================

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            expected_results,
            file,
            indent=4
        )

    print("\n" + "=" * 70)

    print(
        "✓ Ground truth saved successfully."
    )

    print(
        f"File: {OUTPUT_PATH}"
    )

    print(
        f"Questions generated: "
        f"{len(expected_results)}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()