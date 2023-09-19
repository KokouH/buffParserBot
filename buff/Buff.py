
from . import utils
import requests
import time
import json
from typing import Dict
from multiprocessing import Process, Queue
from models.Goods import Good, GoodsDict
from loguru import logger


class Buff(Process):
	def __init__(self, goods: Dict[int, Good] = {}, goodsQin: Queue = None, infoQout: Queue = None, loadGoods: bool = True):
		self.goods = goods
		self.goodsQin = goodsQin
		self.outQueue = infoQout
		self.loadGoods = loadGoods
		self.lastSaveTime = 0
		super().__init__(daemon=True)

	def _get_goods(self, goods):
		curTimeStamp = utils.cur_timestamp()
		URL = f'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={goods}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_={curTimeStamp}'
		response = requests.get(url=URL)
		if response.status_code != 200:
			return None

		return response.json()['data']

	def save_current_goods(self):
		if time.time() - self.lastSaveTime < 10:
			return

		logger.info("Save current goods")
		with open("session/buff_goods.json", 'w') as File:
			File.write( GoodsDict(goods=self.goods).model_dump_json() )
		self.lastSaveTime = time.time()

	def load_goods(self):
		self.lastSaveTime = time.time()

		with open("session/buff_goods.json", "r") as File:
			goodsDict = json.loads( File.read() )['goods']
			self.goods = {}
			for gId in goodsDict:
				self.goods[gId] = Good.parse_raw(goodsDict[gId])

		logger.info("Goods loaded")

	def get_first_buy_price(self, goods, resp: requests.Response = None):
		if not resp:
			resp = self._get_goods(goods)

		return float(resp['items'][0]['price'])

	def run(self):
		logger.info("Buff process started")
		if (self.loadGoods):
			self.load_goods()
		while True:
			for gId in self.goods.keys():
				sgId = str(gId)
				resp = self._get_goods(gId)

				buffPrice = self.get_first_buy_price(gId, resp)
				hashName = resp['goods_infos'][sgId]['market_hash_name']
				iconUrl = resp['goods_infos'][sgId]['icon_url']
				steamPrice = resp['goods_infos'][str(gId)]['steam_price_cny']
				newGood = Good(id=gId, hashName=hashName, iconUrl=iconUrl,
							   priceBuff=buffPrice, priceSteam=steamPrice)

				if (self.goods[gId].priceBuff == None):
					self.goods[gId] = newGood
					self.outQueue.put(newGood)

				priceChangePercent = abs( buffPrice / self.goods[gId].priceBuff - 1 )
				if priceChangePercent > 0.03:
					self.goods[gId] = newGood
					self.outQueue.put(newGood)
				time.sleep(1)

			while not self.goodsQin.empty():
				# Messages from goodQueue
				# 1) {'type': 'add', 'good': 12345}
				# 2) {'type': 'del', 'good': 12345}

				msg = self.goodsQin.get()
				if (msg['type'] == 'del'):
					if (msg['good'] in self.goods):
						del(self.goods[msg['good']])

				if (msg['type'] == 'add'):
					if (msg['good'] not in self.goods):
						self.goods[msg['good']] = Good(id=msg['good'])
						logger.info(self.goods[msg['good']])

			# self.save_current_goods()
			time.sleep(0.01)
			# print('shit')


if __name__ == "__main__":
	import json

	print(Buff().get_first_buy_price(857657))
