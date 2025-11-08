import logging
from src.utils.templates import get_template
from src.utils.helpers import extract_symbol, log_example_run
from src.services import llm_service, pricing_service, search_service

logger = logging.getLogger(__name__)


def generate_reply(user_query: str, request_id: str = "Standalone") -> str:
    """
    Orchestrates the full reply generation process.
    1. Classifies query
    2. Routes to pricing or research
    3. Returns final reply string
    """

    # 1. Classify query
    query_type, lang = llm_service.decide_query_type(user_query)

    log_prefix = f"[{request_id}] (lang={lang})"
    logger.info(f"{log_prefix} - Decision: {query_type}")

    t = get_template(lang)
    reply_text = ""

    # 2. Route to "price" logic
    if query_type == "price":
        symbol = extract_symbol(user_query)
        if symbol:
            logger.info(f"{log_prefix} - Extracted symbol: {symbol}. Fetching price.")
            reply_text = pricing_service.get_wallex_price(symbol, lang)
        else:
            logger.info(f"{log_prefix} - Price query, but no symbol found. Switching to research.")
            query_type = "research"  # Fallback to research

    # 3. Route to "research" logic (or fallback)
    if query_type == "research":
        logger.info(f"{log_prefix} - Performing web search.")
        context_text, sources = search_service.search_web(user_query, lang)

        if sources:
            logger.info(f"{log_prefix} - Synthesizing answer from {len(sources)} sources.")
            answer = llm_service.synthesize_answer(user_query, context_text, lang)

            if answer:
                source_links = [f"• {s['title']} ({s['link']})" for s in sources]
                reply_text = f"{answer}{t['synth_sources_header']}" + "\n".join(source_links)
            else:
                reply_text = t['synth_api_error']  # Synthesis failed
        else:
            reply_text = context_text  # This will be the error message from search_web

    logger.info(f"{log_prefix} - Generation complete. Reply snippet: {reply_text[:150]}...")

    # 4. Log and return
    log_example_run(user_query, f"{query_type} ({lang})", reply_text)
    return reply_text