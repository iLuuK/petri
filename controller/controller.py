import uuid

from model.model import Model
from shared.iModel import IModel
from shared.action import Action
from view.view import View
from shared.iController import IController
import time


class Controller(IController):
    def __init__(self):
        self.__model: IModel = Model()
        self.__view = View(self, self.__model)
        self.__run = True
        self.__play = True

    def live(self):
        if self.__model.getIsLoadPetri():
            self.__model.setLoadPetri()
            round = 0
            while round < self.__model.getNumberRound():
                round += 1
                if self.__play:
                    self.__model.getRoundCell(round)
                    self.__view.show()
                else:
                    time.sleep(5)
        else:
            self.__model.savePetri()
            while self.__run:
                if self.__play:
                    uid = uuid.uuid4()
                    self.__model.saveRound(uid)
                    self.__model.updateNumberRound()
                    self.__view.show()
                    oldCells = self.__model.getCells().copy()

                    for cell in oldCells:
                        cell.live()
                else:
                    time.sleep(1)

    def performAction(self, action: Action):
        if action == Action.play:
            if self.__play:
                print("Pause")
                self.__play = False
            else:
                print("Play")
                self.__play = True
        elif action == Action.close:
            self.__run = False
