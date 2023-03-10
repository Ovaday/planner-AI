from typing import Literal
labels = {
    'start':
        {'russian': 'Спасибо за запуск бота. Я проект разработки @Ovaday.',
         'english': 'Thank you for starting the bot. I am a development project of @Ovaday.'},
    'language_is_set':
        {'russian': 'Установлен русский язык. Для сброса введите /start',
         'english': 'English language is set. To reset, call /start'},
}


_TYPES = Literal[labels.keys()]
_LANGUAGE_TYPES = Literal['english', 'russian']

def get_label(name: _TYPES, language: _LANGUAGE_TYPES):
    return labels.get(name).get(language)