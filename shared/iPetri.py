from abc import abstractmethod
from shared.iCell import *
from shared.iData import IData


class IPetri(IData):
    @abstractmethod
    def getWidth(self) -> int:
        ...

    @abstractmethod
    def getHeight(self) -> int:
        ...

    @abstractmethod
    def getCells(self) -> [ICell]:
        ...

    @abstractmethod
    def addCell(self, cell: ICell):
        ...

    @abstractmethod
    def isSquareFree(self, x: int, y: int) -> bool:
        ...
