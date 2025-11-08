import logging
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction

from src.core.config import TELEGRAM_BOT_TOKEN
from src.bot.logic import generate_reply

logger = logging.getLogger(__name__)


# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.first_name}! I'm your Crypto Chatbot.\n\n"
        f"Ask me for a coin price (e.g., 'price of BTC') or a research question (e.g., 'what is solana?').\n\n"
        f"می‌توانید فارسی هم بپرسید (مثلا: «قیمت بیت کوین» یا «سولانا چیست؟»)",
    )


# --- Message Handlers ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all non-command text messages."""
    if not update.message or not update.message.text:
        return

    user_query = update.message.text
    user_id = update.effective_user.id
    request_id = f"User:{user_id}_{datetime.now().strftime('%H%M%S')}"

    logger.info(f"[{request_id}] Processing new query. Content: '{user_query}'")

    # Show "Typing..." action to the user
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    # Run the blocking function in a separate thread
    loop = asyncio.get_running_loop()
    try:
        reply_text = await loop.run_in_executor(None, generate_reply, user_query, request_id)
    except Exception as e:
        logger.error(f"[{request_id}] Unhandled exception in generate_reply: {e}", exc_info=True)
        reply_text = "Sorry, an unexpected error occurred. I've notified the developers."

    await update.message.reply_text(reply_text)


# --- Bot Setup ---

def run_bot() -> None:
    """Initializes and runs the Telegram bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.critical("TELEGRAM_BOT_TOKEN not found. Bot cannot start.")
        return

    logger.info("Building Telegram application...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    logger.info("Starting Telegram bot polling...")
    application.run_polling()