from shared.iCell import ICell
from shared.iColor import IColor
from model.data.data import Data
from model.data.color import Color
from shared.iPetri import IPetri
from model.data.behavior.behaviorLive import BehaviorLive
import random


class Cell(ICell, Data):
    def __init__(self, petri: IPetri, behaviorLive: BehaviorLive, birthStep: int):
        self.__petri = petri
        self.__birthStep = birthStep
        self.__x = random.randint(0, self.__petri.getWidth())
        self.__y = random.randint(0, self.__petri.getHeight())
        self.__color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.__behaviorLive = behaviorLive
        self.__behaviorLive.setCell(self)
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
