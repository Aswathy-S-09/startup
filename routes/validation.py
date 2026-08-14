"""
Validation API routes.

Provides endpoints for:
    - Full startup validation (all 5 agents)
    - Individual agent analyses (market / competitor / risk / investor)
    - Health check
"""

from io import BytesIO
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import logging
import os

from models.input import StartupInput
from services.validation_service import (
    run_full_validation,
    run_market_analysis,
    run_competitor_analysis,
    run_risk_analysis,
    run_investor_analysis,
)
from services.pdf_export_service import generate_report_pdf, generate_report_pdf_bytes

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Startup Validation"])


# ── Health Check ──────────────────────────────────────────

@router.get("/health")
def health_check():
    """Check if the API is running."""
    return {"status": "healthy", "service": "Startup Validator API"}


# ── Full Validation ──────────────────────────────────────

@router.post("/validate")
def validate_startup(startup: StartupInput):
    """
    Run the full 5-agent pipeline against the startup idea.

    Agents executed in order:
    1. Market Agent
    2. Competitor Agent
    3. Risk Agent
    4. Investor Agent
    5. Final Decision Agent (synthesizes all above)

    Returns a combined report with results from all agents plus
    a final go/no-go verdict.
    """
    try:
        result = run_full_validation(startup)
        return {
            "success": True,
            "data": result,
        }
    except Exception as e:
        logger.exception("Full validation failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate/download")
def download_validation_report(startup: StartupInput):
    """Generate a PDF report and save it to the user's desktop."""
    try:
        result = run_full_validation(startup)
        output_path = generate_report_pdf(result, startup.idea)
        return {
            "success": True,
            "downloaded_to": output_path,
            "filename": os.path.basename(output_path),
        }
    except Exception as e:
        logger.exception("PDF report generation failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/pdf")
def export_pdf_from_report(payload: dict[str, Any] = Body(...)):
    """Generate a downloadable PDF from an existing analysis report payload."""
    idea = payload.get("idea", "Startup Report")
    report = payload.get("report")
    if report is None:
        raise HTTPException(status_code=422, detail="Missing report payload for PDF export.")

    try:
        pdf_bytes = generate_report_pdf_bytes(report, idea)
        safe_name = (''.join(ch if ch.isalnum() else '_' for ch in idea).strip('_') or 'startup_report')[:50]
        filename = f"{safe_name}.pdf"
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        logger.exception("PDF export failed")
        raise HTTPException(status_code=500, detail=str(e))


# ── Individual Agent Endpoints ────────────────────────────

@router.post("/analyze/market")
def analyze_market(startup: StartupInput):
    """
    Run only the Market Agent.

    Returns market size, growth rate, trends, opportunities,
    and viability score.
    """
    try:
        report = run_market_analysis(startup)
        return {
            "success": True,
            "agent": "Market Agent",
            "data": report,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Market analysis failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/competitor")
def analyze_competitor(startup: StartupInput):
    """
    Run only the Competitor Agent.

    Returns competitor profiles, competitive advantages,
    market gaps, and competitiveness score.
    """
    try:
        report = run_competitor_analysis(startup)
        return {
            "success": True,
            "agent": "Competitor Agent",
            "data": report,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Competitor analysis failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/risk")
def analyze_risk(startup: StartupInput):
    """
    Run only the Risk Agent.

    Returns identified risks, likelihood/impact ratings,
    mitigation strategies, and overall risk score.
    """
    try:
        report = run_risk_analysis(startup)
        return {
            "success": True,
            "agent": "Risk Agent",
            "data": report,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Risk analysis failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/investor")
def analyze_investor(startup: StartupInput):
    """
    Run only the Investor Agent.

    Returns investment highlights, funding stage recommendation,
    revenue model assessment, exit potential, and attractiveness score.
    """
    try:
        report = run_investor_analysis(startup)
        return {
            "success": True,
            "agent": "Investor Agent",
            "data": report,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Investor analysis failed")
        raise HTTPException(status_code=500, detail=str(e))
