import asyncio
import json
from asgiref.sync import sync_to_async
import telegram

from helpers.DatabaseHelpers import get_collection_handle, get_db_handle
from bson.json_util import dumps

from helpers.tokenHelpers import get_token
from tg_bot.models import Chat


def get_release_message(version: str):
    db_handle, mongo_client = get_db_handle('service_data')
    coll_handle = get_collection_handle(db_handle, "releases")

    return json.loads(dumps(coll_handle.find_one({"version": version})['translations'], ensure_ascii=False))


def get_all_chats():
    query = Chat.objects.all()
    all_chats = []
    for obj in query.iterator():
        all_chats.append(obj)
    return all_chats


async def async_release_handler(release_version):
    bot = telegram.Bot(get_token("TG_BOT_TOKEN"))
    all_chats = await async_get_all_chats()
    release_message = await async_get_release_message(release_version)
    for chat in all_chats:
        print(chat)
        text = release_message[chat.language]
        await bot.send_message(chat_id=chat.chat_id, text=text)


def release_handler(event):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return asyncio.get_event_loop().run_until_complete(async_release_handler(event))
    except Exception as e:
        print(e)
        return asyncio.get_event_loop().run_until_complete(async_release_handler(event))


async_get_release_message = sync_to_async(get_release_message)
async_get_all_chats = sync_to_async(get_all_chats)
