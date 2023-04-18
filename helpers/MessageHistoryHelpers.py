import pymongo
from asgiref.sync import sync_to_async
from telegram import Message

from helpers.DatabaseHelpers import get_collection_handle, get_db_handle, return_records_list


def construct_message(chat_id: int, message_time: any, message_id: int, is_response: bool, username: str, message: str,
                      additional_info=None, external_id=None, classification_results=None):
    if additional_info is None:
        additional_info = {}
    if classification_results is not None:
        additional_info = {
            'reminder_probability': classification_results[0],
            'openai_classification': classification_results[1],
            'local_classification': classification_results[2],
        }
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


def insert_input_message(in_msg: Message, classification_results=None):
    message = construct_message(in_msg.chat_id, in_msg.date, in_msg.message_id, False, in_msg.chat.username,
                                in_msg.text, classification_results=classification_results)
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    return coll_handle.insert_one(message)


def insert_response(in_msg: Message, response_text: str, tokens_used: int):
    additional_info = {
        'tokens_used': tokens_used
    }
    message = construct_message(in_msg.chat_id, in_msg.date, in_msg.message_id, True, in_msg.chat.username,
                                response_text, additional_info=additional_info)
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    return coll_handle.insert_one(message)


def get_messages_for_user(user_id: int):
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")

    return return_records_list(coll_handle.find({"chat_id": user_id}))


def get_last_user_messages(user_id: int):
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    return return_records_list(
        coll_handle.find({"chat_id": user_id}).sort('message_time', pymongo.DESCENDING).limit(10))


def get_last_messages_from_user(user_id: int):
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    return return_records_list(
        coll_handle.find({"chat_id": user_id, "is_response": False}).sort('message_time', pymongo.DESCENDING).limit(3))


def get_last_messages_to_user(user_id: int):
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    return return_records_list(
        coll_handle.find({"chat_id": user_id, "is_response": True}).sort('message_time', pymongo.DESCENDING).limit(3))


async_insert_input_message = sync_to_async(insert_input_message)
async_insert_response = sync_to_async(insert_response)
async_get_messages_for_user = sync_to_async(get_messages_for_user)
async_get_last_user_messages = sync_to_async(get_last_user_messages)
async_get_last_messages_from_user = sync_to_async(get_last_messages_from_user)
async_get_last_messages_to_user = sync_to_async(get_last_messages_to_user)