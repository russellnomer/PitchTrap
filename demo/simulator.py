"""
PitchTrap Demo Mode – pure simulation.

No Twilio, no SignalWire, no real credentials required.
Used for sales demos, marketing site, and onboarding previews.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from triage import classify_offer, TriageResult
from bot_logic import LEVEL_2_QUESTIONS, CLOSING_STATEMENT  # re-export for clarity
from config import LEVEL_2_QUESTIONS as QUESTIONS, CLOSING_STATEMENT as CLOSING


@dataclass
class DemoSession:
    session_id: str
    step: int = 0          # 0 = waiting for offer text, 1+ = question index
    category: Optional[str] = None
    finished: bool = False
    history: list[dict] = field(default_factory=list)


_sessions: dict[str, DemoSession] = {}


def get_demo_session(session_id: str) -> DemoSession:
    if session_id not in _sessions:
        _sessions[session_id] = DemoSession(session_id=session_id)
    return _sessions[session_id]


def reset_demo(session_id: str) -> None:
    _sessions.pop(session_id, None)


def process_demo_turn(session_id: str, user_text: str) -> dict:
    """
    Process one turn of the interactive demo.

    Returns a structured response the frontend can render:
    {
        "type": "triage" | "question" | "closing" | "error",
        "category": "Ugly" | "Bad" | "Good" | None,
        "message": "...",
        "finished": bool,
        "step": int
    }
    """
    session = get_demo_session(session_id)
    user_text = (user_text or "").strip()

    if not user_text:
        return {
            "type": "error",
            "category": None,
            "message": "Please paste a sample funding offer or sales pitch.",
            "finished": False,
            "step": session.step,
        }

    # First turn → triage
    if session.step == 0:
        result: TriageResult = classify_offer(user_text)
        session.category = result.category
        session.history.append({"role": "user", "text": user_text})
        session.history.append({
            "role": "system",
            "text": f"Triage result: {result.category} ({result.confidence:.0%}) – {result.reasons[0] if result.reasons else ''}"
        })

        if result.category == "Ugly":
            session.finished = True
            return {
                "type": "triage",
                "category": "Ugly",
                "message": (
                    f"**Triage: Ugly**\n\n"
                    f"Reason: {result.reasons[0] if result.reasons else 'Predatory signals detected'}\n\n"
                    "Action: Immediate block / delete. No engagement."
                ),
                "finished": True,
                "step": 0,
            }

        if result.category == "Good":
            session.finished = True
            return {
                "type": "triage",
                "category": "Good",
                "message": (
                    f"**Triage: Potentially Good**\n\n"
                    f"Reason: {result.reasons[0] if result.reasons else 'Transparent terms detected'}\n\n"
                    "Action: Surface for human review. No bot engagement."
                ),
                "finished": True,
                "step": 0,
            }

        # Bad → start Level 2
        session.step = 1
        question = QUESTIONS[0]["text"]
        session.history.append({"role": "bot", "text": question})
        return {
            "type": "question",
            "category": "Bad",
            "message": (
                f"**Triage: Bad** – Engaging Level 2 playbook\n\n"
                f"Bot: {question}"
            ),
            "finished": False,
            "step": 1,
        }

    # Subsequent turns → walk the questions
    if session.finished:
        return {
            "type": "closing",
            "category": session.category,
            "message": "Demo conversation already finished. Refresh to start over.",
            "finished": True,
            "step": session.step,
        }

    session.history.append({"role": "user", "text": user_text})

    idx = session.step - 1
    if idx >= len(QUESTIONS):
        session.finished = True
        return {
            "type": "closing",
            "category": "Bad",
            "message": f"Bot: {CLOSING}",
            "finished": True,
            "step": session.step,
        }

    # Advance
    session.step += 1
    if session.step > len(QUESTIONS):
        session.finished = True
        session.history.append({"role": "bot", "text": CLOSING})
        return {
            "type": "closing",
            "category": "Bad",
            "message": f"Bot: {CLOSING}",
            "finished": True,
            "step": session.step,
        }

    next_q = QUESTIONS[session.step - 1]["text"]
    session.history.append({"role": "bot", "text": next_q})
    return {
        "type": "question",
        "category": "Bad",
        "message": f"Bot: {next_q}",
        "finished": False,
        "step": session.step,
    }
