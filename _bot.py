#! /usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters
def handle_message(update, context):
    message = update.message.text
    if message.lower() == 'привет':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Привет, как дела?')
updater = Updater(token='YOUR_TOKEN_HERE', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()