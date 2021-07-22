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
    def getCell(self, x: int, y: int) -> ICell:
        ...

    @abstractmethod
    def isCellType(self, x: int, y: int, cellType: CellType) -> bool:
        ...

    @abstractmethod
    def isCellTypeNotSame(self, actualId: int, x: int, y: int, cellType: CellType) -> bool:
        ...

    @abstractmethod
    def addCellFirstTime(self, cell: ICell):
        ...

    @abstractmethod
    def addCell(self, newCell: ICell, oldCell: ICell):
        ...


    @abstractmethod
    def removeCell(self, oldCell: ICell):
        ...

    @abstractmethod
    def isSquareFree(self, scale: int, x: int, y: int) -> bool:
        ...

    @abstractmethod
    def canFeed(self, x: int, y: int, cellType: CellType):
        ...

    @abstractmethod
    def getNumberRound(self) -> int:
        ...

    @abstractmethod
    def setNumberRound(self):
        ...

    @abstractmethod
    def updateNumberRound(self):
        ...


