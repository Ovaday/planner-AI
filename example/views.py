import logging
from datetime import datetime

import telebot
from django.http import HttpResponse
from telebot import types

from helpers.openAIHelper import chatGPT_req
from helpers.tokenHelpers import get_token
from tg_bot.models import Chat
import json

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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = get_token('TG_BOT_TOKEN')
bot = telebot.TeleBot(TUTORIAL_BOT_TOKEN)

@bot.message_handler(commands=['help', 'start', 'english'])
def send_welcome(message):
    print(message.text)
    chat_id = message.from_user.id
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
        )
        print(response)
        chat = response
    else:
        chat = chat.first()
    bot.send_message(chat_id, """\
Thank you for launch.

Please wait for the approval | Пожалуйста подождите одобрения\
""")
    creator = Chat.objects.get(pk=1)
    if not chat.is_approved:
        markup_admin = types.InlineKeyboardMarkup()
        markup_admin.add(types.InlineKeyboardButton("approve", callback_data=f'approve_{chat_id}'))
        markup_admin.add(types.InlineKeyboardButton("decline", callback_data=f'decline_{chat_id}'))
        bot.send_message(creator.chat_id, f"New request from {chat_id}. First Name: {message.chat.first_name}. Username: {message.chat.username}", reply_markup=markup_admin)

    msg = f"For now, please select your preferred language: | Пока, выберите предпочитаемый язык:"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("english", callback_data='english'))
    markup.add(types.InlineKeyboardButton("русский", callback_data='русский'))
    ret_msg = bot.send_message(chat_id, msg, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print('echo_message')
    print(message)
    chat_id = message.chat.id
    print(chat_id)

    chat = Chat.objects.get(chat_id=chat_id)
    print(chat)
    print(chat.is_approved)

    if not chat:
        print('no chat')
        send_welcome(message)
    if not chat.is_approved:
        msg = 'Please wait till you are approved | Подождите одобрения'
        bot.reply_to(message, msg)
    else:
        markup = types.ReplyKeyboardRemove(selective=False)
        if message.text == 'ChatGPT':
            if chat.language == 'english':
                msg = 'Write any text and the answer will be written by the ChatGPT neural network. If the answer comes in English, try specifying (Answer in Russian). Despite the fact that some answers may require a very meaningful response, try not to formulate them so that the answers are longer than the possible maximum length of the message (1 thousand characters).'
            else:
                msg = 'Напишите любой текст и ответ на него будет написан нейросетью ChatGPT. Если ответ придет на английском, попробуйте специфицировать (Отвечай на русском). Не смотря на то, что некоторые ответы могут требовать очень содержательного ответа, старайтесь не формулировать их так, чтобы ответы были длиной больше, чем возможная макс. длина сообщения (1 тыс.символов).'
            bot.send_message(chat_id, msg, reply_markup=markup)
        else:
            chat.counter += 1
            chat.save()
            if len(message.text) > 1000:
                bot.send_message(chat_id, 'Error: Text is too big | Текст слишком длинный')
            else:
                chatgpt_response = chatGPT_req(message.text, chat)
                print(chatgpt_response)
                bot.send_message(chat_id, chatgpt_response)

@bot.callback_query_handler(func=lambda call: True)
def callback_query_model(call):
    print('callback_query_model')
    chat_id = call.message.chat.id
    print(chat_id)
    creator = Chat.objects.get(pk=1)

    choice = call.data
    chat = Chat.objects.get(chat_id=chat_id)
    if choice == 'english' or choice == 'русский':
        if choice == 'english':
            msg = f"Language preference is set, thank you."
            chat.language = 'english'
            chat.save()
        else:
            msg = f"Спасибо, предпочитаемый язык обновлен."
            chat.language = 'russian'
            chat.save()
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(call.message.chat.id, msg, reply_markup=markup)
    elif (choice[:7] == 'approve' or choice[:7] == 'decline') and str(creator.chat_id) == str(chat_id):
        chat = Chat.objects.get(chat_id=choice[8:])
        print(chat)
        if choice[:7] == 'approve':
            chat.is_approved = True
            chat.save()
            markup = types.ReplyKeyboardMarkup()
            itembtn1 = types.KeyboardButton('ChatGPT')
            markup.add(itembtn1)
            if chat.language == 'english':
                bot.send_message(chat.chat_id, 'Your account is approved', reply_markup=markup)
            else:
                bot.send_message(chat.chat_id, 'Аккаунт подтвержден', reply_markup=markup)

        else:
            bot.send_message(chat.chat_id, 'Your account is declined')

        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(chat_id, choice[:7]+'d', reply_markup=markup)


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/tutorial/
class TutorialBotView(View):
    async def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        if t_data:
            update = telebot.types.Update.de_json(t_data)
            bot.process_new_updates([update])

            return JsonResponse({"ok": "POST request processed"})
        else:
            return JsonResponse({"ok": "POST request processed"})

        print(t_data)
        creator = Chat.objects.get(pk=2)
        inline_data = None
        try:
            t_message = t_data["message"]
            t_chat = t_message["chat"]
        except:
            t_message = t_data["message"]
            t_chat = t_data["chat"]
            inline_data = t_data["data"]

        try:
            text = t_message["text"].strip().lower()
        except Exception as e:
            return JsonResponse({"ok": "POST request processed"})

        text = text.lstrip("/")
        print(t_chat["id"])
        chat = Chat.objects.filter(chat_id=t_chat["id"])
        print(chat)
        response = f"Received: {text}"
        self.send_message(response, t_chat["id"])

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
            msg = 'Please wait till you are approved | Подождите одобрения'
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
            inline_keyboard = TutorialBotView.parse_keyboard(keyboard_params)

        data = {
            "chat_id": chat_id,
            "text": message,
        }
        if len(inline_keyboard) != 0:
            data['reply_markup'] = (None, inline_keyboard )
        #else:
            #data['reply_markup'] = {'remove_keyboard': 'true'}
        print(data)
        if message is None:
            return

        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )

    @staticmethod
    def parse_keyboard(keyboard_params):
        inline_keyboard = []
        for param in keyboard_params:
            inline_keyboard.append({'text': param, "callback_data": param})
        kb = json.dumps(
            {"inline_keyboard":[inline_keyboard]}
        )
        return kb