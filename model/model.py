from uuid import UUID

from model.dao.daoRound import DAORound
from model.data.behavior.carnivorousLive import CarnivorousLive
from model.data.behavior.grassDie import GrassDie
from model.data.behavior.herbivorLive import HerbivorLive
from model.data.behavior.omnivorous import OmnivorousLive
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
        self.__daoRound = DAORound(self.__dbConnector)
        self.__loadConf()
        self.__petriIdLoad = self.__petriPythonConf["loadPetriId"]
        self.__isLoadPetri = self.__petriPythonConf["isLoadPetri"]
        self.__petri: IPetri = Petri(self.__petriPythonConf["width"], self.__petriPythonConf["height"])
        for i in range(self.__petriPythonConf["nbCellsHerbivor"]):
            self.__petri.addCellFirstTime(Cell(self.__petri, HerbivorLive(), 0, CellType.HERBIVOR))
        for i in range(self.__petriPythonConf["nbCellsGrass"]):
            self.__petri.addCellFirstTime(Cell(self.__petri, GrassDie(), 0, CellType.GRASS))
        for i in range(self.__petriPythonConf["nbCellsCarnivorous"]):
                self.__petri.addCellFirstTime(Cell(self.__petri, CarnivorousLive(), 0, CellType.CARNIVOROUS))
        for i in range(self.__petriPythonConf["nbCellsOmnivorous"]):
                self.__petri.addCellFirstTime(Cell(self.__petri, OmnivorousLive(), 0, CellType.OMNIVOROUS))

    def getRoundCell(self, round: int):
        cells = self.__daoRound.loadRound(self.__petri.getRoundsId()[round], self.__petri)
        self.__petri.setCells(cells)

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

    def saveRound(self, uuid: UUID):
        self.__daoPetri.saveRound(self.__petri, uuid)
        self.__daoRound.saveRound(self.__petri, uuid)

    def updateNumberRound(self):
        self.__petri.updateNumberRound()
