from openenv_core.env_server import Action, Observation, State
from pydantic import Field
from typing import Optional


class PiiRedactorAction(Action):
    """Action for the Pii Redactor environment."""
    redacted_text: str = Field(..., description="The text with PII replaced by [REDACTED]")


class PiiRedactorObservation(Observation):
    """Observation from the Pii Redactor environment."""
    raw_text: str = Field(..., description="The raw text containing sensitive data")
    task_description: str = Field(..., description="Description of what needs to be redacted")


class PiiRedactorState(State):
    """State of the Pii Redactor environment."""
    raw_text: str = Field(..., description="The original raw text")
    ground_truth: str = Field(..., description="The correctly redacted text")
    task_type: str = Field(..., description="Easy, Medium, or Hard")
