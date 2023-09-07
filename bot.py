#! /usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram import ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, RegexHandler, ConversationHandler
import logging
import subprocess 
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ['TOKEN']

# def start(bot, update):
#     update.message.reply_text(
#         'This is personal bot of Andrey Useinov.\n'
#         'Send /help for more information about commands.')
                                                             
# updater = Updater(api_key)
# dp = updater.dispatcher
# dp.add_handler(CommandHandler("start", start)) 

# def echo(bot, update):
#     update.message.reply_text(update.message.text) 

# dp.add_handler(MessageHandler(Filters.text, echo))  