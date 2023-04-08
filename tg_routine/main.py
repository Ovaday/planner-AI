import asyncio
from django.http import JsonResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from helpers.tokenHelpers import get_token
from tg_routine.commandHandlers import *
from tg_routine.handlers import start, echo, button, timeout, chapt_gpt_message
from tg_routine.templates import fill_template
import traceback
application = Application.builder().token(get_token('TG_BOT_TOKEN')).build()

async def main(event):
    print('main')
    try:
        await application.initialize()
        application.add_handler(CallbackQueryHandler(button))

        start_handler = CommandHandler(['start'], start)
        help_handler = CommandHandler(['help'], help)
        application.add_handler(start_handler)
        application.add_handler(help_handler)

        timeout_handler = CommandHandler(['timeout'], timeout)
        message_specific_handler = CommandHandler(['message_specific'], message_specific)
        application.add_handler(timeout_handler)
        application.add_handler(message_specific_handler)

        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
        application.add_handler(echo_handler)

        reminder_handler = CommandHandler(['reminder'], reminder)
        my_reminders_handler = CommandHandler(['my_reminders'], my_reminders)
        application.add_handler(reminder_handler)
        application.add_handler(my_reminders_handler)


        message_non_specific_handler = MessageHandler(filters.COMMAND, message_specific)
        application.add_handler(message_non_specific_handler)

        update = Update.de_json(event, application.bot)
        print(update)
        await application.process_update(
            update
        )
        return JsonResponse({"ok": "POST request processed"})

    except Exception as exc:
        print(exc)
        return JsonResponse(status=500, data={"nok": "POST request failed"})

async def main_qcluster(event):
    print('main_qcluster')
    try:
        await application.initialize()
        print('application.initialize')
        chapt_gpt_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chapt_gpt_message)
        print('chapt_gpt_message_handler')
        application.add_handler(chapt_gpt_message_handler)

        update = Update.de_json(event, application.bot)
        print(update)
        await application.process_update(
            update
        )
        return JsonResponse({"ok": "POST request processed"})

    except Exception as exc:
        traceback.print_tb(exc.__traceback__)
        print(traceback.format_exc())
        print(exc)
        return JsonResponse(status=500, data={"nok": "POST request failed"})

async def main_wrapper(event, is_fictious=False):
    print('main_wrapper')
    try:
        if not is_fictious:
            return await asyncio.wait_for(main(event), timeout=9.3)
        else:
            #my_event = fill_template('128454636', 'message_specific')
            return await asyncio.wait_for(main_qcluster(event), timeout=40.3)
    except asyncio.TimeoutError:
        my_event = {'update_id': event['update_id'], 'message': {'message_id': event['message']['message_id'],
                                            'from': {'id': event['message']['from']['id'], 'is_bot': False, 'first_name': 'Leo',
                                                     'last_name': 'Kalbhenn', 'language_code': 'ru'},
                                            'chat': {'id': event['message']['from']['id'], 'first_name': 'Leo', 'last_name': 'Kalbhenn',
                                                     'type': 'private'}, 'date': event['message']['date'], 'text': '/timeout',
                                            'entities': [{'offset': 0, 'length': 8, 'type': 'bot_command'}]}}
        return await asyncio.wait_for(main(my_event), timeout=0.2)



def lambda_handler(event):
    try:
        print(asyncio.get_event_loop())
    except Exception as e:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return asyncio.get_event_loop().run_until_complete(main_wrapper(event))

def task_handler(event):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print('set_event_loop')
        return asyncio.get_event_loop().run_until_complete(main_wrapper(json.loads(event), True))
    except Exception as e:
        print('run with exception')
        print(e)
        return asyncio.get_event_loop().run_until_complete(main_wrapper(event, True))

