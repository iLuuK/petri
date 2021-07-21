from abc import abstractmethod


class IData:
    @abstractmethod
    def getId(self) -> int:
        ...

    @abstractmethod
    def setId(self, myId: int):
        ...
