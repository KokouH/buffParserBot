
from . import msg_data
from telebot import types

def start():
	markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

	markup.add(
		types.KeyboardButton(msg_data.ADD_NEW_ITEMS),
		types.KeyboardButton(msg_data.DELETE_ITEMS),
		types.KeyboardButton(msg_data.VIEW_ITEMS)
	)

	return markup

def back():

	markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

	markup.add(
		types.KeyboardButton(msg_data.BACK)
	)

	return markup
