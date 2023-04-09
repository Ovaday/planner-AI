GPT_request_classification_template = {
    'is_event': False,
    'is_chat': False,
    'is_appointment': False,
    'is_intention': False,
    'is_reminder': False,
    'is_save': False,
    'is_calender': False,
    'is_goal': False
}


def fill_classif_template(response: str):
    template = GPT_request_classification_template.copy()
    template[define_class(response)] = True
    return template


def define_class(response: str):
    if len(response) < 3:
        return 'is_chat'

    if 'cal' in response:
        return 'is_calender'
    elif 'chat' in response:
        return 'is_chat'
    elif 'goal' in response:
        return 'is_goal'
    elif 'sav' in response:
        return 'is_save'
    elif 'remind' in response:
        return 'is_reminder'
    elif 'intent' in response:
        return 'is_intention'
    elif 'appoi' in response:
        return 'is_appointment'
    elif 'event' in response:
        return 'is_event'
    else:
        return 'is_chat'
