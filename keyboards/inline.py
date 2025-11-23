import json

from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def main_options():
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data="opt1")],
        [InlineKeyboardButton("Option 2", callback_data="opt2")],
        [InlineKeyboardButton("Visit Google", url="https://google.com")]
    ]
    return InlineKeyboardMarkup(keyboard)





def option2_submenu():
    keyboard = [
        [InlineKeyboardButton("Sub-Option A", callback_data="subA")],
        [InlineKeyboardButton("Sub-Option B", callback_data="subB")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)


