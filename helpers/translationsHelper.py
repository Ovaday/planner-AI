import datetime
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
        {'russian': """Напишите любой текст и ответ на него будет написан нейросетью ChatGPT. Если ответ придет на английском, попробуйте специфицировать (Отвечай на русском).
Не смотря на то, что некоторые ответы могут требовать очень содержательного ответа, старайтесь не формулировать их так, чтобы ответы были длиной больше, чем возможная макс. длина сообщения (1 тыс.символов). 
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
    'help':
        {'russian':
             """Данный чат-бот призван улучшить жизнь, оптимизируя все необходимое для организации эффективного планирования и работы в одном месте. Для своей работы бот использует передовые технологии, нейронные сети с ChatGPT и распознавание голоса (в будущем).

Текущий функционал команд:
/help - получение справки
/start - запрос одобрения и смена языка
/my_reminders - мои напоминания""",
         'english':
             """This chatbot is designed to improve life by streamlining everything you need to organize efficient scheduling and work in one place. The bot uses advanced technology, neural networks with ChatGPT and voice recognition (in the future) for its work.

The current functionality of the commands:
/help - getting help
/start - request approval and change the language.
/my_reminders - my reminders"""},
    'no_reminders':
        {'russian': 'У вас пока нет напоминаний.',
         'english': 'There are no reminders yet.'},
    'reminder_word':
        {'russian': 'Напоминание',
         'english': 'Reminder'},
    'due_till':
        {'russian': 'придет',
         'english': 'will be received on'},
    'at':
        {'russian': 'в',
         'english': 'at'},
    'analyze_request':
        {'russian': 'Проанализируй следующий запрос пользователя, для которого установлено напоминание',
         'english': 'Analyze the following users request for which the reminder is set'},
    'analyze_request_requirement':
        {'russian': 'На основе этого составьте очень короткий совет, который будет отправлен пользователю при установке уведомления. Не нужно писать что нужно поставить напоминание или уведомление. Напишите его на русском языке. Используйте не более 100 слов, чтобы рассказать пользователю, как он может преуспеть в этом.',
         'english': 'Based on that provide very short advice that will be sent to the user. Use max 100 words to tell user how he can succeed in that.'},
    'event_identified':
        {
            'russian': 'Я определил это как событие, которое произойдет',
            'english': 'I have defined it as an event that will happen on'},
    'reminder_will_be_set':
        {
            'russian': 'Будут установлено напоминание на',
            'english': 'There will be reminder set to'},
    'with_a_probability':
        {
            'russian': 'и с вероятностью',
            'english': 'and with a probability'},
    'it_needs_a_reminder':
        {
            'russian': 'ему нужно уведомление',
            'english': 'it needs a reminder'},
    'additional_answer_chat_gpt':
        {
            'russian': 'Также последуюет обычный ответ ChatGPT',
            'english': 'In addition, there will follow normal answer of ChatGPT'},
    'additional_reminder_will_be_set':
        {
            'russian': 'Кроме того, ещё одно уведомление придет',
            'english': 'In addition, there is one more reminder will be set to'},
    'error':
        {
            'russian': 'Ошибка',
            'english': 'Error'},
    'based_on_your_message':
        {
            'russian': 'на основе вашего сообщения',
            'english': 'based on your text'},
    'edit_time':
        {
            'russian': 'Изменить время',
            'english': 'Change time'},
    'delete':
        {
            'russian': 'Удалить',
            'english': 'Delete'},
    'decline_reminders_ask':
        {
            'russian': 'Отменить уведомления и спросить ChatGPT напрямую',
            'english': 'Decline reminders and ask ChatGPT directly'},
    'ask_to_save':
        {
            'russian': 'Похоже, вы попросили сохранить что-то для вас, однако я пока не могу сохранять вещи. Это будет в будущих обновлениях. Пока я могу только устанавливать напоминания или отвечать на ващи вопросы.',
            'english': 'It sounds like you asked me to save something for you, however, I cant save things yet. That will be in future updates. For now I can only set reminders or answer your questions.'},

}


_TYPES = Literal[
    'ask_to_save',
    'additional_answer_chat_gpt',
    'with_a_probability',
    'it_needs_a_reminder',
    'decline_reminders_ask',
    'edit_time',
    'delete',
    'based_on_your_message',
    'error',
    'additional_reminder_will_be_set',
    'reminder_will_be_set',
    'event_identified',
    'start',
    'language_is_set',
    'wait_till_approved',
    'chat_gpt_intro',
    'too_long_msg',
    'too_short_msg',
    'account_is_approved',
    'account_is_declined',
    'response_cut',
    'timeout',
    'help',
    'no_reminders',
    'reminder_word',
    'due_till',
    'at',
    'analyze_request',
    'analyze_request_requirement',
    'event_identified'
]

_LANGUAGE_TYPES = Literal['english', 'russian']

def get_label(name: _TYPES, language: _LANGUAGE_TYPES):
    return labels.get(name).get(language)

week_labels = {
    'Monday':
        {'russian': 'Понедельник',
         'english': 'Monday'},
    'Tuesday':
        {'russian': 'Вторник',
         'english': 'Tuesday'},
    'Wednesday':
        {'russian': 'Среда',
         'english': 'Wednesday'},
    'Thursday':
        {'russian': 'Четверг',
         'english': 'Thursday'},
    'Friday':
        {'russian': 'Пятница',
         'english': 'Friday'},
    'Saturday':
        {'russian': 'Суббота',
         'english': 'Saturday'},
    'Sunday':
        {'russian': 'Воскресенье',
         'english': 'Sunday'},
    'Today':
        {'russian': 'Сегодня',
         'english': 'Today'},
    'Tomorrow':
        {'russian': 'Завтра',
         'english': 'Tomorrow'},

}

def get_day(datetime, language):
    day_index = datetime.weekday()
    day_name = DAYS[day_index]
    if day_name == get_current_day():
        day_name = 'Today'
    elif day_name == get_tomorrow_day():
        day_name = 'Tomorrow'
    return week_labels.get(day_name).get(language)

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
def get_current_day():
    now = datetime.datetime.now()
    day_index = now.weekday()
    return DAYS[day_index]

def get_tomorrow_day():
    now = datetime.datetime.now()
    day_index = now.weekday()
    tomorrow_index = (day_index + 1) % 7
    return DAYS[tomorrow_index]