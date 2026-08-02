"""
PitchTrap global configuration and Master Playbook constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
PORT = int(os.getenv("PORT", 5000))

# Used to encrypt user-provided Twilio / SignalWire credentials at rest
CREDENTIALS_ENCRYPTION_KEY = os.getenv("CREDENTIALS_ENCRYPTION_KEY", "dev-encryption-key-change-me")

# Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_ACTIVATION_PRICE_ID = os.getenv("STRIPE_ACTIVATION_PRICE_ID")
STRIPE_SUBSCRIPTION_PRICE_ID = os.getenv("STRIPE_SUBSCRIPTION_PRICE_ID")

# ---------------------------------------------------------------------------
# Master Playbook – Triage Keywords
# ---------------------------------------------------------------------------

UGLY_KEYWORDS = [
    "offer expires today", "limited time", "pre-approved", "you've been pre-approved",
    "guaranteed approval", "guaranteed funding", "no credit check", "bad credit ok",
    "instant approval", "same day funding", "cash in 24 hours", "easy terms", "no paperwork",
]

UGLY_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"]

BAD_KEYWORDS = [
    "factor rate", "daily payment", "weekly payment", "daily remittance", "weekly remittance",
    "merchant cash advance", "mca", "fast cash", "lightning capital", "express funds",
    "sudden funds", "quick capital", "rapid funding", "business cash advance",
]

GOOD_SIGNALS = [
    "amortization", "apr", "annual percentage rate", "monthly payment",
    "term of", "months", "years", "total repayment", "total funding", "number of installments",
]

# ---------------------------------------------------------------------------
# Level 2 Engagement Questions
# ---------------------------------------------------------------------------

LEVEL_2_QUESTIONS = [
    {
        "id": 1,
        "text": (
            "I might be interested. I just need to confirm a few things for my records first. "
            "What is the simple, annualized interest rate — the APR — for this offer? "
            "Please do not give me a factor rate. I need the actual APR."
        ),
    },
    {
        "id": 2,
        "text": (
            "Thank you. Are you a direct lender or a broker? "
            "If you are a broker, please tell me the name of the actual funder."
        ),
    },
    {
        "id": 3,
        "text": (
            "Can you please send me a full amortization schedule for this loan? "
            "I need to see principal and interest broken out for every payment."
        ),
    },
    {
        "id": 4,
        "text": (
            "What is your company’s state lending license number? "
            "Please provide the license number and the state that issued it."
        ),
    },
    {
        "id": 5,
        "text": (
            "Finally, please confirm in writing that there are no prepayment penalties "
            "and that the only fee is the stated interest. Can you confirm that?"
        ),
    },
]

CLOSING_STATEMENT = (
    "I have everything I need for now. Please email the full written offer, "
    "including the APR, amortization schedule, and license information to the address "
    "on file. I will review it with my advisor and get back to you if we decide to proceed. "
    "Thank you for your time."
)
