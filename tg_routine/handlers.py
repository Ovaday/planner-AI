import asyncio
import datetime
import io

import httpx
from asgiref.sync import async_to_sync, sync_to_async
from django.http import JsonResponse
from django_q.tasks import async_task, result_group, delete_group
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from helpers.DatabaseHelpers import async_set_language, async_get_chat, async_get_creator, async_set_approved, \
    async_tick_counter, async_assign_last_conversation
from cryptography.fernet import Fernet

from helpers.openAIHelper import chatGPT_req, chatGPT_req_test
from helpers.tokenHelpers import get_token
from helpers.translationsHelper import get_label, get_day
from open_ai.requestsHandler import voice_to_text
from tg_routine.serviceHelpers import check_is_chat_approved
from tg_routine.templates import fill_classification_request, fill_reminder_template, fill_reminder_advice_request, \
    fill_advanced_classification_request
import soundfile as sf


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    creator = await async_get_creator()
    choice = query.data
    if (choice == 'english' or choice == 'russian'):
        await async_set_language(chat_id, choice)
        await query.edit_message_text(text=f"{get_label('language_is_set', choice)}")
        chat = await async_get_chat(chat_id)
        if not chat.is_approved:
            await context.bot.send_message(chat_id=chat_id, text=get_label('wait_till_approved', choice))

    elif (choice[:7] == 'approve' or choice[:7] == 'decline') and str(creator.chat_id) == str(chat_id):
        chat = await async_get_chat(choice[8:])
        print(chat)
        if choice[:7] == 'approve':
            await async_set_approved(chat.chat_id, True)
            reply_keyboard = [['ChatGPT']]
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="ChatGPT"
            )
            await context.bot.send_message(chat_id=chat.chat_id, text=get_label('account_is_approved', chat.language), reply_markup=reply_markup)
        else:
            await async_set_approved(chat.chat_id, False)
            await context.bot.send_message(chat_id=chat.chat_id, text=get_label('account_is_declined', chat.language))

        await context.bot.send_message(chat_id=creator.chat_id, text=choice[:7] + 'd')

async def timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message, chat_id, chat = await resolve_main_params(update)
    await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id, text=get_label('timeout', chat.language))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message, chat_id, chat = await resolve_main_params(update)
    creator = await async_get_creator()

    await context.bot.send_message(chat_id=chat_id, text=f"""
    {get_label('start', 'english')}

{get_label('start', 'russian')}
    """)
    print(chat)
    print(chat.is_approved)

    if chat.is_approved == False:
        print('sending msg to creator')
        msg = f"New request from {chat_id}. First Name: {message.chat.first_name}. Username: {message.chat.username}"
        keyboard = [[InlineKeyboardButton("approve", callback_data=f'approve_{chat_id}'),
                     InlineKeyboardButton("decline", callback_data=f'decline_{chat_id}'), ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=creator.chat_id, text=msg, reply_markup=reply_markup)

    msg = f"For now, please select your preferred language: | Пока, выберите предпочитаемый язык:"
    keyboard = [[InlineKeyboardButton("english", callback_data="english"),
                 InlineKeyboardButton("русский", callback_data="russian"), ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=reply_markup)

async def lambda_call_wrapper(event):
    asyncio.ensure_future(lambda_call(event))
    await asyncio.sleep(1)
    return JsonResponse({"ok": "POST request processed"})

async def lambda_call(event):
    key = bytes(str(get_token('COMMON_KEY')), 'utf-8')
    fernet = Fernet(key)
    encMessage = fernet.encrypt(bytes(event,'utf-8'))
    gateway_url = get_token('GATEWAY_URL')
    async with httpx.AsyncClient() as client:
        response = await client.post(gateway_url, data={'data': encMessage.decode("utf-8") })

    return JsonResponse({"ok": "POST request processed"})

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message, chat_id, chat = await resolve_main_params(update)
    if not chat:
        print('no chat')
        return await start(update, context)
    if not await check_is_chat_approved(chat, context, message):
        return

    else:
        if message.text == 'ChatGPT':
            reply_markup = ReplyKeyboardRemove()
            await context.bot.send_message(chat_id=chat_id, text=get_label('chat_gpt_intro', chat.language), reply_markup=reply_markup)
        else:
            await async_tick_counter(chat_id)
            if len(message.text) > 500:
                await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id, text=get_label('too_long_msg', chat.language))
            elif len(message.text) < 5:
                await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id, text=get_label('too_short_msg', chat.language))
            else:
                await async_assign_last_conversation(chat_id, message.text)
                print('Invoke Lambda Function')
                # return await lambda_call_wrapper(update.to_json())
                async_task('helpers.SQSHelpers.task_receiver', update.to_json(), kwargs={})

