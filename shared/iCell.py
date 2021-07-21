from abc import abstractmethod
from shared.iColor import IColor
from shared.iData import IData
from shared.cellType import CellType


class ICell(IData):
    @abstractmethod
    def getX(self) -> int:
        ...

    @abstractmethod
    def getY(self) -> int:
        ...

    @abstractmethod
    def getColor(self) -> IColor:
        ...

    @abstractmethod
    def getPetri(self):
        ...

    @abstractmethod
    def live(self):
        ...

    @abstractmethod
    def setBehaviorLive(self, behaviorLive):
        ...

    @abstractmethod
    def getBirthStep(self) -> int:
        ...

    @abstractmethod
    def getType(self) -> CellType:
        ...

    @abstractmethod
    def setType(self, type):
        ...

    @abstractmethod
    def setEnergy(self, int):
        ...

    @abstractmethod
    def getEnergy(self) -> int:
        ...

    @abstractmethod
    def canAction(self, int) -> bool:
        ...

    def setIsAlive(self, bool):
        ...

    def getIsAlive(self) -> bool:
        ...
