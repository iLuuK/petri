from model.data.behavior.behaviorLive import BehaviorLive
from model.data.behavior.grassDie import GrassDie
from model.data.cell import Cell
from model.data.color import Color
from shared.cellType import CellType
import random


class CarnivorousLive(BehaviorLive):
    __energyStart = 50
    __energyReproduce = 150
    __energyWait = 1
    __energyMove = 2
    __baseColor = Color(135, 0, 0)
    __rangeSearchFeed = 30
    __rangeGoToFeed = 3
    __scaleUp1 = 500
    __scaleUp2 = 1000
    __cellTypesFeed = [CellType.HERBIVOR]

    def __init__(self):
        BehaviorLive.__init__(self, self.__energyStart, self.__baseColor)

    def live(self):
        self.commonCheckScale(self.__scaleUp1, self.__scaleUp2)
        if not self.commonCheckIsAlive():
            if not self.commonReproduce(self.__energyReproduce, self.__energyMove, self.__energyWait):
                if not self.commonFeed(self.__rangeSearchFeed, self.__cellTypesFeed):
                    if not self.commonGoToFood(self.__rangeSearchFeed, self.__rangeGoToFeed, self.__energyMove, self.__cellTypesFeed):
                        if not self.commonRandomMove(self.getCell().getEnergy(), self.__energyMove):
                            self.commonWait(self.getCell().getEnergy(), self.__energyWait)

    def createCell(self, params: []):
        newCell = Cell(self.getCell().getPetri(), CarnivorousLive(), params[4], CellType.CARNIVOROUS)
        newCell.setEnergy(params[0])
        newCell.setColor(Color(135, 0, 0))
        newCell.setX(params[1])
        newCell.setY(params[2])
        newCell.setScale(params[3])
        self.getCell().getPetri().addCell(newCell, self.getCell())

    def createDeadCell(self, params: []):
        newCell = Cell(self.getCell().getPetri(), GrassDie(), params[0], CellType.GRASS)
        newCell.setX(params[0])
        newCell.setY(params[1])
        self.getCell().getPetri().addCell(newCell, self.getCell())
