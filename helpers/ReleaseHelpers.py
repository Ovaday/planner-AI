import asyncio
import datetime
import json

import pymongo
from asgiref.sync import sync_to_async
import telegram
from telegram.constants import ParseMode

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


def get_latest_update():
    db_handle, mongo_client = get_db_handle('service_data')
    coll_handle = get_collection_handle(db_handle, "updates_log")

    return json.loads(dumps(coll_handle.find_one(sort=[('update_time', pymongo.DESCENDING)]), ensure_ascii=False))


def fill_update(last_update, version: str, update_time):
    update = {}
    if last_update:
        update = last_update.copy()
        if "_id" in update:
            del update["_id"]

    update["update_time"] = update_time
    update["app_version"] = version
    return update


def insert_update(update):
    db_handle, mongo_client = get_db_handle('service_data')
    coll_handle = get_collection_handle(db_handle, "updates_log")

    return coll_handle.insert_one(update)


async def async_release_handler(release_version):
    bot = telegram.Bot(get_token("TG_BOT_TOKEN"))
    all_chats = await async_get_all_chats()
    release_message = await async_get_release_message(release_version)
    for chat in all_chats:
        print(chat)
        text = release_message[chat.language]
        await bot.send_message(chat_id=chat.chat_id, text=text, parse_mode=ParseMode.HTML)

    last_update = await async_get_latest_update()
    update = fill_update(last_update, release_version, datetime.datetime.now())
    await async_insert_update(update)


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
async_get_latest_update = sync_to_async(get_latest_update)
async_insert_update = sync_to_async(insert_update)
