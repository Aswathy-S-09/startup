"""
Risk Agent — identifies and evaluates startup risks across
market, technology, regulatory, financial, and operational dimensions.
"""

from pydantic import BaseModel

from agents.base_agent import BaseAgent
from models.input import StartupInput
from models.reports import RiskReport
from prompts.risk_prompt import build_risk_prompt


class RiskAgent(BaseAgent):
    """
    Evaluates the risk profile of a startup idea.

    Analysis covers:
        - Market, technology, regulatory, financial, operational risks
        - Likelihood and impact assessment for each risk
        - Individual risk scores
        - Mitigation strategies
        - Overall risk level and composite score
    """

    @property
    def agent_name(self) -> str:
        return "Risk Agent"

    @property
    def report_model(self) -> type[BaseModel]:
        return RiskReport

    def build_prompt(self, startup: StartupInput) -> str:
        return build_risk_prompt(startup)
