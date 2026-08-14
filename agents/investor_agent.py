"""
Investor Agent — evaluates the investment attractiveness,
funding readiness, and investor appeal of a startup idea.
"""

from pydantic import BaseModel

from agents.base_agent import BaseAgent
from models.input import StartupInput
from models.reports import InvestorReport
from prompts.investor_prompt import build_investor_prompt


class InvestorAgent(BaseAgent):
    """
    Evaluates the investor attractiveness of a startup idea.

    Analysis covers:
        - Investment highlights and red flags
        - Funding stage and requirement estimation
        - Revenue model and scalability assessment
        - Exit potential and acquirer landscape
        - Overall investor attractiveness score
    """

    @property
    def agent_name(self) -> str:
        return "Investor Agent"

    @property
    def report_model(self) -> type[BaseModel]:
        return InvestorReport

    def build_prompt(self, startup: StartupInput) -> str:
        return build_investor_prompt(startup)
