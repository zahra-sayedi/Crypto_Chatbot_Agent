import logging
import requests
import re
import serpapi
from bs4 import BeautifulSoup
from src.core.config import SERPAPI_KEY
from src.utils.templates import get_template

logger = logging.getLogger(__name__)

# --- Client Initialization ---
serpapi_client = serpapi.Client(api_key=SERPAPI_KEY)


# --- Service Functions ---

def search_web(query: str, lang: str = 'en') -> tuple[str, list | None]:
    """
    Performs a web search, scrapes top results, and returns context.
    Returns (context_text, sources_list) or (error_message, None)
    """
    t = get_template(lang)
    logger.info(f"Performing web search for: '{query}' (lang={lang})")

    if not SERPAPI_KEY:
        logger.error("SERPAPI_KEY is not set. Web search is disabled.")
        return t['search_api_error'].format(e="API key not configured"), None

    try:
        search_results = serpapi_client.search(
            q=query,
            engine="google",
            hl=lang,
            gl="us"
        )
        organic_results = search_results.get("organic_results", [])

        if not organic_results:
            logger.warning("Web search returned no organic results.")
            return t['search_no_results'], None

        snippets = []
        sources = []

        scraper_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Scrape top 3 results
        for i, result in enumerate(organic_results[:3]):
            link = result.get("link")
            title = result.get("title", "No title")
            original_snippet = result.get('snippet', 'No snippet available.')

            if not link:
                continue

            sources.append({"title": title, "link": link})

            try:
                logger.info(f"Scraping {link} for context...")
                page_response = requests.get(link, headers=scraper_headers, timeout=5)
                page_response.raise_for_status()

                soup = BeautifulSoup(page_response.text, 'html.parser')

                # Get text from all <p> tags
                paragraphs = soup.find_all('p')
                page_text = "\n".join([p.get_text() for p in paragraphs])

                # Clean up whitespace
                page_text = re.sub(r'\s+', ' ', page_text).strip()

                if len(page_text) > 2000:
                    page_text = page_text[:2000] + "..."

                if page_text and len(page_text) > len(original_snippet):
                    snippets.append(f"Source {i + 1} ({title}): {page_text}")
                else:
                    logger.warning(f"Scraping {link} yielded little text. Falling back to snippet.")
                    snippets.append(f"Source {i + 1} ({title}): {original_snippet}")

            except Exception as e:
                logger.warning(f"Failed to scrape {link}: {e}. Falling back to snippet.")
                snippets.append(f"Source {i + 1} ({title}): {original_snippet}")

        if not snippets:
            return t['search_no_results'], None

        context_text = "\n\n".join(snippets)
        logger.info(f"Gathered {len(sources)} scraped snippets for synthesis.")
        return context_text, sources

    except Exception as e:
        logger.error(f"Error during SerpAPI call: {e}")
        return t['search_api_error'].format(e=e), None