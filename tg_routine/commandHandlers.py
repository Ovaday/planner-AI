import asyncio
import datetime
import json

from asgiref.sync import async_to_sync
from django_q.tasks import async_task
from telegram import Update
from telegram.ext import ContextTypes

from helpers.DatabaseHelpers import async_get_chat
from helpers.ScheduleHelpers import async_to_schedule, get_my_reminders
from helpers.translationsHelper import get_label
from tg_routine.handlers import lambda_call_wrapper
from tg_routine.serviceHelpers import check_is_chat_approved
from tg_routine.templates import fill_reminder_template


async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    print(message)
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id)
    if not await check_is_chat_approved(chat, context, message):
        return

    now = datetime.datetime.now()  # get the current time
    future = now + datetime.timedelta(seconds=100)

    # schedule the event to run at the specified time
    #schedule_wrapper(future)
    #schedule_my_task(future)
    #async_task('tg_routine.commandHandlers.schedule_my_task', future, hook='tg_routine.commandHandlers.print_result')

    #asyncio.create_task(async_to_schedule(chat, future, message.text))
    json_update = json.loads(str(update.to_json()))
    print('json_update')
    print(json_update)
    json_update['message']['text'] = fill_reminder_template(message.text)
    print(json_update)
    async_task('helpers.SQSHelpers.task_receiver', 2.5, kwargs={'first_param': 3, 'second_param': 6})
    #return await lambda_call_wrapper(json.dumps(json_update))
    #print(check_aws_validity())


async def my_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message

    chat = await async_get_chat(chat_id)
    if not await check_is_chat_approved(chat, context, message.text):
        return

    reminders = await get_my_reminders(chat)
    if not reminders or len(reminders.keys()) < 1:
        return await context.bot.send_message(chat_id=chat_id, text=get_label('no_reminders', chat.language))

    reminder_strings = ""
    for reminder_key in reminders.keys():
        reminder = reminders[reminder_key]
        reminder_string = f"""
{get_label('reminder_word', chat.language)} '{reminder['request']}' {get_label('due_till', chat.language)} {reminder['schedule'].next_run.strftime("%d.%m.%Y")} {get_label('at', chat.language)} {reminder['schedule'].next_run.strftime("%H:%M")}"""
        reminder_strings +=reminder_string
    return await context.bot.send_message(chat_id=chat_id, text=reminder_strings)

async def message_specific(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('message_specific')
    message = update.message
    print(message)
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=get_label('chat_gpt_intro', chat.language))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('help')
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=get_label('help', chat.language))