
from . import msg_data
from . import markup_generators
from . Users import UserState
from models.Users import User
from models.Goods import Good, SimpleGood
from reps.Users import add_user, get_user_by_id, add_goods, del_goods
from loguru import logger

from telebot import types


def add_bot_message_handlers(bot):

	# COMMAND HANDLERS

	@bot.message_handler(commands=['start'])
	def start_handler(msg):
		
		try:
			newUser = User(id=msg.chat.id, goods=dict())
			add_user(bot.users, newUser, bot.usersLock)
			logger.info(bot.users)
		except Exception as e:
			print(e)

		markup = markup_generators.start()
		bot.send_message(msg.chat.id, msg_data.START_MESSAGE, reply_markup=markup)

	@bot.message_handler(commands=['help'])
	def help_handler(msg):

		bot.send_message(msg.chat.id, msg_data.HELP_MESSAGE)

	@bot.message_handler(commands=['info'])
	def info_handler(msg):

		bot.send_message(msg.chat.id, msg_data.INFO_MESSAGE)

	# OTHER MESSAGE HANDLE

	@bot.message_handler(func=lambda msg: msg.text == msg_data.ADD_NEW_ITEMS)
	def add_new_items_handler(msg):

		curUser = get_user_by_id(bot.users, msg.chat.id, bot.usersLock)
		curUser.state = UserState.ADDING_NEW_GOODS
		markup = markup_generators.back()
		bot.send_message(msg.chat.id, msg_data.NEW_GOODS, reply_markup=markup)

	@bot.message_handler(func=lambda msg: msg.text == msg_data.VIEW_ITEMS)
	def view_items_handler(msg):

		curUser = get_user_by_id(bot.users, msg.chat.id, bot.usersLock)
		textToSend = msg_data.YOUR_ITEMS
		for gId in curUser.goods:
			good = curUser.goods[gId]
			addText = f"{good.hashName} : {good.priceBuff}¥\n"
			textToSend = f"{textToSend}{addText}"
		bot.send_message(msg.chat.id, textToSend)

	@bot.message_handler(func=lambda msg: msg.text == msg_data.DELETE_ITEMS)
	def delete_items_handler(msg):
		curUser = get_user_by_id(bot.users, msg.chat.id, bot.usersLock)
		curUser.state = UserState.DELETE_ITEMS
		markup = markup_generators.back()
		bot.send_message(msg.chat.id, msg_data.DEL_GOODS, reply_markup=markup)

	@bot.message_handler()
	def handle_plain_text(msg):

		curUser = get_user_by_id(bot.users, msg.chat.id, bot.usersLock)
		curUserState = curUser.state
		if (curUserState == UserState.WAIT):
			bot.send_message(msg.chat.id, msg_data.ERROR_NOT_CHOOSEN_ACT)
			return None

		elif msg.text == msg_data.BACK:
			get_user_by_id(bot.users, msg.chat.id, bot.usersLock).state = UserState.WAIT
			markup = markup_generators.start()
			bot.send_message(msg.chat.id, msg_data.START_WAIT, reply_markup=markup)
			return None

		# HANDLE ADD/DEL ITEMS
		if (curUserState == UserState.DELETE_ITEMS
				or curUserState == UserState.ADDING_NEW_GOODS):
			message = msg.text.strip()
			links = message.split('\n')
			try:
				goods = list(map(int, [i.split('/')[4] for i in links])) # 4 index goods in link
				goods = list(set(goods))
				for gId in goods:
					if (curUserState == UserState.DELETE_ITEMS):
						sendType = 'del'
						del_goods(curUser, gId, bot.usersLock)
					else:
						sendType = 'add'
						add_goods(curUser, Good(id=gId), bot.usersLock)
					dataToGoods = {'type': sendType, 'good': gId}
					bot.goodsQin.put(dataToGoods)

			except Exception as e:
				# logger.error(e)
				bot.send_message(msg.chat.id, msg_data.ERROR_NOT_VALID_LINKS, disable_web_page_preview=True)

			return None


