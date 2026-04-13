# QwenClaw — Operations Log

## What is this
Personal AI assistant in Telegram powered by Qwen Code CLI.
One-command installer for Ubuntu/Debian VPS. Free (1000 req/day).
GitHub: https://github.com/a-prs/QwenClaw

## Current state (2026-04-13)
- Bot works end-to-end: text messages, voice (Groq), sessions, inline buttons
- Tested on clean Ubuntu 24.04 VPS (1 vCPU, 1GB RAM)
- Installer handles: Node.js 20, Qwen CLI, Python venv, systemd, OAuth
- Self-update via /update command (git pull + restart from Telegram)
- Self-configure voice via /setup command (Groq API key via chat)

## Issues resolved during development

### Installer
1. `curl|bash` breaks stdin → detect pipe, tell user to download first
2. NodeSource setup_20.x deprecated on Ubuntu 24.04 → GPG key + manual repo
3. Missing ca-certificates, gnupg → added to apt install
4. `useradd -m` creates skeleton → git clone fails → removed -m flag
5. pip install too slow, SSH drops → show progress, verify after install
6. CRLF from Windows git → .gitattributes eol=lf + sed strip
7. npm global bin not in PATH → always symlink to /usr/local/bin/
8. .env world-readable → chmod 600
9. git pull as root in qwenbot-owned dir → safe.directory

### Qwen CLI
1. `--max-turns` flag doesn't exist → removed
2. `--auth-type qwen-oauth` required for non-interactive mode
3. `qwen auth qwen-oauth` (not `auth login --auth-type`)
4. JSON output is array `[{...}]` not line-by-line → rewrote parser
5. OAuth on headless: works via device flow (prints URL, user opens in browser)
6. OAuth needs 2 attempts: first to register, second to complete OAuth

### Architecture
1. is_busy flag loses messages → in-memory queue (5 msg)
2. Root + --yolo dangerous → dedicated qwenbot user + systemd sandbox
3. Markdown breaks Telegram HTML → md_to_telegram_html() + fallback

## Server requirements
- 1 vCPU, 512MB-1GB RAM, 5-10GB disk
- Ubuntu 22.04+ / Debian 11+
- No GPU needed (all AI is cloud-based)

## Install command
```
curl -fsSL https://raw.githubusercontent.com/a-prs/QwenClaw/main/install.sh -o /tmp/install.sh && sudo bash /tmp/install.sh
```
