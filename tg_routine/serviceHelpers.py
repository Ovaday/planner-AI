from helpers.translationsHelper import get_label


async def check_is_chat_approved(chat, context, message):
    if not chat.is_approved:
        await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat.chat_id,
                                       text=get_label('wait_till_approved', chat.language))
        return False
    return True
