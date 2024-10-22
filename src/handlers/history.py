from telethon import events, TelegramClient
from telethon.events import NewMessage
from telethon.types import Message, Channel
from tempfile import NamedTemporaryFile
import jsonlines
from typing import Any

from src.utils import deep_datetime_to_str, extract_channel_name_or_url


@events.register(events.NewMessage(pattern="/history"))
async def history_handler(event: NewMessage.Event) -> None:
    channel_name = extract_channel_name_or_url(event.message.message)
    await event.reply(f"Получаю историю канала - {channel_name}")

    client: TelegramClient = event.client
    channel = await get_channel_if_exists(client, channel_name)

    messages_data = await fetch_channel_history(client, channel.id)
    file_path = await write_history_to_file(messages_data)

    await client.send_file(entity=event.chat_id, file=file_path)


async def get_channel_if_exists(client: TelegramClient, channel_name) -> Channel | None:
    channel = await client.get_entity(channel_name)
    if isinstance(channel, Channel):
        return channel


async def fetch_channel_history(
    client: TelegramClient, channel_id: int
) -> list[dict[str, Any]]:
    """Получает историю сообщений канала и преобразует их в список словарей."""
    messages = []
    async for message in client.iter_messages(channel_id):
        message_data = format_message_data(message)
        messages.append(message_data)
    return messages


def format_message_data(message: Message) -> dict[str, Any]:
    """Форматирует данные сообщения в словарь."""
    data = {
        "id": message.id,
        "date": message.date.strftime("%d.%m.%Y %H:%M:%S"),
        "message": message.message
        or "Здесь нет сообщения, а есть только медиагруппа (фото/видео/голосовое/и тд)",
        "views": message.views,
    }

    if message.reactions:
        data["reactions"] = format_reactions_data(message.reactions)

    if message.media:
        data["media"] = deep_datetime_to_str(message.media.to_dict())

    return data


def format_reactions_data(reactions) -> dict[str, int]:
    """Форматирует данные о реакциях в удобный для чтения словарь."""
    formatted_reactions = {}
    for reaction in reactions.results:
        formatted_reactions[reaction.reaction.emoticon] = reaction.count
    return formatted_reactions


async def write_history_to_file(messages: list[dict[str, Any]]) -> str:
    """Записывает историю сообщений в JSONL файл и возвращает путь к файлу."""
    with NamedTemporaryFile(suffix=".jsonl", delete=False) as temp_file:
        with jsonlines.open(temp_file.name, mode="w") as writer:
            writer.write_all(messages)
        return temp_file.name
