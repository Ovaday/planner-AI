# example/views.py
from datetime import datetime

import openai
from django.http import HttpResponse

from helpers.tokenHelpers import get_token
from telegram.models import Chat
import json
import os

import requests
from django.http import JsonResponse
from django.views import View


def index(request):
    now = datetime.now()
    openai.api_key = get_token('OPENAI_API')
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
            <p>openai.Model.list is { openai.Model.list() }.</p>
        </body>
    </html>
    '''

    print('ok')
    return HttpResponse(html)



TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = get_token('TG_BOT_TOKEN')


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
        elif text == "envs":
            msg = f"Env variable: {os.getenv('VERCEL_URL')}"
            self.send_message(msg, t_chat["id"])
        elif text[:3] == "chat":
            chatgpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": text}
                ]
            )
            self.send_message(chatgpt_response, t_chat["id"])
        elif text == "restart":
            chat.counter = 0
            chat.save()
            msg = "The Tutorial bot was restarted"
            self.send_message(msg, t_chat["id"])
        else:
            test = text[:3]
            msg = f"Unknown command: {text}, doesn't fit {test}"
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