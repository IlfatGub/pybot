#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from telegram import Updater         # пакет называется python-telegram-bot, но Python-
from telegram.ext import CommandHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯

def start(bot, update):
    # подробнее об объекте update: https://core.telegram.org/bots/api#update
    bot.sendMessage(chat_id=update.message.chat_id, text="Здравствуйте.")

updater = Updater(token='TOKEN')  # тут токен, который выдал вам Ботский Отец!

start_handler = CommandHandler('start', start)  # этот обработчик реагирует
                                                # только на команду /start

updater.dispatcher.add_handler(start_handler)   # регистрируем в госреестре обработчиков
updater.start_polling()  # поехали!



print(os.environ['TOKEN'])

# def handle_message(update, context):
#     message = update.message.text
#     if message.lower() == 'привет':
#         context.bot.send_message(chat_id=update.effective_chat.id, text='Привет, как дела?')
# updater = Updater(token='YOUR_TOKEN_HERE', use_context=True)
# dispatcher = updater.dispatcher
# dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
# updater.start_polling()