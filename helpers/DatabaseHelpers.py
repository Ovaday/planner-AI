from asgiref.sync import sync_to_async

from tg_bot.models import Chat


def get_chat(chat_id):
    chat = Chat.objects.filter(chat_id=chat_id)
    print('chat')
    print(chat)
    if not chat or len(chat) < 1:
        print('no chat')
        chat = {
            "chat_id": chat_id,
            "counter": 0
        }
        response = Chat.objects.create(
            chat_id=chat['chat_id'],
            counter=chat['counter'],
            is_approved=False,
        )
        print(response)
        chat = response
    else:
        chat = chat.first()
    return chat


def get_creator():
    return Chat.objects.get(pk=1)


def set_language(chat_id, language):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.language = language
    chat.save()


def set_approved(chat_id, option: bool):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.is_approved = option
    chat.save()


def tick_counter(chat_id):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.counter += 1
    chat.save()


def tick_tokens(chat_id, tokens: int):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.tokens_used += tokens
    chat.save()


def tick_expenses(chat_id, tokens, model: str, is_classification=False):
    chat = Chat.objects.get(chat_id=chat_id)

    if "whisper-1" in model:
        chat.expenses += 0.006 * tokens / 60
    elif "ada" in model:
        if is_classification:
            chat.expenses += 0.0016 * tokens / 1000
        else:
            chat.expenses += 0.0004 * tokens / 1000
    elif "babbage" in model:
        if is_classification:
            chat.expenses += 0.0024 * tokens / 1000
        else:
            chat.expenses += 0.0005 * tokens / 1000
    elif "davinci" in model:
        chat.expenses += 0.02 * tokens / 1000
    else:
        chat.expenses += 0.002 * tokens / 1000
    chat.save()


def assign_last_conversation(chat_id, conversation):
    chat = Chat.objects.get(chat_id=chat_id)
    chat.last_conversation = conversation
    chat.save()


async_get_chat = sync_to_async(get_chat)
async_get_creator = sync_to_async(get_creator)
async_set_language = sync_to_async(set_language)
async_set_approved = sync_to_async(set_approved)
async_tick_counter = sync_to_async(tick_counter)
async_tick_tokens = sync_to_async(tick_tokens)
async_tick_expenses = sync_to_async(tick_expenses)
async_assign_last_conversation = sync_to_async(assign_last_conversation)