#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, os, logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
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
    await message.answer("Hello, <b>world</b>!", parse_mode="HTML")
    await message.answer("Hello, *world*\!", parse_mode="MarkdownV2")

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())