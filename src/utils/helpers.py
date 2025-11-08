import os
import json
import logging
from datetime import datetime
from src.core.config import EXAMPLE_LOG_FILE
from src.services import pricing_service

logger = logging.getLogger(__name__)

def extract_symbol(text: str) -> str | None:
    """
    Extracts a coin symbol from text by matching against the COIN_MAP.
    This version normalizes both the input text AND the map keys for matching.
    """
    current_coin_map = pricing_service.COIN_MAP
    print(current_coin_map)
    text_lower = text.lower()
    text_lower = text_lower.replace(' ', '').replace('‌', '')

    sorted_coin_keys = sorted(current_coin_map.keys(), key=len, reverse=True)

    for coin_name in sorted_coin_keys:
        if coin_name in current_coin_map and coin_name in text_lower:
            found_symbol = current_coin_map[coin_name]
            logger.info(f"Map-based extraction found symbol: {found_symbol} via match: '{coin_name}'")
            return found_symbol

    logger.warning(f"Failed to extract a clear coin symbol from query: '{text}' using COIN_MAP.")
    return None

def log_example_run(query: str, decision: str, response: str):
    """Logs an example query and response to a JSON file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query_text": query,
        "decision": decision,
        "response_text_snippet": response
    }
    try:
        logs = []
        if os.path.exists(EXAMPLE_LOG_FILE):
            with open(EXAMPLE_LOG_FILE, "r", encoding='utf-8') as f:
                logs = json.load(f)

        logs.append(log_entry)

        with open(EXAMPLE_LOG_FILE, "w", encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Failed to write to {EXAMPLE_LOG_FILE}: {e}")