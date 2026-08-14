"""
Validation Service — orchestrates the execution of multiple AI agents
to produce a startup validation analysis.

Agent pipeline:
  1. Market Agent       — market size, trends, opportunities
  2. Competitor Agent   — competitive landscape, advantages, gaps
  3. Risk Agent         — risk identification, scoring, mitigation
  4. Investor Agent     — funding readiness, attractiveness, exit potential
  5. Final Decision Agent — synthesizes all reports → go/no-go verdict
"""

import logging
import time
from typing import Any

from models.input import StartupInput
from agents.market_agent import MarketAgent
from agents.competitor_agent import CompetitorAgent
from agents.risk_agent import RiskAgent
from agents.investor_agent import InvestorAgent
from agents.decision_agent import DecisionAgent

logger = logging.getLogger(__name__)

# ── Agent instances (singleton-like, stateless) ────────────
market_agent = MarketAgent()
competitor_agent = CompetitorAgent()
risk_agent = RiskAgent()
investor_agent = InvestorAgent()
decision_agent = DecisionAgent()


def run_market_analysis(startup: StartupInput) -> dict[str, Any]:
    """
    Run only the Market Agent on the given startup idea.

    Args:
        startup: Validated startup input.

    Returns:
        Market analysis report dict.
    """
    return market_agent.run(startup)


def run_competitor_analysis(startup: StartupInput) -> dict[str, Any]:
    """
    Run only the Competitor Agent on the given startup idea.

    Args:
        startup: Validated startup input.

    Returns:
        Competitor analysis report dict.
    """
    return competitor_agent.run(startup)


def run_risk_analysis(startup: StartupInput) -> dict[str, Any]:
    """
    Run only the Risk Agent on the given startup idea.

    Args:
        startup: Validated startup input.

    Returns:
        Risk analysis report dict.
    """
    return risk_agent.run(startup)


def run_investor_analysis(startup: StartupInput) -> dict[str, Any]:
    """
    Run only the Investor Agent on the given startup idea.

    Args:
        startup: Validated startup input.

    Returns:
        Investor attractiveness report dict.
    """
    return investor_agent.run(startup)


def run_full_validation(startup: StartupInput) -> dict[str, Any]:
    """
    Run all agents in sequence and aggregate their results.

    Pipeline:
        1. Market Agent
        2. Competitor Agent
        3. Risk Agent
        4. Investor Agent
        5. Final Decision Agent (synthesizes all above)

    Args:
        startup: Validated startup input.

    Returns:
        Dict containing all agent reports, the final decision, and metadata.
    """
    idea_snippet = startup.idea[:50] + ("..." if len(startup.idea) > 50 else "")
    logger.info("═" * 60)
    logger.info("Starting full validation for idea: %s", idea_snippet)
    logger.info("═" * 60)

    start_time = time.time()
    results: dict[str, Any] = {
        "idea_snippet": idea_snippet,
        "agents_executed": [],
        "reports": {},
        "errors": {},
    }

    # ── Phase 1: Run the four analysis agents ─────────────
    analysis_agents = [
        ("market_analysis", market_agent),
        ("competitor_analysis", competitor_agent),
        ("risk_analysis", risk_agent),
        ("investor_analysis", investor_agent),
    ]

    for index, (agent_key, agent) in enumerate(analysis_agents):
        try:
            if index > 0:
                logger.info("Pausing briefly between agent calls for stability...")
                time.sleep(1)
                
            report = agent.run(startup)
            results["reports"][agent_key] = report
            results["agents_executed"].append(agent.agent_name)
        except (ValueError, Exception) as e:
            logger.error("Agent '%s' failed: %s", agent.agent_name, e)
            results["errors"][agent_key] = str(e)

    # ── Phase 2: Final Decision Agent (only if all 4 succeeded) ──
    required = {"market_analysis", "competitor_analysis", "risk_analysis", "investor_analysis"}
    available = set(results["reports"].keys())

    if required.issubset(available):
        try:
            logger.info("Pausing briefly before Decision Agent...")
            time.sleep(1)
            
            decision_report = decision_agent.run(
                startup=startup,
                market_report=results["reports"]["market_analysis"],
                competitor_report=results["reports"]["competitor_analysis"],
                risk_report=results["reports"]["risk_analysis"],
                investor_report=results["reports"]["investor_analysis"],
            )
            results["reports"]["final_decision"] = decision_report
            results["agents_executed"].append(decision_agent.agent_name)
        except Exception as e:
            logger.error("Final Decision Agent failed: %s", e)
            results["errors"]["final_decision"] = str(e)
    else:
        missing = required - available
        logger.warning(
            "Skipping Final Decision Agent — missing reports: %s", missing
        )
        results["errors"]["final_decision"] = (
            f"Skipped — prerequisite agents failed: {missing}"
        )

    # ── Metadata ──────────────────────────────────────────
    elapsed = time.time() - start_time
    results["total_time_seconds"] = round(elapsed, 2)
    results["agents_completed"] = len(results["reports"])
    results["agents_failed"] = len(results["errors"])

    logger.info(
        "═ Validation complete: %d/%d agents succeeded (%.1fs) ═",
        results["agents_completed"],
        len(analysis_agents) + 1,  # +1 for decision agent
        elapsed,
    )

    return results
