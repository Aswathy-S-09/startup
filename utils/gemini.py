"""
Enhanced Gemini API client for the Startup Validator platform.
Provides both raw text and structured JSON generation capabilities
with automatic retry and error handling.
"""

import os
import time
import random
import logging
from typing import Any, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_RETRIES, RETRY_DELAY_SECONDS
from utils.json_parser import extract_json

load_dotenv()

logger = logging.getLogger(__name__)

# ── Gemini client singleton ────────────────────────────────
client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt: str, model: Optional[str] = None) -> str:
    """
    Send a prompt to Gemini and return the raw text response.

    Args:
        prompt: The full prompt string.
        model:  Override the default model if needed.

    Returns:
        Response text, or an error message after exhausting retries.
    """
    target_model = model or GEMINI_MODEL

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=prompt,
            )
            return response.text

        except errors.ServerError:
            logger.warning(
                "Gemini server error (attempt %d/%d). Retrying in %ds...",
                attempt, MAX_RETRIES, RETRY_DELAY_SECONDS,
            )
            time.sleep(RETRY_DELAY_SECONDS)
        except errors.ClientError as e:
            # Retry on rate limits (429), fail quickly on other client errors.
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = min(RETRY_DELAY_SECONDS * (2 ** (attempt - 1)), 10)
                wait_time = wait_time + random.uniform(0, 1)
                logger.warning(
                    "Rate limited (attempt %d/%d). Retrying in %.1fs...",
                    attempt, MAX_RETRIES, wait_time,
                )
                time.sleep(wait_time)
            else:
                logger.error("Gemini client error (not retryable): %s", e)
                raise
        except Exception as e:
            logger.error("Unexpected Gemini error: %s", e)
            raise

    return "Gemini server is currently busy. Please try again later."


def ask_gemini_json(prompt: str, model: Optional[str] = None) -> Optional[dict[str, Any]]:
    """
    Send a prompt to Gemini and parse the response as JSON.

    The prompt should instruct the model to return JSON.
    This function handles extraction from markdown fences, etc.

    Args:
        prompt: The full prompt (should request JSON output).
        model:  Override the default model if needed.

    Returns:
        Parsed dict on success, None on failure.
    """
    def ask_gemini_json(prompt: str, model: Optional[str] = None) -> Optional[dict[str, Any]]:
    raw_text = ask_gemini(prompt, model)

    if raw_text.startswith("Gemini server is currently busy"):
        logger.error("Could not get Gemini response after retries.")
        return None

    # Log full Gemini response
    logger.info("=" * 80)
    logger.info("RAW GEMINI RESPONSE:")
    logger.info(raw_text)
    logger.info("=" * 80)

    parsed = extract_json(raw_text)

    if parsed is None:
        logger.error(
            "Failed to parse JSON from Gemini response. Raw output:\n%s",
            raw_text[:500],
        )

    return parsed