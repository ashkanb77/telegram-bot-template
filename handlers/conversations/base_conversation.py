from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    MessageHandler,
    ConversationHandler, ContextTypes, filters
)

from keyboards.reply import main_menu


class BaseConversation:
    def __init__(self, trigger_title, cancel_title="❌Cancel", starting_message=None, cancel_message=None):
        self.trigger_title = trigger_title
        self.cancel_title = cancel_title
        self.CANCEL_MENU = [[cancel_title]]
        self.WAITING_FOR_TEXT = 1
        if not starting_message:
            self.starting_message = "Please type your message (or tap Cancel):"
        else:
            self.starting_message = starting_message

        if not cancel_message:
            self.cancel_message = "❌ Cancelled.\nBack to main menu:"
        else:
            self.cancel_message = cancel_message

    def cancel_menu_markup(self):
        return ReplyKeyboardMarkup(self.CANCEL_MENU, resize_keyboard=True)

    async def entry(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(self.starting_message,reply_markup=self.cancel_menu_markup())
        return self.WAITING_FOR_TEXT

    async def response(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplemented("this function is not implemented yet")

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(self.cancel_message, reply_markup=main_menu())
        return ConversationHandler.END

    def get_conversation(self):
        conversation = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex(rf"^{self.trigger_title}$"), self.entry)],
            states={
                self.WAITING_FOR_TEXT: [
                    MessageHandler(filters.Regex(rf"^{self.cancel_title}$"), self.cancel),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.response),
                ],
            },

            fallbacks=[],
            per_message=False,
        )

        return conversation
