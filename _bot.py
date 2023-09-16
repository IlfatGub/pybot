#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, os, logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram import html
from datetime import datetime
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
import re

# from dotenv import load_dotenv
import settings

# from pyconfig import config
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=settings.BOT_TOKEN)
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
    await message.answer(f"{message.text}{message}\n\n{added_text}", parse_mode="HTML")

@dp.message(Command("name"))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"Привет, {html.bold(html.quote(command.args))}", parse_mode="HTML")
    else:
        await message.answer("Пожалуйста, укажи своё имя после команды /name!")

# @dp.message(content_types=types.ContentTypes.PHOTO)
# async def handle_photo(message: types.Message):
#     for photo in message.photo:
#         await message.reply(f"Вы отправили фотографию с размером {photo.width}x{photo.height} пикселей.")

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="С пюрешкой")],
        [types.KeyboardButton(text="Без пюрешки")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

user_debt = {}

@dp.message(F.text.startswith("-"))
async def with_puree(message: types.Message):
    user_debt[message.from_user.id] = message.text
    await message.answer("Кому записываем долг?", reply_markup=debtor())

def debtor():
    buttons = [
        [
            types.InlineKeyboardButton(text="Человек 1", callback_data="add_debt")
        ],
        [
            types.InlineKeyboardButton(text="Человек 2", callback_data="add_debt")
        ],
        [
            types.InlineKeyboardButton(text="Отмена", callback_data="add_debt")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@dp.callback_query(F.data.startswith("add_debt"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_debt.get(callback.from_user.id, 0)
    action = user_value.split(",")
    user_value = re.findall(r'\d+', user_value)

    # if action == "incr":
    #     user_data[callback.from_user.id] = user_value+1
    #     await update_num_text(callback.message, user_value+1)
    # elif action == "decr":
    #     user_data[callback.from_user.id] = user_value-1
    #     await update_num_text(callback.message, user_value-1)
    # elif action == "finish":
    #     await callback.message.edit_text(f"Итого: {user_value}")
        
    await callback.message.edit_text(f"{user_value[0]},{action},{len(action)}")
    await callback.answer()
    
@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!")

@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(random.randint(1, 10)))
    await callback.answer(
        text="Спасибо, что воспользовались ботом!",
        show_alert=True
    )

# Здесь хранятся пользовательские данные.
# Т.к. это словарь в памяти, то при перезапуске он очистится
user_data = {}




def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [
            types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Укажите число: {new_value}",
            reply_markup=get_keyboard()
        )

@dp.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())

@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")

    await callback.answer()

@dp.message(Command("delete_last"))
async def handle_delete_last(message: types.Message):
    # Получаем информацию о чате
    chat_id = message.chat.id
    # Получаем список последних двух сообщений в чате
    messages = await bot.get_chat_history(chat_id, limit=2)
    # Удаляем последние два сообщения
    for message_data in messages:
        await bot.delete_message(chat_id, message_data.message_id)
    
# @dp.message(F.text)
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



    
# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())