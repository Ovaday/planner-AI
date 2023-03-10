from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from helpers.DatabaseHelpers import async_set_language, async_get_chat, async_get_creator
from helpers.translationsHelper import get_label


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if (query.data == 'english' or query.data == 'russian'):
        await async_set_language(update.effective_chat.id, query.data)
        await query.edit_message_text(text=f"{get_label('language_is_set', query.data)}")


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

    if not chat.is_approved:
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
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)