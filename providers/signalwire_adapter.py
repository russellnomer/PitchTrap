"""
SignalWire implementation of the provider interface.

SignalWire offers Twilio-compatible APIs, so the adapter is intentionally thin.
"""

from __future__ import annotations

from typing import Any, Optional

import requests
from twilio.rest import Client  # SignalWire is Twilio-API compatible
from twilio.twiml.voice_response import VoiceResponse, Gather

from .base import BaseProvider


class SignalWireAdapter(BaseProvider):

    def __init__(self, credentials: dict[str, str]):
        super().__init__(credentials)
        self.project_id = credentials.get("project_id")
        self.api_token = credentials.get("api_token")
        self.space_url = credentials.get("space_url", "").rstrip("/")

        # SignalWire is reachable via the standard Twilio client by pointing
        # the base URL at the user's Space.
        if self.project_id and self.api_token and self.space_url:
            self.client = Client(
                self.project_id,
                self.api_token,
                http_client=None,
            )
            # Override the base URL for SignalWire
            self.client.api.base_url = f"https://{self.space_url}/api"
        else:
            self.client = None

    def get_provider_name(self) -> str:
        return "signalwire"

    def validate_credentials(self) -> tuple[bool, str]:
        if not all([self.project_id, self.api_token, self.space_url]):
            return False, "Missing Project ID, API Token, or Space URL"
        try:
            # Simple authenticated request against the Space
            url = f"https://{self.space_url}/api/laml/2010-04-01/Accounts/{self.project_id}.json"
            resp = requests.get(url, auth=(self.project_id, self.api_token), timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return True, f"Valid SignalWire project: {data.get('friendly_name', self.project_id)}"
            return False, f"SignalWire returned status {resp.status_code}"
        except Exception as e:
            return False, f"SignalWire validation failed: {str(e)[:120]}"

    def send_sms(self, to: str, body: str, from_number: str) -> dict[str, Any]:
        if not self.client:
            raise RuntimeError("SignalWire client not initialized")
        message = self.client.messages.create(
            body=body,
            from_=from_number,
            to=to,
        )
        return {"sid": message.sid, "status": message.status}

    def build_voice_response(self, say_text: str, gather: bool = False, action_url: Optional[str] = None) -> str:
        # SignalWire accepts standard TwiML
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
            resp.say("I did not receive a response. Goodbye.")
            resp.hangup()

        return str(resp)
