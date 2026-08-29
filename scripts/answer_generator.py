import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

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
# GENERATE NATURAL LANGUAGE ANSWER
# ============================================================

def generate_answer(question, columns, results):

    if not results:

        return (
            "No results were found for your question."
        )

    # --------------------------------------------------------
    # Convert database results into readable text
    # --------------------------------------------------------

    formatted_results = "\n".join(
        " | ".join(
            str(value)
            for value in row
        )
        for row in results
    )

    column_names = " | ".join(
        columns
    )

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an assistant that explains database
results to users in simple natural language.

USER QUESTION:
{question}

DATABASE COLUMNS:
{column_names}

DATABASE RESULTS:
{formatted_results}

Instructions:

1. Answer the user's original question directly.
2. Use ONLY the information contained in the results.
3. Do not invent facts.
4. If the question asks for rankings, clearly
   present the ranking.
5. Use numbers and names from the results accurately.
6. Keep the answer concise and easy to understand.
7. Do not mention SQL, databases, Gemini, or
   internal implementation details.
"""

    # --------------------------------------------------------
    # Call Gemini
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response.text:

            return (
                "Unable to generate an answer."
            )

        return response.text.strip()

    except Exception as error:

        error_text = str(error)

        # ----------------------------------------------------
        # Gemini quota error
        # ----------------------------------------------------

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
        ):

            return (
                "The AI answer service has reached "
                "its current API quota. Please try "
                "again later."
            )

        # ----------------------------------------------------
        # Model unavailable
        # ----------------------------------------------------

        if (
            "404" in error_text
            or "NOT_FOUND" in error_text
        ):

            return (
                f"The configured Gemini model "
                f"'{GEMINI_MODEL}' is unavailable."
            )

        # ----------------------------------------------------
        # Other errors
        # ----------------------------------------------------

        return (
            f"Unable to generate an AI answer: {error}"
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_question = (
        "What is the total revenue?"
    )

    test_columns = [
        "total_revenue"
    ]

    test_results = [
        (23066974.11,)
    ]

    print("Testing answer generator...")

    answer = generate_answer(
        test_question,
        test_columns,
        test_results
    )

    print("\n===== AI ANSWER =====\n")

    print(answer)