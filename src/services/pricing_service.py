import logging
import requests
from datetime import datetime
from src.core.config import WALLEX_API_URL
from src.utils.templates import get_template

logger = logging.getLogger(__name__)

# This map is populated by initialize_coin_map()
COIN_MAP: dict[str, str] = {}


def _normalize_key(key: str) -> str:
    """Helper to consistently normalize keys."""
    if not key:
        return ""
    return key.lower().replace(' ', '').replace('‌', '')  # '‌' is the Farsi zero-width non-joiner


def initialize_coin_map() -> bool:
    """
    Fetches market data from Wallex and builds a *normalized* name-to-symbol map.
    This function *modifies* the global COIN_MAP.
    """
    global COIN_MAP

    logger.info("Initializing coin map from Wallex API...")
    try:
        response = requests.get(WALLEX_API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        markets = data.get("result", {}).get("markets", [])

        temp_map = {}
        for market in markets:
            symbol = market.get("symbol", "").strip()
            base_asset = market.get("base_asset", "").strip()
            fa_base_asset = market.get("fa_base_asset", "").strip()
            en_base_asset = market.get("en_base_asset", "").strip()

            if base_asset:
                base_symbol = base_asset.upper()
                if base_asset: temp_map[base_asset.lower()] = base_symbol
                if en_base_asset: temp_map[en_base_asset.lower()] = base_symbol
                if fa_base_asset:
                    temp_map[fa_base_asset.lower()] = base_symbol
                    no_space_farsi = fa_base_asset.replace(' ', '').replace('‌', '')
                    temp_map[no_space_farsi.lower()] = base_symbol
                if symbol: temp_map[symbol.lower()] = base_symbol

        COIN_MAP = temp_map
        logger.info(f"Successfully loaded {len(COIN_MAP)} coin names/symbols into the map.")
        print("Initializing COIN_MAP...")
        print(COIN_MAP)
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to initialize coin map from Wallex API: {e}")
        return False
    except Exception as e:
        logger.error(f"Error processing Wallex response for map initialization: {e}")
        return False


def get_wallex_price(symbol: str, lang: str = 'en') -> str:
    """Fetches all market prices for a given base symbol from Wallex."""
    t = get_template(lang)
    logger.info(f"Attempting to fetch all market prices for base symbol: {symbol}")

    try:
        response = requests.get(WALLEX_API_URL, timeout=10)
        response.raise_for_status()

        data = response.json()
        markets = data.get("result", {}).get("markets", [])
        if not isinstance(markets, list):
            logger.error(f"Wallex API 'markets' is not a list as expected. Type: {type(markets)}")
            markets = []

        symbol_lower = symbol.lower()
        found_prices = []

        for market_data in markets:
            base_asset = market_data.get("base_asset", "").lower()

            if base_asset == symbol_lower:
                last_price = market_data.get("price")
                market_symbol = market_data.get("symbol")
                quote_asset = market_data.get("quote_asset")

                if last_price and market_symbol and quote_asset:
                    found_prices.append({
                        "symbol": market_symbol,
                        "price": last_price,
                        "quote": quote_asset
                    })

        if found_prices:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Sort to show TMN and USDT first
            found_prices.sort(key=lambda x: (x['quote'] != 'TMN', x['quote'] != 'USDT', x['quote']))

            reply_lines = [t['price_header'].format(symbol=symbol, timestamp=timestamp)]
            for p in found_prices:
                reply_lines.append(t['price_line'].format(quote=p['quote'], symbol=p['symbol'], price=p['price']))

            reply = "\n".join(reply_lines)
            logger.info(f"Successfully found and compiled prices for {symbol} across {len(found_prices)} markets.")
            return reply
        else:
            logger.warning(f"Symbol '{symbol}' not found in Wallex.ir markets.")
            return t['price_not_found'].format(symbol=symbol)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Wallex API: {e}")
        return t['price_api_error']
    except Exception as e:
        logger.error(f"Error parsing Wallex response: {e}")
        return t['price_parse_error']