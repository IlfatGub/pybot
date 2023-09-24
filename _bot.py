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
from tabulate import tabulate
import prettytable as pt
import settings


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
# Диспетчер
dp = Dispatcher()

db = DataBase("my_database.db")


@dp.message(Command("name"))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"Привет, {html.bold(html.quote(command.args))}", parse_mode="MARKDOWN_V2")
    else:
        await message.answer("Пожалуйста, укажи своё имя после команды /name!")

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [ [types.KeyboardButton(text="Узнать долги", callback_data="find_out_debts")], ]
    keyboard = types.ReplyKeyboardMarkup( keyboard=kb, )
    await message.answer("-", reply_markup=keyboard)


@dp.message(F.text.startswith("debt"))
async def debt_add(message: types.Message):
    res = message.text.split()
    if len(res) == 1:
        await message.answer(f"Надо указать должника")
    else:
        db.debtor = res[1] 
        db.addDebtor()
        await message.answer(f"{html.bold(res[1])} - Добавлен")
        
@dp.message(F.text.startswith(("+", "-")))
async def with_puree(message: types.Message):
    _sp = message.text.split(' ', 1)
    
    if len(_sp) > 1:
        db.comment = _sp[1] 
        
    db.setSumm(_sp[0])
    summ = re.sub(r'(\+|-)', r'', _sp[0])   
    db.summ = _sp[0]
    db.user_ct_id = message.from_user.id
    if summ.isdigit() == False:
        await message.answer("Должно быть числом")
    else:
        await message.answer("Кому записываем долг?", reply_markup=debtor(db.getActiveDebtorList()))

def debtor(list, prefixs = 'add_debt_'):
    buttons = []
    for user in list:
        buttons.append([types.InlineKeyboardButton(text=f"{user[1]}", callback_data=f"{prefixs}{user[0]}")])
        
    buttons.append([types.InlineKeyboardButton(text=f"Отмена", callback_data=f"cancel")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@dp.callback_query(F.data.startswith("add_debt"))
async def callbacks_num(callback: types.CallbackQuery):
    id_debtor = callback.data.split("_")[2]
    db.id = id_debtor
    db.debtor = db.getDebetorById()[1]
    old_summ = db.getDebtorSumm()
    db.debt()
    
    string = getListDebtForDebtor()
    
    await callback.message.edit_text(string)
    # await callback.answer()

@dp.callback_query(F.data.startswith("cancel"))
async def callbacks_num(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Отмена")
    await callback.answer()

def format_comment(comment, max_line_length):
    ACC_length = 0
    words = comment.split(" ")
    formatted_comment = ""
    for word in words:
        if ACC_length + (len(word) + 1) <= max_line_length:
            formatted_comment = formatted_comment + word + " "
            ACC_length = ACC_length + len(word) + 1
        else:
            formatted_comment = formatted_comment + "\n" + word + " "
            ACC_length = len(word) + 1
    return formatted_comment


@dp.callback_query(F.data.startswith("list_debt_"))
async def callbacks_num(callback: types.CallbackQuery):
    id_debtor = callback.data.split("_")[2]
    db.id = id_debtor
    string = getListDebtForDebtor()
    await callback.message.edit_text(string)

def getListDebtForDebtor():
    _debtor = db.getDebetorById()
    db.debtor = _debtor[1]
    debts = db.getDebtorHistoryList()

    string = ''    
    if debts:
        string = html.bold(f'{db.debtor}. Общая сумма долга: {_debtor[2]} \n')
        for debt in debts:
            string = f"{string} {debt[4][0:10]}  |  {debt[3]}руб  |  {str(debt[6])} \n"
    else:
        string = 'пусто'
    return string


@dp.message(F.text.lower() == "узнать долги")
async def with_puree(message: types.Message):
    await message.answer("Кому записываем долг?", reply_markup=debtor(db.getActiveDebtorList(), "list_debt_"))


@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


@dp.message(F.text)
async def extract_data(message: types.Message):
    text = "Привет. Вот какие команды у меня есть:"
    row1 = f"{html.bold('debt ')} {html.italic('[name]')}"
    row2 = f"{html.bold('+')}{html.italic('[price] [comment]')}"
    row3= f"{html.bold('-')}{html.italic('[price] [comment]')}"
    await message.answer(
        f"{html.bold(text)}\n"
        f"{row1.ljust(50)} добавляем должника \n"
        f"{row2.ljust(50)} добавляем дол \n"
        f"{row3.ljust(50)} уменьшаем долг \n"
    )

    
# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())