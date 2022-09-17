import skimage, skimage.io
from io import BytesIO
import responses as resp
import api_key as key
from telegram import ForceReply, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, Filters, Updater, CallbackContext
from image_process import chromashift
import numpy as np
import cv2

print("Bot started...")


def start_command(update, context):
    update.message.reply_text("Type something random to get started.")


def help_command(update, context):
    update.message.reply_text("I can't even help myself.")


def handle_message(update, context):
    text = str(update.message.text).lower()  # receives text from user
    response = resp.sample_responses(text)  # processes text from user

    update.message.reply_text(response)  # gives back response to user


# def get_url():
# contents = requests.get('https://random.dog/woof.json').json()
# url = contents['url']
# return url

# def bop_command(update, context):
# file = context.bot.get_file(update.message.photo[-1].file_id)
# f = BytesIO(file.download_as_bytearray())
# f = skimage.io.imread(f)
# url = get_url()
# chat_id = update.message.chat_id
# update.message.send_photo(chat_id=chat_id, photo=url)


def handle_photo(update: Update, context: CallbackContext):
    file = context.bot.get_file(update.message.photo[-1].file_id)
    f = BytesIO(file.download_as_bytearray())
    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    result = chromashift(image)
    is_success, buffer = cv2.imencode(".png",result)
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
    # dp.add_handler(CommandHandler("bop", bop_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle


lookabot()