async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message, chat_id, chat = await resolve_main_params(update)

    if not chat:
        print('no chat')
        return await start(update, context)
    if not await check_is_chat_approved(chat, context, message):
        return

    else:
        voice_message = await context.bot.get_file(update.message.voice.file_id)
        voice_file = io.BytesIO()
        await voice_message.download_to_memory(voice_file)
        await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id,
                                       text=f'File received.')
        voice_file.seek(0)
        voice_file.name = f'voice_{update.message.chat_id}_{update.message.message_id}.ogg'

        data, samplerate = sf.read(voice_file)
        mem_file = io.BytesIO()
        sf.write(mem_file, data, samplerate, 'PCM_16', format='wav')
        mem_file.seek(0)
        duration = sf.info(mem_file).duration
        mem_file.seek(0)
        mem_file.name = f'voice_{update.message.chat_id}_{update.message.message_id}.wav'
        recognized_text = await voice_to_text(chat, mem_file, duration)
        await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id,
                                       text=f'Recognized: {recognized_text}')


async def chapt_gpt_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('chapt_gpt_message')
    message, chat_id, chat = await resolve_main_params(update)
    original_request = message.text.replace('\'', '').replace('\"', '')
    if not chat:
        print('no chat')
        return await start(update, context)
    if not await check_is_chat_approved(chat, context, message):
        return

    else:
        results = await asyncio.gather(chatGPT_req(fill_classification_request(message.text), chat,
                                                 type='reminder_classification'), chatGPT_req(fill_advanced_classification_request(message.text), chat,
                                                 type='advanced_classification_request'))
        print('asyncio.gather executed')
        print(results)
        reminder_probability = results[0]
        advanced_reminder_probability = results[1]
        await context.bot.send_message(chat_id=chat_id, text=reminder_probability)
        await context.bot.send_message(chat_id=chat_id, text=advanced_reminder_probability)

        if define_needs_reminder(reminder_probability, advanced_reminder_probability):
            await set_reminder(message, chat, chat_id, context, reminder_probability)
        elif define_probably_needs_reminder(reminder_probability, advanced_reminder_probability):
            await set_reminder_and_answer(message, chat, chat_id, context, reminder_probability)
        elif define_needs_save(reminder_probability, advanced_reminder_probability):
            await context.bot.send_message(chat_id=chat_id, text=get_label('ask_to_save', chat.language))
        else:
            await ask_chatGPT(message, chat, chat_id, context)


async def ask_chatGPT(message, chat, chat_id, context):
    chat_gpt_response = await chatGPT_req(message.text, chat, type='normal')
    await context.bot.send_message(chat_id=chat_id, text=chat_gpt_response)

async def set_reminder(message, chat, chat_id, context, prob):
    results = await asyncio.gather(chatGPT_req(fill_reminder_template(message.text), chat, type='reminder_time', initial_text=message.text),
                                   chatGPT_req(fill_reminder_advice_request(message.text, chat.language), chat, type='advice_for_reminder'))
    print(' set_reminder asyncio.gather executed')
    print(results)
    reminder_time = results[0]
    additional_info = results[1]
    print(reminder_time)
    print(additional_info)
    await sent_reminder(reminder_time, additional_info, message, chat, chat_id, context, prob)

async def set_reminder_and_answer(message, chat, chat_id, context, prob):
    results = await asyncio.gather(chatGPT_req(fill_reminder_template(message.text), chat, type='reminder_time', initial_text=message.text),
                                   chatGPT_req(message.text, chat, type='normal'))
    print(' set_reminder_and_answer asyncio.gather executed')
    print(results)
    reminder_time = results[0]
    additional_info = results[1]
    print(reminder_time)
    print(additional_info)
    await sent_reminder(reminder_time, additional_info, message, chat, chat_id, context, prob, is_answer=True)

async def sent_reminder(reminder_time, additional_info, message, chat, chat_id, context, prob, is_answer=False):
    await resolve_is_defined_time_of_event(reminder_time, chat, chat_id, context, message, prob, is_answer)
    await resolve_when_is_better_to_remind(reminder_time, chat, chat_id, context)
    await resolve_additional_reminder(reminder_time, chat, chat_id, context)
    if is_answer:
        advice_markup = get_reminder_decline_inline_keyboard(chat)
    else:
        advice_markup = None
    await context.bot.send_message(chat_id=chat_id, text=additional_info, reply_markup=advice_markup)

