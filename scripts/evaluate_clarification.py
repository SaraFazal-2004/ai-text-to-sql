import json

from clarification_engine import analyze_question


QUESTIONS_PATH = "evaluation/questions.json"


def main():

    print("=" * 70)
    print("           CLARIFICATION ENGINE EVALUATION")
    print("=" * 70)

    # Load questions
    with open(
        QUESTIONS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        questions = json.load(file)

    total = 0
    passed = 0

    for item in questions:

        question_id = item["id"]
        question = item["question"]

        expected = item[
            "clarification_required"
        ]

        print("\n" + "=" * 70)

        print(
            f"QUESTION #{question_id}"
        )

        print(question)

        print(
            f"\nExpected clarification: "
            f"{expected}"
        )

        # Run clarification engine
        try:

            analysis = analyze_question(
                question
            )

            actual = analysis[
                "clarification_required"
            ]

        except Exception as error:

            print(
                f"\n❌ Engine error: {error}"
            )

            continue

        print(
            f"Actual clarification:   "
            f"{actual}"
        )

        total += 1

        # Compare
        if actual == expected:

            print(
                "✓ CLARIFICATION TEST: PASS"
            )

            passed += 1

        else:

            print(
                "❌ CLARIFICATION TEST: FAIL"
            )

    # ==========================================
    # FINAL SUMMARY
    # ==========================================

    print("\n" + "=" * 70)
    print("                    SUMMARY")
    print("=" * 70)

    print(
        f"Passed: {passed}/{total}"
    )

    if total > 0:

        accuracy = (
            passed / total
        ) * 100

        print(
            f"Clarification Accuracy: "
            f"{accuracy:.2f}%"
        )

    print("=" * 70)


if __name__ == "__main__":

    main()