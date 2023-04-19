from asgiref.sync import sync_to_async

from helpers.tokenHelpers import get_mongo_db_conn
from tg_bot.models import Chat
from pymongo import MongoClient


def get_db_handle(db_name='user_data'):
    DB_DATA = get_mongo_db_conn()
    mongodb_uri = f"mongodb+srv://{DB_DATA['USER']}:{DB_DATA['PASSWORD']}@{DB_DATA['HOST']}/?retryWrites=true&w=majority"

    client = MongoClient(mongodb_uri)
    db_handle = client[db_name]
    return db_handle, client


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]


def get_chat(chat_id):
    chat = Chat.objects.filter(chat_id=chat_id)
    print('chat')
    print(chat)
    if not chat or len(chat) < 1:
        print('no chat')
        chat = {
            "chat_id": chat_id,
            "counter": 0
        }
        response = Chat.objects.create(
            chat_id=chat['chat_id'],
            counter=chat['counter'],
            is_approved=False,
        )
        print(response)
        chat = response
    else:
        chat = chat.first()
    return chat


def get_creator():
    return Chat.objects.get(pk=1)


def set_language(chat_id, language):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.language = language
    chat.save()


def set_approved(chat_id, option: bool):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.is_approved = option
    chat.save()


def tick_counter(chat_id):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.counter += 1
    chat.save()


def tick_tokens(chat_id, tokens: int):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.tokens_used += tokens
    chat.save()


def assign_last_conversation(chat_id, conversation):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.last_conversation = conversation
    chat.save()


def return_records_list(search_result):
    print("return_records_list")
    print(search_result)
    records_list = []
    for record in search_result:
        records_list.append(record)
    return records_list


def return_single_record(search_result):
    if search_result:
        return search_result.copy()
    else:
        return None


async_get_chat = sync_to_async(get_chat)
async_get_creator = sync_to_async(get_creator)
async_set_language = sync_to_async(set_language)
async_set_approved = sync_to_async(set_approved)
async_tick_counter = sync_to_async(tick_counter)
async_tick_tokens = sync_to_async(tick_tokens)
async_assign_last_conversation = sync_to_async(assign_last_conversation)
