"""
Pydantic models for structured agent output reports.
Each agent returns a well-defined JSON structure so the
Final Decision-Making Agent can consume them consistently.
"""

from pydantic import BaseModel, Field, validator
from typing import Any, Dict, List, Optional, Union


# ═══════════════════════════════════════════════════════════════
#  MARKET AGENT REPORT
# ═══════════════════════════════════════════════════════════════

class MarketTrend(BaseModel):
    """A single industry trend relevant to the startup."""
    trend: str = Field(..., description="Name or title of the trend")
    description: str = Field(..., description="Brief explanation of the trend")
    relevance: str = Field(..., description="How this trend impacts the startup")


class MarketOpportunity(BaseModel):
    """A market opportunity the startup can leverage."""
    opportunity: str = Field(..., description="Name of the opportunity")
    description: str = Field(..., description="Detailed explanation")
    potential_impact: str = Field(..., description="High / Medium / Low")


class MarketReport(BaseModel):
    """Complete structured output from the Market Agent."""
    agent_name: str = Field(default="Market Agent")

    # Core analysis
    market_size_estimate: str = Field(
        ..., description="Estimated total addressable market (TAM)"
    )
    market_growth_rate: str = Field(
        ..., description="Annual growth rate or CAGR of the market"
    )
    customer_demand_analysis: str = Field(
        ..., description="Assessment of current and projected customer demand"
    )
    target_audience_fit: str = Field(
        ..., description="How well the solution fits the target audience"
    )

    # Trends & opportunities
    industry_trends: List[MarketTrend] = Field(
        ..., description="Key industry trends (3-5 items)"
    )
    market_opportunities: List[MarketOpportunity] = Field(
        ..., description="Market opportunities for the startup (3-5 items)"
    )

    # Summary
    market_viability_summary: str = Field(
        ..., description="Overall summary of market viability"
    )
    market_viability_score: float = Field(
        ..., ge=0, le=10, description="Market viability score from 0 to 10"
    )
    key_insights: List[str] = Field(
        ..., description="Top 3-5 key insights from the analysis"
    )
    recommendations: List[str] = Field(
        ..., description="Strategic recommendations (3-5 items)"
    )


# ═══════════════════════════════════════════════════════════════
#  COMPETITOR AGENT REPORT
# ═══════════════════════════════════════════════════════════════

class Competitor(BaseModel):
    """Profile of a single competitor."""
    name: str = Field(..., description="Competitor company name")
    type: str = Field(..., description="Direct / Indirect")
    description: str = Field(..., description="What the competitor does")
    strengths: List[str] = Field(..., description="Competitor strengths")
    weaknesses: List[str] = Field(..., description="Competitor weaknesses")
    market_share: Optional[str] = Field(
        default=None, description="Estimated market share, if available"
    )


class CompetitiveAdvantage(BaseModel):
    """An advantage the startup has over existing competitors."""
    advantage: str = Field(..., description="Title of the advantage")
    description: str = Field(..., description="Detailed explanation")
    sustainability: str = Field(
        ..., description="How sustainable this advantage is (High / Medium / Low)"
    )


class MarketGap(BaseModel):
    """A gap in the current market that the startup can exploit."""
    gap: str = Field(..., description="Title of the gap")
    description: str = Field(..., description="Explanation of the gap")
    opportunity_level: str = Field(
        ..., description="High / Medium / Low"
    )


class CompetitorReport(BaseModel):
    """Complete structured output from the Competitor Agent."""
    agent_name: str = Field(default="Competitor Agent")

    # Competitors
    competitors: List[Competitor] = Field(
        ..., description="List of identified competitors (5-8 items)"
    )

    # Analysis
    competitive_landscape_summary: str = Field(
        ..., description="Overview of the competitive landscape"
    )
    competitive_advantages: List[CompetitiveAdvantage] = Field(
        ..., description="Startup's competitive advantages (3-5 items)"
    )
    market_gaps: List[MarketGap] = Field(
        ..., description="Identified gaps in the market (3-5 items)"
    )

    # Summary
    threat_level: str = Field(
        ..., description="Overall competitive threat level (High / Medium / Low)"
    )
    competitiveness_score: float = Field(
        ..., ge=0, le=10, description="Competitiveness score from 0 to 10"
    )
    key_insights: List[str] = Field(
        ..., description="Top 3-5 key insights from the analysis"
    )
    recommendations: List[str] = Field(
        ..., description="Strategic recommendations (3-5 items)"
    )


