from shared.iPetri import IPetri
from shared.iCell import ICell
from model.data.data import Data
from shared.cellType import CellType
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

    def isCellType(self, x: int, y: int, cellType: CellType) -> bool:
        value = False
        for cell in self.__cells:
            if cell.getY() == y and cell.getX() == x and cell.getType() == cellType:
                value = True
        return value

    def getCell(self, x: int, y: int) -> ICell:
        value = type(None)()
        for cell in self.__cells:
            if cell.getY() == y and cell.getX() == x:
                value = cell
        return value

    def addCell(self, newCell: ICell, oldCell: ICell):
        if oldCell in self.__cells:
            self.__squareUsed[oldCell.getX(), oldCell.getY()] = False
            self.__cells.remove(oldCell)

        self.__squareUsed[newCell.getX(), newCell.getY()] = True
        self.__cells.append(newCell)

    def addCellFirstTime(self, newCell: ICell):
        if self.isSquareFree(newCell.getX(), newCell.getY()):
            self.__squareUsed[newCell.getX(), newCell.getY()] = True
            self.__cells.append(newCell)

    def removeCell(self, oldCell: ICell):
        self.__squareUsed[oldCell.getX(), oldCell.getY()] = False
        self.__cells.remove(oldCell)

    def isSquareFree(self, x: int, y: int) -> bool:
        if 0 <= x < self.__width and 0 <= y < self.__height:
            if not self.__squareUsed[x, y]:
                return True
        return False

    def canFeed(self, initialX: int, initialY: int, cellType):
        value = []
        distance = 10000
        isUse = False
        for x in range(-20, 20):
            for y in range(-20, 20):
                useX = (x + initialX) % self.getWidth()
                useY = (y + initialY) % self.getHeight()
                test = self.__squareUsed[useX, useY]
                if self.__squareUsed[useX, useY]:

                    for type in cellType:
                        if self.isCellType(useX, useY, type):
                            newDistance = abs(useX - initialX) + abs(useY - initialY)
                            if newDistance < distance:
                                value = [useX, useY]
                                distance = newDistance

        if isUse:
            value = []

        return value
