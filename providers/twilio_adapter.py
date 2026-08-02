"""
Twilio implementation of the provider interface.
"""

from __future__ import annotations

from typing import Any, Optional

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

from .base import BaseProvider


class TwilioAdapter(BaseProvider):

    def __init__(self, credentials: dict[str, str]):
        super().__init__(credentials)
        self.account_sid = credentials.get("account_sid")
        self.auth_token = credentials.get("auth_token")
        self.client = Client(self.account_sid, self.auth_token) if self.account_sid and self.auth_token else None

    def get_provider_name(self) -> str:
        return "twilio"

    def validate_credentials(self) -> tuple[bool, str]:
        if not self.account_sid or not self.auth_token:
            return False, "Missing Account SID or Auth Token"
        try:
            # Lightweight validation call
            account = self.client.api.accounts(self.account_sid).fetch()
            if account.status == "active":
                return True, f"Valid Twilio account: {account.friendly_name}"
            return False, f"Account status is {account.status}"
        except Exception as e:
            return False, f"Twilio validation failed: {str(e)[:120]}"

    def send_sms(self, to: str, body: str, from_number: str) -> dict[str, Any]:
        if not self.client:
            raise RuntimeError("Twilio client not initialized")
        message = self.client.messages.create(
            body=body,
            from_=from_number,
            to=to,
        )
        return {"sid": message.sid, "status": message.status}

    def build_voice_response(self, say_text: str, gather: bool = False, action_url: Optional[str] = None) -> str:
        resp = VoiceResponse()
        resp.say(say_text, voice="Polly.Matthew", language="en-US")

        if gather and action_url:
            g = Gather(
                input="speech",
                action=action_url,
                method="POST",
                speech_timeout="auto",
                timeout=8,
                language="en-US",
            )
            resp.append(g)
            # Fallback if no speech
            resp.say("I did not receive a response. Goodbye.")
            resp.hangup()

        return str(resp)
