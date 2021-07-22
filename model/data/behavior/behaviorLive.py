from abc import abstractmethod

from model.data.color import Color
from shared.iCell import ICell

import random


class BehaviorLive:
    def __init__(self, energy: int, color: Color):
        self.__cell: ICell = None
        self.__energy = energy
        self.__color = color

    def getCell(self) -> ICell:
        return self.__cell

    def setCell(self, cell: ICell):
        self.__cell = cell

    def getEnergy(self) -> int:
        return self.__energy

    def setEnergy(self, energy: int):
        self.__energy = energy

    def getColor(self) -> Color:
        return self.__color

    @abstractmethod
    def live(self):
        ...
    def checkIsAlive(self):
        if self.getCell().getEnergy() == 0:
            self.getCell().setIsAlive(False)
            return True
        return False

    def reproduce(self, energyReproduce):
        if self.getCell().getIsAlive() and self.getCell().canAction(energyReproduce):
            self.getCell().setEnergy(int(self.getCell().getEnergy() / 2))
            self.wait()
            self.randomMove()
            return True
        return False


    def randomMove(self, energyMove):
        if self.getCell().canAction(energyMove):
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
                energy = self.getCell().getEnergy() - energyMove
                return [energy, self.getCell().getX(), self.getCell().getY()]
            return False
        return False

    def feed(self, foodType):
        myPosition = [self.getCell().getX(), self.getCell().getY()]
        feedPosition = self.getCell().getPetri().canFeed(self.getCell().getX(), self.getCell().getY(), foodType)
        cell = self.getCell()
        if feedPosition:
            if feedPosition[0] == self.getCell().getX() and feedPosition[1] == self.getCell().getY():
                food = self.getCell().getPetri().getCell(feedPosition[0], feedPosition[1])
                energy = self.getCell().getEnergy() + food.getEnergy()
                food.setIsAlive(False)
                return [energy, self.getCell().getX(), self.getCell().getY()]
        return False

    def canGo(self, x: int, y: int, cellType) -> bool:
        return not self.getCell().getPetri().isCellType(x, y, cellType)

    def goToFeed(self, foodType, energyMove, cellType):
        feedPosition = self.getCell().getPetri().canFeed(self.getCell().getX(), self.getCell().getY(), foodType)
        if feedPosition and self.getCell().canAction(energyMove) and self.canGo(feedPosition[0],
                                                                                       feedPosition[1], cellType):

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
                for i in foodType:
                    if futureCell.getType() != i:
                        return False
            energy = self.getCell().getEnergy() - energyMove
            return [energy, newPositionX, newPositionY]
        return False