
from typing import Optional, Dict
from pydantic import BaseModel

class SimpleGood(BaseModel):
	id: int

class Good(SimpleGood):
	# id: int
	hashName: Optional[str] = None
	iconUrl: Optional[str] = None
	priceBuff: Optional[float] = None
	priceSteam: Optional[float] = None

class GoodsDict(BaseModel):
	goods: Dict[int, Good]



