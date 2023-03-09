# example/views.py
from datetime import datetime

import openai
from django.http import HttpResponse

from helpers.openAIHelper import chatGPT_req
from helpers.tokenHelpers import get_token
from telegram.models import Chat
import json
import os

import requests
from django.http import JsonResponse
from django.views import View


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
        creator = Chat.objects.get(pk=1)
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
            msg = f"Please wait for the approval | Пожалуйста подождите одобрения"
            self.send_message(msg, t_chat["id"])
            msg = "New request from " + str(t_chat["id"])
            self.send_message(msg, creator.chat_id)
            msg = f"For now, please select your preferred language: | Пока, выберите предпочитаемый язык:"
            self.send_message(msg, t_chat["id"], ['english', 'русский'])
            return JsonResponse({"ok": "POST request processed"})
        else:
            chat = chat.first()

        if not chat.is_approved:
            if text != 'english' or text != 'русский':
                msg = 'Please wait till you are approved | Подождите одобрения'
            elif text == 'english':
                msg = f"Language preference is set, thank you"
                chat.language = 'english'
                chat.save()
            else:
                msg = f"Спасибо, предпочитаемый язык обновлен"
                chat.language = 'russian'
                chat.save()

            self.send_message(msg, t_chat["id"])
            return JsonResponse({"ok": "POST request processed"})

        if text == "restart":
            chat.counter = 0
            chat.save()
            msg = "The bot was restarted"
            self.send_message(msg, t_chat["id"])
        else:
            chat.counter += 1
            chat.save()
            if len(text) > 1000:
                self.send_message('Request is too big', t_chat["id"])
            else:
                chatgpt_response = chatGPT_req(text, chat)
                print(chatgpt_response)
                self.send_message(chatgpt_response, t_chat["id"])

        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(message, chat_id, keyboard_params=None):
        inline_keyboard = []
        if keyboard_params:
            inline_keyboard = message.parse_keyboard(keyboard_params)

        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        if len(inline_keyboard) != 0:
            data['inline_keyboard'] = inline_keyboard

        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )

    @staticmethod
    def parse_keyboard(keyboard_params):
        inline_keyboard = []
        for param in keyboard_params:
            inline_keyboard.append({'text': param, 'callback_data': 'string'})
        return [inline_keyboard]