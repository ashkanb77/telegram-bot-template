from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler, MessageHandler, ConversationHandler, filters
)

from keyboards.reply import main_menu

CHOOSING_INLINE_KEYBOARD = 3
CALL_FUNCTION = 4


class InlineKeyboardConversation:

    def __init__(self, trigger_title, inline_keyboard, callback_message, prefix=None, starting_message=None,
                 cancel_title="❌Cancel", cancel_message=None):
        """

        :param trigger_title: str
        :param inline_keyboard: [[('keyboard', function), ...]]
        :param callback_message: str
        :param starting_message: Optional[str]
        :param cancel_title: Optional[str]
        :param cancel_message: Optional[str]
        """
        self.trigger_title = trigger_title
        if not prefix:
            self.prefix = trigger_title + '_'
        self.inline_keyboard = inline_keyboard
        self.callbacks = {}
        for row in inline_keyboard:
            for keyboard, function in row:
                self.callbacks[keyboard] = function
        self.cancel_title = cancel_title
        self.CANCEL_MENU = [[cancel_title]]
        self.WAITING_FOR_TEXT = 1
        self.callback_message = callback_message
        if not starting_message:
            self.starting_message = "chose from keyboards (or tap Cancel):"
        else:
            self.starting_message = starting_message

        if not cancel_message:
            self.cancel_message = "❌ Cancelled.\nBack to main menu:"
        else:
            self.cancel_message = cancel_message

    def cancel_menu_markup(self):
        return ReplyKeyboardMarkup(self.CANCEL_MENU, resize_keyboard=True)

    async def show_inline_keyboards(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []
        for row in self.inline_keyboard:
            keyboard.append([InlineKeyboardButton(title, callback_data=self.prefix + title) for title, _ in row])
        keyboard.append([InlineKeyboardButton(self.cancel_title, callback_data=f"{self.prefix}cancel")])
        await update.message.reply_text("❌ you can cancel your request from menu.",
                                        reply_markup=self.cancel_menu_markup())
        await update.message.reply_text(self.starting_message, reply_markup=InlineKeyboardMarkup(keyboard))
        return CHOOSING_INLINE_KEYBOARD

    async def choose_inline_keyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == f"{self.prefix}cancel":
            await self.cancel(update, context)
            return ConversationHandler.END
        context.user_data['keyboard'] = query.data.replace(self.prefix, "")
        await query.message.reply_text(self.callback_message, reply_markup=self.cancel_menu_markup())
        return CALL_FUNCTION

    async def call_function(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text.strip()
        if user_message == self.cancel_title:
            await self.cancel(update, context)
            return ConversationHandler.END

        keyboard = context.user_data.get('keyboard')

        function = self.callbacks.get(keyboard)
        if function:
            user_data = {'keyboard': keyboard, 'message': user_message}
            await function(user_data, update=update, context=context)
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.callback_query:
            await update.callback_query.message.reply_text(self.cancel_message, reply_markup=main_menu())
        elif update.message:
            await update.message.reply_text(self.cancel_message, reply_markup=main_menu()
                                            )
        return ConversationHandler.END

    def get_conversation(self):
        conversation = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex(rf"^{self.trigger_title}$"), self.show_inline_keyboards)],
            states={
                CHOOSING_INLINE_KEYBOARD: [
                    CallbackQueryHandler(self.choose_inline_keyboard, pattern=rf'^{self.prefix}')],
                CALL_FUNCTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.call_function)],

            },
            fallbacks=[MessageHandler(filters.Regex(rf"^{self.cancel_title}$"), self.cancel)],
            per_message=False
        )

        return conversation
