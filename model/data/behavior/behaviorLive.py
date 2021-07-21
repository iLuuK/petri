from abc import abstractmethod
from shared.iCell import ICell


class BehaviorLive:
    def __init__(self):
        self.__cell: ICell = None

    def getCell(self) -> ICell:
        return self.__cell

    def setCell(self, cell: ICell):
        self.__cell = cell

    @abstractmethod
    def live(self):
        ...
