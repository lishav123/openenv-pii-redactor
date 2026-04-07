import re
import random
from uuid import uuid4
from typing import List, Tuple

from openenv_core.env_server import Environment

try:
    from ..models import PiiRedactorAction, PiiRedactorObservation, PiiRedactorState
except (ImportError, ValueError):
    from models import PiiRedactorAction, PiiRedactorObservation, PiiRedactorState


class PiiRedactorEnvironment(Environment):
    """
    PII Redactor Environment.
    Tasks:
    - Easy: Redact emails.
    - Medium: Redact phone numbers and credit cards.
    - Hard: Redact Names and SSNs embedded in natural language.
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    EMAILS = ["john.doe@example.com", "jane_smith@gmail.com", "support@company.org", "dev.team@startup.io"]
    PHONES = ["(555) 123-4567", "555-987-6543", "555.000.1111", "5551234444"]
    CREDIT_CARDS = ["1234-5678-9012-3456", "9876-5432-1098-7654", "1111222233334444", "5555-6666-7777-8888"]
    NAMES = ["Alice Johnson", "Bob Miller", "Charlie Davis", "Diana Prince"]
    SSNS = ["123-45-6789", "987-65-4321", "000-11-2222", "555-66-7777"]

    TEMPLATES = [
        "Please contact {pii} for more information.",
        "The user's account identifier is {pii}.",
        "Send the invoice to {pii} immediately.",
        "Your new verification code is tied to {pii}.",
        "I saw {pii} at the conference yesterday.",
        "The document was signed by {pii} on Friday.",
        "My social security number is {pii}.",
        "You can reach me at {pii} anytime."
    ]

    def __init__(self):
        self._state = None
        self._task_levels = ["Easy", "Medium", "Hard"]

    def _generate_task(self) -> Tuple[str, str, str]:
        level = random.choice(self._task_levels)
        pii_items = []
        task_description = ""

        if level == "Easy":
            pii_items = [random.choice(self.EMAILS)]
            task_description = "Redact all email addresses in the following text."
        elif level == "Medium":
            pii_items = [random.choice(self.PHONES), random.choice(self.CREDIT_CARDS)]
            task_description = "Redact all phone numbers and credit card numbers in the following text."
        elif level == "Hard":
            pii_items = [random.choice(self.NAMES), random.choice(self.SSNS)]
            task_description = "Redact all full names and Social Security Numbers (SSNs) in the following text."

        raw_text = random.choice(self.TEMPLATES).format(pii=pii_items[0])
        if len(pii_items) > 1:
            raw_text += " Also, " + random.choice(self.TEMPLATES).format(pii=pii_items[1])

        ground_truth = raw_text
        for item in pii_items:
            ground_truth = ground_truth.replace(item, "[REDACTED]")

        return raw_text, ground_truth, task_description, level

    def reset(self) -> PiiRedactorObservation:
        raw_text, ground_truth, task_description, level = self._generate_task()
        self._state = PiiRedactorState(
            episode_id=str(uuid4()),
            step_count=0,
            raw_text=raw_text,
            ground_truth=ground_truth,
            task_type=level
        )
        return PiiRedactorObservation(
            raw_text=raw_text,
            task_description=task_description,
            reward=0.01, # FIX: Replaced 0.0 with 0.01
            done=False
        )

    def step(self, action: PiiRedactorAction) -> PiiRedactorObservation:
        self._state.step_count += 1
        
        pred = action.redacted_text
        gt = self._state.ground_truth
        
        if pred == gt:
            reward = 0.99 # FIX: Replaced 1.0 with 0.99
        else:
            gt_parts = gt.split("[REDACTED]")
            pred_parts = pred.split("[REDACTED]")
            
            if len(gt_parts) == len(pred_parts):
                matches = sum(1 for g, p in zip(gt_parts, pred_parts) if g == p)
                reward = matches / len(gt_parts)
            else:
                # Penalize for wrong number of redactions
                reward = max(0.01, 0.5 * (1.0 - abs(len(gt_parts) - len(pred_parts)) / max(len(gt_parts), len(pred_parts))))

        # FINAL SAFETY CLAMP: Guarantees the reward is strictly between (0, 1)
        reward = max(0.01, min(0.99, float(reward)))

        done = True # Single step environment for this task
        
        return PiiRedactorObservation(
            raw_text=self._state.raw_text,
            task_description="Task complete.",
            reward=reward,
            done=done,
            metadata={"ground_truth": gt}
        )

    @property
    def state(self) -> PiiRedactorState:
        return self._state