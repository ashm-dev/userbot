import base64
from datetime import datetime


def deep_datetime_to_str(obj):
    """Преобразует дату и время и байты в строку."""
    if isinstance(obj, dict):
        return {k: deep_datetime_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_datetime_to_str(elem) for elem in obj]
    elif isinstance(obj, tuple):
        return tuple(deep_datetime_to_str(elem) for elem in obj)
    elif isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode("utf-8")
    else:
        return obj


def extract_channel_name_or_url(message: str) -> str | None:
    """Извлекает имя канала из сообщения или URL канала."""
    return message.replace("/history ", "")
