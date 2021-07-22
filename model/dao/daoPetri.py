from model.dao.dao import DAO
from model.data.behavior.grassDie import GrassDie
from model.data.behavior.herbivorLive import HerbivorLive
from model.dbconnector import DBConnector
from shared.cellType import CellType
from shared.iPetri import IPetri
from model.data.petri import Petri
from model.data.cell import Cell
from model.data.cell import Color


class DAOPetri(DAO):
    def __init__(self, dbConnector: DBConnector):
        DAO.__init__(self, dbConnector, "Petris")

    def savePetri(self, petri: IPetri):
        petriDict = {"_id": petri.getId(),
                     "width": petri.getWidth(),
                     "height": petri.getHeight()}
        self.getCollection().insert(petriDict)

    def saveRound(self, petri: IPetri):
        cellsDict = []
        for cell in petri.getCells():
            cellDict = {
                "_id": cell.getId(),
                "x": cell.getX(),
                "y": cell.getY(),
                "birthStep": cell.getBirthStep(),
                "color": {
                    "red": cell.getColor().getRed(),
                    "green": cell.getColor().getGreen(),
                    "blue": cell.getColor().getBlue()
                },
                "isAlive": cell.getIsAlive(),
                "cellType": cell.getType().value,
                "energy": cell.getEnergy()
            }
            cellsDict.append(cellDict)

        self.getCollection().update_one({"_id": petri.getId()}, {"$push": {"Rounds": cellsDict}})
        self.getCollection().find_one_and_update({"_id": petri.getId()},
                                                 {"$set": {"numberRound": petri.getNumberRound()}})
        print(petri.getNumberRound())

    def loadRound(self, myId: int, round: int):
        petriDict = self.getCollection().find({"_id": myId})[0]
        petri = Petri(petriDict["width"], petriDict["height"])
        petri.setNumberRound(petriDict["numberRound"])
        petri.setId(petriDict["_id"])
        for cellDict in petriDict["Rounds"][round]:
            if hasattr(cellDict["cellType"], "__len__"):
                if cellDict["cellType"][0] == 1:
                    cell = Cell(petri, HerbivorLive(), cellDict["birthStep"], CellType.HERBIVOR)
                elif cellDict["cellType"][0] == 4:
                    cell = Cell(petri, GrassDie(), cellDict["birthStep"], CellType.GRASS)
            else:
                if cellDict["cellType"] == 1:
                    cell = Cell(petri, HerbivorLive(), cellDict["birthStep"], CellType.HERBIVOR)
                elif cellDict["cellType"] == 4:
                    cell = Cell(petri, GrassDie(), cellDict["birthStep"], CellType.GRASS)

            cell.setId(cellDict["_id"])
            cell.setX(cellDict["x"])
            cell.setY(cellDict["y"])
            cell.setIsAlive(cellDict["isAlive"])
            cell.setEnergy(cellDict["energy"])
            cell.setColor(Color(cellDict["color"]["red"], cellDict["color"]["green"], cellDict["color"]["blue"]))
            petri.addCellFirstTime(cell)
        return petri

    def loadPetri(self, myId: int):
        petriDict = self.getCollection().find({"_id": myId})[0]
        petri = Petri(petriDict["width"], petriDict["height"])
        petri.setNumberRound(petriDict["numberRound"])
        petri.setId(petriDict["_id"])
        return petri
