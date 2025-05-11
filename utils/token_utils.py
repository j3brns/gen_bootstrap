# utils/token_utils.py

import subprocess

DEFAULT_ENCODING = "cl100k_base"  # Example encoding


def count_text_tokens(text: str, encoding: str = DEFAULT_ENCODING) -> int:
    """Counts the number of tokens in a given text string."""
    try:
        result = subprocess.run(
            ["poetry", "run", "ttok", text], capture_output=True, text=True, check=True
        )
        return int(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error counting tokens: {e}")
        return 0


def trim_text_to_tokens(
    text: str, max_tokens: int, encoding: str = DEFAULT_ENCODING
) -> str:
    """Trims text to a maximum number of tokens."""
    try:
        result = subprocess.run(
            ["poetry", "run", "ttok", "-t", str(max_tokens), text],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error trimming text: {e}")
        return ""
