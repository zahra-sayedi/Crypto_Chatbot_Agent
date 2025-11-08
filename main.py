import logging
from src.core.logging_config import setup_logging
from src.bot.handlers import run_bot
from src.services.pricing_service import initialize_coin_map

# Set up logging as the first thing
setup_logging()
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application."""
    logger.info("Application starting...")

    # Initialize the coin map on startup
    if not initialize_coin_map():
        logger.warning("Could not initialize coin price list. Price queries may fail.")
    else:
        # Accessing the map from its module to log length
        from src.services.pricing_service import COIN_MAP
        logger.info(f"Initialized {len(COIN_MAP)} coin lookup keys.")

    # Run the bot
    run_bot()


if __name__ == "__main__":
    main()