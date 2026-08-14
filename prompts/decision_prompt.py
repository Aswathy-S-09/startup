"""
Final Decision Agent prompt template.
Aggregates reports from all agents and produces a final
go/no-go recommendation with a comprehensive summary.
"""

from models.input import StartupInput
import json


def build_decision_prompt(
    startup: StartupInput,
    market_report: dict,
    competitor_report: dict,
    risk_report: dict,
    investor_report: dict,
) -> str:
    """
    Build the final decision prompt using all agent reports.

    Args:
        startup: Validated startup input data.
        market_report: Output from Market Agent.
        competitor_report: Output from Competitor Agent.
        risk_report: Output from Risk Agent.
        investor_report: Output from Investor Agent.

    Returns:
        Formatted prompt string that instructs Gemini to return JSON.
    """
    return f"""
You are an expert **Startup Evaluation Committee** — a panel comprising a
market strategist, competitive analyst, risk manager, and venture capitalist.
You have collectively reviewed thousands of startup pitches and made final
go/no-go decisions worth billions in investment.

## Your Task

Based on the comprehensive analysis provided by four specialized agents,
synthesize the insights and make a final, definitive recommendation on
whether this startup should proceed (GO) or should not proceed (NO-GO),
along with a conditional path for improvement.

## Startup Details

- **Startup Idea / Business Description:**
{startup.idea}

## Agent Reports Summary

### Market Analysis
- Market Viability Score: {market_report.get('market_viability_score', 'N/A')}/10
- Market Size: {market_report.get('market_size_estimate', 'N/A')}
- Growth Rate: {market_report.get('market_growth_rate', 'N/A')}
- Summary: {market_report.get('market_viability_summary', 'N/A')}
- Key Insights: {json.dumps(market_report.get('key_insights', []))}

### Competitor Analysis
- Competitiveness Score: {competitor_report.get('competitiveness_score', 'N/A')}/10
- Threat Level: {competitor_report.get('threat_level', 'N/A')}
- Summary: {competitor_report.get('competitive_landscape_summary', 'N/A')}
- Key Insights: {json.dumps(competitor_report.get('key_insights', []))}

### Risk Analysis
- Overall Risk Level: {risk_report.get('overall_risk_level', 'N/A')}
- Risk Score: {risk_report.get('risk_score', 'N/A')}/10
- Summary: {risk_report.get('risk_summary', 'N/A')}
- Key Insights: {json.dumps(risk_report.get('key_insights', []))}

### Investor Analysis
- Investor Attractiveness Score: {investor_report.get('investor_attractiveness_score', 'N/A')}/10
- Recommended Funding Stage: {investor_report.get('funding_stage_recommendation', 'N/A')}
- Estimated Funding: {investor_report.get('estimated_funding_requirement', 'N/A')}
- Key Insights: {json.dumps(investor_report.get('key_insights', []))}

## Decision Requirements

Synthesize all four reports and provide:

1. **Final Verdict** — One of: "STRONG GO", "GO", "CONDITIONAL GO", "NO-GO"
   - STRONG GO: All indicators are highly favorable (scores > 7.5, risks manageable)
   - GO: Most indicators are positive with manageable challenges
   - CONDITIONAL GO: Proceed only if specific critical conditions are met
   - NO-GO: Fundamental flaws that make proceeding inadvisable

2. **Overall Startup Score** — A composite score from 0 to 10 that aggregates
   all four agent scores weighted as:
   - Market Viability: 30%
   - Competitiveness: 25%
   - Risk (inverted, 10-risk_score): 25%
   - Investor Attractiveness: 20%

3. **Executive Summary** — A compelling 4-5 sentence executive summary that
   captures the startup's essence, promise, and key challenges.

4. **Strengths** — Top 3-5 strengths of this startup idea synthesized across all analyses.

5. **Weaknesses** — Top 3-5 critical weaknesses or challenges identified across all analyses.

6. **Conditions (if applicable)** — If verdict is "CONDITIONAL GO", list the 2-5 specific
   conditions that must be met before proceeding. Leave empty array if not applicable.

7. **Recommended Next Steps** — 3-5 concrete, prioritized action items the founding
   team should execute immediately.

8. **12-Month Roadmap** — A high-level 12-month milestone roadmap with 4-5 phases.

9. **Verdict Reasoning** — 3-4 sentences explaining why you reached this verdict.

## Output Format

Return your analysis as a valid JSON object with **exactly** this structure:

```json
{{
    "final_verdict": "STRONG GO | GO | CONDITIONAL GO | NO-GO",
    "overall_score": 7.5,
    "executive_summary": "string — 4-5 sentence executive summary",
    "strengths": ["string", "string", "..."],
    "weaknesses": ["string", "string", "..."],
    "conditions": ["string (only if CONDITIONAL GO, else empty array)"],
    "recommended_next_steps": ["string", "string", "..."],
    "roadmap": [
        {{
            "phase": "string — e.g., 'Phase 1: Validation (0-3 months)'",
            "milestones": ["string", "string"],
            "goal": "string — key goal for this phase"
        }}
    ],
    "verdict_reasoning": "string — 3-4 sentence explanation of verdict",
    "score_breakdown": {{
        "market_score": 0.0,
        "competitiveness_score": 0.0,
        "risk_score": 0.0,
        "investor_score": 0.0
    }}
}}
```

## Important Rules

- Return ONLY the JSON object — no markdown, no explanations, no code fences.
- The overall_score must be a weighted composite (Market 30%, Competitive 25%, Risk-inverted 25%, Investor 20%).
- Be decisive — do not hedge on the final verdict.
- Recommendations must be specific, actionable, and prioritized.
- The roadmap should be realistic and achievable.
""".strip()
