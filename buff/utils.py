
import datetime

def cur_timestamp() -> str:
	t = datetime.datetime.now()
	t = str(int( t.timestamp() * 1000)) # 1000 is include milisecs

	return t