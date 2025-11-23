from telegram import Update
from telegram.ext import ContextTypes

from keyboards.reply import main_menu


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Help":
        await update.message.reply_text("This is a demo bot. Use 'Show Options' to see inline buttons.",
                                        reply_markup=main_menu())



async def send_daily_message(context):
    """Callback function for the daily message."""
    chat_id = context.job.data['chat_id']
    await context.bot.send_message(chat_id=chat_id, text="This is your daily reminder!")
