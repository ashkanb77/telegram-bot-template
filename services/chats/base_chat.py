from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from config import settings


class BaseChat:
    def __init__(self):
        self.llm = ChatOpenAI(model=settings.model, api_key=settings.chat_api_key, base_url=settings.chat_api_url,
                              temperature=0.1)

    def get_output_parser(self):
        return StrOutputParser()

    def get_prompt_template(self):
        raise NotImplementedError("get prompt function not implemented")

    def get_chain(self):
        raise NotImplementedError("get chain function not implemented")

