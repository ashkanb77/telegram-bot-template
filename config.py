from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    sync_database_url: str
    chat_api_key: str
    chat_api_url: str
    bot_token: str
    model: str
    welcome_message: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

menu_messages = {
    "options": "Show Options",
    "translate": "💡Translate",
    "help": "Help",
}

menu_order = [
    [menu_messages["options"], menu_messages['translate']],
    [menu_messages["help"]]
]
