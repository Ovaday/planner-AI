import pymongo
from asgiref.sync import sync_to_async
from telegram import Message

from helpers.DatabaseHelpers import get_collection_handle, get_db_handle, return_records_list, return_single_record


def construct_message(chat_id: int, message_time: any, message_id: int, username: str, message: str,
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
        "username": username,
        "external_id": external_id,
        "additional_info": additional_info,
        "message_raw": message,
        "message_encrypted": None,
        "response_raw": None,
        "response_encrypted": None,
    }


def insert_input_message(in_msg: Message, classification_results=None):
    message = construct_message(in_msg.chat_id, in_msg.date, in_msg.message_id, in_msg.chat.username,
                                in_msg.text, classification_results=classification_results)
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    return coll_handle.insert_one(message)


def insert_response(in_msg: Message, response_text: str, tokens_used=None):
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    additional_info = {}
    if tokens_used:
        additional_info = {
            'tokens_used': tokens_used
        }
    update_query = {"chat_id": in_msg.chat_id, "message_id": in_msg.message_id}
    new_values = {"$set": {"response_raw": response_text, "additional_info": additional_info}}

    return coll_handle.update_one(update_query, new_values)


def insert_web_message(message):
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    return coll_handle.insert_one(message)


def get_message_for_user_by_id(user_id: int, message_id: int):
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")

    return return_single_record(coll_handle.find_one({"chat_id": user_id, "message_id": message_id}))


def get_messages_for_user(user_id: int):
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")

    return return_records_list(coll_handle.find({"chat_id": user_id}))


def get_last_user_messages(user_id: int):
    print(user_id)
    db_handle, mongo_client = get_db_handle()
    coll_handle = get_collection_handle(db_handle, "messages_history")
    return return_records_list(
        coll_handle.find({"chat_id": user_id}).sort('message_time', pymongo.DESCENDING).limit(10))


async_insert_input_message = sync_to_async(insert_input_message)
async_insert_response = sync_to_async(insert_response)
async_get_messages_for_user = sync_to_async(get_messages_for_user)
async_get_last_user_messages = sync_to_async(get_last_user_messages)