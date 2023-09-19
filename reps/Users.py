
from typing import Optional
from models import Users, Goods
from threading import RLock


def add_user(users: Users.Users, user: Users.User, lock: RLock) -> None:
	if user.id in users:
		return
	lock.acquire()
	users.usersDict[user.id] = user
	lock.release()

def get_user_by_id(users: Users.Users, id: int, lock: RLock) -> Optional[Users.User]:
	if id in users.usersDict:
		return users.usersDict[id]

	newUser = Users.User(id=id, goods=dict())
	add_user(users, newUser, lock)
	return newUser

def get_all_unique_goods(users: Users.Users) -> list[Goods.Good]:
	goodsList = []

	for u in users.usersDict:
		goodsList.extend(users.usersDict[u].goods)

	goodsList = list(set( goodsList ))
	return goodsList

def add_goods(user: Users.User, good: Goods.Good, lock: RLock):
	lock.acquire()
	user.goods[good.id] = good
	lock.release()

def del_goods(user: Users.User, goodId: int, lock: RLock):
	lock.acquire()
	del(user.goods[goodId])
	lock.release()

