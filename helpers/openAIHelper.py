import openai
from helpers.tokenHelpers import get_token


def chatGPT_req(message):
    print(message)
    if len(message) < 7:
        return None
    openai.api_key = get_token('OPENAI_API')
    chatgpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            #{"role": "system", "content": "You are a helpful assistant."},
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
