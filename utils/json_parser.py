"""
JSON parsing utility.
Extracts valid JSON from Gemini responses that may include
markdown code fences or surrounding text.
"""

import json
import re
from typing import Any, Optional


def extract_json(text: str) -> Optional[dict[str, Any]]:
    """
    Extract a JSON object from raw LLM text output.

    Handles cases where the model wraps JSON inside ```json ... ```
    code blocks, or returns JSON mixed with conversational text.

    Args:
        text: Raw string output from the Gemini API.

    Returns:
        Parsed dict if extraction succeeds, else None.
    """
    if not text or not text.strip():
        return None

    # ── Attempt 1: strip markdown code fences ──────────────
    fenced = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            pass

    # ── Attempt 2: find the outermost { ... } block ────────
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    # ── Attempt 3: direct parse ────────────────────────────
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
