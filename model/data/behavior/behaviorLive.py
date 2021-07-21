from abc import abstractmethod

from model.data.color import Color
from shared.iCell import ICell


class BehaviorLive:
    def __init__(self, energy: int, color: Color):
        self.__cell: ICell = None
        self.__energy = energy
        self.__color = color

    def getCell(self) -> ICell:
        return self.__cell

    def setCell(self, cell: ICell):
        self.__cell = cell

    def getEnergy(self) -> int:
        return self.__energy

    def setEnergy(self, energy: int):
        self.__energy = energy

    def getColor(self) -> Color:
        return self.__color

    @abstractmethod
    def live(self):
        ...
