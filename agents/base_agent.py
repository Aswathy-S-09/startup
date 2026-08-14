"""
Base Agent — abstract class for all validation agents.

Every agent in the platform inherits from BaseAgent, ensuring a
consistent interface for prompt building, API calls, response
parsing, and validation.
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel, ValidationError

from models.input import StartupInput
from utils.gemini import ask_gemini_json

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for validation agents.

    Subclasses must implement:
        - `agent_name`        (property)
        - `build_prompt()`    (method)
        - `report_model`      (property → Pydantic model class)
    """

    # ── Abstract interface ────────────────────────────────

    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Human-readable name for this agent."""
        ...

    @abstractmethod
    def build_prompt(self, startup: StartupInput) -> str:
        """Build the full prompt string for this agent."""
        ...

    @property
    @abstractmethod
    def report_model(self) -> type[BaseModel]:
        """The Pydantic model class used to validate the output."""
        ...

    # ── Core execution ────────────────────────────────────

    def run(self, startup: StartupInput) -> dict[str, Any]:
        """
        Execute the full agent pipeline:
        1. Build prompt from startup input.
        2. Send to Gemini API and get JSON response.
        3. Validate response against the Pydantic report model.
        4. Return the validated dict.

        Args:
            startup: Validated startup input data.

        Returns:
            Validated report dict on success.

        Raises:
            ValueError: If Gemini returns invalid or unparseable output
                        after all retries.
        """
        logger.info("🚀 [%s] Starting analysis...", self.agent_name)
        start_time = time.time()

        # Step 1: Build prompt
        prompt = self.build_prompt(startup)
        logger.info("[%s] Prompt built (%d chars)", self.agent_name, len(prompt))

        # Step 2: Call Gemini
        raw_data = ask_gemini_json(prompt)

        if raw_data is None:
            raise ValueError(
                f"[{self.agent_name}] Failed to get valid JSON from Gemini API."
            )

        # Step 3: Validate against Pydantic model
        report = self._validate_report(raw_data)

        elapsed = time.time() - start_time
        logger.info(
            "✅ [%s] Analysis complete (%.1fs)", self.agent_name, elapsed
        )

        return report

    def _validate_report(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate raw JSON data against the agent's Pydantic model.

        Args:
            data: Parsed JSON dict from Gemini.

        Returns:
            Validated and serialized dict.

        Raises:
            ValueError: If validation fails.
        """
        try:
            model_instance = self.report_model(**data)
            return model_instance.model_dump()
        except ValidationError as e:
            logger.error(
                "[%s] Report validation failed:\n%s",
                self.agent_name,
                e.errors(),
            )
            raise ValueError(
                f"[{self.agent_name}] Generated report failed validation: {e}"
            ) from e
