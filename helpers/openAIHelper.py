import openai
from helpers.tokenHelpers import get_token


def chatGPT_req(message, tg_chat):
    print(message)
    if len(message) < 7:
        return None
    openai.api_key = get_token('OPENAI_API')
    system_content = f"For the answer, use max limit of 200 words. Preferred language: {tg_chat.language}"
    if tg_chat.role == 'admin':
        system_content = f"For the answer, use max limit of 200 words"
    chatgpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": message}
        ]
    )
    return parse_response(chatgpt_response)


def parse_response(response):
    if not response:
        return None
    print(f"Response: {response}")

    message = response.choices[0].message.content
    print(f"Message: {message}")
    return message