def define_text_parameter(data, param_name, param_min_length=0):
    return param_name in data and len(data[param_name]) > param_min_length and (not 'YYYY-MM-DD HH:MM' in data[param_name] or param_name == 'planned_event_start')

def get_time(data, param_name, language):
    if (data) and param_name in data:
        try:
            date_time_param = datetime.datetime.strptime(data[param_name], '%Y-%m-%d %H:%M')
            week_day = get_day(date_time_param, language)
            return date_time_param.strftime('%H:%M %d.%m.%Y') + f" ({week_day})"
        except:
            return f"[{get_label('error', language)}]"

    return f"[{get_label('error', language)}]"


async def resolve_is_defined_time_of_event(reminder_time, chat, chat_id, context, message, prob, is_answer=False):
    if 'is_defined_time_of_event' in reminder_time and bool(
            reminder_time['is_defined_time_of_event']) and define_text_parameter(reminder_time, 'planned_event_start', 5):
        additional_text = ''
        if is_answer:
            additional_text = f" {get_label('additional_answer_chat_gpt', chat.language)}."
        text_to_send = f"{get_label('event_identified', chat.language)}: {get_time(reminder_time, 'planned_event_start', chat.language)} {get_label('based_on_your_message', chat.language)}: {message.text} {get_label('with_a_probability', chat.language)} {prob}/10 {get_label('it_needs_a_reminder', chat.language)}.{additional_text}"
        await context.bot.send_message(chat_id=chat_id, text=text_to_send)

async def resolve_when_is_better_to_remind(reminder_time, chat, chat_id, context):
    if define_text_parameter(reminder_time, 'when_is_better_to_remind', 5):
        text_to_send = f"{get_label('reminder_will_be_set', chat.language)}: {get_time(reminder_time, 'when_is_better_to_remind', chat.language)}"
        reply_markup = get_reminder_inline_keyboard(chat)
        await context.bot.send_message(chat_id=chat_id, text=text_to_send, reply_markup=reply_markup)

async def resolve_additional_reminder(reminder_time, chat, chat_id, context):
    if define_text_parameter(reminder_time, 'additional_reminder', 5):
        text_to_send = f"{get_label('additional_reminder_will_be_set', chat.language)}: {get_time(reminder_time, 'additional_reminder', chat.language)}"
        reply_markup = get_reminder_inline_keyboard(chat)
        await context.bot.send_message(chat_id=chat_id, text=text_to_send, reply_markup=reply_markup)


def get_reminder_inline_keyboard(chat):
    keyboard = [[InlineKeyboardButton(get_label('edit_time', chat.language), callback_data=f'edit_time_{chat.chat_id}'),
                 InlineKeyboardButton(get_label('delete', chat.language), callback_data=f'decline_{chat.chat_id}'), ]]
    return InlineKeyboardMarkup(keyboard)

def get_reminder_decline_inline_keyboard(chat):
    keyboard = [[InlineKeyboardButton(get_label('decline_reminders_ask', chat.language), callback_data=f'decline_reminders_ask_{chat.chat_id}')]]
    return InlineKeyboardMarkup(keyboard)

def bool_val(data, param):
    return param in data and bool(data[param])

#{"is_event": "true", "is_question": "false", "is_appointment": "false", "is_intention": "false", "is_reminder_request": "false", "is_save_request": "false", "none_of_the_above": "false"}
def define_needs_reminder(prob, json_classif):
    if json_classif["is_event"] == "true":
        return json_classif["is_appointment"] == "true" or json_classif["is_reminder_request"] == "true" or prob > 7
    elif json_classif["is_question"] == "true":
        return prob >= 7 and json_classif["is_reminder_request"] == "true"
    elif json_classif["is_reminder_request"] == "true":
        return True
    elif json_classif["none_of_the_above"] == "true":
        return json_classif["is_intention"] == "true" and json_classif["is_reminder_request"] == "true"
    else:
        return False


def define_probably_needs_reminder(prob, json_classif):
    if json_classif["is_event"] == "true":
        return json_classif["is_question"] == "true"
    elif json_classif["is_intention"] == "true" and prob > 7:
        return True
    elif len(json_classif) < 1 and prob > 6:
        return True
    else:
        return False


def define_needs_save(prob, json_classif):
    return json_classif["is_save_request"] == "true"


async def resolve_main_params(update: Update):
    message = update.message
    print(message)
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id)
    return message, chat_id, chat