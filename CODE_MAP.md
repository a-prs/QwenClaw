## Bot Core
bot/main.py                    — Telegram bot: aiogram 3.x, handlers, keyboards, session management
  :cmd_start()                 — /start greeting with voice status
  :cmd_menu()                  — /menu control panel
  :cmd_new()                   — /new force new session
  :cmd_sessions()              — /sessions list
  :cmd_status()                — /status system info
  :cmd_setup()                 — /setup configure Groq key via chat
  :cmd_update()                — /update self-update from GitHub + restart
  :handle_message()            — Main handler: extract text -> route -> run qwen
  :on_result()                 — Callback when Qwen finishes: send result to Telegram
  :extract_text()              — Text/voice/caption extraction
  :build_main_menu()           — Inline keyboard: sessions, new, status, close all
  :build_sessions_keyboard()   — Paginated session list with switch/close buttons
  NOTE: Buttons on responses use edit_text which replaces the answer — needs fix

bot/qwen_runner.py             — Qwen Code CLI subprocess runner
  :run_qwen()                  — Public API: queue or launch qwen
  :_process_prompt()           — Execute + drain queue
  :_execute_qwen()             — Build cmd, subprocess, parse JSON
  :_parse_output()             — Parse Qwen JSON array [{type:result}]
  NOTE: Qwen outputs JSON array, NOT line-by-line like Claude
  NOTE: --max-turns NOT supported by Qwen CLI
  NOTE: --auth-type qwen-oauth required for every call

bot/config.py                  — .env loader + dynamic config update
  :set_env_var()               — Write key=value to .env file
  :reload_groq_key()           — Hot-reload GROQ_API_KEY without restart

bot/db.py                      — SQLite: sessions + message history
  :init_db()                   — Schema versioning via PRAGMA user_version
  :create_session()            — INSERT OR IGNORE
  :get_active_sessions()       — Non-done, within timeout window

bot/formatting.py              — Markdown -> Telegram HTML converter
  :md_to_telegram_html()       — Extracts code blocks first, escapes HTML, converts bold/italic/links
  :split_message()             — Split >4000 char messages at newlines
  NOTE: Falls back to plain text on TelegramBadRequest

bot/voice.py                   — Groq Whisper API transcription
  :transcribe_voice()          — Download .ogg from TG, POST to Groq, return text
  NOTE: Language hardcoded "ru"

bot/scheduler.py               — Cron-like scheduler reading workspace/schedules.json
  :run_scheduler()             — asyncio loop, checks every 30s
  :_cron_matches()             — 5-field cron parser (min hour day month weekday)
  :get_due_tasks()             — Find tasks matching current time
  NOTE: Qwen writes schedules.json via QWEN.md instructions

## Workspace
workspace/QWEN.md              — Identity + instructions for Qwen Code (read on every launch)
workspace/.qwen/skills/schedule/SKILL.md — Schedule skill for natural language cron

## Deploy
install.sh                     — One-command installer for Ubuntu/Debian VPS
  NOTE: Detects pipe (curl|bash) and tells user to download first
  NOTE: Uses `qwen auth qwen-oauth` (not `auth login --auth-type`)
  NOTE: .gitattributes forces LF for .sh files (Windows CRLF breaks bash)
qwenbot.service                — systemd unit with sandbox (ProtectSystem, ProtectHome)
  NOTE: HOME=/opt/qwenbot set explicitly for Qwen credential access
.env.example                   — Template

## Key Decisions
- Qwen Code CLI as backend (free 1000 req/day, headless via --auth-type qwen-oauth)
- Groq Whisper API for voice (not local faster-whisper — avoids 3GB model download)
- In-memory message queue (not SQLite — single-user bot, 5 msg max)
- HTML parse_mode (not Markdown — fewer escaping issues in Telegram)
- Scheduler reads schedules.json that Qwen itself writes (natural language cron)
- Dedicated qwenbot system user (not root) with systemd sandbox
