import logging
import json
import ollama
from src.core.config import OLLAMA_HOST, LLM_MODEL1, LLM_MODEL2
from src.utils.templates import get_template

logger = logging.getLogger(__name__)

# --- Client Initialization ---

def get_ollama_client():
    """Initializes and returns the Ollama client."""
    try:
        client = ollama.Client(host=OLLAMA_HOST)
        client.list()
        logger.info(f"Successfully connected to Ollama at {OLLAMA_HOST}")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Ollama at {OLLAMA_HOST}. Is it running? Error: {e}")
        return None

ollama_client = get_ollama_client()

# --- Service Functions ---

def decide_query_type(text: str) -> tuple[str, str]:
    """Classifies query intent ('price'/'research') and language ('en'/'fa')."""
    if not ollama_client:
        logger.error("Ollama client not initialized. Falling back to ('research', 'en').")
        return "research", "en"

    logger.info("Using LLM to classify query type and language.")

    prompt = f"""
    Analyze the user query below. Classify its intent ('price' or 'research') AND identify its primary language ('en' for English, 'fa' for Farsi, or 'other').

    'price': Use this if the user is explicitly asking for the current market value, cost, or price of a specific cryptocurrency (e.g., "how much is BTC?", "قیمت اتریوم؟").
    'research': Use this for all other questions, including general crypto questions, news, historical data, or definitions (e.g., "what is Solana?", "NFT چیست؟").

    Your response MUST be a single, valid JSON object in the format:
    {{"intent": "...", "language": "..."}}

    User Query: "{text}"

    Response:
    """

    try:
        response = ollama_client.generate(
            model=LLM_MODEL1,
            prompt=prompt,
            format="json",
            options={"temperature": 0.0}
        )

        raw_response = response.get("response", "{}").strip()
        data = json.loads(raw_response)

        intent = data.get("intent", "research").lower()
        language = data.get("language", "en").lower()

        if intent not in ["price", "research"]:
            logger.warning(f"LLM returned invalid intent: '{intent}'. Defaulting to 'research'.")
            intent = "research"

        if language not in ["en", "fa"]:
            logger.warning(f"LLM returned unsupported language: '{language}'. Defaulting to 'en'.")
            language = "en"

        logger.info(f"LLM classified query as (Intent: '{intent}', Language: '{language}').")
        return intent, language

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON response: {raw_response}. Error: {e}. Defaulting to ('research', 'en').")
        return "research", "en"
    except Exception as e:
        logger.error(f"Error calling Ollama for classification: {e}. DefaultTing to ('research', 'en').")
        return "research", "en"


def synthesize_answer(query: str, context: str, lang: str = 'en') -> str | None:
    """Generates an answer based on search context using an LLM."""
    t = get_template(lang)

    if not ollama_client:
        logger.error("Ollama client not initialized. Cannot synthesize answer.")
        return t['synth_service_unavailable']

    logger.info(f"Synthesizing answer with LLM in language: {lang}")

    prompt = f"""
    {t['synth_prompt']}

    Search Results:
    {context}

    User's Question:
    {query}

    Answer:
    """
    try:
        response = ollama_client.generate(model=LLM_MODEL2, prompt=prompt)
        logger.info("LLM synthesis successful.")
        return response.get("response")
    except Exception as e:
        logger.error(f"Error calling Ollama: {e}")
        return t['synth_api_error']