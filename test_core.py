#!/usr/bin/env python3
"""Quick verification of triage + bot + provider loading."""

from triage import classify_offer
from bot_logic import next_response, clear_state
from providers import get_provider

print("=== Triage ===")
samples = [
    "PRE-APPROVED $250k! Offer expires TODAY!",
    "1.35 factor rate, daily ACH of $412 from Fast Cash Capital",
    "Term sheet: $120k, 36 monthly payments, APR 12.4%, amortization available",
]
for s in samples:
    r = classify_offer(s)
    print(f"  {r.category:5} | {r.reasons[0][:60]}")

print("\n=== Bot sequence ===")
sid = "test-1"
clear_state(sid)
for i in range(6):
    print(f"  Q{i+1}: {next_response(sid, f'answer {i}')[:70]}...")

print("\n=== Provider loading ===")
try:
    get_provider("twilio", {"account_sid": "ACtest", "auth_token": "test"})
    print("  Twilio adapter loaded")
    get_provider("signalwire", {"project_id": "p", "api_token": "t", "space_url": "example.signalwire.com"})
    print("  SignalWire adapter loaded")
except Exception as e:
    print("  Error:", e)

print("\nCore MVP is ready.")
