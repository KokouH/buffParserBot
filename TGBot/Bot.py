
import telebot
from typing import Dict
from loguru import logger
from . import message_handlers
from . anal import Analizer
from models.Users import Users, User
from threading import RLock, Thread
from multiprocessing import Process, Queue
# from Users import Users

class BotBuffProc(Process):
	def __init__(self, TG_API, goodsQin, infoQout):
		self.TG_API = TG_API
		self.goodsQin = goodsQin
		self.infoQout = infoQout
		super().__init__(daemon=True)

	def run(self):
		logger.info("Telegram Bot process started")
		self.buffParserBot = BuffParserBot(self.TG_API, self.goodsQin, self.infoQout)
		message_handlers.add_bot_message_handlers(self.buffParserBot)
		self.buffParserBot.analThread.start()
		self.buffParserBot.polling()


class BuffParserBot(telebot.TeleBot):
	def __init__(self, token: str, goodsQin: Queue = None, infoQout: Queue = None, usersDict: Dict[int, User] = {}):
		super().__init__(token)
		self.usersLock = RLock()
		self.analThread = Analizer(self)
		self.goodsQin = goodsQin
		self.infoQout = infoQout
		self.users = Users(usersDict=usersDict)

if __name__ == "__main__":

	buffParserBot = BuffParserBot('6321792496:AAHiWlYAOZA8aozqHozQhzuR2RoZKct_s3E')
	message_handlers.add_bot_message_handlers(buffParserBot)

	buffParserBot.polling()

	