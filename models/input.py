"""
Pydantic models for startup idea input data.
These models define the structured input that users provide
and that gets passed to each AI agent for analysis.
"""

from pydantic import BaseModel, Field
from typing import Optional


class StartupInput(BaseModel):
    """
    Schema for the startup idea submitted by the user.
    This is the primary input consumed by all agents.
    """

    idea: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="The startup idea or business description",
        examples=[
            "An electric scooter rental platform with an app-based booking system, "
            "solar-powered charging stations, and AI-optimized route planning."
        ],
    )
