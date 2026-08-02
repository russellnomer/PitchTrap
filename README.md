# PitchTrap

**The digital sentinel for small business owners.**

PitchTrap triages unsolicited sales pitches (email, SMS, and phone calls) and, when warranted, deploys a structured engagement agent that wastes the salesperson’s time with precise, high-friction questions.

This is the **monetized MVP**:
- Users bring their own Twilio **or** SignalWire keys (BYOK)
- Thin provider abstraction so the core logic is provider-agnostic
- Activation fee + monthly subscription (Stripe)
- PitchTrap itself pays for almost nothing except hosting

---

## Architecture Overview

```
Incoming Offer
  ├── Email
  ├── SMS      ──→  Provider Abstraction  ──→  Triage Engine  ──→  Engagement Bot
  └── Voice
```

### Core Components

| Module | Responsibility |
|--------|----------------|
| `providers/` | Thin abstraction over Twilio & SignalWire |
| `triage.py` | Ugly / Bad / Good classification (Master Playbook) |
| `bot_logic.py` | Stateful Level 2 interrogation sequence |
| `onboarding/` | Guided key collection + validation flow |
| `app.py` | Flask entrypoint + multi-tenant routing |
| `billing.py` | Stripe activation fee + subscription (stub) |

---

## Business Model

- **Activation Fee**: One-time (covers guided onboarding)
- **Monthly Subscription**: Recurring access to the platform
- **Telephony/SMS costs**: Paid directly by the user to Twilio or SignalWire

PitchTrap never holds or pays for the user’s minutes.

---

## Quick Start (Replit)

1. Clone or pull this repo
2. Add secrets (see `.env.example`)
3. Run `python app.py` or use the Replit Run button
4. Visit the onboarding flow to connect Twilio or SignalWire keys

---

## Supported Providers

- **Twilio** (full SMS + Voice)
- **SignalWire** (full SMS + Voice, Twilio-compatible APIs)

Email intake works independently of either provider.

---

Built by Russell Nomer  
Cybersecurity executive · Builder · Small business defender
