import asyncio

from django.http import JsonResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from helpers.tokenHelpers import get_token
from tg_routine.handlers import start, echo, button

application = Application.builder().token(get_token('TG_BOT_TOKEN')).build()

async def main(event):
    try:
        await application.initialize()
        start_handler = CommandHandler(['start', 'help'], start)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
        application.add_handler(CallbackQueryHandler(button))

        application.add_handler(echo_handler)
        application.add_handler(start_handler)

        await application.process_update(
            Update.de_json(event, application.bot)
        )
        return JsonResponse({"ok": "POST request processed"})

    except Exception as exc:
        return JsonResponse(status=500, data={"nok": "POST request failed"})


def lambda_handler(event):
    try:
        print(asyncio.get_event_loop())
    except Exception as e:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return asyncio.get_event_loop().run_until_complete(main(event))