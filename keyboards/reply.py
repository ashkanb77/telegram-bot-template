from telegram import ReplyKeyboardMarkup, KeyboardButton

from config import *


def main_menu():
    keyboard = []
    for row in menu_order:
        keyboard.append([KeyboardButton(col) for col in row])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
# ReplyKeyboardRemove()