# ═══════════════════════════════════════════════════════════════
#  RISK AGENT REPORT
# ═══════════════════════════════════════════════════════════════

class Risk(BaseModel):
    """A single identified risk for the startup."""
    risk_name: str = Field(..., description="Name of the risk")
    category: str = Field(
        ..., description="Market | Technology | Regulatory | Financial | Operational | Competitive"
    )
    description: str = Field(..., description="Detailed description of the risk")
    likelihood: str = Field(..., description="High | Medium | Low")
    impact: str = Field(..., description="High | Medium | Low")
    risk_score: float = Field(..., ge=0, le=10, description="Risk severity score 0-10")
    mitigation_strategies: Union[List[str], str] = Field(
        ..., description="Concrete mitigation strategies (2-3 items)"
    )

    @validator("mitigation_strategies", pre=True)
    def _normalize_mitigation(cls, value):
        if isinstance(value, str):
            lines = [line.strip("- •\n \t") for line in value.splitlines() if line.strip()]
            return lines or [value.strip()]
        return value


class RiskReport(BaseModel):
    """Complete structured output from the Risk Agent."""
    agent_name: str = Field(default="Risk Agent")

    risks: List[Risk] = Field(..., description="Identified risks (5-8 items)")
    overall_risk_level: str = Field(
        ..., description="High | Medium | Low — overall risk profile"
    )
    risk_summary: str = Field(
        ..., description="Overview of the startup's risk landscape (3-4 sentences)"
    )
    risk_score: float = Field(
        ..., ge=0, le=10,
        description="Composite risk score 0-10 (10 = extremely risky)"
    )
    key_insights: Union[List[str], str] = Field(
        ..., description="Top 3-5 risk-related insights"
    )
    recommendations: Union[List[str], str] = Field(
        ..., description="Risk mitigation recommendations (3-5 items)"
    )

    @validator("key_insights", "recommendations", pre=True)
    def _normalize_list_fields(cls, value):
        if isinstance(value, str):
            lines = [line.strip("- •\n \t") for line in value.splitlines() if line.strip()]
            return lines or [value.strip()]
        return value


# ═══════════════════════════════════════════════════════════════
#  INVESTOR AGENT REPORT
# ═══════════════════════════════════════════════════════════════

class InvestorType(BaseModel):
    """A type of investor likely to back this startup."""
    investor_type: str = Field(..., description="Type of investor")
    reasoning: str = Field(..., description="Why they would invest")
    examples: Union[List[str], str] = Field(..., description="Example firms or programs")

    @validator("examples", pre=True)
    def _normalize_examples(cls, value):
        if isinstance(value, str):
            lines = [line.strip("- •\n \t") for line in value.splitlines() if line.strip()]
            return lines or [value.strip()]
        return value


class ExitPotential(BaseModel):
    """Exit opportunity assessment."""
    exit_options: Union[List[str], str] = Field(..., description="Possible exit routes")
    likely_acquirers: Union[List[str], str] = Field(..., description="Likely acquiring companies")
    estimated_timeline: str = Field(..., description="Estimated exit timeline")

    @validator("exit_options", "likely_acquirers", pre=True)
    def _normalize_exit_lists(cls, value):
        if isinstance(value, str):
            lines = [line.strip("- •\n \t") for line in value.splitlines() if line.strip()]
            return lines or [value.strip()]
        return value


