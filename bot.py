#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from aiogram import Bot, Dispatcher, executor, types
bot = Bot(token=os.environ["BOTKEY"])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем. 
async def send_welcome(message: types.Message):
   await message.reply("Привет!\nЯ Эхо-бот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.") #Так как код работает асинхронно, то обязательно пишем await.

@dp.message_handler() #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
   await message.answer(message.text)

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
   
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#   if message.text == "Привет":
#     bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#   elif message.text == "/help":
#     bot.send_message(message.from_user.id, "Напиши привет")
#   else:
#     bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


