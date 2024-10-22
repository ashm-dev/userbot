import logging
from tempfile import NamedTemporaryFile

import jsonlines
from telethon import TelegramClient, events
from telethon.events import NewMessage

from settings import Settings


logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

settings = Settings.from_env()
client = TelegramClient(settings.APP_NAME, api_id=settings.API_ID, api_hash=settings.API_HASH)


@client.on(events.NewMessage(pattern='/history'))
async def history(event: NewMessage.Event) -> None:
    logging.info('new event')
    logging.info(event)   
     
    await event.reply('Получаю историю твоего канала')
    
    res = []
    channel = await client.get_entity('mlecchnii')
    
    async for message in client.iter_messages(channel.id):
        res.append(message.to_dict())
        # data = {
        #     'id': message.id,
        #     'date': message.date.strftime('%d.%m.%Y %H:%M:%S'),
        #     'message': message.message if message.message else 'Здесь нет сообщения, а есть только медиагруппа (фото/видео/голосовое/и тд)',
        #     'views': message.views,
        # }
        # if message.reactions:
        #     reactions = {}
        #     for i in message.reactions.results:
        #         reactions[i.reaction.emoticon] =  i.count
        #     data['reactions'] = reactions
        
        # res.append(data)
    
    with NamedTemporaryFile(suffix='.jsonl') as f:
        with jsonlines.open(f.name, mode='w') as writer:
            writer.write_all(res)
        
        await client.send_file(entity=event.chat_id, file=f.name)


if __name__ == '__main__':
    logging.info('Бот запущен')
    client.start()
    client.run_until_disconnected()
