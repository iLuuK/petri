from model.dao.dao import DAO
from model.dbconnector import DBConnector
from shared.iPetri import IPetri
from model.data.petri import Petri
from model.data.cell import Cell
from model.data.cell import Color
from model.data.behavior.classicDie import ClassicDie


class DAOPetri(DAO):
    def __init__(self, dbConnector: DBConnector):
        DAO.__init__(self, dbConnector, "Petris")

    def save(self, petri: IPetri):
        cellsDict = []
        for cell in petri.getCells():
            cellDict = {
                "_id": cell.getId(),
                "x": cell.getX(),
                "y": cell.getY(),
                "birthStep": cell.getBirthStep(),
                "color":  {
                    "red": cell.getColor().getRed(),
                    "green": cell.getColor().getGreen(),
                    "blue": cell.getColor().getBlue()
                }
            }
            cellsDict.append(cellDict)

        petriDict = {"_id": petri.getId(),
                     "width": petri.getWidth(),
                     "height": petri.getHeight(),
                     "cells": cellsDict}
        self.getCollection().insert(petriDict)

    def load(self, myId: int):
        petriDict = self.getCollection().find({"_id": myId})[0]
        petri = Petri(petriDict["width"], petriDict["height"])
        petri.setId(petriDict["_id"])
        for cellDict in petriDict["cells"]:
            cell = Cell(petri, ClassicDie(), cellDict["birthStep"])
            cell.setId(cellDict["_id"])
            cell.setX(cellDict["x"])
            cell.setY(cellDict["y"])
            cell.setColor(Color(cellDict["color"]["red"], cellDict["color"]["green"], cellDict["color"]["blue"]))
            petri.addCell(cell)
        return petri
