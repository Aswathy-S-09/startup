"""
Investor Agent prompt template.
Generates a detailed prompt for Gemini to evaluate investor attractiveness
and funding potential of a startup idea.
"""

from models.input import StartupInput


def build_investor_prompt(startup: StartupInput) -> str:
    """
    Build the investor attractiveness prompt from structured startup input.

    Args:
        startup: Validated startup input data.

    Returns:
        Formatted prompt string that instructs Gemini to return JSON.
    """
    return f"""
You are an expert **Venture Capital Advisor** and **Startup Investment Analyst**
with 20+ years of experience evaluating early-stage and growth-stage startups
for investment. You have evaluated thousands of startups across sectors including
technology, healthcare, sustainability, fintech, and consumer products.

## Your Task

Analyze the following startup idea from an investor's perspective. Evaluate its
investment attractiveness, funding readiness, and potential for returns.

## Startup Details

- **Startup Idea / Business Description:**
{startup.idea}

## Analysis Requirements

Evaluate the following investor-critical dimensions:

1. **Investment Highlights** — List 3-5 compelling reasons why investors
   would be excited about this startup. Focus on USPs, market timing,
   scalability, and competitive moats.

2. **Funding Stage Recommendation** — Recommend the most appropriate current
   funding stage (Pre-Seed, Seed, Series A, etc.) based on the idea's maturity
   and capital requirements. Explain why.

3. **Estimated Funding Requirement** — Estimate a realistic funding range
   needed to reach the next milestone (e.g., $500K–$1M for MVP, etc.).

4. **Potential Investor Types** — Identify 3-5 types of investors most likely
   to back this startup (e.g., impact VCs, industry-specific angels, corporate
   VCs, government grants, etc.).

5. **Revenue Model Assessment** — Evaluate the startup's potential revenue
   models and their viability. Which model(s) would resonate best with investors?

6. **Estimated Revenue Projections** — Provide realistic revenue projections for
   the next 12-24 months, including the main revenue drivers.

7. **Return on Investment (ROI)** — Estimate the investor ROI potential and
   time horizon, expressed in a clear statement.

8. **Funding Amount Required** — State the funding amount needed to reach the
   next major milestone and why that investment is required.

6. **Scalability Assessment** — Assess the startup's ability to scale rapidly.
   What are the key scaling levers and bottlenecks?

7. **Exit Potential** — Evaluate the exit opportunities (IPO, strategic acquisition,
   merger). Who are the likely acquirers? What is the estimated exit timeline?

8. **Investment Red Flags** — Identify 3-5 concerns or red flags that would
   make investors hesitant. These must be specific to this startup.

9. **Investor Attractiveness Score** — Rate the overall investment attractiveness
   from 0 to 10.

10. **Key Insights** — List 3-5 most important insights from an investor's perspective.

11. **Recommendations** — Provide 3-5 recommendations for making the startup
    more attractive to investors.

## Output Format

Return your analysis as a valid JSON object with **exactly** this structure:

```json
{{
    "investment_highlights": ["string", "string", "..."],
    "funding_stage_recommendation": "string — recommended stage and reasoning",
    "estimated_funding_requirement": "string — e.g., '$500K – $2M for MVP and first 18 months'",
    "estimated_revenue_projections": "string — projected revenue for the next 12-24 months",
    "roi_projection": "string — expected investor ROI and timeline",
    "funding_amount_required": "string — funding required to reach next milestone",
    "potential_investor_types": [
        {{
            "investor_type": "string — type of investor",
            "reasoning": "string — why they would invest",
            "examples": "string — example firms or programs"
        }}
    ],
    "revenue_model_assessment": "string — evaluation of revenue models (3-4 sentences)",
    "scalability_assessment": "string — scaling potential evaluation (3-4 sentences)",
    "exit_potential": {{
        "exit_options": ["string", "string"],
        "likely_acquirers": ["string", "string"],
        "estimated_timeline": "string — e.g., '5-8 years'"
    }},
    "investment_red_flags": ["string", "string", "..."],
    "investor_attractiveness_score": 7.5,
    "key_insights": ["string", "string", "..."],
    "recommendations": ["string", "string", "..."]
}}
```

## Important Rules

- Return ONLY the JSON object — no markdown, no explanations, no code fences.
- All scores must be between 0.0 and 10.0.
- Be realistic and specific — generic advice is not acceptable.
- Red flags must be honest and startup-specific, not generic.
- Funding estimates should be realistic for the stage and industry.
""".strip()
