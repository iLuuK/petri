from abc import abstractmethod
from shared.iColor import IColor
from shared.iData import IData


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
