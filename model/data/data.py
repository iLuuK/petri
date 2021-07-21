from shared.iData import IData


class Data(IData):
    def __init__(self, myId: int):
        self.__id = myId

    def getId(self) -> int:
        return self.__id

    def setId(self, myId: int):
        self.__id = myId
