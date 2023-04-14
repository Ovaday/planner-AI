import asyncio

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from helpers.DatabaseHelpers import async_get_chat
from helpers.openAIHelper import chatGPT_req
from helpers.translationsHelper import get_label, get_day
from open_ai.helpers import MID_PROB, LOW_PROB, HIGH_PROB
from tg_routine.templates import *


async def check_is_chat_approved(chat, context, message):
    if not chat.is_approved:
        await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat.chat_id,
                                       text=get_label('wait_till_approved', chat.language))
        return False
    return True


def audio_json_to_text(json_update, recognized_text):
    del json_update['message']['voice']
    json_update['message']['text'] = recognized_text
    json_update['message']['group_chat_created'] = False
    json_update['message']['delete_chat_photo'] = False
    json_update['message']['supergroup_chat_created'] = False
    json_update['message']['channel_chat_created'] = False
    return json_update


async def set_reminder(message, chat, chat_id, context, prob):
    results = await asyncio.gather(
        chatGPT_req(fill_reminder_template(message.text), chat, type='reminder_time', initial_text=message.text),
        chatGPT_req(fill_reminder_advice_request(message.text, chat.language), chat, type='advice_for_reminder'))
    print(' set_reminder asyncio.gather executed')
    print(results)
    reminder_time = results[0]
    additional_info = results[1]
    print(reminder_time)
    print(additional_info)
    await sent_reminder(reminder_time, additional_info, message, chat, chat_id, context, prob)


async def set_reminder_and_answer(message, chat, chat_id, context, prob):
    results = await asyncio.gather(
        chatGPT_req(fill_reminder_template(message.text), chat, type='reminder_time', initial_text=message.text),
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
    return param_name in data and len(data[param_name]) > param_min_length and (
            not 'YYYY-MM-DD HH:MM' in data[param_name] or param_name == 'planned_event_start')


def get_time(data, param_name, language):
    if data and param_name in data:
        try:
            date_time_param = datetime.datetime.strptime(data[param_name], '%Y-%m-%d %H:%M')
            week_day = get_day(date_time_param, language)
            return date_time_param.strftime('%H:%M %d.%m.%Y') + f" ({week_day})"
        except:
            return f"[{get_label('error', language)}]"

    return f"[{get_label('error', language)}]"


async def resolve_is_defined_time_of_event(reminder_time, chat, chat_id, context, message, prob, is_answer=False):
    if 'is_defined_time_of_event' in reminder_time and bool(
            reminder_time['is_defined_time_of_event']) and define_text_parameter(reminder_time, 'planned_event_start',
                                                                                 5):
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
    keyboard = [[InlineKeyboardButton(get_label('decline_reminders_ask', chat.language),
                                      callback_data=f'decline_reminders_ask_{chat.chat_id}')]]
    return InlineKeyboardMarkup(keyboard)


def bool_val(data, param):
    return param in data and bool(data[param])


"""{
    'is_event': False,
    'is_chat': False,
    'is_appointment': False,
    'is_intention': False,
    'is_reminder': False,
    'is_save': False,
    'is_goal': False
}"""


def define_needs_reminder(prob, json_classif):
    if json_classif["is_reminder"]:
        return True
    if (json_classif["is_event"] or json_classif["is_appointment"]) and (prob == MID_PROB or prob == HIGH_PROB):
        return True
    if json_classif["is_intention"] or json_classif["is_goal"]:
        return False
    if json_classif["is_chat"] or json_classif["is_save"]:
        return False

    return False


def define_sets_goal(prob, json_classif):
    if json_classif["is_intention"] or json_classif["is_goal"]:
        return True

    return False


def define_probably_needs_reminder(prob, json_classif):
    if json_classif["is_save"] or json_classif["is_reminder"]:
        return False
    if (json_classif["is_event"] or json_classif["is_appointment"]) and (prob == LOW_PROB):
        return True
    if json_classif["is_chat"] and (prob == HIGH_PROB):
        return True
    if (json_classif["is_intention"] or json_classif["is_goal"]) and (prob == MID_PROB or prob == HIGH_PROB):
        return True

    return False


def define_needs_save(prob, json_classif):
    return json_classif["is_save"]


async def resolve_main_params(update: Update):
    message = update.message
    print(message)
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id)
    return message, chat_id, chat
