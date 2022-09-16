import logging
from telegram import ForceReply, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, Filters, Updater

import responses as resp
import api_key as key

print("Bot started...")


def start_command(update, context):
    update.message.reply_text("Type something random to get started.")


def help_command(update, context):
    update.message.reply_text("I can't even help myself.")


def handle_message(update, context):
    text = str(update.message.text).lower()     # receives text from user
    response = resp.sample_responses(text)      # processes text from user

    update.message.reply_text(response)         # gives back response to user


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(key.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle


main()