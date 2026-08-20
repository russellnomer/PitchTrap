# PitchTrap

PitchTrap (Repl name **VibeCode**) is a small-business “annoyance automator”: a gatekeeper that triages unsolicited business-loan and merchant-cash-advance pitches and, for the predatory ones, wastes the salesperson’s time instead of yours.

The product idea is a **Triage Engine** plus an **Engagement Bot**:

1. Ingest email/SMS offer text.
2. Classify it **Ugly** (block), **Bad** (high-cost MCA / factor-rate junk), or **Good** (transparent, monthly, documented APR).
3. For Bad offers, walk a script of pointed questions (true APR, factor rate vs APR, daily vs monthly drafts, prepayment penalties) designed to expose the business model.

This repository currently holds the **product brief and playbook**, not a complete running app. Treat it as the PitchTrap design snapshot.

## Who it is for

- Small-business owners drowning in loan spam
- Operators who want a TCPA-aware, documented “STOP / Do Not Call / waste their time” workflow
- Russell Nomer Consulting experiments in defensive automation

## Live domains

No custom domain is recorded. There is no production service in this tree.

## Stack (intended)

From the design prompt in `attached_assets/`:

| Layer | Intended choice |
| --- | --- |
| App | Python / Flask |
| Classification | Local `transformers` or an LLM API |
| Telephony | Twilio (inbound/outbound, TwiML) |
| Voice | Expressive TTS (e.g. ElevenLabs) |
| Data | Postgres names appear in `SECRETS_MANIFEST.txt` (`DATABASE_URL`, `PG*`) |

Planned modules (not present as source in this backup): `app.py`, `triage.py`, `bot_logic.py`, `templates/`.

## How to run

This GitHub snapshot does **not** contain application source. To rebuild:

1. Read the vibe prompt and Master Playbook under `attached_assets/`.
2. Scaffold Flask + Twilio as described there.
3. Put secrets in the host secret manager (see [SECURITY.md](SECURITY.md)) — never in git.
4. Local sketch once code exists:

```bash
pip install -r requirements.txt
export TWILIO_* OPENAI_API_KEY DATABASE_URL SESSION_SECRET
flask --app app run --port 5000
```

`gitbackup/backup.sh` is the universal Replit→GitHub backup helper (requires a `GH_TOKEN` account secret). It is not the product.

## Repository layout

```text
attached_assets/     Vibe-coding prompt + Master Playbook (triage + waste-their-time script)
gitbackup/backup.sh  Replit snapshot script
SECRETS_MANIFEST.txt Env *names* from the original Repl (no values)
.gitignore
```

## Replit

- Repl: [https://replit.com/@RussellNomer/VibeCode](https://replit.com/@RussellNomer/VibeCode)
- GitHub: [https://github.com/russellnomer/PitchTrap](https://github.com/russellnomer/PitchTrap)

## Owner

Russell Nomer / Russell Nomer Consulting.
