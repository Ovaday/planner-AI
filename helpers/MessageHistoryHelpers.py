from asgiref.sync import sync_to_async
from telegram import Message
from helpers.DatabaseHelpers import get_collection_handle, get_db_handle


def construct_message(chat_id: int, message_time: any, message_id: int, is_response: bool, username: str, message: str,
                      additional_info=None, external_id=None):
    if additional_info is None:
        additional_info = {}
    return {
        "chat_id": chat_id,
        "message_time": message_time,
        "message_id": message_id,
        "is_response": is_response,
        "username": username,
        "external_id": external_id,
        "additional_info": additional_info,
        "message_raw": message,
        "message_encrypted": None
    }


def insert_input_message(in_msg: Message):
    message = construct_message(in_msg.chat_id, in_msg.date, in_msg.message_id, False, in_msg.chat.username,
                                in_msg.text)
    db_handle, mongo_client = get_db_handle()
    collection_handle = get_collection_handle(db_handle, "messages_history")
    return collection_handle.insert_one(message)


def get_messages_for_user(user_id: int):
    db_handle, mongo_client = get_db_handle()
    collection_handle = get_collection_handle(db_handle, "messages_history")
    return collection_handle.find({}, {"ChatId": user_id})


async_insert_input_message = sync_to_async(insert_input_message)
async_get_messages_for_user = sync_to_async(get_messages_for_user)