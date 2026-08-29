import sqlite3

from clarification_engine import analyze_question
from llm_sql_generator import generate_sql
from sql_validator import validate_sql
from answer_generator import generate_answer
from logger import logger
from config import DATABASE_PATH, APP_NAME


DATABASE_PATH = "data/ecommerce.db"


def execute_sql(sql):

    logger.info("Executing SQL query.")

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:

        cursor.execute(sql)

        results = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        logger.info(
            f"SQL executed successfully. "
            f"Rows returned: {len(results)}"
        )

        return columns, results

    finally:

        connection.close()


def display_results(columns, results):

    if not results:

        print("\nNo results found.")

        return

    print("\n===== RESULTS =====\n")

    print(" | ".join(columns))

    print("-" * 80)

    for row in results:

        print(
            " | ".join(
                str(value)
                for value in row
            )
        )


def run_query(question):

    logger.info(
        f"User question: {question}"
    )

    # ==================================
    # 1. GEMINI → SQL
    # ==================================

    print(
        "\nGenerating SQL with Gemini..."
    )

    try:

        sql = generate_sql(question)

        logger.info(
            f"SQL generated successfully: {sql}"
        )

    except Exception as error:

        logger.error(
            f"Gemini error: {error}"
        )

        print(
            f"\n❌ Gemini error: {error}"
        )

        return

    print(
        "\n===== GENERATED SQL =====\n"
    )

    print(sql)

    # ==================================
    # 2. SQL VALIDATION
    # ==================================

    valid, message = validate_sql(sql)

    print(
        "\n===== SQL VALIDATION ====="
    )

    if not valid:

        logger.warning(
            f"SQL validation failed: {message}"
        )

        print(
            f"❌ {message}"
        )

        return

    logger.info(
        "SQL validation passed."
    )

    print(
        "✓ SQL query passed validation."
    )

    # ==================================
    # 3. EXECUTE SQL
    # ==================================

    try:

        columns, results = execute_sql(sql)

    except Exception as error:

        logger.error(
            f"Database error: {error}"
        )

        print(
            f"\n❌ Database error: {error}"
        )

        return

    # ==================================
    # 4. DISPLAY RESULTS
    # ==================================

    display_results(
        columns,
        results
    )

    # ==================================
    # 5. GENERATE NATURAL LANGUAGE ANSWER
    # ==================================

    print(
        "\n===== AI ANSWER =====\n"
    )

    try:

        answer = generate_answer(
            question,
            columns,
            results
        )

        logger.info(
            "Natural language answer generated successfully."
        )

        print(answer)

    except Exception as error:

        logger.error(
            f"Answer generation error: {error}"
        )

        print(
            f"\n❌ Answer generation error: {error}"
        )


def main():

    logger.info(
        "Text-to-SQL application started."
    )

    print("=" * 60)

    print(
        "           AI TEXT → SQL SYSTEM"
    )

    print("=" * 60)

    print(
        "\nAsk questions about your e-commerce database."
    )

    print(
        "Type 'exit' to quit."
    )

    pending_question = None

    while True:

        # ==================================
        # ASK QUESTION / CLARIFICATION
        # ==================================

        if pending_question:

            question = input(
                "\nClarification answer: "
            )

        else:

            question = input(
                "\nEnter your question: "
            )

        # ==================================
        # EXIT
        # ==================================

        if question.lower().strip() == "exit":

            logger.info(
                "Application terminated by user."
            )

            print(
                "\nGoodbye!"
            )

            break

        # ==================================
        # EMPTY INPUT
        # ==================================

        if not question.strip():

            print(
                "Please enter something."
            )

            continue

        # ==================================
        # HANDLE CLARIFICATION
        # ==================================

        if pending_question:

            original_question = pending_question

            logger.info(
                f"Clarification answer received: {question}"
            )

            combined_question = f"""
Original user request:
{original_question}

Clarification provided by the user:
{question}

Interpretation:
Answer the ORIGINAL request using the clarification
as the requested ranking or filtering metric.

IMPORTANT:
Do not replace the original subject with the clarification.

For example:

Original request:
Show me the best products.

Clarification:
Revenue.

Correct interpretation:
Show me the best PRODUCTS ranked by REVENUE.

The clarification "Revenue" does NOT mean:
"What is the total revenue?"

It means:
"Rank the PRODUCTS according to revenue."
"""

            print(
                "\n✓ Clarification received."
            )

            pending_question = None

            run_query(
                combined_question
            )

            continue

        # ==================================
        # CLARIFICATION ENGINE
        # ==================================

        analysis = analyze_question(
            question
        )

        if analysis[
            "clarification_required"
        ]:

            logger.info(
                f"Clarification required for: "
                f"{question}"
            )

            print(
                "\n⚠ Clarification required:\n"
            )

            for clarification in analysis[
                "clarification_questions"
            ]:

                print(
                    f"- {clarification}"
                )

            pending_question = question

            continue

        # ==================================
        # NORMAL QUERY
        # ==================================

        run_query(question)


if __name__ == "__main__":

    main()