import logging

from telethon import TelegramClient

from src.settings import Settings
from src.handlers import history_handler

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


if __name__ == "__main__":
    settings = Settings.from_env()
    with TelegramClient(
        settings.APP_NAME, api_id=settings.API_ID, api_hash=settings.API_HASH
    ) as client:
        client.add_event_handler(history_handler)
        client.start()
        client.run_until_disconnected()
