from abc import abstractmethod
from shared.iPetri import IPetri
from shared.iPetri import ICell


class IModel:
    @abstractmethod
    def getPetriById(self, idPetri: int) -> IPetri:
        ...

    @abstractmethod
    def getCells(self) -> [ICell]:
        ...

    @abstractmethod
    def savePetri(self):
        ...

    @abstractmethod
    def getIsLoadPetri(self) -> bool:
        ...

    @abstractmethod
    def getLoadPetriId(self) -> int:
        ...

    @abstractmethod
    def setLoadPetri(self):
        ...

    @abstractmethod
    def getPetriById(self, idPetri: int) -> IPetri:
        ...

    @abstractmethod
    def getRoundCell(self, round: int):
        ...

    @abstractmethod
    def getNumberRound(self) -> int:
        ...

    @abstractmethod
    def updateNumberRound(self):
        ...


