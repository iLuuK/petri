from shared.iPetri import IPetri
from shared.iCell import ICell
from model.data.data import Data
import numpy


class Petri(Data, IPetri):
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__cells: [ICell] = []
        self.__squareUsed = numpy.zeros((width, height), dtype=bool)
        Data.__init__(self, id(self))

    def getWidth(self) -> int:
        return self.__width

    def setWidth(self, width: int):
        self.__width = width

    def getHeight(self) -> int:
        return self.__height

    def setHeight(self, height: int):
        self.__height = height

    def getCells(self) -> [ICell]:
        return self.__cells

    def addCell(self, cell: ICell):
        if self.isSquareFree(cell.getX(), cell.getY()):
            self.__squareUsed[cell.getX(), cell.getY()] = True
            self.__cells.append(cell)

    def isSquareFree(self, x: int, y: int) -> bool:
        if 0 <= x < self.__width and 0 <= y < self.__height:
            if not self.__squareUsed[x, y]:
                return True
        return False

