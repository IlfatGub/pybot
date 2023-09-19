#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, os, logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram import html
from datetime import datetime
from aiogram import F
# from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
import re
from base import DataBase

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

db = DataBase("my_database.db")

# db.addTableUsers()
# db.deleteTable()
# db.addTableUsers()
# db.addUser('ilat', 'ilfat@mail.ru', '31')
# db.getUser()


# Если не указать фильтр F.text, 
# то хэндлер сработает даже на картинку с подписью /test,
# но пока нам это не важно и рассматриваем только текстовые сообщения
# @dp.message(Command("test"))
# async def any_message(message: types.Message):
#     # Получаем текущее время в часовом поясе ПК
#     time_now = datetime.now().strftime('%H:%M')
#     # Создаём подчёркнутый текст
#     added_text = html.underline(f"Создано в {time_now}")
#     # Отправляем новое сообщение с добавленным текстом
#     await message.answer(f"{db.getUser()}\n\n{added_text}", parse_mode="HTML")

# @dp.message(Command("name"))
# async def cmd_name(message: types.Message, command: CommandObject):
#     if command.args:
#         await message.answer(f"Привет, {html.bold(html.quote(command.args))}", parse_mode="HTML")
#     else:
        # await message.answer("Пожалуйста, укажи своё имя после команды /name!")

# @dp.message(content_types=types.ContentTypes.PHOTO)
# async def handle_photo(message: types.Message):
#     for photo in message.photo:
#         await message.reply(f"Вы отправили фотографию с размером {photo.width}x{photo.height} пикселей.")

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [ [types.KeyboardButton(text="Узнать долги", callback_data="find_out_debts")], ]
    keyboard = types.ReplyKeyboardMarkup( keyboard=kb, )
    await message.answer("-", reply_markup=keyboard)

# @dp.callback_query_handler(text=["In_First_button", "In_Second_button"])
# async def callbacks_num(callback: types.CallbackQuery):
#     print('1')

# user_debt = {}

@dp.message(F.text.startswith(("+", "-")))
async def with_puree(message: types.Message):
    _sp = message.text.split()
    
    if len(_sp) > 1:
        db.debtor = _sp[1] 
        
        
    db.setSumm(_sp[0])
    summ = re.sub(r'(\+|-)', r'', _sp[0])   
    db.summ = _sp[0]
    db.user_ct_id = message.from_user.id
    if summ.isdigit() == False:
        await message.answer("Должно быть числом")
    elif len(_sp) == 1:
        await message.answer("Кому записываем долг?", reply_markup=debtor(db.getDebtorList()))
        # await message.answer("Добавьте должника. Пример Сообщения '+100 Вася'")
        # await message.answer(F"{db.getDebtorList()}")
    else:
        old_summ = db.getDebtorSumm()
        db.debt()
        await message.answer(f"db.debtor. Старый долг: {old_summ}.  Новый долг {db.getDebtorSumm()}")
    
# @dp.message(F.text.startswith("-") )
# async def with_puree(message: types.Message):
#     user_debt[message.from_user.id] = message.text
#     await message.answer("Кому записываем долг?", reply_markup=debtor())

def debtor(list, prefixs = 'add_debt_'):
    buttons = []
    for user in list:
        buttons.append([types.InlineKeyboardButton(text=f"{user[1]}", callback_data=f"{prefixs}{user[0]}")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@dp.callback_query(F.data.startswith("add_debt"))
async def callbacks_num(callback: types.CallbackQuery):
    # print(callback)
    id_debtor = callback.data.split("_")[2]
    db.id = id_debtor
    db.debtor = db.getDebetorById()[1]
    old_summ = db.getDebtorSumm()
    # print(db.getDebetorById()[1])
    db.debt()
    
    await callback.message.edit_text(f"{db.debtor}. Старый долг: {old_summ}.  Новый долг {db.getDebtorSumm()}")
    await callback.answer()

@dp.callback_query(F.data.startswith("list_debt_"))
async def callbacks_num(callback: types.CallbackQuery):
    id_debtor = callback.data.split("_")[2]
    db.id = id_debtor
    db.debtor = db.getDebetorById()[1]
    debts = db.getDebtorHistoryList()
    if debts:
        string = f"{db.debtor} \n"
        for debt in debts:
            string = f"{string}{str(debt[3])}руб - {str(debt[4][0:10])} \n"
    else:
        string = 'пусто'
        
    await callback.message.edit_text(f"{string}")
    await callback.answer()
    
@dp.message(F.text.lower() == "узнать долги")
async def with_puree(message: types.Message):
    await message.answer("Кому записываем долг?", reply_markup=debtor(db.getDebtorList(), "list_debt_"))


@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


# @dp.message(Command("random"))
# async def cmd_random(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="Нажми меня",
#         callback_data="random_value")
#     )
#     await message.answer(
#         "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
#         reply_markup=builder.as_markup()
#     )

# @dp.callback_query(F.data == "random_value")
# async def send_random_value(callback: types.CallbackQuery):
#     await callback.message.answer(str(random.randint(1, 10)))
#     await callback.answer(
#         text="Спасибо, что воспользовались ботом!",
#         show_alert=True
#     )

# Здесь хранятся пользовательские данные.
# Т.к. это словарь в памяти, то при перезапуске он очистится
# user_data = {}




# def get_keyboard():
#     buttons = [
#         [
#             types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
#             types.InlineKeyboardButton(text="+1", callback_data="num_incr")
#         ],
#         [
#             types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
#         ]
#     ]
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard

# async def update_num_text(message: types.Message, new_value: int):
#     with suppress(TelegramBadRequest):
#         await message.edit_text(
#             f"Укажите число: {new_value}",
#             reply_markup=get_keyboard()
#         )

# @dp.message(Command("numbers"))
# async def cmd_numbers(message: types.Message):
#     user_data[message.from_user.id] = 0
#     await message.answer("Укажите число: 0", reply_markup=get_keyboard())

# @dp.callback_query(F.data.startswith("num_"))
# async def callbacks_num(callback: types.CallbackQuery):
#     user_value = user_data.get(callback.from_user.id, 0)
#     action = callback.data.split("_")[1]

#     if action == "incr":
#         user_data[callback.from_user.id] = user_value+1
#         await update_num_text(callback.message, user_value+1)
#     elif action == "decr":
#         user_data[callback.from_user.id] = user_value-1
#         await update_num_text(callback.message, user_value-1)
#     elif action == "finish":
#         await callback.message.edit_text(f"Итого: {user_value}")

#     await callback.answer()

# @dp.message(Command("delete_last"))
# async def handle_delete_last(message: types.Message):
#     # Получаем информацию о чате
#     chat_id = message.chat.id
#     # Получаем список последних двух сообщений в чате
#     messages = await bot.get_chat_history(chat_id, limit=2)
#     # Удаляем последние два сообщения
#     for message_data in messages:
#         await bot.delete_message(chat_id, message_data.message_id)
    
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