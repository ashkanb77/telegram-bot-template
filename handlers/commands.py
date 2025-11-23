from telegram import Update
from telegram.ext import ContextTypes
from config import settings
from keyboards.reply import main_menu
from models import User


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await User.save_user(user, context.bot_data.get('db_session'))
    await update.message.reply_text(settings.welcome_message, reply_markup=main_menu())
