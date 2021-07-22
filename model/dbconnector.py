import gridfs
from pymongo import MongoClient
import json


class DBConnector:
    def __init__(self):
        self.__db: MongoClient
        self.__dbConf = {}
        self.__loadConf()
        self.__DBConnect()
        self.__fs: gridfs

    def __DBConnect(self):
        __mongoDbConf = self.__dbConf["mongodb"]
        self.__db = MongoClient(host=__mongoDbConf["host"], port=__mongoDbConf["port"])[__mongoDbConf["database"]]
        self.__fs = gridfs.GridFS(self.__db)

    def __loadConf(self):
        with open('conf/dbconf.json') as jsonfile:
            self.__dbConf = json.load(jsonfile)

    def getCollection(self, collection: str):
        return self.__db[collection]

    def getFs(self) -> gridfs:
        return self.__fs

