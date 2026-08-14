"""
Final Decision Agent — synthesizes reports from all other agents
and produces a go/no-go verdict with an executive summary and roadmap.

Unlike other agents, this agent takes pre-computed reports as input
instead of calling Gemini for each dimension independently.
"""

import logging
import time
from typing import Any

from models.input import StartupInput
from models.reports import DecisionReport
from prompts.decision_prompt import build_decision_prompt
from utils.gemini import ask_gemini_json

logger = logging.getLogger(__name__)


class DecisionAgent:
    """
    Final synthesis agent that aggregates all other agent reports.

    Unlike BaseAgent subclasses, this agent requires the reports
    from the other agents as input — it cannot run independently.
    """

    agent_name = "Final Decision Agent"

    def run(
        self,
        startup: StartupInput,
        market_report: dict[str, Any],
        competitor_report: dict[str, Any],
        risk_report: dict[str, Any],
        investor_report: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute the final decision pipeline.

        Args:
            startup: Validated startup input data.
            market_report: Output from Market Agent.
            competitor_report: Output from Competitor Agent.
            risk_report: Output from Risk Agent.
            investor_report: Output from Investor Agent.

        Returns:
            Validated decision report dict.

        Raises:
            ValueError: If Gemini returns invalid or unparseable output.
        """
        logger.info("🏁 [%s] Starting final decision synthesis...", self.agent_name)
        start_time = time.time()

        # Build the aggregation prompt
        prompt = build_decision_prompt(
            startup=startup,
            market_report=market_report,
            competitor_report=competitor_report,
            risk_report=risk_report,
            investor_report=investor_report,
        )
        logger.info("[%s] Prompt built (%d chars)", self.agent_name, len(prompt))

        # Call Gemini
        raw_data = ask_gemini_json(prompt)

        if raw_data is None:
            raise ValueError(
                f"[{self.agent_name}] Failed to get valid JSON from Gemini API."
            )

        # Validate against Pydantic model
        try:
            report_instance = DecisionReport(**raw_data)
            report = report_instance.model_dump()
        except Exception as e:
            logger.error("[%s] Report validation failed: %s", self.agent_name, e)
            raise ValueError(
                f"[{self.agent_name}] Generated report failed validation: {e}"
            ) from e

        elapsed = time.time() - start_time
        logger.info(
            "✅ [%s] Decision complete: %s (%.1fs)",
            self.agent_name,
            report.get("final_verdict", "UNKNOWN"),
            elapsed,
        )

        return report
