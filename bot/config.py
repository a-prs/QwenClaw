"""QwenBot configuration — loaded from .env."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (/opt/qwenbot/.env)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)

# Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

# Qwen CLI
QWEN_BIN = os.getenv("QWEN_BIN", "qwen")
QWEN_MAX_TURNS = int(os.getenv("QWEN_MAX_TURNS", "15"))
QWEN_TIMEOUT = int(os.getenv("QWEN_TIMEOUT", "600"))

# Working directory for Qwen Code
WORK_DIR = Path(os.getenv("QWEN_WORK_DIR", str(PROJECT_ROOT / "workspace")))

# Groq Whisper API (optional, for voice messages)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Database
DB_PATH = PROJECT_ROOT / "data" / "bot.db"

# Limits
MESSAGE_QUEUE_MAX = 5
SESSION_IDLE_TIMEOUT_HOURS = 48


def set_env_var(key: str, value: str):
    """Write or update a variable in .env file and apply to current process."""
    lines = []
    found = False

    if ENV_PATH.exists():
        lines = ENV_PATH.read_text().splitlines()
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}"
                found = True
                break

    if not found:
        lines.append(f"{key}={value}")

    ENV_PATH.write_text("\n".join(lines) + "\n")
    os.environ[key] = value


def reload_groq_key():
    """Reload GROQ_API_KEY from .env into module-level variable."""
    global GROQ_API_KEY
    load_dotenv(ENV_PATH, override=True)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
