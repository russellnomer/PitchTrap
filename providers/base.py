"""
Provider abstraction layer.

Any telephony/SMS provider must implement this interface so the rest of
PitchTrap remains provider-agnostic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseProvider(ABC):
    """Common interface for Twilio, SignalWire, and future providers."""

    def __init__(self, credentials: dict[str, str]):
        self.credentials = credentials

    @abstractmethod
    def validate_credentials(self) -> tuple[bool, str]:
        """
        Returns (success: bool, message: str)
        Called during onboarding before we store the keys.
        """
        ...

    @abstractmethod
    def send_sms(self, to: str, body: str, from_number: str) -> dict[str, Any]:
        """Send an outbound SMS. Returns provider response dict."""
        ...

    @abstractmethod
    def build_voice_response(self, say_text: str, gather: bool = False, action_url: Optional[str] = None) -> str:
        """
        Return the raw XML / response body that should be sent back to the
        provider for an incoming voice call.
        """
        ...

    @abstractmethod
    def get_provider_name(self) -> str:
        ...
