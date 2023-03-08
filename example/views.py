# example/views.py
from datetime import datetime

from django.http import HttpResponse

from telegram.models import Chat


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

import json
import os

import requests
from django.http import JsonResponse
from django.views import View

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = "6193255741:AAHnh1ZluVB8KkIFXBuhpIent7Fk9Hj5vhM"


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/tutorial/
class TutorialBotView(View):
    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        t_message = t_data["message"]
        t_chat = t_message["chat"]

        try:
            text = t_message["text"].strip().lower()
        except Exception as e:
            return JsonResponse({"ok": "POST request processed"})

        text = text.lstrip("/")
        print(t_chat["id"])
        chat = Chat.objects.filter(chat_id=t_chat["id"])
        print(chat)
        if not chat or len(chat) < 1:
            chat = {
                "chat_id": t_chat["id"],
                "counter": 0
            }
            response = Chat.objects.create(
                chat_id=chat['chat_id'],
                counter=chat['counter'],
            )
            print(response)
            chat["_id"] = response.id
        else:
            chat = chat.first()

        if text == "+":
            current_counter = chat.counter + 1
            chat.counter = current_counter
            chat.save()
            msg = f"Number of '+' messages that were parsed: {current_counter}"
            self.send_message(msg, t_chat["id"])
        elif text == "restart":
            chat.counter = 0
            chat.save(chat)
            msg = "The Tutorial bot was restarted"
            self.send_message(msg, t_chat["id"])
        else:
            msg = "Unknown command"
            self.send_message(msg, t_chat["id"])

        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )