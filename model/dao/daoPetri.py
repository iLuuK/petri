from model.dao.dao import DAO
from model.data.behavior.grassDie import GrassDie
from model.data.behavior.herbivorLive import HerbivorLive
from model.dbconnector import DBConnector
from shared.cellType import CellType
from shared.iPetri import IPetri
from model.data.petri import Petri
from model.data.cell import Cell
from model.data.cell import Color
import uuid

class DAOPetri(DAO):
    def __init__(self, dbConnector: DBConnector):
        DAO.__init__(self, dbConnector, "Petris")

    def savePetri(self, petri: IPetri):
        petriDict = {"_id": petri.getId(),
                     "width": petri.getWidth(),
                     "height": petri.getHeight()}
        self.getCollection().insert(petriDict)

    def saveRound(self, petri: IPetri, uuid: uuid.UUID):
        self.getCollection().update_one({"_id": petri.getId()}, {"$push": {"rounds": uuid}})
        self.getCollection().find_one_and_update({"_id": petri.getId()},
                                                 {"$set": {"numberRound": petri.getNumberRound()}})


    def loadPetri(self, myId: int):
        petriDict = self.getCollection().find({"_id": myId})[0]
        petri = Petri(petriDict["width"], petriDict["height"])
        petri.setNumberRound(petriDict["numberRound"])
        petri.setId(petriDict["_id"])
        petri.setRoundsId(petriDict['rounds'])
        return petri
