"""
Market Agent — analyzes the target market, size, growth,
trends, and opportunities for a startup idea.
"""

from pydantic import BaseModel

from agents.base_agent import BaseAgent
from models.input import StartupInput
from models.reports import MarketReport
from prompts.market_prompt import build_market_prompt


class MarketAgent(BaseAgent):
    """
    Evaluates the market potential of a startup idea.

    Analysis covers:
        - Market size estimation (TAM / SAM / SOM)
        - Growth rate and CAGR
        - Customer demand assessment
        - Target audience fit
        - Industry trends
        - Market opportunities
        - Overall viability score
    """

    @property
    def agent_name(self) -> str:
        return "Market Agent"

    @property
    def report_model(self) -> type[BaseModel]:
        return MarketReport

    def build_prompt(self, startup: StartupInput) -> str:
        return build_market_prompt(startup)
