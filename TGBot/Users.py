
import json
import copy

from loguru import logger

class UserState:
	WAIT = 0
	ADDING_NEW_GOODS = 1
	DELETE_ITEMS = 2

class User(): # User  in botBuffParser users
	def __init__(self, id: int, state: int = UserState.WAIT, goods: list[int] = list()):
		self.id = id
		self.state = state
		self.goods = goods

	def add_goods(self, addGoods: list):

		for good in addGoods:
			if good not in self.goods:
				self.goods.append(good)

	def get_json(self):
		_json = {}
		_json['id'] = self.id
		_json['state'] = self.state
		_json['goods'] = self.goods

		return _json


	def __repr__(self):
		return f"id={self.id} : state={self.state} : goods={len(self.goods)}"

	def __str__(self):
		return f"id={self.id} : state={self.state} : goods={len(self.goods)}"

class Users():
	def __init__(self, users: dict = dict()):
		self.usersList = users

	def get_user_by_id(self, id: int):
		
		if (id in self.usersList):
			return self.usersList[id]
		return None

	def add_user(self, id:int, state: int = UserState.WAIT, goods: list = list()):

		if (id not in self.usersList):
			self.usersList[id] = User(id, state, goods) 
		else:
			# Exception('User exists')
			logger.error(f'User exists {id}')

	def get_all_goods(self):

		goods = []
		for user in self.usersList:
			goods.extend( user.goods )

		goods = list(set(goods))

		return goods

	def get_json(self):
		_json = copy.deepcopy(self.usersList)
		for _id in _json:
			_json[_id] = _json[_id].get_json()
		return _json

	def __repr__(self):
		# return "[\n\t" + '\n\t'.join([i.__str__() for i in self.usersList]) + "\n]"
		return 'Users'