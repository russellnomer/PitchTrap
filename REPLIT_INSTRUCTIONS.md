# PitchTrap – Replit Unpack Instructions

**IMPORTANT – READ THIS FIRST**

This repository already contains a complete, working codebase.
Do **NOT** generate, rewrite, scaffold, or “improve” any code.
Do **NOT** run any AI code-generation agents against this project.

Your only job is to **unpack and place** the existing files into the correct locations so the application can run.

## Exact steps for Replit

1. If the files arrive as a zip, extract them so the project root contains:
   - `app.py`
   - `config.py`
   - `triage.py`
   - `bot_logic.py`
   - `requirements.txt`
   - `providers/` (folder)
   - `demo/` (folder)
   - `templates/` (folder)
   - `.env.example`
   - `README.md`

2. Install dependencies once:
   ```
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` (optional for demo mode).

4. Run the application:
   ```
   python app.py
   ```

5. Open the webview / preview URL.

## What is already built

- Full triage engine (Ugly / Bad / Good)
- Level 2 engagement bot
- Multi-provider abstraction (Twilio + SignalWire)
- BYOK onboarding flow
- Interactive Demo Mode at `/demo` (no keys required)
- SMS + Voice webhook stubs

## Do not

- Do not ask the Replit Agent to “build the app”
- Do not regenerate any Python files
- Do not change the folder structure

This is a finished MVP that only needs to be unpacked and run.
