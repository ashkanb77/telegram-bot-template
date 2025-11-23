import asyncio

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from handlers.conversations.base_conversation import BaseConversation
from keyboards.reply import main_menu
from models import Message
from services.chats.simple_chat import SimpleChat
from services.prompts import translator_prompt


class TranslateConversation(BaseConversation):
    def __init__(self, trigger_title, **kwargs):
        super().__init__(trigger_title=trigger_title, **kwargs)
        self.translator_chat = SimpleChat(translator_prompt)
        self.llm_chain = self.translator_chat.get_chain()

    async def response(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        user_text = update.message.text
        user = update.effective_user

        # fire-and-forget background task (keeps bot responsive)
        asyncio.create_task(self._handle_llm_and_reply(chat_id, user_text, context.bot, user, context))

        # immediately return so the ConversationHandler (or other handlers) can continue
        return ConversationHandler.END

    # the background worker
    async def _handle_llm_and_reply(self, chat_id, user_text, bot, user, context):
        try:
            result = await self.llm_chain.ainvoke({'input': user_text})

            # get sessionmaker from application (set at startup)
            session = context.application.bot_data.get("db_session")

            msg = Message(user_id=user.id, content=user_text, answer=result)
            session.add(msg)
            await session.commit()

            await bot.send_message(chat_id=chat_id,
                                   text=f"✅ {result}\n\nBack to main menu:",
                                   reply_markup=main_menu())
        except Exception as e:
            # handle errors & notify user
            await bot.send_message(chat_id=chat_id,
                                   text=f"❌ Error while processing your request: {e}")

