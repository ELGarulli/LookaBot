import skimage, skimage.io
from io import BytesIO
import responses as resp
import api_key as key
from telegram import ForceReply, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, Filters, Updater, CallbackContext
from image_process import test_pipeline
import numpy as np
import cv2
from PIL import Image

print("Bot started...")


def start_command(update, context):
    #update.message.reply_text("Type something random to get started.")
    buttons = [[KeyboardButton("Deuteranopia")], [KeyboardButton("Protanopia")], [KeyboardButton("Tritanopia")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your type of colorblindness",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def help_command(update, context):
    update.message.reply_text("I can't even help myself.")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = resp.sample_responses(text)

    update.message.reply_text(response)



def handle_photo(update: Update, context: CallbackContext):
    file = context.bot.get_file(update.message.photo[-1].file_id)
    f = BytesIO(file.download_as_bytearray())
    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    convert_rgb = Image.fromarray(image, mode="RGB")
    rgb = np.asarray(convert_rgb, dtype=float)
    result = test_pipeline(rgb)

    is_success, buffer = cv2.imencode(".png", result)
    bytes_im = buffer.tobytes()
    # context.bot.send_message(chat_id=update.message.chat_id, text=result.shape)
    # context.bot.send_message(chat_id=update.message.chat_id, text=result)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=bytes_im)
    # update.message.reply_photo(result)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def lookabot():
    updater = Updater(key.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle


lookabot()
