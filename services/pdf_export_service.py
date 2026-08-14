"""Generate downloadable PDF reports for startup validation results."""

from __future__ import annotations

import os
import re
from datetime import datetime
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, ListFlowable


def _sanitize_filename(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip())
    return cleaned or "startup_report"


def _append_value(story: list[Any], label: str, value: Any, styles: dict[str, ParagraphStyle]) -> None:
    if value is None:
        return

    if isinstance(value, (dict, list)):
        if isinstance(value, dict):
            if label:
                story.append(Paragraph(f"<b>{label}</b>", styles["Heading3"]))
            for key, item in value.items():
                _append_value(story, f"{key}", item, styles)
        else:
            if label:
                story.append(Paragraph(f"<b>{label}</b>", styles["Heading3"]))
            for index, item in enumerate(value, start=1):
                if isinstance(item, (dict, list)):
                    _append_value(story, f"Item {index}", item, styles)
                else:
                    story.append(Paragraph(f"• {item}", styles["BodyText"]))
        return

    text = str(value)
    story.append(Paragraph(f"<b>{label}:</b> {text}", styles["BodyText"]))


def generate_report_pdf_bytes(report_payload: dict[str, Any], idea: str) -> bytes:
    """Render a PDF report into bytes without writing to disk."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.HexColor("#4c1d95"),
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=colors.HexColor("#1d4ed8"),
        spaceAfter=8,
        leading=16,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=4,
    )

    def _append_summary(title: str, text: str | None) -> None:
        if not text:
            return
        story.append(Paragraph(title, heading_style))
        story.append(Paragraph(str(text), body_style))
        story.append(Spacer(1, 6))

    def _append_bullets(title: str, items: list[str] | None) -> None:
        if not items:
            return
        story.append(Paragraph(title, heading_style))
        for item in items:
            story.append(Paragraph(f"• {item}", body_style))
        story.append(Spacer(1, 6))

    story: list[Any] = []
    story.append(Paragraph("Startup Validation Report", title_style))
    story.append(Paragraph("AI-generated startup assessment", subtitle_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Startup Idea", heading_style))
    story.append(Paragraph(idea or "No idea provided", body_style))
    story.append(Spacer(1, 10))

    data = report_payload
    if isinstance(report_payload, dict):
        data = report_payload.get("data", report_payload)

    reports = {}
    if isinstance(data, dict):
        reports = data.get("reports", {}) if isinstance(data.get("reports"), dict) else {}

    final = reports.get("final_decision", {}) if isinstance(reports, dict) else {}
    market = reports.get("market_analysis", {}) if isinstance(reports, dict) else {}
    competitor = reports.get("competitor_analysis", {}) if isinstance(reports, dict) else {}
    risk = reports.get("risk_analysis", {}) if isinstance(reports, dict) else {}
    investor = reports.get("investor_analysis", {}) if isinstance(reports, dict) else {}

    if final:
        _append_summary("Final Verdict", final.get("final_verdict") or final.get("verdict") or "N/A")
        _append_summary("Why", final.get("executive_summary") or final.get("verdict_reasoning") or final.get("summary"))
        _append_bullets(
            "Recommended Next Steps",
            final.get("recommended_next_steps") or final.get("next_steps") or [],
        )

    if market:
        _append_summary("Market Summary", market.get("market_viability_summary") or market.get("summary") or market.get("market_opportunity") or market.get("market_analysis_summary"))
        if market.get("market_size_estimate"):
            story.append(Paragraph(f"Market Size: {market['market_size_estimate']}", body_style))
        if market.get("market_growth_rate"):
            story.append(Paragraph(f"Growth Rate: {market['market_growth_rate']}", body_style))
        story.append(Spacer(1, 6))

    if competitor:
        _append_summary("Competition Summary", competitor.get("competitive_landscape_summary") or competitor.get("summary") or competitor.get("market_competition_summary"))
        if competitor.get("threat_level"):
            story.append(Paragraph(f"Threat Level: {competitor['threat_level']}", body_style))
        story.append(Spacer(1, 6))

    if risk:
        _append_summary("Risk Summary", risk.get("risk_summary") or risk.get("summary") or risk.get("risk_overview"))
        if isinstance(risk.get("risks"), list):
            top_risks = [
                f"{r.get('risk_name') or r.get('name') or 'Risk'}: {r.get('description') or r.get('impact') or ''}".strip()
                for r in risk.get("risks", [])[:3]
            ]
            _append_bullets("Top Risks", [r for r in top_risks if r])
        story.append(Spacer(1, 6))

    if investor:
        _append_summary("Investor Summary", investor.get("investor_attractiveness_summary") or investor.get("summary") or investor.get("investment_overview"))
        if investor.get("funding_stage_recommendation"):
            story.append(Paragraph(f"Funding Stage: {investor['funding_stage_recommendation']}", body_style))
        _append_bullets("Investment Highlights", investor.get("investment_highlights") or investor.get("key_highlights") or [])
        story.append(Spacer(1, 6))

    if not final and not market and not competitor and not risk and not investor:
        story.append(Paragraph("Report Details", heading_style))
        if isinstance(data, dict):
            for key, value in data.items():
                _append_summary(key.replace("_", " ").title(), str(value))
        else:
            story.append(Paragraph(str(data), body_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def generate_report_pdf(report_payload: dict[str, Any], idea: str, output_path: str | None = None) -> str:
    """Create a PDF report and save it to the desktop by default."""
    pdf_bytes = generate_report_pdf_bytes(report_payload, idea)

    if output_path is None:
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        os.makedirs(desktop_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{_sanitize_filename(idea)}_{timestamp}.pdf"
        output_path = os.path.join(desktop_dir, filename)

    with open(output_path, "wb") as fh:
        fh.write(pdf_bytes)

    return output_path
