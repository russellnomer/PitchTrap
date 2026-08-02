"""
PitchTrap – Multi-provider, BYOK monetized MVP + Demo Mode
"""

from __future__ import annotations

import logging
from flask import Flask, request, Response, render_template, redirect, url_for, session, flash, jsonify

from config import SECRET_KEY, DEBUG, PORT
from triage import classify_offer
from bot_logic import next_response, clear_state, is_finished
from providers import get_provider
from demo import process_demo_turn, reset_demo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pitchtrap")

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ---------------------------------------------------------------------------
# Public pages
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/demo")
def demo_page():
    """Interactive simulation – no provider keys required."""
    return render_template("demo.html")


@app.route("/demo/turn", methods=["POST"])
def demo_turn():
    """API endpoint for the interactive demo."""
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id") or request.remote_addr or "anon"
    user_text = data.get("text", "")

    if data.get("reset"):
        reset_demo(session_id)
        return jsonify({"ok": True, "message": "Demo reset."})

    result = process_demo_turn(session_id, user_text)
    return jsonify(result)


@app.route("/onboarding")
def onboarding():
    """Guided flow for users to connect their own Twilio or SignalWire keys."""
    return render_template("onboarding.html")


@app.route("/onboarding/connect", methods=["POST"])
def onboarding_connect():
    """
    Receive provider choice + credentials from the user.
    In production this would:
      1. Validate the keys
      2. Encrypt and store them against the user account
      3. Mark the account as activated
    """
    provider = request.form.get("provider", "").lower()
    if provider not in ("twilio", "signalwire"):
        flash("Please choose a valid provider", "error")
        return redirect(url_for("onboarding"))

    creds = {}
    if provider == "twilio":
        creds = {
            "account_sid": request.form.get("account_sid", "").strip(),
            "auth_token": request.form.get("auth_token", "").strip(),
        }
    else:
        creds = {
            "project_id": request.form.get("project_id", "").strip(),
            "api_token": request.form.get("api_token", "").strip(),
            "space_url": request.form.get("space_url", "").strip(),
        }

    try:
        adapter = get_provider(provider, creds)
        ok, message = adapter.validate_credentials()
        if not ok:
            flash(f"Validation failed: {message}", "error")
            return redirect(url_for("onboarding"))

        session["provider"] = provider
        session["provider_ok"] = True
        flash(f"Successfully connected {provider.title()}: {message}", "success")
        return redirect(url_for("dashboard"))
    except Exception as e:
        flash(f"Error: {str(e)[:150]}", "error")
        return redirect(url_for("onboarding"))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", provider=session.get("provider"))


# ---------------------------------------------------------------------------
# Telephony / SMS webhooks (multi-tenant ready)
# ---------------------------------------------------------------------------

@app.route("/voice/incoming", methods=["POST"])
def voice_incoming():
    call_sid = request.values.get("CallSid", "unknown")
    speech = request.values.get("SpeechResult", "").strip()

    provider_name = session.get("provider", "twilio")
    creds = {}  # real system loads encrypted keys by tenant
    try:
        adapter = get_provider(provider_name, creds)
    except Exception:
        from twilio.twiml.voice_response import VoiceResponse
        resp = VoiceResponse()
        resp.say("PitchTrap is not fully configured for this number yet.")
        resp.hangup()
        return Response(str(resp), mimetype="application/xml")

    if not speech:
        twiml = adapter.build_voice_response(
            "Thank you for calling. Please briefly describe the funding offer you are presenting.",
            gather=True,
            action_url="/voice/incoming",
        )
        return Response(twiml, mimetype="application/xml")

    result = classify_offer(speech)
    logger.info("Voice triage %s → %s", call_sid, result.category)

    if result.category == "Ugly":
        twiml = adapter.build_voice_response(
            "We are not interested in this type of offer. Please remove this number from your list. Goodbye."
        )
        clear_state(call_sid)
        return Response(twiml, mimetype="application/xml")

    if result.category == "Good":
        twiml = adapter.build_voice_response(
            "This appears complete enough for human review. Please email the full written offer. Goodbye."
        )
        clear_state(call_sid)
        return Response(twiml, mimetype="application/xml")

    bot_text = next_response(call_sid, speech)
    finished = is_finished(call_sid)

    twiml = adapter.build_voice_response(
        bot_text,
        gather=not finished,
        action_url="/voice/incoming" if not finished else None,
    )
    if finished:
        clear_state(call_sid)
    return Response(twiml, mimetype="application/xml")


@app.route("/sms/incoming", methods=["POST"])
def sms_incoming():
    body = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")

    result = classify_offer(body)
    logger.info("SMS triage from %s → %s", from_number, result.category)

    if result.category == "Ugly":
        reply = "Not interested. Please remove this number from your list."
    elif result.category == "Good":
        reply = "Thank you. Please email the complete written offer for review."
    else:
        reply = next_response(f"sms-{from_number}", body)

    return Response(
        f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{reply}</Message></Response>',
        mimetype="application/xml",
    )


# ---------------------------------------------------------------------------
# Local runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
