from model.data.behavior.behaviorLive import BehaviorLive
from model.data.behavior.grassDie import GrassDie
from model.data.cell import Cell
from model.data.color import Color
from shared.cellType import CellType
import random


class HerbivorLive(BehaviorLive):

    __energyStart = 20
    __energyReproduce = 50
    __energyWait = 1
    __energyMove = 2
    __baseColor = Color(0, 135, 0)

    def __init__(self):
        BehaviorLive.__init__(self, self.__energyStart, self.__baseColor)

    def live(self):
        if not self.checkIsAlive():
            self.__createDedCell()
        self.__createCell(self.__lifeCycle())

    def __lifeCycle(self):
            if self.reproduce(self.__energyReproduce):
                return self.reproduce(self.__energyReproduce)
            elif self.feed([CellType.GRASS]):
                param = self.feed([CellType.GRASS])
                return self.feed([CellType.GRASS])
            elif self.goToFeed([CellType.GRASS], self.__energyMove, CellType.HERBIVOR):
                return self.goToFeed([CellType.GRASS], self.__energyMove, CellType.HERBIVOR)
            elif self.randomMove(self.__energyMove):
                self.randomMove(self.__energyMove)
            else:
                return [self.getCell().getEnergy() - self.__energyWait, self.getCell().getX(), self.getCell().getY()]

    def __createDedCell(self):
        newCell = Cell(self.getCell().getPetri(), GrassDie(), self.getCell().getBirthStep() + 1,
                       CellType.GRASS)
        newCell.setX(self.getCell().getX())
        newCell.setY(self.getCell().getY())
        self.getCell().getPetri().addCell(newCell, self.getCell())

    def __createCell(self, params):
        newCell = Cell(self.getCell().getPetri(), HerbivorLive(), self.getCell().getBirthStep() + 1, CellType.HERBIVOR)
        newCell.setEnergy(params[0])
        newCell.setColor( Color(0, 135, 0))
        newCell.setX(params[1])
        newCell.setY(params[2])
        self.getCell().getPetri().addCell(newCell, self.getCell())