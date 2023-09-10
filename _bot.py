#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, os, logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram import html
from datetime import datetime
# from pyconfig import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.environ['TOKEN'])
# Диспетчер
dp = Dispatcher()

# Если не указать фильтр F.text, 
# то хэндлер сработает даже на картинку с подписью /test,
# но пока нам это не важно и рассматриваем только текстовые сообщения
@dp.message(Command("test"))
async def any_message(message: types.Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = html.underline(f"Создано в {time_now}")
    # Отправляем новое сообщение с добавленным текстом
    await message.answer(f"{message.text}\n\n{added_text}", parse_mode="HTML")

@dp.message(Command("name"))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"Привет, {html.bold(html.quote(command.args))}", parse_mode="HTML")
    else:
        await message.answer("Пожалуйста, укажи своё имя после команды /name!")

@dp.message(content_types=types.ContentTypes.PHOTO)
async def handle_photo(message: types.Message):
    for photo in message.photo:
        await message.reply(f"Вы отправили фотографию с размером {photo.width}x{photo.height} пикселей.")
# @dp.message(content_types=types.ContentType.TEXT)
# async def extract_data(message: types.Message):
#     data = {
#         "url": "<N/A>",
#         "email": "<N/A>",
#         "code": "<N/A>"
#     }
#     entities = message.entities or []
#     for item in entities:
#         if item.type in data.keys():
#             # Неправильно
#             # data[item.type] = message.text[item.offset : item.offset+item.length]
#             # Правильно
#             data[item.type] = item.extract_from(message.text)
#     await message.reply(
#         "Вот что я нашёл:\n"
#         f"URL: {html.quote(data['url'])}\n"
#         f"E-mail: {html.quote(data['email'])}\n"
#         f"Пароль: {html.quote(data['code'])}"
#     )

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())