
from typing import Dict, Optional
from enum import Enum
from pydantic import BaseModel

from . Goods import SimpleGood, Good

class UserState(Enum):
	WAIT = 0
	ADDING_NEW_GOODS = 1
	DELETE_ITEMS = 2

class User(BaseModel):
	id: int
	state: UserState = UserState.WAIT
	goods: Dict[int, Good]
	# goods: Dict[int, SimpleGood]

class Users(BaseModel):
	usersDict: Optional[Dict[int, User]]


