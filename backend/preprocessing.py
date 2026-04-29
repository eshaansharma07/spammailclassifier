from __future__ import annotations

import re
import string


def clean_text(text: str) -> str:
    """Normalize email content before vectorization."""
    lowered = text.lower()
    without_punctuation = lowered.translate(str.maketrans("", "", string.punctuation))
    return re.sub(r"\s+", " ", without_punctuation).strip()
