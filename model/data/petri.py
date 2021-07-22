from uuid import UUID

from shared.iPetri import IPetri
from shared.iCell import ICell
from model.data.data import Data
from shared.cellType import CellType
import numpy


class Petri(Data, IPetri):
    def __init__(self, width: int, height: int, rounds=None):
        if rounds is None:
            rounds = []
        self.__rounds = rounds
        self.__numberRound = 0
        self.__width = width
        self.__height = height
        self.__cells: [ICell] = []
        self.__squareUsed = numpy.zeros((width, height), dtype= bool)
        self.__squareType = numpy.zeros((width, height), dtype= CellType)
        self.__squareId = numpy.zeros((width, height), dtype= UUID)
        Data.__init__(self, id(self))


    def getNumberRound(self) -> int:
        return self.__numberRound

    def setNumberRound(self, number: int):
        self.__numberRound = number

    def updateNumberRound(self):
        self.__numberRound += 1

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

    def setCells(self, cells: [ICell]):
        self.__cells = cells

    def isCellType(self, x: int, y: int, cellType: CellType) -> bool:
        value = False
        if self.__squareType[x, y] == cellType:
            value = True
        return value

    def isCellTypeNotSame(self, actualId: int, x: int, y: int, cellType: CellType) -> bool:
        return self.__squareType[x, y] == cellType and self.__squareId[x, y] != actualId

    def getCell(self, x: int, y: int, cellTypes: []) -> ICell:
        value = type(None)()
        searchId = self.__squareId[x, y]
        for cell in self.__cells:
            if cell.getCustomId() == searchId:
                for cellType in cellTypes:
                    if cell.getType() == cellType:
                        value = cell
        return value

    def addCell(self, newCell: ICell, oldCell: ICell):
        if oldCell in self.getCells():
            self.removeCell(oldCell)

        for scaleX in range(0, newCell.getScale()):
            for scaleY in range(0, newCell.getScale()):
                valueX = (newCell.getX() + scaleX) % self.getWidth()
                valueY = (newCell.getY() + scaleY) % self.getHeight()
                self.__squareUsed[valueX, valueY] = True
                self.__squareType[valueX, valueY] = newCell.getType()
                self.__squareId[valueX, valueY] = newCell.getCustomId()

        self.__cells.append(newCell)

    def addCellFirstTime(self, newCell: ICell):
        if self.isSquareFree(1, newCell.getX(), newCell.getY()):
            valueX = newCell.getX() % self.getWidth()
            valueY = newCell.getY() % self.getHeight()
            self.__squareUsed[valueX, valueY] = True
            self.__squareType[valueX, valueY] = newCell.getType()
            self.__squareId[valueX, valueY] = newCell.getCustomId()
            self.__cells.append(newCell)

    def removeCell(self, oldCell: ICell):
        if oldCell in self.__cells:
            for scaleX in range(0, oldCell.getScale()):
                for scaleY in range(0, oldCell.getScale()):
                    valueX = (oldCell.getX() + scaleX) % self.getWidth()
                    valueY = (oldCell.getY() + scaleY) % self.getHeight()
                    self.__squareUsed[valueX, valueY] = False
                    self.__squareType[valueX, valueY] = CellType.NONE
                    self.__squareType[valueX, valueY] = 0
            self.__cells.remove(oldCell)


    def isSquareFree(self, scale: int, x: int, y: int) -> bool:
        value = True
        for scaleX in range(-scale + 1, scale):
            for scaleY in range(-scale + 1, scale):
                valueX = (x + scaleX) % self.__width
                valueY = (y + scaleY) % self.__width
                if 0 <= x < self.__width and 0 <= y < self.__height:
                    if self.__squareUsed[valueX, valueY]:
                        value = False
        return value

    def canFeed(self, rangeFeed: int, initialX: int, initialY: int, cellTypes: []):
        value = []
        distance = 10000
        for x in range(rangeFeed * -1, rangeFeed + 1):
            for y in range(rangeFeed * -1, rangeFeed + 1):
                useX = (x + initialX) % self.getWidth()
                useY = (y + initialY) % self.getHeight()
                if self.__squareUsed[useX, useY]:
                    for type in cellTypes:
                        if self.isCellType(useX, useY, type):
                            newDistance = abs(useX - initialX) + abs(useY - initialY)
                            if newDistance < distance:
                                value = [useX, useY]
                                distance = newDistance

        return value

    def setRoundsId(self, roundsId: [int]):
        self.__rounds = roundsId

    def getRoundsId(self) -> [int]:
        return self.__rounds
