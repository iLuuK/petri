from uuid import UUID

from model.dao.dao import DAO
from model.data.behavior.grassDie import GrassDie
from model.data.behavior.herbivorLive import HerbivorLive
from model.dbconnector import DBConnector
from shared.cellType import CellType
from shared.iCell import ICell
from shared.iPetri import IPetri
from model.data.petri import Petri
from model.data.cell import Cell
from model.data.cell import Color


class DAORound(DAO):
    def __init__(self, dbConnector: DBConnector):
        DAO.__init__(self, dbConnector, "Round")

    def saveRound(self, petri: IPetri, roundId: UUID):
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
                "energy": cell.getEnergy(),
                "scale": cell.getScale()
            }
            cellsDict.append(cellDict)

        round = {
            "_id": roundId,
            "cells": cellsDict
        }

        self.getCollection().insert(round)

    def loadRound(self, id: UUID, petri: IPetri) -> [ICell]:
        roundDict = self.getCollection().find({"_id": id})[0]
        cells = []
        for cellDict in roundDict["cells"]:
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
            cell.setScale(cellDict["scale"])
            cell.setColorWithoutEffect(Color(cellDict["color"]["red"], cellDict["color"]["green"], cellDict["color"]["blue"]))
            cells.append(cell)
        return cells