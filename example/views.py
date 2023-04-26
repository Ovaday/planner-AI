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
        <h2>hell1</h2>
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