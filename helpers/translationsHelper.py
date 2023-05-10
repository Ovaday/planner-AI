import datetime
from typing import Literal

labels = {
    'start':
        {'russian': 'Спасибо за запуск бота. Я проект разработки @plannerAI.',
         'english': 'Thank you for starting the bot. I am a development project of @plannerAI.'},
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
        {
            'russian': 'Запрос не был обработан из-за слишком долгого времени обработки. Попробуйте сократить запрос или попробовать позже.',
            'english': 'The request was not processed because the processing time was too long. Try shortening the request or try again later.'},
    'help':
        {'russian':
             """Данный чат-бот призван улучшить жизнь, оптимизируя все необходимое для организации эффективного планирования и работы в одном месте. Для своей работы бот использует передовые технологии, нейронные сети с ChatGPT и распознавание голоса.

Текущий функционал команд:
/help - получение справки
/start - запрос одобрения и смена языка

Планируемый функционал в следующих релизах:
* Сохранение сообщения
* Добавление напоминаний
* Создание ToDo-листов""",
         'english':
             """This chatbot is designed to improve life by streamlining everything you need to organize efficient scheduling and work in one place. The bot uses advanced technology, neural networks with ChatGPT and voice recognition for its work.

The current functionality of the commands:
/help - getting help
/start - request approval and change the language.

Planned functionality in the next releases:
* Saving a message
* Adding reminders
* Creation of ToDo lists"""},
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
        {
            'russian': 'На основе этого составьте очень короткий совет, который будет отправлен пользователю при установке уведомления. Не нужно писать что нужно поставить напоминание или уведомление. Напишите его на русском языке. Используйте не более 100 слов, чтобы рассказать пользователю, как он может преуспеть в этом.',
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
    'recognized':
        {
            'russian': 'Распознанный текст',
            'english': 'Recognized text'},
    'processing_wait':
        {
            'russian': 'Обрабатываю запрос...',
            'english': 'Processing the request...'},
    'delete':
        {
            'russian': 'Удалить',
            'english': 'Delete'},
    'reminder_request_type':
        {
            'russian': 'напоминания',
            'english': 'a reminder'},
    'goal_request_type':
        {
            'russian': 'цели',
            'english': 'a goal'},
    'appointment_request_type':
        {
            'russian': 'события',
            'english': 'an appointment/event'},
    'save_request_type':
        {
            'russian': 'чего-либо',
            'english': 'a save'},
    'not_released_functionality_request':
        {
            'russian': """Похоже, что вы отправили запрос на добавление/сохранение {request_type}. Прямо сейчас мы не \
поддерживаем такой тип функциональности, но планируем добавить его. ChatGPT ответит на ваше сообщение. Пожалуйста, \
сообщите нам, если это была ошибка. Это улучшит работу бота в ваших будущих запросах.""",
            'english': """It seems that you have send {request_type} request. Right now we \
don't support that type of functionality, but we plan to. ChatGPT will answer to your message. Please, notify us if \
that was an error. That will improve the bot in your future requests."""
        },
    'decline_reminders_ask':
        {
            'russian': 'Отменить уведомления и спросить ChatGPT напрямую',
            'english': 'Decline reminders and ask ChatGPT directly'},
    'ask_to_save':
        {
            'russian': 'Похоже, вы попросили сохранить что-то для вас, однако я пока не могу сохранять вещи. Это будет в будущих обновлениях. Пока я могу только устанавливать напоминания или отвечать на ващи вопросы.',
            'english': 'It sounds like you asked me to save something for you, however, I cant save things yet. That will be in future updates. For now I can only set reminders or answer your questions.'},
    'thank_you_for_error':
        {
            'russian': 'Спасибо что сообщили нам об ошибке! Мы постараемся учесть это в следующих обновлениях. Если это критично, вы можете связаться с создателем бота @plannerAI.',
            'english': 'Thanks for letting us know about the mistake! We will try to address this in our future updates. If this is critical, you can contact the creator of the bot @plannerAI.'},
    'it_was_mistake':
        {
            'russian': 'Сообщить об ошибке',
            'english': 'Report an error'},
    'list_users_balance_command':
        {
            'russian': '/admin_users_balance - возвращает баланс всех пользователей',
            'english': '/admin_users_balance - returns the balance of all users'},
    'user_balance': {
        'russian': 'Ваш баланс',
        'english': 'Your balance is'},
    'all_user_balance': {
        'russian': 'Баланс всех пользователей',
        'english': 'Balance of all users is', }
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
    'event_identified',
    'recognized',
    'processing_wait',
    'not_released_functionality_request',
    'reminder_request_type',
    'goal_request_type',
    'appointment_request_type',
    'save_request_type',
    'thank_you_for_error',
    'it_was_mistake',
    'list_users_balance_command',
    'user_balance',
    'all_user_balance',
]

_LANGUAGE_TYPES = Literal['english', 'russian']


def get_label(name: _TYPES, language: _LANGUAGE_TYPES = "english"):
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
