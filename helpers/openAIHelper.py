import openai

from helpers.DatabaseHelpers import async_tick_tokens
from helpers.tokenHelpers import get_token
from helpers.translationsHelper import get_label


async def chatGPT_req(message, tg_chat):
    words_limit = 200
    print(message)
    if len(message) < 5:
        return None
    openai.api_key = get_token('OPENAI_API')
    system_content = f"Use max limit of {words_limit} words. Preferred language: {tg_chat.language}"
    if tg_chat.role == 'admin':
        system_content = f"Use max limit of {words_limit} words"
    chatgpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=words_limit,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": message}
        ]
    )

    await async_tick_tokens(tg_chat.chat_id, chatgpt_response.usage.total_tokens)
    return parse_response(chatgpt_response, tg_chat, words_limit)


def parse_response(response, tg_chat, words_limit):
    if not response:
        return None
    print(f"Response: {response}")

    message = response.choices[0].message.content
    print(f"Message: {message}")
    if response.usage.completion_tokens == words_limit:
        return message + f" [{get_label('response_cut', tg_chat.language)}]"
    else:
        return message
