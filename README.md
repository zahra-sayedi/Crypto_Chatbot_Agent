# 🪙 Crypto Chatbot Agent

This is an intelligent, bilingual (English & Farsi) Telegram bot designed to provide real-time cryptocurrency information. It can fetch current coin prices from Wallex.ir and answer complex research questions by searching the web and synthesizing information using a local LLM.

The bot uses an initial LLM call to classify the user's intent (price vs. research) and language, then routes the query to the appropriate service.

## Features

* **Smart Intent Classification**: Uses `gemma2:2b` to determine if a user wants a price or research.
* **Bilingual Support**: Automatically detects and responds in either English or Farsi.
* **Real-Time Price Data**: Connects directly to the Wallex.ir API for up-to-the-minute market prices.
* **Web Research Capability**: Uses SerpApi to perform Google searches for complex, non-price-related questions.
* **LLM-Powered Answers**: Scrapes the top search results and uses `gemma2:9b` to synthesize a natural, helpful answer based *only* on the provided context.
* **Robust & Modular Design**: Code is professionally structured into services, handlers, and core config for easy maintenance and extension.

## How It Works: Request Lifecycle

1. A user sends a message (e.g., "how much is btc?" or "what is solana?").
2. **Classify**: The query is sent to `llm_service` (Ollama `gemma2:2b`) to determine `intent` ("price" or "research") and `language` ("en" or "fa").
3. **Route**:
    * **If "price"**: The `helpers.extract_symbol` function matches the query against a pre-compiled `COIN_MAP`. If a symbol is found (e.g., "BTC"), the `pricing_service` is called to fetch data from the Wallex API.
    * **If "research"**: The query is sent to the `search_service`. It uses SerpApi to get Google results, then scrapes the top 3 links for context.
4. **Synthesize**:
    * For research queries, the scraped context and original query are sent to `llm_service` (Ollama `gemma2:9b`) to generate a comprehensive answer, complete with sources.
5. **Reply**: The final formatted message is sent back to the user via Telegram.

## Project Structure

The project follows a modular, service-oriented architecture to separate concerns.
``` /
├── .env                  # Stores all secret keys
├── .gitignore            # Ignores logs, .env, and venv
├── main.py               # Main entry point to start the bot
├── requirements.txt      # Project dependencies
├── bot.log               # Log file
├── examples.json         # Example queries and responses
|
└── src/
    ├── core/
    │   ├── config.py       # Loads .env and holds all constants
    │   └── logging_config.py # Configures the global logger
    │
    ├── services/
    │   ├── llm_service.py    # All logic for Ollama (classify, synthesize)
    │   ├── pricing_service.py# All logic for Wallex API (get prices, build map)
    │   └── search_service.py # All logic for SerpApi & web scraping
    │
    ├── bot/
    │   ├── handlers.py     # Telegram command/message handlers
    │   └── logic.py        # Core `generate_reply` orchestrator
    │
    └── utils/
        ├── helpers.py      # Utility functions (extract_symbol, log_example)
        └── templates.py    # String templates for all bot replies (en/fa)
```
## Setup and Installation

Follow these steps to get the bot running locally.

### 1. Prerequisites

* Python 3.10+
* An active [Ollama](https://ollama.com/) service running and accessible.
* The required Ollama models pulled:

  ```bash
  ollama pull gemma2:2b
  ollama pull gemma2:9b
  ```

### 2. Clone Repository

  ```bash
  git clone https://github.com/zahra-sayedi/Crypto_Chatbot_Agent.git
  cd your-repo-name
  ```

### 3. Set Up Virtual Environment

  ```bash
    # Create a virtual environment
    python3 -m venv venv
    
    # Activate it
    source venv/bin/activate
    # On Windows: .\venv\Scripts\activate
  ```

### 4. Install Dependencies

  ```bash
  pip install -r requirements.txt
  ```

### 5. Configure Environment
Create a file named .env in the root of the project and add your API keys:

```ini
# Get this from @BotFather on Telegram
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"

# Get this from (https://serpapi.com/)
SERPAPI_KEY="YOUR_SERPAPI_API_KEY_HERE"
  ```

Note: The Ollama host (OLLAMA_HOST) is configured in src/core/config.py. Change this value if you are running Ollama on localhost or another server.

Running the Bot
Once your .env file is set up and your virtual environment is active, simply run:

```bash
python main.py
```

The bot will start, initialize the coin map, and begin polling for messages.
