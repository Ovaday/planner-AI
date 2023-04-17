import logging, json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from tg_routine.main import telegram_async_handler


def index(response):
    current_user = response.user
    username = "anonymous"
    if current_user.id != "": username = current_user.username
    if response.method == "GET":
        print('GET response')

    elif response.method == 'POST':
        print('POST response')

    context = {"form": "none"}
    return render(response, "index.html", context)


def chat_page(response):
    current_user = response.user
    username = "anonymous"
    if current_user.id != "": username = current_user.username
    if response.method == "GET":
        print('GET response')

    elif response.method == 'POST':
        print('POST response')

    context = {"form": "none"}
    return render(response, "index.html", context)

def error_404_view(response):
    return render(response, "404.html")


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
