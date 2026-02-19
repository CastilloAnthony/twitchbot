import time
from threading import Thread
from interface import Interface
from bot import Bot()

class Host():
    def __init__(self):
        self.__intreface = Interface()
        self.__bot = Bot()

    def __del__(self):
        del self.__intreface, self.__bot

    def run(self):
        pass
# end Interface