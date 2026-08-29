import json
import sqlite3
import math

from sql_validator import validate_sql


DATABASE_PATH = "data/ecommerce.db"
EXPECTED_PATH = "evaluation/expected_results.json"
GENERATED_SQL_PATH = "evaluation/generated_sql.json"


def execute_sql(sql):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    connection.close()

    return results


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def values_equal(actual, expected):

    # Numbers
    if isinstance(actual, (int, float)) and \
       isinstance(expected, (int, float)):

        return math.isclose(
            actual,
            expected,
            rel_tol=1e-9,
            abs_tol=1e-6
        )

    # Everything else
    return actual == expected


def compare_results(actual, expected):

    if len(actual) != len(expected):
        return False

    for actual_row, expected_row in zip(
        actual,
        expected
    ):

        if len(actual_row) != len(expected_row):
            return False

        for actual_value, expected_value in zip(
            actual_row,
            expected_row
        ):

            if not values_equal(
                actual_value,
                expected_value
            ):

                return False

    return True


def main():

    print("=" * 70)
    print("              TEXT → SQL EVALUATION REPORT")
    print("=" * 70)

    expected_data = load_json(
        EXPECTED_PATH
    )

    generated_data = load_json(
        GENERATED_SQL_PATH
    )

    expected_results = {
        item["id"]: item["expected_result"]
        for item in expected_data
    }

    generated_sql = {
        item["id"]: item["sql"]
        for item in generated_data
    }

    total = 0
    passed = 0
    failed = 0
    validation_failed = 0
    execution_failed = 0

    failed_tests = []

    for question_id, sql in generated_sql.items():

        total += 1

        print("\n" + "-" * 70)

        print(
            f"Test #{question_id}"
        )

        print(
            f"SQL: {sql}"
        )

        # ==================================
        # SQL VALIDATION
        # ==================================

        valid, message = validate_sql(sql)

        if not valid:

            print(
                "❌ SQL VALIDATION FAILED"
            )

            validation_failed += 1
            failed += 1

            failed_tests.append(
                (
                    question_id,
                    "SQL validation"
                )
            )

            continue

        print(
            "✓ SQL validation passed"
        )

        # ==================================
        # DATABASE EXECUTION
        # ==================================

        try:

            actual = execute_sql(sql)

        except Exception as error:

            print(
                f"❌ DATABASE ERROR: {error}"
            )

            execution_failed += 1
            failed += 1

            failed_tests.append(
                (
                    question_id,
                    "Database execution"
                )
            )

            continue

        print(
            "✓ SQL executed successfully"
        )

        # ==================================
        # EXPECTED RESULT
        # ==================================

        expected = expected_results.get(
            question_id
        )

        if expected is None:

            print(
                "⚠ No expected result"
            )

            failed += 1

            failed_tests.append(
                (
                    question_id,
                    "Missing ground truth"
                )
            )

            continue

        # ==================================
        # RESULT COMPARISON
        # ==================================

        if compare_results(
            actual,
            expected
        ):

            print(
                "✅ RESULT CORRECT"
            )

            passed += 1

        else:

            print(
                "❌ RESULT INCORRECT"
            )

            print(
                f"Expected: {expected}"
            )

            print(
                f"Actual:   {actual}"
            )

            failed += 1

            failed_tests.append(
                (
                    question_id,
                    "Incorrect result"
                )
            )

    # ======================================
    # FINAL REPORT
    # ======================================

    print("\n")
    print("=" * 70)
    print("                    FINAL REPORT")
    print("=" * 70)

    print(
        f"Total Tests:        {total}"
    )

    print(
        f"Passed:             {passed}"
    )

    print(
        f"Failed:             {failed}"
    )

    print(
        f"Validation Failed:  {validation_failed}"
    )

    print(
        f"Execution Failed:   {execution_failed}"
    )

    if total > 0:

        accuracy = (
            passed / total
        ) * 100

        print(
            f"Result Accuracy:    {accuracy:.2f}%"
        )

    # ======================================
    # FAILED TESTS
    # ======================================

    if failed_tests:

        print("\n")
        print("FAILED TESTS")
        print("-" * 70)

        for test_id, reason in failed_tests:

            print(
                f"Test #{test_id}: {reason}"
            )

    print("=" * 70)


if __name__ == "__main__":

    main()