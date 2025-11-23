from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from services.chats.base_chat import BaseChat

class SimpleChat(BaseChat):

    def __init__(self, system_prompt):
        super().__init__()
        self.system_prompt = system_prompt
    def get_prompt_template(self, ):
        prompt_template = ChatPromptTemplate([
            ("system", self.system_prompt),
            ("user", "{input}")
        ])
        return prompt_template

    def get_chain(self):
        return self.get_prompt_template() | self.llm | self.get_output_parser()