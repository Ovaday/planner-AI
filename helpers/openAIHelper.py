import json
import re

import openai

from helpers.DatabaseHelpers import async_tick_tokens
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


async def chatGPT_req(message, tg_chat, type: _TYPES, model='gpt-3.5-turbo', initial_text=''):
    if not type:
        type = 'normal'
    words_limit = 300
    if type == 'normal':
        words_limit = 1000
    print(message)
    if len(message) < 5:
        return None
    examples = {}
    openai.api_key = get_token('OPENAI_API')
    system_content = f"Use max limit of {words_limit} words. Preferred language: {tg_chat.language}"
    if tg_chat.role == 'admin':
        system_content = f"Use max limit of {words_limit} words"
    elif type == 'reminder_classification':
        system_content = f"""Important: Provide ONLY the requested form in the output and no other text!!!"""
        examples = {"role": "system", "content": f"""
    You are a Planner AI tool that defines if the send information requires placing into the calender and further notification.
        Examples:
    * Джобцентр в пятницу к 11:20 - 10
    * Remind me please to go to gym tomorrow - 10
    * Что ты такое? - 0
    * Напомни вытащить курицу из духовки - 10
    * Надо бы записаться в спортзал - 6
    * Сколько будет 2 плюс 2? - 0"""}
    elif type == 'advanced_classification_request':
        system_content = f"""Important: Provide ONLY the requested form in the output and no other text!!!"""
        examples = {"role": "system", "content": f"""
    You are a Planner AI tool that defines if the send information requires placing into the calender and further notification.
        Examples:
    * Джобцентр в пятницу к 11:20 - is_appointment:true
    * Remind me please to go to gym tomorrow - is_reminder_request:true
    * Что ты такое? - is_question:true
    * Напомни вытащить курицу из духовки - is_reminder_request:true
    * Надо бы записаться в спортзал - is_intention:true
    * Сколько будет 2 плюс 2? - is_question:true"""}
    elif type == 'advice_for_reminder':
        system_content = f"""You are writing an advice for the reminder based on the text. Use max 100 words. Output language: {tg_chat.language}"""
    elif type == 'reminder_time':
        system_content = f"""Important: Provide ONLY the requested form in the output and no other text!!!"""

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": message}
    ]
    if examples and len(examples) > 0:
        messages.append(examples)
    chatgpt_response = openai.ChatCompletion.create(
        model=model,
        max_tokens=words_limit,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": message}
        ]
    )

    await async_tick_tokens(tg_chat.chat_id, chatgpt_response.usage.total_tokens)
    return parse_response(chatgpt_response, tg_chat, words_limit, type, initial_text)


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
