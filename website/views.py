import datetime
import logging, json

import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View

from tg_routine.main import telegram_async_handler
from helpers.MessageHistoryHelpers import get_last_user_messages, insert_web_message, construct_message


# Endpoint to retrieve the index page
def index(request):
    current_user = request.user
    username = "anonymous"
    if current_user.id != "": username = current_user.username
    if request.method == "GET":
        print('GET response')

    elif request.method == 'POST':
        print('POST response')

    context = {"form": "none"}
    return render(request, "index.html", context)


# Endpoint to retrieve the web_chat page
def chat_page(request):
    if request.method == "GET":
        print('GET response')

        context = {}
        return render(request, "web_chat.html", context)
    else:
        return error_404_view(request)


# Endpoint to retrieve messages
def get_messages(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    if not user_id:
        return Http401()
    if request.method == "GET":

        record_list = get_last_user_messages(user_id)
        output_template = {
            "chat_id": 'chat_id',
            "message_time": 'message_time',
            "message_id": 'message_id',
            "username": 'username',
            "message_raw": 'message',
            "response_raw": 'response'
        }
        messages_list = []
        if record_list:
            for data in record_list:
                message = {}
                for item in data:
                    if item in output_template:
                        message[item] = data[item]
                messages_list.append(message)
            json_string = json.dumps(messages_list, ensure_ascii=False, indent=4, sort_keys=True, default=str)
            return JsonResponse({"messages": json_string})
        else:
            return messages_list


    else:
        return error_404_view(request)


# ToDo Anastasia: Create endpoint to insert message. We should receive in kwargs following parameters:
#  kwargs.post.user_id: int
#  kwargs.post.message: str
#  Use kwargs.post('user_id') to retrieve the param. It should get only POST requests and validate the message by the
#  length (minimum - 5, max - 1000). In addition, there should be non-null user_id.
#  To insert, use methods from the same helper, construct_message and insert_web_message.
#  As a result return JSON with response 200 - ok (google how it should look like.)


def insert_message(request, *args, **kwargs):
    user_id = int(kwargs.get('user_id'))
    message = kwargs.get('message')
    username = kwargs.get('username')
    if user_id > 0:
        requests.post(user_id)
        if 5 <= len(message) <= 1000:
            data = construct_message(user_id, message_time=datetime.date.today(), message_id=1, username=str(username), message=message, additional_info=None, external_id=None, classification_results=None)
            insert_web_message(data)

    return JsonResponse({"ok": "GET request processed"})



def error_404_view(request):
    return render(request, "404.html")


class Http401(HttpResponse):
    def __init__(self):
        super().__init__('401 Unauthorized', status=401)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/api/telegram_webhook/
class TelegramBotView(View):
    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        print(t_data)
        try:
            return telegram_async_handler(t_data)
        except Exception as e:
            print('Exception: ' + str(e))
            return JsonResponse({"ok": "POST request processed"})
