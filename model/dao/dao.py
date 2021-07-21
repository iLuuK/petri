from model.dbconnector import DBConnector
import json


class DAO:
    def __init__(self, dbConnector: DBConnector, entity: str):
        self.__dbConnector = dbConnector
        self.__entity = entity

    def getDBConnector(self) -> DBConnector:
        return self.__dbConnector

    def getCollection(self):
        return self.__dbConnector.getCollection(self.__entity)
