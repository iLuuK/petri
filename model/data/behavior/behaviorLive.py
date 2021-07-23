from abc import abstractmethod
import random

from model.data.color import Color
from shared.cellType import CellType
from shared.iCell import ICell


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

    def commonWait(self, newEnergy: int, energyWait: int) -> []:
        actualCell = self.getCell()
        newEnergy = newEnergy - energyWait
        x = actualCell.getX()
        y = actualCell.getY()
        scale = actualCell.getScale()
        birthStep = actualCell.getBirthStep() + 1
        self.createCell([newEnergy, x, y, scale, birthStep])

    def commonReproduce(self, energyReproduce: int, energyMove: int, energyWait: int) -> []:
        actualCell = self.getCell()
        if actualCell.getIsAlive() and actualCell.canAction(energyReproduce):
            newEnergy = int(actualCell.getEnergy() / 2)
            self.commonWait(newEnergy, energyWait)
            self.commonRandomMove(newEnergy, energyMove, self.getCell().getScale())
            return True
        return False

    def commonRandomMove(self, newEnergy: int, energyMove: int,  distance: int = 0):
        actualCell = self.getCell()
        if actualCell.canAction(energyMove):

            canMove = False
            nbTry = 0
            while (not canMove) and nbTry < 20:
                nbTry += 1


                if random.randint(0, 1) == 1:
                    randomX = actualCell.getX() + random.randint(-1, 1) + distance
                    randomY = actualCell.getY()
                else:
                    randomY = actualCell.getY() + random.randint(-1, 1) + distance
                    randomX = actualCell.getX()

                if randomX < 0:
                    randomX = actualCell.getPetri().getWidth()

                if randomY < 0:
                    randomY = actualCell.getPetri().getHeight()

                randomX = randomX % actualCell.getPetri().getWidth()
                randomY = randomY % actualCell.getPetri().getHeight()

                if not actualCell.getPetri().isSquareFree(actualCell.getScale(), randomX, randomY):
                    canMove = True

            if canMove:
                energy = newEnergy - energyMove
                x = randomX
                y = randomY
                scale = actualCell.getScale()
                birthStep = actualCell.getBirthStep() + 1
                self.createCell([energy, x, y, scale, birthStep])
                return True

            return False
        return False

    def commonCheckScale(self, scaleUp1: int, scaleUp2: int):
        newScale = 1
        actualCell = self.getCell()
        if actualCell.getEnergy() >= scaleUp1:
            newScale = 2

        if actualCell.getEnergy() >= scaleUp2:
            newScale = 3

        self.getCell().setScale(newScale)

    def commonCheckIsAlive(self):
        actualCell = self.getCell()
        if actualCell.getEnergy() == 0:
            self.getCell().setIsAlive(False)
            x = actualCell.getX()
            y = actualCell.getY()
            birthStep = actualCell.getBirthStep() + 1
            self.createDeadCell([x, y, birthStep])
            return True
        return False

    def commonFeed(self, rangeFeed: int, cellTypes: []):
        actualCell = self.getCell()
        feedPosition = actualCell.getPetri().canFeed(rangeFeed, self.getCell().getX(), self.getCell().getY(), cellTypes)

        if feedPosition:
            canFeed = False
            for scaleX in range(actualCell.getScale()):
                for scaleY in range(actualCell.getScale()):
                    if feedPosition[0] == actualCell.getX() + scaleX and feedPosition[1] == actualCell.getY() + scaleY:
                        canFeed = True

            if canFeed:
                food = actualCell.getPetri().getCell(feedPosition[0], feedPosition[1], cellTypes)

                if food is None:
                    return False

                energy = actualCell.getEnergy() + food.getEnergy()
                food.setIsAlive(False)
                x = actualCell.getX()
                y = actualCell.getY()
                scale = actualCell.getScale()
                birthStep = actualCell.getBirthStep() + 1
                self.createCell([energy, x, y, scale, birthStep])
                return True
        return False

    def commonCanGo(self, cellType: CellType):
        value = True
        actualCell = self.getCell()
        for scaleX in range(0, actualCell.getScale()):
            for scaleY in range(0, actualCell.getScale()):
                valueX = (actualCell.getX() + scaleX) % actualCell.getPetri().getWidth()
                valueY = (actualCell.getY() + scaleY) % actualCell.getPetri().getHeight()
                if actualCell.getPetri().isCellTypeNotSame(actualCell.getCustomId(), valueX, valueY, cellType):
                    value = False
        return value

    def hasNotBrother(self, x: int, y: int, actualCellType: CellType) -> bool:
        return not self.getCell().getPetri().isCellTypeNotSame(self.getCell().getCustomId(), x, y, actualCellType)

    def commonGoToFood(self, rangeFeed: int, rangeGoToFeed: int, energyMove: int, findCellType: []):
        actualCell = self.getCell()
        actualCellType = actualCell.getType()
        feedPosition = actualCell.getPetri().canFeed(rangeFeed, actualCell.getX(), actualCell.getY(), findCellType)
        if feedPosition and actualCell.canAction(energyMove) and self.hasNotBrother(feedPosition[0], feedPosition[1], actualCellType):

            newPositionX = actualCell.getX()
            newPositionY = actualCell.getY()

            distance = abs(feedPosition[0] - newPositionX) + abs(feedPosition[1] - newPositionY)
            findDistance = False
            for directionX in range(rangeGoToFeed * -1, rangeGoToFeed + 1):
                valueX = (newPositionX + directionX) % actualCell.getPetri().getWidth()
                valueY = newPositionY
                if (abs(feedPosition[0] - valueX) + abs(feedPosition[1] - valueY)) < distance:
                    distance = abs(feedPosition[0] - valueX) + abs(feedPosition[1] - valueY)
                    newPositionX = valueX
                    newPositionY = valueY
                    findDistance = True

            if not findDistance:
                for directionY in range(rangeGoToFeed * -1, rangeGoToFeed + 1):
                    valueX = newPositionX
                    valueY = (newPositionY + directionY) % actualCell.getPetri().getHeight()
                    if (abs(feedPosition[0] - valueX) + abs(feedPosition[1] - valueY)) < distance:
                        distance = abs(feedPosition[0] - valueX) + abs(feedPosition[1] - valueY)
                        newPositionX = valueX
                        newPositionY = valueY

            newPositionX = newPositionX % actualCell.getPetri().getWidth()
            newPositionY = newPositionY % actualCell.getPetri().getHeight()

            if not self.commonCanGo(actualCellType):
                return False

            energy = actualCell.getEnergy() - energyMove
            x = newPositionX
            y = newPositionY
            scale = actualCell.getScale()
            birthStep = actualCell.getBirthStep() + 1
            self.createCell([energy, x, y, scale, birthStep])

            return True
        return False

    @abstractmethod
    def live(self):
        ...

    @abstractmethod
    def createCell(self, params: []):
        ...

    @abstractmethod
    def createDeadCell(self, params: []):
        ...
