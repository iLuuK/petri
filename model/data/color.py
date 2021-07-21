from shared.iColor import IColor
from model.data.data import Data


class Color(IColor, Data):
    def __init__(self, red: int, green: int, blue: int):
        self.__red = red
        self.__green = green
        self.__blue = blue
        Data.__init__(self, id(self))

    def getRed(self) -> int:
        return self.__red

    def setRed(self, red: int):
        self.__red = red

    def getGreen(self) -> int:
        return self.__green

    def setGreen(self, green: int):
        self.__green = green

    def getBlue(self) -> int:
        return self.__blue

    def setBlue(self, blue: int):
        self.__blue = blue

    def darken(self, darkCoefficient: int):
        self.__red = max(0, self.__red - darkCoefficient)
        self.__green = max(0, self.__green - darkCoefficient)
        self.__blue = max(0, self.__blue - darkCoefficient)
