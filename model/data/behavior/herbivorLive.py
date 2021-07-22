from model.data.behavior.behaviorLive import BehaviorLive
from model.data.behavior.grassDie import GrassDie
from model.data.cell import Cell
from model.data.color import Color
from shared.cellType import CellType
import random


class HerbivorLive(BehaviorLive):
    __energyStart = 20
    __energyReproduce = 80
    __energyWait = 1
    __energyMove = 2
    __baseColor = Color(0, 255, 0)
    __scaleUp1 = 45
    __scaleUp2 = 60
    __rangeFeed = 20
    __rangeGoToFeed = 1

    def __init__(self):
        BehaviorLive.__init__(self, self.__energyStart, self.__baseColor)

    def live(self):
        self.__checkScale()
        if not self.__checkIsAlive():
            if not self.__reproduce():
                if not self.__feed():
                    if not self.__goToFeed():
                        if not self.__randomMove():
                            self.__wait()

    def __checkScale(self):
        newScale = 1
        if self.getCell().getEnergy() >= self.__scaleUp1:
            newScale = 2

        if self.getCell().getEnergy() >= self.__scaleUp2:
            newScale = 3

        self.getCell().setScale(newScale)

    def __reproduce(self):
        if self.getCell().getIsAlive() and self.getCell().canAction(self.__energyReproduce):
            self.getCell().setEnergy(int(self.getCell().getEnergy() / 2))
            self.__wait()
            self.__randomMove(self.getCell().getScale())
            return True
        return False

    def __wait(self):
        energy = self.getCell().getEnergy() - self.__energyWait
        newCell = Cell(self.getCell().getPetri(), HerbivorLive(), self.getCell().getBirthStep() + 1, CellType.HERBIVOR)
        newCell.setEnergy(energy)
        newCell.setColor(Color(0, 255, 0))
        newCell.setX(self.getCell().getX())
        newCell.setY(self.getCell().getY())
        newCell.setScale(self.getCell().getScale())
        self.getCell().getPetri().addCell(newCell, self.getCell())

    def __randomMove(self, distance: int = 0):
        if self.getCell().canAction(self.__energyMove):

            canMove = False
            nbTry = 0
            while (not canMove) and nbTry < 20:
                nbTry += 1

                if random.randint(0, 1) == 1:
                    randomX = self.getCell().getX() + random.randint(-1, 1) + distance
                    randomY = self.getCell().getY()
                else:
                    randomY = self.getCell().getY() + random.randint(-1, 1) + distance
                    randomX = self.getCell().getX()

                if randomX < 0:
                    randomX = self.getCell().getPetri().getWidth()

                if randomY < 0:
                    randomY = self.getCell().getPetri().getHeight()

                randomX = randomX % self.getCell().getPetri().getWidth()
                randomY = randomY % self.getCell().getPetri().getHeight()

                if not self.getCell().getPetri().isSquareFree(self.getCell().getScale(), randomX, randomY):
                    canMove = True

            if canMove:
                newCell = Cell(self.getCell().getPetri(), HerbivorLive(), self.getCell().getBirthStep() + 1, CellType.HERBIVOR)
                newCell.setEnergy(self.getCell().getEnergy() - self.__energyMove)
                newCell.setColor(Color(0, 255, 0))
                newCell.setX(randomX)
                newCell.setY(randomY)
                newCell.setType(CellType.HERBIVOR)
                newCell.setScale(self.getCell().getScale())
                self.getCell().getPetri().addCell(newCell, self.getCell())
                return True

            return False
        return False

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

    def __feed(self):
        feedPosition = self.getCell().getPetri().canFeed(self.__rangeFeed, self.getCell().getX(), self.getCell().getY(), [CellType.GRASS])

        if feedPosition:
            canFeed = False
            for scaleX in range(self.getCell().getScale()):
                for scaleY in range(self.getCell().getScale()):
                    if feedPosition[0] == self.getCell().getX() + scaleX and feedPosition[1] == self.getCell().getY() + scaleY:
                        canFeed = True

            if canFeed:
                food = self.getCell().getPetri().getCell(feedPosition[0], feedPosition[1], [CellType.GRASS])

                if food is None:
                    return False

                newCell = Cell(self.getCell().getPetri(), HerbivorLive(), self.getCell().getBirthStep() + 1, CellType.HERBIVOR)
                newCell.setEnergy(self.getCell().getEnergy() + food.getEnergy())
                food.setIsAlive(False)
                newCell.setColor(Color(0, 255, 0))
                newCell.setX(self.getCell().getX())
                newCell.setY(self.getCell().getY())
                newCell.setScale(self.getCell().getScale())

                self.getCell().getPetri().addCell(newCell, self.getCell())

                return True
        return False

    def canGo(self, x: int, y: int) -> bool:
        value = True
        for scaleX in range(0, self.getCell().getScale()):
            for scaleY in range(0, self.getCell().getScale()):
                valueX = (self.getCell().getX() + scaleX) % self.getCell().getPetri().getWidth()
                valueY = (self.getCell().getY() + scaleY) % self.getCell().getPetri().getHeight()
                if self.getCell().getPetri().isCellTypeNotSame(self.getCell().getCustomId(), valueX, valueY, CellType.HERBIVOR):
                    value = False

        return value

    def hasNotHerbivor(self, x: int, y: int) -> bool:
        return not self.getCell().getPetri().isCellTypeNotSame(self.getCell().getCustomId(), x, y, CellType.HERBIVOR)

    def __goToFeed(self):
        feedPosition = self.getCell().getPetri().canFeed(self.__rangeFeed, self.getCell().getX(), self.getCell().getY(), [CellType.GRASS])
        if feedPosition and self.getCell().canAction(self.__energyMove) and self.hasNotHerbivor(feedPosition[0], feedPosition[1]):

            newPositionX = self.getCell().getX()
            newPositionY = self.getCell().getY()

            distance = abs(feedPosition[0] - newPositionX) + abs(feedPosition[1] - newPositionY)
            for directionX in range(self.__rangeGoToFeed * -1, self.__rangeGoToFeed + 1):
                valueX = (newPositionX + directionX) % self.getCell().getPetri().getWidth()
                valueY = newPositionY
                if (abs(feedPosition[0] - valueX) + abs(feedPosition[1] - valueY)) < distance:
                    distance = abs(feedPosition[0] - valueX) + abs(feedPosition[1] - valueY)
                    newPositionX = valueX
                    newPositionY = valueY

            for directionY in range(self.__rangeGoToFeed * -1, self.__rangeGoToFeed + 1):
                valueX = newPositionX
                valueY = (newPositionY + directionY) % self.getCell().getPetri().getHeight()
                if (abs(feedPosition[0] - valueX) + abs(feedPosition[1] - valueY)) < distance:
                    distance = abs(feedPosition[0] - valueX) + abs(feedPosition[1] - valueY)
                    newPositionX = valueX
                    newPositionY = valueY

            newPositionX = newPositionX % self.getCell().getPetri().getWidth()
            newPositionY = newPositionY % self.getCell().getPetri().getHeight()

            if not self.canGo(newPositionX, newPositionY):
                return False

            newCell = Cell(self.getCell().getPetri(), HerbivorLive(), self.getCell().getBirthStep() + 1, CellType.HERBIVOR)
            newCell.setEnergy(self.getCell().getEnergy() - self.__energyMove)
            newCell.setColor(Color(0, 255, 0))

            newCell.setX(newPositionX)
            newCell.setY(newPositionY)
            newCell.setType(CellType.HERBIVOR)
            newCell.setScale(self.getCell().getScale())
            self.getCell().getPetri().addCell(newCell, self.getCell())
            return True
        return False
