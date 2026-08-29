def analyze_question(question):

    question_lower = question.lower().strip()

    clarification_questions = []

    # =========================================
    # Ranking keywords
    # =========================================

    ranking_words = [
        "top",
        "best",
        "highest",
        "largest"
    ]

    # =========================================
    # Explicit ranking metrics
    # =========================================

    ranking_metrics = [
        "revenue",
        "sales",
        "units sold",
        "quantity",
        "rating",
        "ratings",
        "orders",
        "number of orders",
        "price"
    ]

    # =========================================
    # Natural-language metric phrases
    # =========================================

    spending_phrases = [
        "spent the most",
        "spend the most",
        "spent most",
        "spending the most",
        "highest spending",
        "most money",
        "money spent"
    ]

    order_phrases = [
        "ordered the most",
        "placed the most orders",
        "most orders",
        "most frequently"
    ]

    rating_phrases = [
        "highest rated",
        "highest ratings",
        "best rated"
    ]

    # =========================================
    # Detect ranking
    # =========================================

    is_ranking_question = any(
        word in question_lower
        for word in ranking_words
    )

    # "most" is a ranking indicator only when
    # it is actually describing a ranking metric.
    #
    # Examples:
    #
    # Which customer spent the most money?
    # → known metric → no clarification
    #
    # Which customers ordered the most?
    # → known metric → no clarification
    #
    # Which country has the most customers?
    # → count customers by country → no clarification

    has_most = "most" in question_lower

    # =========================================
    # Detect known metrics
    # =========================================

    has_metric = any(
        metric in question_lower
        for metric in ranking_metrics
    )

    # =========================================
    # Detect natural-language metrics
    # =========================================

    has_spending_metric = any(
        phrase in question_lower
        for phrase in spending_phrases
    )

    has_order_metric = any(
        phrase in question_lower
        for phrase in order_phrases
    )

    has_rating_metric = any(
        phrase in question_lower
        for phrase in rating_phrases
    )

    # =========================================
    # Combine metric detection
    # =========================================

    metric_is_known = (
        has_metric
        or has_spending_metric
        or has_order_metric
        or has_rating_metric
    )

    # =========================================
    # Ranking clarification
    # =========================================

    if is_ranking_question and not metric_is_known:

        clarification_questions.append(
            "What metric should I use for the ranking "
            "(for example revenue, units sold, rating, "
            "or number of orders)?"
        )

    # =========================================
    # Handle "most" questions
    # =========================================

    if has_most and not metric_is_known:

        # "most customers" means COUNT customers,
        # which is already an explicit metric.
        if "most customers" in question_lower:

            pass

        # Other uses of "most" may require clarification.
        elif not clarification_questions:

            clarification_questions.append(
                "What metric should I use for the ranking "
                "(for example revenue, units sold, rating, "
                "or number of orders)?"
            )

    # =========================================
    # Ambiguous date: "recent"
    # =========================================

    recent_words = [
        "recent",
        "recently",
        "latest"
    ]

    has_ambiguous_date = any(
        word in question_lower
        for word in recent_words
    )

    if has_ambiguous_date:

        clarification_questions.append(
            "What time period should I consider "
            "for 'recent' orders?"
        )

    # =========================================
    # Ambiguous price filter: "expensive"
    # =========================================

    expensive_words = [
        "expensive",
        "costly",
        "high priced",
        "high-price",
        "high priced"
    ]

    has_ambiguous_price = any(
        phrase in question_lower
        for phrase in expensive_words
    )

    if has_ambiguous_price:

        clarification_questions.append(
            "What price threshold should I use "
            "to define 'expensive' products?"
        )

    # =========================================
    # Return result
    # =========================================

    return {
        "clarification_required":
            len(clarification_questions) > 0,

        "clarification_questions":
            clarification_questions
    }


if __name__ == "__main__":

    test_questions = [

        "Which customer spent the most money?",

        "Which customers spent the most money?",

        "Which customers ordered the most?",

        "Which products have the highest ratings?",

        "What are the top 5 products by revenue?",

        "What are the top 10 products?",

        "Show me the best products.",

        "Show me the highest rated products.",

        "Show me recent orders.",

        "Which country has the most customers?",

        "Show me expensive products."
    ]

    for question in test_questions:

        result = analyze_question(question)

        print("\nQuestion:")
        print(question)

        print("\nResult:")
        print(result)

        print("-" * 60)