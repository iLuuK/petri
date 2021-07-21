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
