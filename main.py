

import config
import time
import signal
import json
import multiprocessing as mp

from TGBot import message_handlers
from TGBot.Bot import BotBuffProc

from buff.Buff import Buff
from multiprocessing import Process


def main():

	goodsQin = mp.Queue()
	infoQout = mp.Queue()

	# Buff parser process
	buffProcess = Buff(dict(), goodsQin, infoQout, False)
	buffProcess.start()


	# Bot process
	botProcess = BotBuffProc(config.TG_API, goodsQin, infoQout)
	botProcess.start()
	
	buffProcess.join()
	botProcess.join()

if __name__ == "__main__":
	main()


