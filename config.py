from loguru import logger
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()

logger.add("config.log", rotation="10 MB", level="INFO")
