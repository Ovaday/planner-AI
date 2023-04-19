import datetime
import json
import re

import openai

from helpers.DatabaseHelpers import async_tick_expenses
from helpers.MessageHistoryHelpers import async_get_last_user_messages
from helpers.tokenHelpers import get_token
from helpers.translationsHelper import get_label
from typing import Literal

_TYPES = Literal[
    'normal',
    'reminder_classification',
    'advice_for_reminder',
    'reminder_time',
    'advanced_classification_request'
]


async def chatGPT_req_test(message, tg_chat, type, model='gpt-3.5-turbo', initial_text=''):
    print(message)
    print(tg_chat)
    print(type)
    print(model)
    return message


async def chatGPT_req(message, tg_chat, chat_id, msg_type: _TYPES, model='gpt-3.5-turbo', initial_text=''):
    if not msg_type:
        msg_type = 'normal'
    words_limit = 300
    if msg_type == 'normal':
        words_limit = 2000
    print(message)
    if len(message) < 5:
        return None
    examples = {}
    messages = []
    temperature = 1
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%A, %B %d, %Y %H:%M:%S")

    openai.api_key = get_token('OPENAI_API')
    system_content = f"Pref. lang.: {tg_chat.language}. Current date: {formatted_datetime}."
    if msg_type == 'advice_for_reminder':
        system_content = f"""You are writing an advice for the reminder based on the text. Use max 100 words. Output language: {tg_chat.language}"""
        temperature = 0.7
    elif msg_type == 'reminder_classification' or msg_type == 'advanced_classification_request':
        temperature = 0.1

    elif msg_type == 'reminder_time':
        system_content = f"""Important: Provide ONLY the requested form in the output and no other text!!!"""
        temperature = 0.1

    elif msg_type == 'normal':
        last_messages = await async_get_last_user_messages(chat_id)
        print(last_messages)
        messages = [{"role": "system", "content": system_content}]
        if len(last_messages) > 2:
            if last_messages[2]['response_raw'] and len(last_messages[2]['response_raw']):
                grand_prev_response = str_return_first_n(last_messages[2]['response_raw'])
                messages.append({"role": "assistant", "content": grand_prev_response})
        if len(last_messages) > 1:
            prev_message = str_return_first_n(last_messages[1]['message_raw'])
            messages.append({"role": "user", "content": prev_message})
            if last_messages[1]['response_raw'] and len(last_messages[1]['response_raw']):
                prev_response = str_return_first_n(last_messages[1]['response_raw'])
                messages.append({"role": "assistant", "content": prev_response})
        messages.append({"role": "user", "content": message})

    if len(messages) == 0:
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": message},
        ]

    if len(examples) > 0:
        messages.append(examples)

    print(messages)
    chatgpt_response = openai.ChatCompletion.create(
        model=model,
        max_tokens=words_limit,
        messages=messages
    )

    await async_tick_expenses(tg_chat.chat_id, chatgpt_response.usage.total_tokens, model)
    return parse_response(chatgpt_response, tg_chat, words_limit, msg_type,
                          initial_text), chatgpt_response.usage.total_tokens


def parse_response(response, tg_chat, words_limit, type, initial_text):
    if not response:
        return None
    print(f"Response: {response}")

    message = response.choices[0].message.content
    print(f"Message: {message}")
    if type == 'reminder_classification':
        return parse_reminder_probability(message)
    elif type == 'reminder_time' or type == 'advanced_classification_request':
        return parse_json(message)
    elif response.usage.completion_tokens == words_limit:
        return message + f" [{get_label('response_cut', tg_chat.language)}]"
    else:
        return message


def parse_reminder_probability(text):
    return_val = parse_json(text)
    if 'reminder_probability' in return_val:
        return int(return_val['reminder_probability'])
    elif 'should_place_reminder' in return_val:
        if bool(return_val['should_place_reminder']):
            return 9
        return 1
    else:
        return 5


def parse_json(text):
    pattern = r"{.*}"
    json_dict = {}
    text = "{" + text.split("{", 1)[1]  # remove the text before the JSON
    text = text.split("}", 1)[0] + "}"  # remove the text after the JSON
    text = text.replace("\'", "\"")
    text = replace_bools(text)
    print(text)
    print(type(text))
    try:
        return json.loads(text)
    except Exception as e:
        print(e)

    matches = re.findall(pattern, text)
    print(matches)
    if len(matches) > 0:
        json_dict = json.loads(matches[0])
        print(json_dict)
    return json_dict


def replace_bools(text):
    return text.replace('True', 'true').replace('False', 'false')


def str_return_first_n(string, length=300):
    if len(string) > length:
        string = string[:length] + '[too big text cutted to save tokens]'
    return string


"""elif type == 'reminder_classification':
        system_content = f"Important: Provide ONLY the requested form in the output and no other text!!!"
        examples = {"role": "system", "content": f"
    You are a Planner AI tool that defines if the send information requires placing into the calender and further notification.
        Examples:
    * Джобцентр в пятницу к 11:20 - 10
    * Remind me please to go to gym tomorrow - 10
    * Что ты такое? - 0
    * Напомни вытащить курицу из духовки - 10
    * Надо бы записаться в спортзал - 6
    * Сколько будет 2 плюс 2? - 0"}

    elif type == 'advanced_classification_request':
        system_content = f"Important: Provide ONLY the requested form in the output and no other text!!!"
        examples = {"role": "system", "content": f"
    You are a Planner AI tool that defines if the send information requires placing into the calender and further notification.
        Examples:
    * Джобцентр в пятницу к 11:20 - is_appointment:true
    * Remind me please to go to gym tomorrow - is_reminder_request:true
    * Что ты такое? - is_question:true
    * Напомни вытащить курицу из духовки - is_reminder_request:true
    * Надо бы записаться в спортзал - is_intention:true
    * Сколько будет 2 плюс 2? - is_question:true"}"""
