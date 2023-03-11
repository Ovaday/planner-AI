from typing import Literal
labels = {
    'start':
        {'russian': 'Спасибо за запуск бота. Я проект разработки @Ovaday.',
         'english': 'Thank you for starting the bot. I am a development project of @Ovaday.'},
    'language_is_set':
        {'russian': 'Установлен русский язык. Для сброса введите /start',
         'english': 'English language is set. To reset, call /start'},
    'wait_till_approved':
        {'russian': 'Подождите одобрения',
         'english': 'Please wait till you are approved'},
    'chat_gpt_intro':
        {'russian': """Напишите любой текст и ответ на него будет написан нейросетью ChatGPT. Если ответ придет на английском, попробуйте специфицировать (Отвечай на русском). Не смотря на то, что некоторые ответы могут требовать очень содержательного ответа, старайтесь не формулировать их так, чтобы ответы были длиной больше, чем возможная макс. длина сообщения (1 тыс.символов). 
Примеры:
        'Привет'
        'Что ты такое?'
        'В чем различие между профилем и анфасом?'""",
         'english': 'Write any text and the answer will be written by the ChatGPT neural network. If the answer comes in English, try specifying (Answer in Russian). Despite the fact that some answers may require a very meaningful response, try not to formulate them so that the answers are longer than the possible maximum length of the message (1 thousand characters).'},
    'too_long_msg':
        {'russian': 'Ошибка: Сообщение слишком длинное.',
         'english': 'Error: Message is too long.'},
    'too_short_msg':
        {'russian': 'Ошибка: Сообщение слишком короткое.',
         'english': 'Error: Message is too short.'},
    'account_is_approved':
        {'russian': 'Аккаунт подтвержден.',
         'english': 'Your account is approved.'},
    'account_is_declined':
        {'russian': 'В регистрации отказано.',
         'english': 'Your account request is declined.'},
    'response_cut':
        {'russian': 'Сообщение обрезано.',
         'english': 'Response message is cut.'},
    'timeout':
        {'russian': 'Запрос не был обработан из-за слишком долгого времени обработки. Попробуйте сократить запрос или попробовать позже.',
         'english': 'The request was not processed because the processing time was too long. Try shortening the request or try again later.'},
}

_TYPES = Literal[
    'start',
    'language_is_set',
    'wait_till_approved',
    'chat_gpt_intro',
    'too_long_msg',
    'too_short_msg',
    'account_is_approved',
    'account_is_declined',
    'response_cut',
    'timeout'
]

_LANGUAGE_TYPES = Literal['english', 'russian']

def get_label(name: _TYPES, language: _LANGUAGE_TYPES):
    return labels.get(name).get(language)