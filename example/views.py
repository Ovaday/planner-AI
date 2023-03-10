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