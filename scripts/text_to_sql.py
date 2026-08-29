import sqlite3

from clarification_engine import analyze_question


DATABASE_PATH = "data/ecommerce.db"


def generate_sql(question):

    question_lower = question.lower()

    # Total revenue
    if "total revenue" in question_lower:

        return """
        SELECT SUM(total_amount) AS total_revenue
        FROM orders
        WHERE status = 'Completed';
        """

    # Number of customers
    if (
        "how many customers" in question_lower
        or "number of customers" in question_lower
    ):

        return """
        SELECT COUNT(*) AS customer_count
        FROM customers;
        """

    # Number of orders
    if (
        "how many orders" in question_lower
        and "2025" not in question_lower
    ):

        return """
        SELECT COUNT(*) AS order_count
        FROM orders;
        """

    # Orders in 2025
    if (
        "orders" in question_lower
        and "2025" in question_lower
    ):

        return """
        SELECT COUNT(*) AS order_count
        FROM orders
        WHERE order_date >= '2025-01-01'
          AND order_date < '2026-01-01';
        """

    # Top customers
    if (
        "customer" in question_lower
        and "spent" in question_lower
    ):

        return """
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

    return None


def execute_sql(sql):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    columns = [
        description[0]
        for description in cursor.description
    ]

    connection.close()

    return columns, results


def main():

    print("====================================")
    print("       TEXT → SQL ENGINE")
    print("====================================")

    while True:

        question = input(
            "\nAsk a question "
            "(type 'exit' to quit): "
        )

        if question.lower() == "exit":
            break

        # --------------------------------
        # Step 1: Clarification
        # --------------------------------

        analysis = analyze_question(question)

        if analysis["clarification_required"]:

            print(
                "\n⚠ I need some clarification:"
            )

            for clarification in analysis[
                "clarification_questions"
            ]:

                print(
                    f"- {clarification}"
                )

            continue

        # --------------------------------
        # Step 2: Generate SQL
        # --------------------------------

        sql = generate_sql(question)

        if sql is None:

            print(
                "\n❌ I don't know how to "
                "generate SQL for this question yet."
            )

            continue

        print("\nGenerated SQL:")
        print(sql)

        # --------------------------------
        # Step 3: Execute SQL
        # --------------------------------

        try:

            columns, results = execute_sql(sql)

            print("\nResults:")

            print(" | ".join(columns))

            print("-" * 60)

            for row in results:

                print(
                    " | ".join(
                        str(value)
                        for value in row
                    )
                )

        except Exception as error:

            print(
                f"\n❌ SQL execution error: {error}"
            )


if __name__ == "__main__":
    main()