"""
Stateful Level 2 engagement engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from config import LEVEL_2_QUESTIONS, CLOSING_STATEMENT


@dataclass
class CallState:
    call_sid: str
    current_idx: int = 0
    finished: bool = False
    history: list[str] = field(default_factory=list)


_states: dict[str, CallState] = {}


def get_state(call_sid: str) -> CallState:
    if call_sid not in _states:
        _states[call_sid] = CallState(call_sid=call_sid)
    return _states[call_sid]


def clear_state(call_sid: str) -> None:
    _states.pop(call_sid, None)


def next_response(call_sid: str, user_text: Optional[str] = None) -> str:
    state = get_state(call_sid)
    if user_text:
        state.history.append(user_text[:400])

    if state.finished or state.current_idx >= len(LEVEL_2_QUESTIONS):
        state.finished = True
        return CLOSING_STATEMENT

    question = LEVEL_2_QUESTIONS[state.current_idx]["text"]
    state.current_idx += 1
    if state.current_idx >= len(LEVEL_2_QUESTIONS):
        state.finished = True
    return question


def is_finished(call_sid: str) -> bool:
    return get_state(call_sid).finished
