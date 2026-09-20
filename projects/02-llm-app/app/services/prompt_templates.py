PROMPT_TEMPLATES: dict[str, str] = {
    "chat": (
        "You are a helpful, harmless, and honest AI assistant. "
        "Respond to the user's message in a clear and concise manner.\n\n"
        "{user_message}"
    ),
    "summarize": (
        "You are an expert summarizer. Provide a concise summary of the following text "
        "in no more than {max_length} words. Focus on the key points and main ideas.\n\n"
        "Text to summarize:\n{text}"
    ),
    "classify": (
        "You are a text classification expert. Classify the following text into exactly "
        "one of the provided categories. Respond with ONLY the category name and a "
        "confidence score between 0 and 1.\n\n"
        "Categories: {categories}\n\n"
        "Text to classify:\n{text}\n\n"
        "Respond in this exact format:\n"
        "Category: <category>\n"
        "Confidence: <score>"
    ),
    "extract_keywords": (
        "Extract the top 5 keywords or key phrases from the following text. "
        "Return them as a comma-separated list.\n\n"
        "Text:\n{text}"
    ),
    "translate": (
        "Translate the following text to {target_language}. "
        "Maintain the original tone and meaning.\n\n"
        "Text:\n{text}"
    ),
    "code_review": (
        "You are a senior software engineer performing a code review. "
        "Analyze the following code and provide constructive feedback on:\n"
        "1. Potential bugs or issues\n"
        "2. Performance concerns\n"
        "3. Code style and readability\n"
        "4. Security considerations\n\n"
        "Code to review:\n```\n{code}\n```"
    ),
    "explain": (
        "Explain the following concept or text in simple terms that a "
        "beginner could understand. Use analogies where helpful.\n\n"
        "{text}"
    ),
}
