import logging
from datetime import datetime

from django.http import HttpResponse
from helpers.openAIHelper import chatGPT_req
import json

from django.http import JsonResponse
from django.views import View

from tg_routine.main import lambda_handler


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


"""
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
                bot.send_message(chat_id, 'Error: Text is too long | Текст слишком длинный')
            elif len(message.text) < 5:
                bot.send_message(chat_id, 'Error: Text is too short | Текст слишком короткий')
            else:
                chatgpt_response = chatGPT_req(message.text, chat)
                print(chatgpt_response)
                bot.send_message(chat_id, chatgpt_response)

@bot.callback_query_handler(func=lambda call: True)
def callback_query_model(call):
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
"""


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/tutorial/
class TutorialBotView(View):
    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        print(t_data)
        try:
            return lambda_handler(t_data)
        except Exception as e:
            print('Exception: ' + str(e))
            return JsonResponse({"ok": "POST request processed"})