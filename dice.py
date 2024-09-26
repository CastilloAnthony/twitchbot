import random

class Dice():
    def __init__(self, face:int):
        if face in [4, 6, 8, 10, 12, 20]:
            self.__face = face
        self.__lastRoll = 0
        self.__history = []
    # end __init__

    def __del__(self):
        del self.__face, self.__lastRoll
    # end __del__

    def __str__(self):
        return 'd'+str(self.__face)+': '+str(self.__lastRoll)
    # end __str__

    def face(self):
        return 'd'+str(self.__face)
    # end face

    def roll(self):
        self.__lastRoll = random.randint(1, self.__face)
        self.__history.append(self.__lastRoll)
        return self.__lastRoll
    # end roll

    def lastRoll(self):
        return self.__lastRoll
    # end lastRoll

    def history(self):
        return self.__history
    # end history
# end Dice