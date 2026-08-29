import os
import sqlite3
import re

from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

DATABASE_PATH = "data/ecommerce.db"

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )

GEMINI_MODEL = "gemini-3.6-flash"

client = genai.Client(
    api_key=api_key
)


# ============================================================
# GET DATABASE SCHEMA
# ============================================================

def get_schema():

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    schema = ""

    for (table_name,) in tables:

        schema += f"\nTABLE: {table_name}\n"

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        for column in columns:

            column_name = column[1]
            column_type = column[2]

            schema += (
                f"- {column_name} "
                f"({column_type})\n"
            )

    connection.close()

    return schema


# ============================================================
# CLEAN GENERATED SQL
# ============================================================

def clean_sql(sql):

    sql = sql.strip()

    # Remove ```sql
    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE
    )

    # Remove ```
    sql = re.sub(
        r"```",
        "",
        sql
    )

    sql = sql.strip()

    # Remove trailing semicolon
    sql = sql.rstrip(";").strip()

    return sql


# ============================================================
# GENERATE SQL
# ============================================================

def generate_sql(question):

    schema = get_schema()

    prompt = f"""
You are an expert SQLite Text-to-SQL system.

Your job is to convert the user's complete request
into ONE valid SQLite SQL query.

DATABASE SCHEMA:
{schema}

USER REQUEST:
{question}

IMPORTANT:
The user request may contain an original question and
a clarification answer.

You MUST preserve the original intent.

Example:

Original:
"Show me the best products."

Clarification:
"Revenue"

Correct interpretation:
"Show me the best PRODUCTS ranked by REVENUE."

Do NOT interpret "Revenue" as:
"What is the total revenue?"

Another example:

Original:
"What are the top 10 products?"

Clarification:
"Rating"

Correct interpretation:
"Return the top 10 PRODUCTS ranked by RATING."

RULES:

1. Return ONLY the SQL query.

2. Do not use Markdown code fences.

3. Do not explain the query.

4. Use only tables and columns present in the schema.

5. The query must be READ-ONLY.

6. Never use INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, REPLACE, or TRUNCATE.

7. Use SQLite-compatible SQL.

8. Use correct JOIN conditions.

9. Preserve the main entity from the original question.

10. If the question asks for "top", "best", "highest",
    "most", or "largest", rank the requested entity.

11. If a ranking metric is provided, use that metric.

12. Always use ORDER BY for ranking questions.

13. If the user asks a singular superlative question such as
    "which country has the most customers?",
    "which customer spent the most money?", or
    "which product has the highest rating?",
    return only the single best result using LIMIT 1.

14. If the user explicitly asks for "top N", return exactly
    N results using LIMIT N.

15. If the user asks a plural ranking question such as
    "which customers ordered the most?" without specifying N,
    return the top 10 results.

16. For "best products by revenue", calculate revenue
    at the PRODUCT level, not the entire database level.

17. For product sales, use products and order_items
    when appropriate.

18. Never change the main entity because of the
    clarification answer.

19. For product revenue, use order_items.

20. Product revenue is calculated as:

    quantity * unit_price * (1 - discount)

21. When ranking products by revenue, JOIN products
    with order_items using product_id.

22. GROUP BY the product.

23. ORDER BY calculated revenue DESC.

24. If the user asks for top N products, use LIMIT N.

25. For customer spending, JOIN customers and orders.

26. For customer order counts, JOIN customers and orders.

27. For category revenue, JOIN categories, products,
    order_items, and orders when a date filter is required.

28. For date filtering, use SQLite-compatible date functions.

29. Do not answer an ambiguous question by guessing.

30. Return exactly ONE SQL SELECT statement.

Return ONLY SQL.
"""

    # ========================================================
    # GEMINI API CALL
    # ========================================================

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return clean_sql(
            response.text
        )

    # ========================================================
    # API ERROR HANDLING
    # ========================================================

    except Exception as error:

        error_text = str(error)

        # ----------------------------------------------------
        # 429 - QUOTA EXCEEDED
        # ----------------------------------------------------

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
        ):

            raise RuntimeError(
                "Gemini API quota has been exceeded. "
                "Please try again later."
            )

        # ----------------------------------------------------
        # 503 - MODEL TEMPORARILY UNAVAILABLE
        # ----------------------------------------------------

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            raise RuntimeError(
                "Gemini is temporarily unavailable "
                "because the model is experiencing "
                "high demand. Please try again "
                "in a few moments."
            )

        # ----------------------------------------------------
        # 404 - MODEL NOT FOUND
        # ----------------------------------------------------

        if (
            "404" in error_text
            or "NOT_FOUND" in error_text
        ):

            raise RuntimeError(
                f"The Gemini model "
                f"'{GEMINI_MODEL}' is unavailable."
            )

        # ----------------------------------------------------
        # OTHER GEMINI ERRORS
        # ----------------------------------------------------

        raise RuntimeError(
            f"Gemini error: {error}"
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_question = (
        "Which country has the most customers?"
    )

    print("=" * 60)
    print("           SQL GENERATOR TEST")
    print("=" * 60)

    print("\nQuestion:")
    print(test_question)

    print("\nGenerating SQL...")

    try:

        sql = generate_sql(
            test_question
        )

        print("\n===== GENERATED SQL =====\n")
        print(sql)

    except Exception as error:

        print(
            f"\n❌ {error}"
        )