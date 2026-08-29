import json
import sqlite3

from clarification_engine import analyze_question
from llm_sql_generator import generate_sql
from sql_validator import validate_sql


DATABASE_PATH = "data/ecommerce.db"
QUESTIONS_PATH = "evaluation/questions.json"
EXPECTED_PATH = "evaluation/expected_results.json"


def execute_sql(sql):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    connection.close()

    return results


def load_questions():

    with open(
        QUESTIONS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def load_expected_results():

    with open(
        EXPECTED_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return {
        item["id"]: item["expected_result"]
        for item in data
    }


def normalize_results(results):

    normalized = []

    for row in results:

        normalized.append(
            list(row)
        )

    return normalized


def compare_results(actual, expected):

    actual = normalize_results(actual)

    expected = normalize_results(expected)

    return actual == expected


def evaluate_question(item, expected_results):

    question_id = item["id"]

    question = item["question"]

    print("\n" + "=" * 70)

    print("QUESTION:")
    print(question)

    # ==================================
    # 1. CLARIFICATION TEST
    # ==================================

    expected_clarification = item[
        "clarification_required"
    ]

    analysis = analyze_question(question)

    actual_clarification = analysis[
        "clarification_required"
    ]

    if actual_clarification != expected_clarification:

        print(
            "\n❌ Clarification test FAILED"
        )

        print(
            f"Expected: {expected_clarification}"
        )

        print(
            f"Actual: {actual_clarification}"
        )

        return False

    print(
        "\n✓ Clarification test passed."
    )

    # ==================================
    # Don't generate SQL for ambiguous
    # questions.
    # ==================================

    if expected_clarification:

        print(
            "✓ Ambiguous question correctly detected."
        )

        return True

    # ==================================
    # 2. GENERATE SQL
    # ==================================

    print(
        "\nGenerating SQL with Gemini..."
    )

    try:

        sql = generate_sql(question)

    except Exception as error:

        print(
            f"\n❌ Gemini error: {error}"
        )

        return False

    print(
        "\n===== GENERATED SQL =====\n"
    )

    print(sql)

    # ==================================
    # 3. VALIDATE SQL
    # ==================================

    valid, message = validate_sql(sql)

    print(
        "\n===== SQL VALIDATION ====="
    )

    if not valid:

        print(
            f"❌ Validation failed: {message}"
        )

        return False

    print(
        "✓ SQL validation passed."
    )

    # ==================================
    # 4. EXECUTE SQL
    # ==================================

    try:

        actual_results = execute_sql(sql)

    except Exception as error:

        print(
            f"\n❌ Database error: {error}"
        )

        return False

    print(
        "\n===== ACTUAL RESULT ====="
    )

    print(actual_results)

    # ==================================
    # 5. GET EXPECTED RESULT
    # ==================================

    if question_id not in expected_results:

        print(
            "\n⚠ No expected result stored."
        )

        return False

    expected = expected_results[
        question_id
    ]

    print(
        "\n===== EXPECTED RESULT ====="
    )

    print(expected)

    # ==================================
    # 6. COMPARE
    # ==================================

    if compare_results(
        actual_results,
        expected
    ):

        print(
            "\n✅ RESULT CORRECT"
        )

        return True

    else:

        print(
            "\n❌ RESULT INCORRECT"
        )

        return False


def main():

    print("=" * 70)

    print(
        "        TEXT → SQL GROUND TRUTH EVALUATION"
    )

    print("=" * 70)

    questions = load_questions()

    expected_results = load_expected_results()

    total = 0
    passed = 0

    for item in questions:

        # Only evaluate questions that have
        # expected results.

        if item["id"] not in expected_results:

            continue

        total += 1

        success = evaluate_question(
            item,
            expected_results
        )

        if success:

            passed += 1

    # ==================================
    # SUMMARY
    # ==================================

    print("\n" + "=" * 70)

    print(
        "              EVALUATION SUMMARY"
    )

    print("=" * 70)

    print(
        f"Passed: {passed}/{total}"
    )

    if total > 0:

        accuracy = (
            passed / total
        ) * 100

        print(
            f"Ground Truth Accuracy: "
            f"{accuracy:.2f}%"
        )

    print("=" * 70)


if __name__ == "__main__":

    main()