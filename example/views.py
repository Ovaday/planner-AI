import logging
from django.shortcuts import render

from helpers.openAIHelper import chatGPT_req
import json

from django.http import JsonResponse
from django.views import View

from tg_routine.main import lambda_handler


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


def error_404_view(response):
    return render(response, "404.html")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



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