from abc import abstractmethod
from shared.iData import IData


class IColor(IData):
    @abstractmethod
    def getRed(self) -> int:
        ...

    @abstractmethod
    def getGreen(self) -> int:
        ...

    @abstractmethod
    def getBlue(self) -> int:
        ...

    @abstractmethod
    def darken(self, darkCoefficient: int):
        ...
