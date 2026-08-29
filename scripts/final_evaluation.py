import json
import sqlite3


DATABASE_PATH = "data/ecommerce.db"

QUESTIONS_FILE = "evaluation/questions.json"
GENERATED_SQL_FILE = "evaluation/generated_sql.json"
EXPECTED_RESULTS_FILE = "evaluation/expected_results.json"


# ============================================================
# LOAD JSON FILE
# ============================================================

def load_json(path):

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# EXECUTE SQL
# ============================================================

def execute_sql(sql):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:

        cursor.execute(sql)

        return cursor.fetchall()

    finally:

        connection.close()


# ============================================================
# NORMALIZE RESULTS
# ============================================================

def normalize_value(value):

    if isinstance(value, float):

        return round(value, 2)

    return value


def normalize_result(result):

    normalized = []

    for row in result:

        normalized_row = []

        for value in row:

            normalized_row.append(
                normalize_value(value)
            )

        normalized.append(
            tuple(normalized_row)
        )

    return normalized


# ============================================================
# COMPARE RESULTS
# ============================================================

def compare_results(actual, expected):

    actual_normalized = normalize_result(actual)

    expected_normalized = normalize_result(expected)

    return actual_normalized == expected_normalized


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("              FINAL TEXT → SQL EVALUATION")
    print("=" * 70)

    # ========================================================
    # LOAD FILES
    # ========================================================

    try:

        questions = load_json(
            QUESTIONS_FILE
        )

        generated_sql = load_json(
            GENERATED_SQL_FILE
        )

        expected_results = load_json(
            EXPECTED_RESULTS_FILE
        )

    except FileNotFoundError as error:

        print("\n❌ File not found:")
        print(error)

        return

    except json.JSONDecodeError as error:

        print("\n❌ Invalid JSON file:")
        print(error)

        return

    # ========================================================
    # CREATE LOOKUP MAPS
    # ========================================================

    generated_sql_map = {
        item["id"]: item["sql"]
        for item in generated_sql
    }

    expected_result_map = {
        item["id"]: item["expected_result"]
        for item in expected_results
    }

    # ========================================================
    # CLARIFICATION EVALUATION
    # ========================================================

    print("\n")
    print("=" * 70)
    print("              CLARIFICATION EVALUATION")
    print("=" * 70)

    clarification_passed = 0
    clarification_total = len(questions)

    # Import here so the script can still load files
    # before importing the clarification engine.

    from clarification_engine import analyze_question

    for question_item in questions:

        question_id = question_item["id"]

        question = question_item["question"]

        expected = question_item[
            "clarification_required"
        ]

        analysis = analyze_question(
            question
        )

        actual = analysis[
            "clarification_required"
        ]

        print("\n" + "-" * 70)

        print(
            f"QUESTION #{question_id}"
        )

        print(question)

        print(
            f"\nExpected clarification: {expected}"
        )

        print(
            f"Actual clarification:   {actual}"
        )

        if actual == expected:

            clarification_passed += 1

            print(
                "✓ CLARIFICATION TEST: PASS"
            )

        else:

            print(
                "❌ CLARIFICATION TEST: FAIL"
            )

    if clarification_total > 0:

        clarification_accuracy = (
            clarification_passed
            / clarification_total
            * 100
        )

    else:

        clarification_accuracy = 0

    # ========================================================
    # SQL EVALUATION
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                  SQL EVALUATION")
    print("=" * 70)

    sql_passed = 0
    sql_failed = 0
    validation_failed = 0
    execution_failed = 0

    sql_total = len(generated_sql)

    from sql_validator import validate_sql

    for item in generated_sql:

        question_id = item["id"]

        sql = item["sql"]

        print("\n")
        print("-" * 70)

        print(
            f"Test #{question_id}"
        )

        print(
            f"SQL: {sql}"
        )

        # ====================================================
        # CHECK EXPECTED RESULT
        # ====================================================

        if question_id not in expected_result_map:

            print(
                "⚠ No expected result found."
            )

            sql_failed += 1

            continue

        expected_result = expected_result_map[
            question_id
        ]

        # ====================================================
        # SQL VALIDATION
        # ====================================================

        valid, message = validate_sql(
            sql
        )

        if not valid:

            print(
                f"❌ SQL validation failed: "
                f"{message}"
            )

            validation_failed += 1

            continue

        print(
            "✓ SQL validation passed"
        )

        # ====================================================
        # SQL EXECUTION
        # ====================================================

        try:

            actual_result = execute_sql(
                sql
            )

            print(
                "✓ SQL executed successfully"
            )

        except Exception as error:

            print(
                f"❌ SQL execution failed: "
                f"{error}"
            )

            execution_failed += 1

            continue

        # ====================================================
        # RESULT COMPARISON
        # ====================================================

        if compare_results(
            actual_result,
            expected_result
        ):

            sql_passed += 1

            print(
                "✅ RESULT CORRECT"
            )

        else:

            sql_failed += 1

            print(
                "❌ RESULT INCORRECT"
            )

            print(
                f"Expected: {expected_result}"
            )

            print(
                f"Actual:   {actual_result}"
            )

    # ========================================================
    # SQL ACCURACY
    # ========================================================

    if sql_total > 0:

        sql_accuracy = (
            sql_passed
            / sql_total
            * 100
        )

    else:

        sql_accuracy = 0

    # ========================================================
    # OVERALL SCORE
    # ========================================================

    overall_total = (
        clarification_total
        + sql_total
    )

    overall_passed = (
        clarification_passed
        + sql_passed
    )

    if overall_total > 0:

        overall_accuracy = (
            overall_passed
            / overall_total
            * 100
        )

    else:

        overall_accuracy = 0

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                    FINAL REPORT")
    print("=" * 70)

    print()

    print(
        f"Clarification Tests:     "
        f"{clarification_passed}/{clarification_total}"
    )

    print(
        f"Clarification Accuracy:  "
        f"{clarification_accuracy:.2f}%"
    )

    print()

    print(
        f"SQL Tests:               "
        f"{sql_passed}/{sql_total}"
    )

    print(
        f"SQL Result Accuracy:     "
        f"{sql_accuracy:.2f}%"
    )

    print()

    print(
        f"Validation Failed:       "
        f"{validation_failed}"
    )

    print(
        f"Execution Failed:        "
        f"{execution_failed}"
    )

    print()

    print(
        f"Overall Tests:            "
        f"{overall_passed}/{overall_total}"
    )

    print(
        f"Overall Accuracy:         "
        f"{overall_accuracy:.2f}%"
    )

    print("=" * 70)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()