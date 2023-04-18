import asyncio

from helpers.ReleaseHelpers import release_handler
from helpers.openAIHelper import chatGPT_req_test
from tg_routine.main import aws_tg_message_handler


def task_receiver(update_json, *args, **kwargs):
    print(update_json)
    print(type(update_json))

    kwargs = kwargs['kwargs']
    if kwargs and 'type' in kwargs:
        if kwargs['type'] == 'tg_message':
            aws_tg_message_handler(update_json)
        elif kwargs['type'] == 'release' and 'version' in kwargs:
            release_handler(kwargs['version'])

def async_call_receiver(message, *args, **kwargs):
    print(message)
    kwargs = kwargs['kwargs']
    tg_chat = None if not 'tg_chat' in kwargs else kwargs['tg_chat']
    type = None if not 'type' in kwargs else kwargs['type']
    model = None if not 'model' in kwargs else kwargs['model']
    initial_text = None if not 'initial_text' in kwargs else kwargs['initial_text']
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print('set_event_loop')
        return asyncio.get_event_loop().run_until_complete(
            chatGPT_req_test(message, tg_chat, type, model, initial_text))
    except Exception as e:
        print('run with exception')
        print(e)
        return asyncio.get_event_loop().run_until_complete(
            chatGPT_req_test(message, tg_chat, type, model, initial_text))
