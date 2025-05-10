# utils/token_utils.py

from token_count_trim import count_tokens, trim_text

# Note: The specific model encoding might need to be configured
# depending on the exact model used. token_count_trim supports
# various encodings (e.g., "cl100k_base" for OpenAI models).
# For Google models, the Vertex AI SDK might provide more accurate
# token counting methods, which could be wrapped here.
# For Alpha, we'll use a generic encoding or one suitable for common models.
DEFAULT_ENCODING = "cl100k_base"  # Example encoding


def count_text_tokens(text: str, encoding: str = DEFAULT_ENCODING) -> int:
    """Counts the number of tokens in a given text string."""
    return count_tokens(text, encoding)


def trim_text_to_tokens(
    text: str, max_tokens: int, encoding: str = DEFAULT_ENCODING
) -> str:
    """Trims text to a maximum number of tokens."""
    return trim_text(text, max_tokens, encoding)


# Example usage (for testing)


if __name__ == "__main__":
    sample_text = "This is a sample sentence to test token counting and trimming."
    max_limit = 10

    token_count = count_text_tokens(sample_text)
    print(f"Original text token count: {token_count}")

    trimmed_text = trim_text_to_tokens(sample_text, max_limit)
    print(f"Trimmed text to {max_limit} tokens: {trimmed_text}")

    trimmed_count = count_text_tokens(trimmed_text)
    print(f"Trimmed text token count: {trimmed_count}")
