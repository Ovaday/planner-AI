import asyncio

from django.http import JsonResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from helpers.tokenHelpers import get_token
from tg_routine.handlers import start, echo, button, timeout

application = Application.builder().token(get_token('TG_BOT_TOKEN')).build()

async def main(event):
    try:
        await application.initialize()
        start_handler = CommandHandler(['start', 'help'], start)
        timeout_handler = CommandHandler(['timeout'], timeout)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
        application.add_handler(CallbackQueryHandler(button))

        application.add_handler(echo_handler)
        application.add_handler(start_handler)
        application.add_handler(timeout_handler)

        await application.process_update(
            Update.de_json(event, application.bot)
        )
        return JsonResponse({"ok": "POST request processed"})

    except Exception as exc:
        return JsonResponse(status=500, data={"nok": "POST request failed"})

async def main_wrapper(event):
    try:
        # wait for a task to complete
        return await asyncio.wait_for(main(event), timeout=9.7)
    except asyncio.TimeoutError:
        my_event = {'update_id': event['update_id'], 'message': {'message_id': event['message']['message_id'],
                                            'from': {'id': event['message']['from']['id'], 'is_bot': False, 'first_name': 'Leo',
                                                     'last_name': 'Kalbhenn', 'language_code': 'ru'},
                                            'chat': {'id': event['message']['from']['id'], 'first_name': 'Leo', 'last_name': 'Kalbhenn',
                                                     'type': 'private'}, 'date': event['message']['date'], 'text': '/timeout',
                                            'entities': [{'offset': 0, 'length': 8, 'type': 'bot_command'}]}}
        return await asyncio.wait_for(main(my_event), timeout=0.3)



def lambda_handler(event):
    try:
        print(asyncio.get_event_loop())
    except Exception as e:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return asyncio.get_event_loop().run_until_complete(main_wrapper(event))