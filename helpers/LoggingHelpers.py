import datetime
import json
import traceback
from asgiref.sync import sync_to_async
from helpers.DatabaseHelpers import get_collection_handle, get_db_handle


def fill_log_template(exception, function_name, current_datetime, chat_id):
    if isinstance(exception, Exception):
        exception_str = traceback.format_exc()
    elif isinstance(exception, dict):
        exception_str = exception
    else:
        exception_str = str(exception)

    return {
        "function_name": function_name,
        "exception": exception_str,
        "datetime": current_datetime,
        "chat_id": chat_id
    }


def __insert_log(exception, function_name='', current_datetime=datetime.datetime.now(), chat_id=None):
    error = fill_log_template(exception, function_name, current_datetime, chat_id)
    db_handle, mongo_client = get_db_handle('service_data')
    coll_handle = get_collection_handle(db_handle, "error_log")

    return coll_handle.insert_one(error)


async_insert_log = sync_to_async(__insert_log)
