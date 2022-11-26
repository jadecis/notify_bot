from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

timezone_menu= InlineKeyboardMarkup(row_width=1)

timezone_menu.add(
    InlineKeyboardButton('МСК -1', callback_data='zone_-1'),
    InlineKeyboardButton('МСК +0', callback_data='zone_+0'),
    InlineKeyboardButton('МСК +2', callback_data='zone_+2'),
    InlineKeyboardButton('МСК +3', callback_data='zone_+3'),
    InlineKeyboardButton('МСК +4', callback_data='zone_+4'),
    InlineKeyboardButton('МСК +5', callback_data='zone_+5'),
    InlineKeyboardButton('МСК -6', callback_data='zone_-6'),
    InlineKeyboardButton('МСК -7', callback_data='zone_-7'),
    InlineKeyboardButton('МСК -8', callback_data='zone_-8'),
    InlineKeyboardButton('МСК -9', callback_data='zone_-9')
)

func_menu= InlineKeyboardMarkup(row_width=1)

func_menu.add(
    InlineKeyboardButton('Установить будильник.', callback_data='func_alarm'),
    InlineKeyboardButton('Напоминание', callback_data='func_notify')
)

back_but= InlineKeyboardMarkup(row_width=1)

back_but.add(
    InlineKeyboardButton('Назад', callback_data='back')
)