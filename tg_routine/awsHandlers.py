import io
import json

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from helpers.localClassifiers import predict_class
from open_ai.requestsHandler import voice_to_text, classify, get_reminder_probability
from helpers.MessageHistoryHelpers import async_insert_response, async_insert_input_message
import soundfile as sf

from tg_routine.handlers import start
from tg_routine.serviceHelpers import *


async def audio_aws(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message, chat_id, chat = await resolve_main_params(update)

    print('process_voice_message')
    mem_file, duration = await process_voice_message(update, context)
    print('processed_voice_message')
    recognized_text = await voice_to_text(chat, mem_file, duration)
    print('recognized_text')
    await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id,
                                   text=f"""{get_label('recognized', chat.language)}: {recognized_text}

{get_label('processing_wait', chat.language)}""")

    json_update = json.loads(update.to_json())
    json_update = audio_json_to_text(json_update, recognized_text)
    print('audio_json_to_text')
    new_update = Update.de_json(json_update, context)
    await chat_gpt_message(new_update, context)


async def process_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_message = await context.bot.get_file(update.message.voice.file_id)
    voice_file = io.BytesIO()
    await voice_message.download_to_memory(voice_file)
    voice_file.seek(0)
    voice_file.name = f'voice_{update.message.chat_id}_{update.message.message_id}.ogg'

    data, samplerate = sf.read(voice_file)
    mem_file = io.BytesIO()
    sf.write(mem_file, data, samplerate, 'PCM_16', format='wav')
    mem_file.seek(0)
    duration = sf.info(mem_file).duration
    mem_file.seek(0)
    mem_file.name = f'voice_{update.message.chat_id}_{update.message.message_id}.wav'
    return mem_file, duration


async def chat_gpt_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('chat_gpt_message')
    message, chat_id, chat = await resolve_main_params(update)
    original_request = message.text.replace('\'', '').replace('\"', '')
    if not chat:
        print('no chat')
        return await start(update, context)
    if not await check_is_chat_approved(chat, context, message):
        return

    else:
        results = await asyncio.gather(get_reminder_probability(chat, message),
                                       classify(chat, message),
                                       predict_class(message))
        print('asyncio.gather executed')
        print(results)
        reminder_probability = results[0]
        openai_classification = results[1]
        local_classification = results[2]
        classification_used = openai_classification

        await async_insert_input_message(message, results)
        #await context.bot.send_message(chat_id=chat_id, text=f'Reminder probability: {reminder_probability}')
        #await context.bot.send_message(chat_id=chat_id, text=f'Local classification: {local_classification}')
        #await context.bot.send_message(chat_id=chat_id, text=openai_classification)

        not_released_functionality_request = get_label('not_released_functionality_request', chat.language)
        keyboard = [[InlineKeyboardButton(get_label('it_was_mistake', chat.language), callback_data=f'error_{chat_id}'),]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if define_needs_reminder(reminder_probability, classification_used):
            request_type_label = get_label('reminder_request_type', chat.language)
            # await set_reminder(message, chat, chat_id, context, reminder_probability)
            msg = not_released_functionality_request.format(request_type=request_type_label)
            await context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=reply_markup)
        elif define_sets_goal(reminder_probability, classification_used):
            request_type_label = get_label('goal_request_type', chat.language)
            msg = not_released_functionality_request.format(request_type=request_type_label)
            await context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=reply_markup)
        elif define_probably_needs_reminder(reminder_probability, classification_used):
            request_type_label = get_label('appointment_request_type', chat.language)
            msg = not_released_functionality_request.format(request_type=request_type_label)
            await context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=reply_markup)
            # await set_reminder_and_answer(message, chat, chat_id, context, reminder_probability)
        elif define_needs_save(reminder_probability, classification_used):
            request_type_label = get_label('save_request_type', chat.language)
            msg = not_released_functionality_request.format(request_type=request_type_label)
            await context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=reply_markup)
            # await context.bot.send_message(chat_id=chat_id, text=get_label('ask_to_save', chat.language))
        #else:
        await ask_chatGPT(message, chat, chat_id, context)
        #    await context.bot.send_message(chat_id=chat_id, text='ask_chatGPT')


async def ask_chatGPT(message, chat, chat_id, context):
    chat_gpt_response, tokens_used = await chatGPT_req(message.text, chat, chat_id, msg_type='normal')
    reply_markup = ReplyKeyboardRemove()
    await context.bot.send_message(chat_id=chat_id, text=chat_gpt_response, reply_markup=reply_markup)
    await async_insert_response(message, chat_gpt_response, tokens_used)
