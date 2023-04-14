from aiogram.types import *


def get_main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('❓ Help ❓', callback_data='help'))
    keyboard.row(InlineKeyboardButton('Start', callback_data='start_work'))
    return keyboard


def get_work_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton('Win', callback_data='win'),
        InlineKeyboardButton('Lose', callback_data='lose'),
        InlineKeyboardButton('Stop', callback_data='stop')
    ]
    keyboard.add(*buttons)
    return keyboard
