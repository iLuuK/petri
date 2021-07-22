from model.data.behavior.grassDie import GrassDie
from model.data.behavior.herbivorLive import HerbivorLive
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
        self.__petriIdLoad = self.__petriPythonConf["loadPetriId"]
        self.__isLoadPetri = self.__petriPythonConf["isLoadPetri"]
        self.__petri: IPetri = Petri(self.__petriPythonConf["width"], self.__petriPythonConf["height"])
        for i in range(self.__petriPythonConf["nbCellsHerbivor"]):
            self.__petri.addCellFirstTime(Cell(self.__petri, HerbivorLive(), 0, CellType.HERBIVOR))
        for i in range(self.__petriPythonConf["nbCellsGrass"]):
            self.__petri.addCellFirstTime(Cell(self.__petri, GrassDie(), 0, CellType.GRASS))

    def getRoundCell(self, round: int):
        self.__petri = self.__daoPetri.loadRound(self.__petri.getId(), round)

    def getNumberRound(self):
        return self.__petri.getNumberRound()

    def getIsLoadPetri(self) -> bool:
        return self.__isLoadPetri

    def getLoadPetriId(self) -> int:
        return self.__petriIdLoad

    def setLoadPetri(self):
        self.__petri = self.__daoPetri.loadPetri(self.__petriIdLoad)

    def getPetriById(self, idPetri: int) -> IPetri:
        return self.__petri

    def getCells(self) -> [ICell]:
        return self.__petri.getCells()

    def __loadConf(self):
        with open('conf/petriPython.json') as jsonfile:
            self.__petriPythonConf = json.load(jsonfile)

    def savePetri(self):
        self.__daoPetri.savePetri(self.__petri)

    def saveRound(self):
        self.__daoPetri.saveRound(self.__petri)

    def updateNumberRound(self):
        self.__petri.updateNumberRound()