class InvestorReport(BaseModel):
    """Complete structured output from the Investor Agent."""
    agent_name: str = Field(default="Investor Agent")

    investment_highlights: Union[List[str], str] = Field(
        ..., description="Key reasons investors would be excited (3-5 items)"
    )
    funding_stage_recommendation: str = Field(
        ..., description="Recommended funding stage and reasoning"
    )
    estimated_funding_requirement: str = Field(
        ..., description="Estimated funding range for the next milestone"
    )
    estimated_revenue_projections: str = Field(
        ..., description="Projected revenue for the next 12-24 months"
    )
    roi_projection: str = Field(
        ..., description="Expected investor ROI and timeline"
    )
    funding_amount_required: str = Field(
        ..., description="Funding amount required to reach the next milestone"
    )
    potential_investor_types: List[InvestorType] = Field(
        ..., description="Types of investors likely to invest (3-5 items)"
    )
    revenue_model_assessment: str = Field(
        ..., description="Evaluation of revenue models (3-4 sentences)"
    )
    scalability_assessment: str = Field(
        ..., description="Scaling potential evaluation (3-4 sentences)"
    )
    exit_potential: ExitPotential = Field(
        ..., description="Exit opportunity analysis"
    )
    investment_red_flags: Union[List[str], str] = Field(
        ..., description="Investor concerns and red flags (3-5 items)"
    )
    investor_attractiveness_score: float = Field(
        ..., ge=0, le=10, description="Overall investor attractiveness score 0-10"
    )
    key_insights: Union[List[str], str] = Field(
        ..., description="Top 3-5 insights from investor perspective"
    )
    recommendations: Union[List[str], str] = Field(
        ..., description="Recommendations to improve investor appeal (3-5 items)"
    )

    @validator(
        "investment_highlights",
        "investment_red_flags",
        "key_insights",
        "recommendations",
        pre=True,
    )
    def _normalize_string_lists(cls, value):
        if isinstance(value, str):
            lines = [line.strip("- •\n \t") for line in value.splitlines() if line.strip()]
            return lines or [value.strip()]
        return value


# ═══════════════════════════════════════════════════════════════
#  FINAL DECISION AGENT REPORT
# ═══════════════════════════════════════════════════════════════

class RoadmapPhase(BaseModel):
    """A phase in the 12-month startup roadmap."""
    phase: str = Field(..., description="Phase name and timeframe")
    milestones: List[str] = Field(..., description="Key milestones in this phase")
    goal: str = Field(..., description="Key goal for this phase")


class ScoreBreakdown(BaseModel):
    """Score breakdown across all agents."""
    market_score: float = Field(..., ge=0, le=10)
    competitiveness_score: float = Field(..., ge=0, le=10)
    risk_score: float = Field(..., ge=0, le=10)
    investor_score: float = Field(..., ge=0, le=10)


class DecisionReport(BaseModel):
    """Complete structured output from the Final Decision Agent."""
    agent_name: str = Field(default="Final Decision Agent")

    final_verdict: str = Field(
        ..., description="STRONG GO | GO | CONDITIONAL GO | NO-GO"
    )
    overall_score: float = Field(
        ..., ge=0, le=10, description="Weighted composite score across all agents"
    )
    executive_summary: str = Field(
        ..., description="4-5 sentence executive summary"
    )
    strengths: List[str] = Field(
        ..., description="Top strengths of the startup (3-5 items)"
    )
    weaknesses: List[str] = Field(
        ..., description="Critical weaknesses or challenges (3-5 items)"
    )
    conditions: List[str] = Field(
        default=[], description="Conditions for CONDITIONAL GO (empty if not applicable)"
    )
    recommended_next_steps: List[str] = Field(
        ..., description="Prioritized action items (3-5 items)"
    )
    roadmap: List[RoadmapPhase] = Field(
        ..., description="12-month milestone roadmap (4-5 phases)"
    )
    verdict_reasoning: str = Field(
        ..., description="3-4 sentence explanation of the verdict"
    )
    score_breakdown: ScoreBreakdown = Field(
        ..., description="Individual agent score components"
    )
