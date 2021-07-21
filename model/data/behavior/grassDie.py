from model.data.behavior.behaviorLive import BehaviorLive
from model.data.cell import Cell
from model.data.behavior.classicDie import ClassicDie
from model.data.color import Color
from shared.cellType import CellType
import random


class HerbivorLive(BehaviorLive):
    def __init__(self):
        herbivorColor = Color(0, 255, 0)
        BehaviorLive.__init__(self, 10, herbivorColor)


    def live(self):
        if not self.__checkIsAlive():
            if not self.__feed():
                if not self.__goToFeed():
                    if not self.__randomMove():
                        self.__wait()
                        
                        
    def __wait(self):
        energy = 1
        newCell = Cell(self.getCell().getPetri(), HerbivorLive(), self.getCell().getBirthStep() + 1)
        newCell.setEnergy(self.getEnergy() - energy)
        newColor = self.getCell().getColor()
        newCell.setColor(newColor)
        newCell.setX(self.getCell().getX())
        newCell.setY(self.getCell().getY())
        newCell.setType(CellType.HERBIVOR)
        self.getCell().getPetri().addCell(newCell)


    def __randomMove(self):
        energy = 2
        if self.getCell().canAction(energy):
            
            canMove = False
            nbTry = 0
            while (not canMove) or nbTry < 10:
                nbTry+= 1
                
                if random.randint(0, 1) == 1:
                    randomX = self.getCell().getX() + random.randint(0, 1)
                else:
                    randomY = self.getCell().getY() + random.randint(0, 1)
                
                if self.getCell().getPetri().isSquareFree(randomX, randomY):
                    canMove = True    

            if canMove:
                newCell = Cell(self.getCell().getPetri(), HerbivorLive(), self.getCell().getBirthStep() + 1)
                newCell.setEnergy(self.getEnergy() - energy)
                newColor = self.getCell().getColor()
                newCell.setColor(newColor)
                newCell.setX(randomX)
                newCell.setY(randomY)
                newCell.setType(CellType.HERBIVOR)
                self.getCell().getPetri().addCell(newCell)
                return True
            
            return False
        return False

    def __checkIsAlive(self):
        if self.getCell().getEnergy() == 0:
            self.getCell().setIsAlive(False)
            newCell = Cell(self.getCell().getPetri(), GrassDie(), self.getCell().getBirthStep() + 1)
            newCell.setX(self.getCell().getX())
            newCell.setY(self.getCell().getY())
            newCell.setType(CellType.GRASS)
            self.getCell().getPetri().addCell(newCell)
            return True
        return False

    def __feed(self):
        feedPosition = self.getCell().getPetri().canFeed(self.getCell().getX(), self.getCell().getY(), CellType.GRASS)
        if feedPosition[0] == self.getCell().getX() and feedPosition[1] == self.getCell().getY():
            food = self.getCell().getPetri().getCell(feedPosition[0], feedPosition[1])
            food.setIsAlive(False)
            newCell = self.getCell()
            newCell.setEnergy(self.getEnergy() + food.getEnergy())
            newCell.setColor(self.getColor())
            self.getCell().getPetri().addCell(newCell)
            return True
        return False

    def __goToFeed(self):
        energy = 2
        feedPosition = self.getCell().getPetri().canFeed(self.getCell().getX(), self.getCell().getY(), CellType.GRASS)
        if feedPosition and self.getCell().canAction(energy):

            newColor = self.getCell().getColor()

            newPositionX = self.getCell().getX()
            newPositionY = self.getCell().getX()

            if self.getCell().getX() == feedPosition[0]:
                if self.getCell().getY() - feedPosition[1] < 5:
                    newPositionY -= 1
                else:
                    newPositionY += 1
            else:
                if self.getCell().getX() - feedPosition[0] < 5:
                    newPositionX -= 1
                else:
                    newPositionX += 1
                    
            futureCell = self.getCell().getPetri().getCell(newPositionX, newPositionY)
            if futureCell:
                if futureCell.getType() != CellType.GRASS:
                    return False

            newCell = Cell(self.getCell().getPetri(), HerbivorLive(), self.getCell().getBirthStep() + 1)
            newCell.setEnergy(self.getEnergy() - energy)
            newCell.setColor(newColor)
            newCell.setX(newPositionX)
            newCell.setY(newPositionY)
            newCell.setType(CellType.HERBIVOR)
            self.getCell().getPetri().addCell(newCell)
            return True
        return False
