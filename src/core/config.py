import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Telegram Bot ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.", file=sys.stderr)
    sys.exit(1)

# --- APIs ---
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
if not SERPAPI_KEY:
    print("Warning: SERPAPI_KEY not found. Web search will fail.", file=sys.stderr)

WALLEX_API_URL = "https://api.wallex.ir/hector/web/v1/markets"
OLLAMA_HOST = "http://127.0.0.1:11434"

# --- LLM Models ---
LLM_MODEL1 = "gemma2:2b"  # For classification
LLM_MODEL2 = "gemma2:9b"  # For synthesis

# --- Other ---
LOG_FILE = "bot.log"
EXAMPLE_LOG_FILE = "examples.json"