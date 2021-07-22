from model.data.behavior.behaviorLive import BehaviorLive
from model.data.behavior.grassDie import GrassDie
from model.data.cell import Cell
from model.data.color import Color
from shared.cellType import CellType
import random


class CarnivorLive(BehaviorLive):
    __energyStart = 20
    __energyReproduce = 50
    __energyWait = 1
    __energyMove = 2
    __baseColor = Color(135, 0, 0)
    __nbMove = 2

    def __init__(self):
        BehaviorLive.__init__(self, self.__energyStart, self.__baseColor)

    def live(self):
        if not self.__checkIsAlive():
            if not self.__reproduce():
                    if not self.__feed():
                        if not self.__goToFeed():
                            if not self.__randomMove():
                                self.__wait()

    def __checkIsAlive(self):
        if self.getCell().getEnergy() == 0:
            self.getCell().setIsAlive(False)
            newCell = Cell(self.getCell().getPetri(), GrassDie(), self.getCell().getBirthStep() + 1, CellType.GRASS)
            newCell.setX(self.getCell().getX())
            newCell.setY(self.getCell().getY())
            newCell.setType(CellType.GRASS)
            self.getCell().getPetri().addCell(newCell, self.getCell())
            return True
        return False

    def __reproduce(self):
        if self.getCell().getIsAlive() and self.getCell().canAction(self.__energyReproduce):
            self.getCell().setEnergy(int(self.getCell().getEnergy() / 2))
            self.__wait()
            self.__randomMove()
            return True
        return False



    def __feed(self):
        feedPosition = self.getCell().getPetri().canFeed(self.getCell().getX(), self.getCell().getY(), [CellType.HERBIVOR, CellType.OMNIVOROUS])

        if feedPosition:

            if feedPosition[0] == self.getCell().getX() and feedPosition[1] == self.getCell().getY():
                food = self.getCell().getPetri().getCell(feedPosition[0], feedPosition[1])
                newCell = self.getCell()
                newCell.setEnergy(self.getCell().getEnergy() + food.getEnergy())
                food.setIsAlive(False)
                newCell.setColor(Color(135, 0, 0))
                newCell.setX(self.getCell().getX())
                newCell.setY(self.getCell().getY())
                newCell.setType(CellType.HERBIVOR)
                self.getCell().getPetri().addCell(newCell, self.getCell())
                return True
        return False

    def canGo(self, x: int, y: int) -> bool:
        return not self.getCell().getPetri().isCellType(x, y, CellType.CARNIVOROUS)

    def __goToFeed(self):
        feedPosition = self.getCell().getPetri().canFeed(self.getCell().getX(), self.getCell().getY(), [CellType.HERBIVOR, CellType.OMNIVOROUS])
        if feedPosition and self.getCell().canAction(self.__energyMove) and self.canGo(feedPosition[0],
                                                                                       feedPosition[1]):
            nbAcualMove = 0
            newPositionX = self.getCell().getX()
            newPositionY = self.getCell().getY()

            if self.getCell().getX() == feedPosition[0]:
                if abs(self.getCell().getY() - feedPosition[1]) < 5:
                    if (self.getCell().getY() - feedPosition[1] < 0):
                        newPositionY += 1
                    else:
                        newPositionY -= 1
                else:
                    if (self.getCell().getY() - feedPosition[1] < 0):
                        newPositionY -= 1
                    else:
                        newPositionY += 1
            else:
                if abs(self.getCell().getX() - feedPosition[0]) < 5:
                    if (self.getCell().getX() - feedPosition[0] < 0):
                        newPositionX += 1
                    else:
                        newPositionX -= 1
                else:
                    if (self.getCell().getX() - feedPosition[0] < 0):
                        newPositionX -= 1
                    else:
                        newPositionX += 1

            if newPositionX < 0:
                newPositionX = self.getCell().getPetri().getWidth()

            if newPositionY < 0:
                newPositionY = self.getCell().getPetri().getHeight()

            newPositionX = newPositionX % self.getCell().getPetri().getWidth()
            newPositionY = newPositionY % self.getCell().getPetri().getHeight()

            futureCell = self.getCell().getPetri().getCell(newPositionX, newPositionY)
            if futureCell is not None and self.canGo(newPositionX, newPositionY):
                if futureCell.getType() != CellType.HERBIVOR:
                    return False

            newCell = Cell(self.getCell().getPetri(), CarnivorLive(), self.getCell().getBirthStep() + 1,
                           CellType.CARNIVOROUS)
            newCell.setEnergy(self.getCell().getEnergy() - self.__energyMove)
            newCell.setColor(Color(135, 0, 0))

            newCell.setX(newPositionX)
            newCell.setY(newPositionY)
            newCell.setType(CellType.CARNIVOROUS)
            self.getCell().getPetri().addCell(newCell, self.getCell())
            return True
        return False

    def __randomMove(self):
        if self.getCell().canAction(self.__energyMove):

            canMove = False
            nbTry = 0
            while (not canMove) and nbTry < 10:
                nbTry += 1

                if random.randint(0, 1) == 1:
                    randomX = self.getCell().getX() + random.randint(-1, 1)
                    randomY = self.getCell().getY()
                else:
                    randomY = self.getCell().getY() + random.randint(-1, 1)
                    randomX = self.getCell().getX()

                if randomX < 0:
                    randomX = self.getCell().getPetri().getWidth()

                if randomY < 0:
                    randomY = self.getCell().getPetri().getHeight()

                randomX = randomX % self.getCell().getPetri().getWidth()
                randomY = randomY % self.getCell().getPetri().getHeight()

                if self.getCell().getPetri().isSquareFree(randomX, randomY):
                    canMove = True

            if canMove:
                newCell = Cell(self.getCell().getPetri(), CarnivorLive(), self.getCell().getBirthStep() + 1,
                               CellType.CARNIVOROUS)
                newCell.setEnergy(self.getCell().getEnergy() - self.__energyMove)
                newCell.setColor(Color(135, 0, 0))
                newCell.setX(randomX)
                newCell.setY(randomY)
                newCell.setType(CellType.CARNIVOROUS)
                self.getCell().getPetri().addCell(newCell, self.getCell())
                return True

            return False
        return False

    def __wait(self):
        energy = self.getCell().getEnergy() - self.__energyWait
        newCell = Cell(self.getCell().getPetri(), CarnivorLive(), self.getCell().getBirthStep() + 1, CellType.HERBIVOR)
        newCell.setEnergy(energy)
        newCell.setColor(Color(135, 0, 0))
        newCell.setX(self.getCell().getX())
        newCell.setY(self.getCell().getY())
        self.getCell().getPetri().addCell(newCell, self.getCell())
