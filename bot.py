import os

import dotenv
import pytz
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import *
from handlers.commands import start
from handlers.conversations.translate_conversation import TranslateConversation
from handlers.messages import handle_message
from database import engine, get_session

dotenv.load_dotenv()

time_zone = pytz.timezone("Asia/Tehran")

CHAT_API_KEY = os.getenv("CHAT_API_KEY")
BOT_TOKEN = os.getenv('BOT_TOKEN')


async def on_startup(app: Application):
    # make sure tables exist (optional: use Alembic in production)
    session = await get_session()

    # store session factory on application for handlers to reuse
    app.bot_data["db_session"] = session

async def on_shutdown(app: Application):
    # close engine (drain pool)
    await engine.dispose()


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    translate_conversation = TranslateConversation(menu_messages['translate'])

    app.add_handler(translate_conversation.get_conversation())

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.post_init = on_startup
    app.post_shutdown = on_shutdown

    app.run_polling()


if __name__ == "__main__":
    main()
