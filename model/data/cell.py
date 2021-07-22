from shared.iCell import ICell
from shared.iColor import IColor
from model.data.data import Data
from model.data.color import Color
from shared.iPetri import IPetri
from shared.cellType import CellType
from model.data.behavior.behaviorLive import BehaviorLive
import random


class Cell(ICell, Data):
    def __init__(self, petri: IPetri, behaviorLive: BehaviorLive, birthStep: int, cellType: CellType):
        self.__cellType = cellType
        self.__petri = petri
        self.__birthStep = birthStep
        self.__x = random.randint(0, self.__petri.getWidth())
        self.__y = random.randint(0, self.__petri.getHeight())
        self.__behaviorLive = behaviorLive
        self.__behaviorLive.setCell(self)
        self.__color = behaviorLive.getColor()
        self.__energy = behaviorLive.getEnergy()
        self.__isAlive = True
        Data.__init__(self, id(self))

    def getX(self) -> int:
        return self.__x

    def setX(self, x: int):
        self.__x = x

    def getY(self) -> int:
        return self.__y

    def setY(self, y: int):
        self.__y = y

    def getColor(self) -> IColor:
        return self.__color

    def setColor(self, color: IColor):
        self.__color = color
        if self.getEnergy() < 0:
            nrj = self.getEnergy()
            cell = self.getType()
        self.__color.lighter(self.getEnergy())


    def setColorNoLumen(self, color: IColor):
        self.__color = color

    def getPetri(self) -> IPetri:
        return self.__petri

    def setPetri(self, petri: IPetri):
        self.__petri = petri

    def live(self):
        self.__behaviorLive.live()

    def setBehaviorLive(self, behaviorLive: BehaviorLive):
        self.__behaviorLive = behaviorLive

    def getBirthStep(self):
        return self.__birthStep

    def setBirthStep(self, birthStep: int):
        self.__birthStep = birthStep

    def getType(self) -> CellType:
        return self.__cellType

    def setType(self, cellType):
        self.__cellType = cellType

    def getEnergy(self) -> int:
        return self.__energy

    def setEnergy(self, energy: int):
        self.__energy = energy

    def canAction(self, energy: int) -> int:
        return self.__energy > energy

    def setIsAlive(self, isAlive: bool):
        self.__isAlive = isAlive
        if not isAlive:
            self.setEnergy(0)

    def getIsAlive(self) -> bool:
        return self.__isAlive