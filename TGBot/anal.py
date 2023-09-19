
import time
from loguru import logger
from threading import Thread
from pydantic import BaseModel
from models.Goods import Good

class Analizer(Thread):
	def __init__(self, bot):
		super().__init__(daemon=True)
		self.bot = bot

	def run(self):
		logger.info("Analizer process started")
		while True:
			inputQueue = self.bot.infoQout

			while not inputQueue.empty():

				self.bot.usersLock.acquire()
				# self.bot.usersLock.release()
				good = inputQueue.get()
				
				usersDict = self.bot.users.usersDict
				for userId in usersDict:
					if good.id in usersDict[userId].goods:
						usersDict[userId].goods[good.id] = good

				self.bot.usersLock.release()
				
			# time.sleep(0.01)


if __name__ == "__main__":
	an = Analizer(1)

	item = AnalItems(cur_prise=0.2, hash_name='asdff', goods=123435)
	an.items.append(item)

	print(an.items)
