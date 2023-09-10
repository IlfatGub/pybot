#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from aiogram import Bot, Dispatcher, executor
import handlers

print(os.environ['TOKEN'])

API_TOKEN =  os.environ['TOKEN']
 
# создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
 
# регистрируем функции
dp.register_message_handler(handlers.start, commands=["start"])
dp.register_message_handler(handlers.echo)
 
# запускаем программу
if __name__ == '__main__':
# указание skip_updates=True
# пропустит команды,
# которые отправили
# до старта бота
# executor.start_polling(dp, skip_updates=True)