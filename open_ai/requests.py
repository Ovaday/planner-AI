import openai

from helpers.DatabaseHelpers import async_tick_tokens
from helpers.tokenHelpers import get_token
from open_ai.helpers import fill_classification_template, define_probability


async def classify(tg_chat, message: str):
    openai.api_key = get_token('OPENAI_API')
    ft_classification_model = get_token('FT_CL_MODEL')

    response = openai.Completion.create(model=ft_classification_model, prompt=str(message) + '\n\n###\n\n', max_tokens=2, temperature=0)
    classifier = response['choices'][0]['text']

    await async_tick_tokens(tg_chat.chat_id, response.usage.total_tokens)
    return fill_classification_template(classifier)


async def reminder_probability(tg_chat, message: str):
    openai.api_key = get_token('OPENAI_API')
    ft_reminder_probability_model = get_token('FT_REM_MODEL')

    response = openai.Completion.create(model=ft_reminder_probability_model, prompt=str(message) + '\n\n###\n\n', max_tokens=2, temperature=0)
    classifier = response['choices'][0]['text']

    await async_tick_tokens(tg_chat.chat_id, response.usage.total_tokens)
    return define_probability(classifier)

