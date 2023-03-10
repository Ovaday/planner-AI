from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from helpers.DatabaseHelpers import async_set_language, async_get_chat, async_get_creator, async_set_approved, \
    async_tick_counter
from helpers.openAIHelper import chatGPT_req
from helpers.translationsHelper import get_label


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    creator = await async_get_creator()
    choice = query.data
    if (choice == 'english' or choice == 'russian'):
        await async_set_language(chat_id, choice)
        await query.edit_message_text(text=f"{get_label('language_is_set', choice)}")
        await context.bot.send_message(chat_id=chat_id, text=get_label('wait_till_approved', choice))

    elif (choice[:7] == 'approve' or choice[:7] == 'decline') and str(creator.chat_id) == str(chat_id):
        chat = await async_get_chat(choice[8:])
        print(chat)
        if choice[:7] == 'approve':
            await async_set_approved(chat.chat_id, True)
            reply_keyboard = [['ChatGPT']]
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="ChatGPT"
            )
            await context.bot.send_message(chat_id=chat.chat_id, text=get_label('account_is_approved', chat.language), reply_markup=reply_markup)
        else:
            await async_set_approved(chat.chat_id, False)
            await context.bot.send_message(chat_id=chat.chat_id, text=get_label('account_is_declined', chat.language))

        await context.bot.send_message(chat_id=creator.chat_id, text=choice[:7] + 'd')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    print(message)
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id)
    creator = await async_get_creator()

    await context.bot.send_message(chat_id=chat_id, text=f"""
    {get_label('start', 'english')}

{get_label('start', 'russian')}
    """)
    print(chat)
    print(chat.is_approved)

    if chat.is_approved == False:
        print('sending msg to creator')
        msg = f"New request from {chat_id}. First Name: {message.chat.first_name}. Username: {message.chat.username}"
        keyboard = [[InlineKeyboardButton("approve", callback_data=f'approve_{chat_id}'),
                     InlineKeyboardButton("decline", callback_data=f'decline_{chat_id}'), ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=creator.chat_id, text=msg, reply_markup=reply_markup)

    msg = f"For now, please select your preferred language: | Пока, выберите предпочитаемый язык:"
    keyboard = [[InlineKeyboardButton("english", callback_data="english"),
                 InlineKeyboardButton("русский", callback_data="russian"), ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=reply_markup)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    print(message)
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id)
    if not chat:
        print('no chat')
        return await start(update, context)
    if not chat.is_approved:
        await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id, text=get_label('wait_till_approved', chat.language))
    else:
        if message.text == 'ChatGPT':
            reply_markup = ReplyKeyboardRemove()
            await context.bot.send_message(chat_id=chat_id, text=get_label('chat_gpt_intro', chat.language), reply_markup=reply_markup)
        else:
            await async_tick_counter(chat_id)
            if len(message.text) > 1000:
                await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id, text=get_label('too_long_msg', chat.language))
            elif len(message.text) < 5:
                await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id, text=get_label('too_short_msg', chat.language))
            else:
                chatgpt_response = chatGPT_req(message.text, chat)
                print(chatgpt_response)
                await context.bot.send_message(chat_id=chat_id, text=chatgpt_response)