from model.data.behavior.grassDie import GrassDie
from model.data.behavior.herbivorLive import HerbivorLive
from model.data.behavior.carnivorLive import CarnivorLive
from model.data.behavior.omnivorLive import OmenivorLive
from model.dbconnector import DBConnector
from shared.cellType import CellType
from shared.iCell import ICell
from shared.iModel import IModel
from shared.iPetri import IPetri
from model.data.petri import Petri
from model.data.cell import Cell
from model.dao.daoPetri import DAOPetri
import json


class Model(IModel):
    def __init__(self):
        self.__dbConnector = DBConnector()
        self.__daoPetri = DAOPetri(self.__dbConnector)
        self.__loadConf()
#        self.__petri: IPetri = self.__daoPetri.load(225426424)
        self.__petri: IPetri = Petri(self.__petriPythonConf["width"], self.__petriPythonConf["height"])
        for i in range(self.__petriPythonConf["nbCellsHerbivor"]):
            self.__petri.addCellFirstTime(Cell(self.__petri, HerbivorLive(), 0, CellType.HERBIVOR))
        for i in range(self.__petriPythonConf["nbCellsCarnivor"]):
            self.__petri.addCellFirstTime(Cell(self.__petri, CarnivorLive(), 0, CellType.CARNIVOROUS))
        for i in range(self.__petriPythonConf["nbCellsCarnivor"]):
            self.__petri.addCellFirstTime(Cell(self.__petri, OmenivorLive(), 0, CellType.OMNIVOROUS))
        for i in range(self.__petriPythonConf["nbCellsOmnivor"]):
            self.__petri.addCellFirstTime(Cell(self.__petri, GrassDie(), 0, CellType.GRASS))

    def getPetriById(self, idPetri: int) -> IPetri:
        return self.__petri

    def getCells(self) -> [ICell]:
        return self.__petri.getCells()

    def __loadConf(self):
        with open('conf/petriPython.json') as jsonfile:
            self.__petriPythonConf = json.load(jsonfile)

    def savePetri(self):
        self.__daoPetri.save(self.__petri)
