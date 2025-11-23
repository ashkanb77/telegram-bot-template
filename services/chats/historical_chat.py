from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from services.chats.base_chat import BaseChat
from services.prompts import simple_prompt


class HistoricalChat(BaseChat):
    history = {}

    def __init__(self, system_prompt=None):
        super().__init__()
        if system_prompt:
            self.system_prompt = system_prompt
        else:
            self.system_prompt = simple_prompt

    def get_prompt_template(self):
        prompt_template = ChatPromptTemplate([
            ("system", self.system_prompt),
            MessagesPlaceholder('chat_history'),
            ("user", "{input}")
        ])
        return prompt_template

    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        if not self.history.get(session_id):
            self.history[session_id] = ChatMessageHistory()
        return self.history[session_id]

    def get_chain(self):
        chain = self.get_prompt_template() | self.llm | self.get_output_parser()
        chat = RunnableWithMessageHistory(
            chain,
            get_session_history=self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        return chat
