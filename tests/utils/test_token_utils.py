from utils.token_utils import count_text_tokens, trim_text_to_tokens


def test_count_text_tokens():
    text = "This is a test sentence."
    token_count = count_text_tokens(text)
    assert token_count > 0


def test_trim_text_to_tokens():
    text = "This is a longer test sentence that needs to be trimmed."
    max_tokens = 5
    trimmed_text = trim_text_to_tokens(text, max_tokens)
    assert count_text_tokens(trimmed_text) == len(trimmed_text.split())


def test_count_text_tokens_with_encoding():
    text = "This is a test sentence."
    encoding = "cl100k_base"
    token_count = count_text_tokens(text, encoding)
    assert token_count > 0


def test_trim_text_to_tokens_with_encoding():
    text = "This is a longer test sentence that needs to be trimmed."
    max_tokens = 5
    encoding = "cl100k_base"
    trimmed_text = trim_text_to_tokens(text, max_tokens, encoding)
    assert count_text_tokens(trimmed_text, encoding) == len(trimmed_text.split())
