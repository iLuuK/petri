from model.dbconnector import DBConnector
from shared.iCell import ICell
from shared.iModel import IModel
from shared.iPetri import IPetri
from model.data.petri import Petri
from model.data.cell import Cell
from model.data.behavior.classicLive import ClassicLive
from model.data.behavior.nagLive import NagLive
from model.dao.daoPetri import DAOPetri
import json


class Model(IModel):
    def __init__(self):
        self.__dbConnector = DBConnector()
        self.__daoPetri = DAOPetri(self.__dbConnector)
        self.__loadConf()
#        self.__petri: IPetri = self.__daoPetri.load(225426424)
        self.__petri: IPetri = Petri(self.__petriPythonConf["width"], self.__petriPythonConf["height"])
        for i in range(self.__petriPythonConf["nbCells"]):
            self.__petri.addCell(Cell(self.__petri, NagLive(), 0))

    def getPetriById(self, idPetri: int) -> IPetri:
        return self.__petri

    def getCells(self) -> [ICell]:
        return self.__petri.getCells()

    def __loadConf(self):
        with open('conf/petriPython.json') as jsonfile:
            self.__petriPythonConf = json.load(jsonfile)

    def savePetri(self):
        self.__daoPetri.save(self.__petri)
