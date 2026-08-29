import streamlit as st
import sqlite3

from clarification_engine import analyze_question
from llm_sql_generator import generate_sql
from sql_validator import validate_sql
from answer_generator import generate_answer


DATABASE_PATH = "data/ecommerce.db"

st.set_page_config(page_title="Text → SQL", page_icon="◆", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #101317;
        color: #E7E5DF;
    }

    /* Console header */
    .console-header {
        border-bottom: 1px solid #2A2E35;
        padding-bottom: 1.6rem;
        margin-bottom: 2rem;
    }
    .console-eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6FCF97;
        margin-bottom: 0.5rem;
    }
    .console-title {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2.6rem;
        color: #F4F2EC;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.01em;
    }
    .console-subtitle {
        font-size: 1rem;
        color: #9A9890;
        margin: 0;
    }

    /* Inputs */
    .stTextInput input {
        background-color: #171B21 !important;
        color: #E7E5DF !important;
        border: 1px solid #2A2E35 !important;
        border-radius: 6px !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }
    .stTextInput input:focus {
        border-color: #6FCF97 !important;
        box-shadow: 0 0 0 1px #6FCF97 !important;
    }
    .stTextInput label {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.82rem !important;
        color: #9A9890 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* Buttons */
    .stButton button {
        background-color: #6FCF97 !important;
        color: #101317 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.5rem 1.4rem !important;
        transition: opacity 0.15s ease;
    }
    .stButton button:hover {
        opacity: 0.85;
    }

    /* Section labels, styled like a query-log prompt */
    .section-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6FCF97;
        margin: 2rem 0 0.6rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-label::before {
        content: "›";
        color: #6FCF97;
        font-size: 1rem;
    }

    .answer-box {
        background: #16201B;
        border: 1px solid #2C4A3A;
        border-left: 3px solid #6FCF97;
        border-radius: 6px;
        padding: 1.1rem 1.3rem;
        font-size: 1.02rem;
        color: #E7E5DF;
        line-height: 1.5;
    }

    .stCode, code {
        font-family: 'IBM Plex Mono', monospace !important;
    }

    hr, [data-testid="stDivider"] {
        border-color: #2A2E35 !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #14171D;
        border-right: 1px solid #2A2E35;
    }
    section[data-testid="stSidebar"] h2 {
        font-family: 'Fraunces', serif;
        color: #F4F2EC;
    }
    section[data-testid="stSidebar"] * {
        color: #B5B3AB;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def execute_sql(sql):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    connection.close()
    return columns, results


# Set up session state defaults once, on first load
defaults = {
    "pending_question": None,
    "clarification_questions": [],
    "answer": None,
    "sql": None,
    "columns": None,
    "results": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


st.markdown(
    """
    <div class="console-header">
        <div class="console-eyebrow">Query Console</div>
        <p class="console-title">Text → SQL</p>
        <p class="console-subtitle">Ask a question about your e-commerce data. It gets translated into SQL, run, and answered in plain language.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

question = st.text_input("Your question", placeholder="e.g. What is the total revenue?")


def run_pipeline(question_for_sql, question_for_answer):
    """Generate SQL, validate it, run it, and produce a natural-language answer."""

    with st.spinner("Generating SQL..."):
        try:
            sql = generate_sql(question_for_sql)
        except Exception as error:
            st.error(str(error))
            st.stop()

    valid, message = validate_sql(sql)
    if not valid:
        st.error(f"SQL validation failed: {message}")
        st.stop()

    try:
        columns, results = execute_sql(sql)
    except Exception as error:
        st.error(f"Database error: {error}")
        st.stop()

    with st.spinner("Generating answer..."):
        try:
            answer = generate_answer(question_for_answer, columns, results)
        except Exception as error:
            answer = f"Unable to generate AI answer: {error}"

    return sql, columns, results, answer


if st.button("Ask Question", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        # Reset whatever was there before
        st.session_state.answer = None
        st.session_state.sql = None
        st.session_state.columns = None
        st.session_state.results = None

        analysis = analyze_question(question)

        if analysis["clarification_required"]:
            st.session_state.pending_question = question
            st.session_state.clarification_questions = analysis["clarification_questions"]
            st.rerun()
        else:
            sql, columns, results, answer = run_pipeline(question, question)
            st.session_state.sql = sql
            st.session_state.columns = columns
            st.session_state.results = results
            st.session_state.answer = answer


# --- Clarification flow ---
if st.session_state.pending_question:
    st.markdown('<div class="section-label">Needs clarification</div>', unsafe_allow_html=True)

    st.write("**Your question:**")
    st.info(st.session_state.pending_question)

    st.write("**Please specify the metric:**")
    for clarification in st.session_state.clarification_questions:
        st.write(f"- {clarification}")

    clarification_answer = st.text_input(
        "Your clarification",
        key="clarification_input",
        placeholder="e.g. Revenue"
    )

    if st.button("Submit Clarification", type="primary"):
        if not clarification_answer.strip():
            st.warning("Please provide a clarification.")
        else:
            original_question = st.session_state.pending_question

            combined_question = f"""
Original user request:
{original_question}

Clarification provided by the user:
{clarification_answer}

Interpretation:
Answer the ORIGINAL request using the clarification as the requested ranking or filtering metric.

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

            st.session_state.pending_question = None
            st.session_state.clarification_questions = []

            sql, columns, results, answer = run_pipeline(combined_question, original_question)
            st.session_state.sql = sql
            st.session_state.columns = columns
            st.session_state.results = results
            st.session_state.answer = answer
            st.rerun()


# --- Results ---
if st.session_state.answer:
    st.markdown('<div class="section-label">Answer</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="answer-box">{st.session_state.answer}</div>', unsafe_allow_html=True)

if st.session_state.sql:
    st.markdown('<div class="section-label">Generated SQL</div>', unsafe_allow_html=True)
    st.code(st.session_state.sql, language="sql")

if st.session_state.columns and st.session_state.results:
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)
    table_data = [dict(zip(st.session_state.columns, row)) for row in st.session_state.results]
    st.dataframe(table_data, use_container_width=True)


with st.sidebar:
    st.markdown("## About")
    st.write(
        """
        This application converts natural-language questions into SQL queries.

        **Pipeline**
        1. Question
        2. Clarification
        3. SQL generation
        4. SQL validation
        5. Database execution
        6. Plain-language answer
        """
    )
    st.divider()
    st.caption("Text → SQL Console")