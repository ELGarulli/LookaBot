from functools import partial
from io import BytesIO
from uuid import uuid4

import cv2
import numpy as np
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackContext, PicklePersistence

import api_key as key
import responses as resp
from const import color_blindness
from image_process import lookap


print("Bot started...")


def start_command(update, context):
    buttons = [[KeyboardButton("Deuteranopia")], [KeyboardButton("Protanopia")], [KeyboardButton("Tritanopia")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your type of colorblindness",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def help_command(update, context):
    update.message.reply_text("I can't even help myself.")


def handle_message(update, context, key_):
    text = str(update.message.text).lower()
    response = resp.sample_responses(text)
    if response in ("t", "d", "p"):
        context.user_data[key_] = response
        update.message.reply_text("Ok! I set your preference to " + color_blindness[response])
    else:
        update.message.reply_text(response)


def handle_photo(update: Update, context: CallbackContext, key_):
    defect = context.user_data[key_]
    file = context.bot.get_file(update.message.photo[-1].file_id)
    f = BytesIO(file.download_as_bytearray())

    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    rgb = np.asarray(im, dtype=float)

    result = lookap(rgb, defect)
    result = np.flip(result, 2)
    is_success, buffer = cv2.imencode(".png", result)
    bytes_im = buffer.tobytes()
    context.bot.send_photo(chat_id=update.message.chat_id, photo=bytes_im)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def lookabot():
    updater = Updater(key.API_KEY, persistence=PicklePersistence(filename='user_data'), use_context=True)
    dp = updater.dispatcher

    key_ = str(uuid4())
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, partial(handle_message, key_=key_)))
    dp.add_handler(MessageHandler(Filters.photo, partial(handle_photo, key_=key_)))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle


lookabot()
