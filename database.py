from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure, BulkWriteError
import logging
from config import MONGO_CONNECT, MONGO_DB_NAME


class MongoDatabase:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__connect()
        self.bulk_delete_points_of_interest()

    def __connect(self):
        try:
            self.client = MongoClient(MONGO_CONNECT, serverSelectionTimeoutMS=2000)
            self.db = self.client.get_database(MONGO_DB_NAME)
        except ServerSelectionTimeoutError:
            self.logger.error("Failed to connect to MongoDB server")

    def insert_many(self, data: list):
        self.db['address'].insert_many(data)

    def bulk_delete_points_of_interest(self):
        try:
            result = self.db['address'].delete_many({})
            deleted_count = result.deleted_count
            self.logger.info(f"Points of interest bulk deleted: {deleted_count} deleted")
        except Exception as e:
            self.logger.error(f"Error bulk deleting points of interest: {str(e)}")

    def insert_categories(self, data):
        self.db['categories'].delete_many({})
        self.db['categories'].insert_one(data)

    def get_all_pois(self):
        return self.db['address'].find({})

    def create_pois_collection(self):
        pois_collection = self.db['pois_names']

        try:
            pois_collection.create_index([('sub_category', 1), ('category', 1), ('name', 1)], unique=True)
        except OperationFailure as e:
            print(f"Failed to create index: {e}")

    def save_pois(self, pois: set):
        try:
            self.db['pois_names'].insert_many(pois, ordered=False)
        except BulkWriteError as e:
            print(f"Some documents were not inserted: {e.details['writeErrors']}")
