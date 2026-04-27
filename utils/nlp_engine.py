import re


def summarize_text(text, max_sentences=3):
    """
    Basic extractive summarization.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)

    if len(sentences) <= max_sentences:
        return text

    return " ".join(sentences[:max_sentences])


def extract_keywords(text):
    """
    Extract important legal keywords.
    """
    legal_terms = [
        "contract",
        "agreement",
        "negligence",
        "liability",
        "fraud",
        "property",
        "murder",
        "appeal",
        "damages",
        "breach",
        "injunction",
        "evidence"
    ]

    found = []

    text_lower = text.lower()

    for term in legal_terms:
        if term in text_lower:
            found.append(term.title())

    return found