import openai
from helpers.tokenHelpers import get_token
from helpers import fill_classif_template, define_probability


def classify(message: str):
    openai.api_key = get_token('OPENAI_API')
    ft_classification_model = get_token('FT_CL_MODEL')

    response = openai.Completion.create(model=ft_classification_model, prompt=str(message) + '\n\n###\n\n', max_tokens=2, temperature=0)
    classifier = response['choices'][0]['text']
    return fill_classif_template(classifier)


def reminder_probability(message: str):
    openai.api_key = get_token('OPENAI_API')
    ft_reminder_probability_model = get_token('FT_REM_MODEL')

    response = openai.Completion.create(model=ft_reminder_probability_model, prompt=str(message) + '\n\n###\n\n', max_tokens=2, temperature=0)
    classifier = response['choices'][0]['text']
    return define_probability(classifier)

