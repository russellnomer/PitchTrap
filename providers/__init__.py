from .base import BaseProvider
from .twilio_adapter import TwilioAdapter
from .signalwire_adapter import SignalWireAdapter

PROVIDERS = {
    "twilio": TwilioAdapter,
    "signalwire": SignalWireAdapter,
}


def get_provider(name: str, credentials: dict) -> BaseProvider:
    cls = PROVIDERS.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown provider: {name}")
    return cls(credentials)
