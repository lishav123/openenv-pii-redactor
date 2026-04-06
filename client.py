from typing import Dict, Any
from openenv.core import EnvClient
from openenv.core.client_types import StepResult

try:
    from .models import PiiRedactorAction, PiiRedactorObservation, PiiRedactorState
except ImportError:
    from models import PiiRedactorAction, PiiRedactorObservation, PiiRedactorState
    
class PiiRedactorEnv(EnvClient[PiiRedactorAction, PiiRedactorObservation, PiiRedactorState]):
    """HTTP Client for the PII Redactor Environment."""

    def _step_payload(self, action: PiiRedactorAction) -> Dict[str, Any]:
        return {"redacted_text": action.redacted_text}

    def _parse_result(self, payload: Dict[str, Any]) -> StepResult[PiiRedactorObservation]:
        obs_data = payload.get("observation", {})
        observation = PiiRedactorObservation(
            raw_text=obs_data.get("raw_text", ""),
            task_description=obs_data.get("task_description", ""),
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False)
        )
        return StepResult(
            observation=observation,
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False)
        )

    def _parse_state(self, payload: Dict[str, Any]) -> PiiRedactorState:
        return PiiRedactorState(**payload)