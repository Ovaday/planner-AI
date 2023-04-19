from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from helpers.DatabaseHelpers import async_get_chat
from helpers.translationsHelper import get_day
from tg_routine.templates import *


async def check_is_chat_approved(chat, context, message):
    if not chat.is_approved:
        await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat.chat_id,
                                       text=get_label('wait_till_approved', chat.language))
        return False
    return True


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


async def resolve_main_params(update: Update):
    message = update.message
    print(message)
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id, update)
    return message, chat_id, chat
