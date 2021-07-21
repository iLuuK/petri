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
        while self.__run:
            if self.__play:
                self.__view.show()
                oldCells = self.__model.getCells().copy()
                for cell in oldCells:
                    cell.live()
            else:
                time.sleep(1)
        self.__model.savePetri()

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
