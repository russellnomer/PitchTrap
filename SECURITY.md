# Security Policy

## Classification

**Public** GitHub repository (`russellnomer/PitchTrap`). This file is intentionally high-level. Do not publish exploit steps, payloads, or credential values.

The tracker listed the Repl as private; the GitHub repo is public. Assume anything in this tree is world-readable.

## Data handled

This snapshot does not include application source or a database. If the original Repl was used:

- Offer text (email/SMS) and call transcripts would be sensitive
- Phone numbers and Twilio call metadata
- Session and database credentials named in the manifest

Do not upload real customer messages, call recordings, or dumps here.

## Authentication

No application auth is implemented in this repository (no app code). Any future telephony bot must authenticate Twilio callbacks (request signature) and protect admin/debug routes.

## Secrets (names only)

`SECRETS_MANIFEST.txt` lists environment **names** only. Application-relevant names include:

- `DATABASE_URL`
- `SESSION_SECRET`
- `PGDATABASE`, `PGHOST`, `PGPASSWORD`, `PGPORT`, `PGUSER`

The rest of the file is Replit/Nix/tooling noise. **Values must never be committed.** Because this repo is public, treat every credential that ever lived in the VibeCode Repl as potentially exposed: rotate database passwords, session secrets, and any Twilio/LLM keys, then store replacements only in a secret manager.

`gitbackup/backup.sh` documents a `GH_TOKEN` / `GITHUB_TOKEN` GitHub PAT used for backups. That token must be an account secret, never a file in git, and should be least-privilege / fine-grained.

## Attack surface

- Public git history and attached playbook text
- Future: Twilio webhooks, Flask admin, classifier APIs, outbound calling
- Backup script that talks to the GitHub API when `GH_TOKEN` is set

## Findings

1. **Incomplete public snapshot** — design docs only; do not assume production hardening exists.
2. **Public secrets manifest** — even names help attackers guess the stack (Postgres + sessions). Rotate associated credentials.
3. **Telephony products are high-risk** — when code is added, verify provider signatures, rate-limit inbound webhooks, and keep recordings out of logs.

## Reporting

Report vulnerabilities to **help@russellnomerconsulting.com**.

For this public repo, do not include secret values, personal data, or step-by-step exploit details in GitHub issues. Email first if the report is sensitive.

Owner: Russell Nomer / Russell Nomer Consulting.
