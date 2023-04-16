import datetime

from helpers.translationsHelper import get_label, get_current_day

my_event_template = {'update_id': 'TO_FILL',
                     'message': {'message_id': 'TO_FILL',
                                 'from': {'id': 'TO_FILL', 'is_bot': False,
                                          'first_name': 'TO_FILL',
                                          'last_name': 'TO_FILL', 'language_code': 'TO_FILL'},
                                 'chat': {'id': 'TO_FILL',
                                          'first_name': 'TO_FILL', 'last_name': 'TO_FILL',
                                          'type': 'private'}, 'date': 0,
                                 'text': 'TO_FILL',
                                 'entities': [
                                     {'offset': 0, 'length': 0, 'type': 'bot_command'}]}}
def current_datetime():
    return datetime.datetime.timestamp(datetime.datetime.now())  # datetime format

def fill_template(from_id, text, type='bot_command', update_id='9999999', message_id='99999', first_name='first_name', last_name='last_name', language_code='en', date=current_datetime()):
    template = my_event_template
    template['update_id'] = update_id
    template['message']['message_id'] = message_id

    template['message']['from']['id'] = from_id
    template['message']['from']['first_name'] = first_name
    template['message']['from']['last_name'] = last_name
    template['message']['from']['language_code'] = language_code

    template['message']['chat']['id'] = from_id
    template['message']['chat']['first_name'] = first_name
    template['message']['chat']['last_name'] = last_name

    template['message']['date'] = int(date)
    template['message']['text'] = text

    template['message']['entities'][0]['length'] = len(text)
    template['message']['entities'][0]['type'] = type
    return template

GPT_reminder_template = {
    'seconds_difference': 0,
    'minutes_difference': 0,
    'hours_difference': 0,
    'days_difference': 0,
    'month_difference': 0,
    'years_difference': 0,

    'reminder_text': ''
}
GPT_seconds_reminder_template = {
    'is_defined_time_of_event': 'true/false',
    'planned_event_start': 'YYYY-MM-DD HH:MM',
    'probable_length_of_event_in_seconds': 0,
    'difference_in_seconds_between_now_and_event_moment': 0,
    'when_is_better_to_remind': 'YYYY-MM-DD HH:MM',
    'additional_reminder': 'YYYY-MM-DD HH:MM',
}

GPT_reminder_probability_template = {
    'reminder_probability': 0,
    'should_place_reminder': 'true/false'
}

def fill_reminder_template(request):
    GPT_request_reminder_template = f"""
    Please transform the following request for the future event:
    {request}
    To the output in the following form:
    {GPT_seconds_reminder_template}
    
    In the field when_is_better_to_remind place assumption at which time and date better to remind the person in advance. If there is two reminders needed, place second in field additional_reminder.
    In the probable_length_of_event_in_seconds predict how long the event will take.
    Don't place None to any field, fill every of them.
    Current time is:
    {datetime.datetime.now()}
    Current day:
    {get_current_day()}
    
    In the output provide only the form and no other text.
    """
    return GPT_request_reminder_template


def fill_classification_request(request):
    GPT_request_template = f"""
    You are a Planner AI tool that defines if the received information requires placing into the calender and further notification. Analyze the following text:
    {request}
    To the output in the following form:
    {GPT_reminder_probability_template}
    If there is user intention to do something or he explicitly asks to notify him, or there is a date and time, or it is an event/action/appointment, then the probability in json field reminder_probability should be high.
    If it is just a general or specific question to do another things, then the probability is low.
    Define if this text requires the notification-reminder for the user or not and place as a boolean to json field should_place_reminder. 
    Important: the result send ONLY AS A FILLED FORM with probability from 0 to 10.
    """
    return GPT_request_template

def fill_reminder_advice_request(request, language):
    GPT_advice_template = f"""
        {get_label('analyze_request', language)}:
        {request}
        {get_label('analyze_request_requirement', language)}.
        """
    return GPT_advice_template

GPT_request_classification_template = {
    'is_event': 'true/false',
    'is_question': 'true/false',
    'is_appointment': 'true/false',
    'is_intention': 'true/false',
    'is_reminder_request': 'true/false',
    'is_save_request': 'true/false',
    'none_of_the_above': 'true/false'
}


def fill_advanced_classification_request(request):
    GPT_request_template = f"""
    You are a Planner AI tool that receives an input from the user:
    {request}
    And you should define what is the reason of this request. Fill the following form:
    {GPT_request_classification_template}
    In the json form different can be 'true' value, but except the none_of_the_above. Use that field only if none of others met. As output, provide ONLY the json form.
    
    Place is_event:true if there there is a date or time, or it is a planned event/action.
    Place is_question:true if there is a general question knowledge like the google search request.
    Place is_appointment:true if there there is a date or time, or it is an appointment.
    Place is_intention:true if there there is a users intention to do something in the future.
    Place is_reminder_request:true if there there is a request from the user to remind him about something.
    Place is_save_request:true if there there is a request from the user to save something for him for the future.
    Place none_of_the_above:true if there none of the above fields can be evaluated to true.
    """
    return GPT_request_template