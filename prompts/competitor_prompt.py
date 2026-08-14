"""
Competitor Agent prompt template.
Generates a detailed prompt for Gemini to perform competitive analysis
on a given startup idea.
"""

from models.input import StartupInput


def build_competitor_prompt(startup: StartupInput) -> str:
    """
    Build the competitor analysis prompt from structured startup input.

    Args:
        startup: Validated startup input data.

    Returns:
        Formatted prompt string that instructs Gemini to return JSON.
    """
    return f"""
You are an expert **Competitive Intelligence Analyst** with 20+ years of experience
in identifying, profiling, and evaluating business competitors across industries.
You specialize in competitive strategy, market positioning, SWOT analysis, and
identifying exploitable gaps in the competitive landscape.

## Your Task

Analyze the competitive landscape for the following startup idea. Identify real-world
competitors (or realistic hypothetical ones if real data is limited), evaluate their
strengths and weaknesses, and determine how the startup can differentiate itself.

## Startup Details

- **Startup Idea / Business Description:**
{startup.idea}

## Analysis Requirements

1. **Competitor Identification** — Identify 5-8 competitors, including both direct
   competitors (solving the same problem in a similar way) and indirect competitors
   (alternative solutions or adjacent players). Use real-world company names wherever
   possible, especially current players in the same category as the startup idea.
   For each competitor, provide:
   - Name and brief description
   - Whether they are Direct or Indirect
   - 2-3 strengths
   - 2-3 weaknesses
   - Estimated market share (if available)

2. **Competitive Landscape Summary** — Provide an overview of the competitive
   landscape: how crowded is the market, who are the dominant players, what does
   the competition intensity look like.

3. **Competitive Advantages** — Identify 3-5 ways the startup can differentiate
   itself from existing competitors. For each advantage, assess its sustainability
   (High / Medium / Low).

4. **Market Gaps** — Identify 3-5 gaps in the current market that competitors are
   not adequately addressing. Rate each gap's opportunity level (High / Medium / Low).

5. **Threat Level** — Assess the overall competitive threat level for the startup
   (High / Medium / Low) based on the number, strength, and positioning of
   competitors.

6. **Competitiveness Score** — Rate the startup's competitiveness on a scale of
   0 to 10 (higher = more competitive / better positioned).

7. **Key Insights** — List the 3-5 most important competitive insights.

8. **Recommendations** — Provide 3-5 strategic recommendations for competing
   effectively in this market.

## Output Format

Return your analysis as a valid JSON object with **exactly** this structure:

```json
{{
    "competitors": [
        {{
            "name": "string — competitor name",
            "type": "Direct | Indirect",
            "description": "string — what they do",
            "strengths": ["string", "string"],
            "weaknesses": ["string", "string"],
            "market_share": "string or null"
        }}
    ],
    "competitive_landscape_summary": "string — overview (3-4 sentences)",
    "competitive_advantages": [
        {{
            "advantage": "string — advantage name",
            "description": "string — detailed explanation",
            "sustainability": "High | Medium | Low"
        }}
    ],
    "market_gaps": [
        {{
            "gap": "string — gap name",
            "description": "string — explanation",
            "opportunity_level": "High | Medium | Low"
        }}
    ],
    "threat_level": "High | Medium | Low",
    "competitiveness_score": 0.0,
    "key_insights": ["string", "string", "..."],
    "recommendations": ["string", "string", "..."]
}}
```

## Important Rules

- Return ONLY the JSON object — no markdown, no explanations, no code fences.
- All scores must be between 0.0 and 10.0.
- Provide 5-8 competitors and 3-5 items for other list fields.
- Use real competitor names where possible for credibility.
- Be specific and actionable in your analysis.
""".strip()
