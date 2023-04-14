GPT_request_classification_template = {
    'is_event': False,
    'is_chat': False,
    'is_appointment': False,
    'is_intention': False,
    'is_reminder': False,
    'is_save': False,
    'is_goal': False
}

HIGH_PROB = 'high'
MID_PROB = 'mid'
LOW_PROB = 'low'


def fill_classification_template(response: str):
    template = GPT_request_classification_template.copy()
    template[define_class(response)] = True
    return template


def define_probability(response: str):
    if len(response) < 3:
        return LOW_PROB

    if 'high' in response:
        return HIGH_PROB
    elif 'mid' in response:
        return MID_PROB
    else:
        return LOW_PROB


def define_class(response: str):
    if len(response) < 3:
        return 'is_chat'

    if 'chat' in response:
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
