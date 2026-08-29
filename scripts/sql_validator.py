import re


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "REPLACE",
    "TRUNCATE",
    "ATTACH",
    "DETACH",
    "PRAGMA",
    "VACUUM",
]


def validate_sql(sql):

    if not isinstance(sql, str):

        return False, "SQL must be a string."

    sql = sql.strip()

    # ==========================================
    # Remove Markdown code fences
    # ==========================================

    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"```",
        "",
        sql
    )

    sql = sql.strip()

    # ==========================================
    # Empty SQL
    # ==========================================

    if not sql:

        return False, "SQL query is empty."

    # ==========================================
    # Remove trailing semicolon
    # ==========================================

    sql_without_semicolon = sql.rstrip(";").strip()

    # ==========================================
    # Prevent multiple SQL statements
    # ==========================================

    if ";" in sql_without_semicolon:

        return False, (
            "Multiple SQL statements are not allowed."
        )

    # ==========================================
    # Only SELECT queries
    # ==========================================

    if not re.match(
        r"^SELECT\b",
        sql,
        re.IGNORECASE
    ):

        return False, (
            "Only SELECT queries are allowed."
        )

    # ==========================================
    # Forbidden operations
    # ==========================================

    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(
            pattern,
            sql,
            re.IGNORECASE
        ):

            return False, (
                f"Forbidden SQL operation detected: "
                f"{keyword}"
            )

    # ==========================================
    # Basic suspicious comment detection
    # ==========================================

    if "--" in sql:

        return False, (
            "SQL comments are not allowed."
        )

    if "/*" in sql or "*/" in sql:

        return False, (
            "SQL block comments are not allowed."
        )

    # ==========================================
    # Validation successful
    # ==========================================

    return True, "SQL query is valid."


if __name__ == "__main__":

    print("=" * 60)
    print("              SQL VALIDATOR TEST")
    print("=" * 60)

    test_queries = [

        (
            "SELECT * FROM customers;",
            True
        ),

        (
            "SELECT COUNT(*) FROM orders;",
            True
        ),

        (
            "DELETE FROM customers;",
            False
        ),

        (
            "DROP TABLE products;",
            False
        ),

        (
            "UPDATE customers SET name='Test';",
            False
        ),

        (
            "SELECT * FROM customers; DELETE FROM customers;",
            False
        ),

        (
            "SELECT * FROM customers -- comment",
            False
        ),

        (
            "SELECT * FROM customers /* comment */",
            False
        ),

    ]

    passed = 0

    for query, expected in test_queries:

        valid, message = validate_sql(query)

        correct = valid == expected

        if correct:

            passed += 1

        print("\nQuery:")
        print(query)

        print(
            f"Expected: {expected}"
        )

        print(
            f"Actual:   {valid}"
        )

        print(
            f"Message:  {message}"
        )

        if correct:

            print("✓ TEST PASS")

        else:

            print("❌ TEST FAIL")

    print("\n" + "=" * 60)

    print(
        f"Validator Tests: "
        f"{passed}/{len(test_queries)}"
    )

    print("=" * 60)