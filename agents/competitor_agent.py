"""
Competitor Agent — identifies and analyzes competitors,
competitive advantages, and market gaps for a startup idea.
"""

from pydantic import BaseModel

from agents.base_agent import BaseAgent
from models.input import StartupInput
from models.reports import CompetitorReport
from prompts.competitor_prompt import build_competitor_prompt


class CompetitorAgent(BaseAgent):
    """
    Evaluates the competitive landscape of a startup idea.

    Analysis covers:
        - Direct and indirect competitor identification
        - Competitor strengths and weaknesses
        - Competitive advantages for the startup
        - Market gaps and opportunities
        - Overall competitiveness score
    """

    @property
    def agent_name(self) -> str:
        return "Competitor Agent"

    @property
    def report_model(self) -> type[BaseModel]:
        return CompetitorReport

    def build_prompt(self, startup: StartupInput) -> str:
        return build_competitor_prompt(startup)
