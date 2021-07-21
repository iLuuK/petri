from model.data.behavior.behaviorLive import BehaviorLive
from model.data.cell import Cell
from model.data.color import Color
from shared.cellType import CellType
import random


class GrassDie(BehaviorLive):

    __energyStart = 20
    __baseColor = Color(173, 103, 0)

    def __init__(self):
        BehaviorLive.__init__(self, self.__energyStart, self.__baseColor)


    def live(self):
        self.__checkIsAlive()

    def __checkIsAlive(self):
        if self.getCell().getIsAlive():
            newCell = Cell(self.getCell().getPetri(), GrassDie(), self.getCell().getBirthStep() + 1, CellType.GRASS)
            newCell.setX(self.getCell().getX())
            newCell.setY(self.getCell().getY())
            newCell.setEnergy(self.getCell().getEnergy())
            newCell.setColorNoLumen(self.getColor())
            newCell.setType(CellType.GRASS)
            self.getCell().getPetri().addCell(newCell, self.getCell())
        else:
            self.getCell().getPetri().removeCell(self.getCell())
