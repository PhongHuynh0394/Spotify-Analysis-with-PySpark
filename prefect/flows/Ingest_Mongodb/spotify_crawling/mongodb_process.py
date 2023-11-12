import pymongo


class MongoDB:
    def __init__(self, client: pymongo.MongoClient):
        self.client = client

    def __check_database_exist(self, db: pymongo.database.Database):
        """_summary_

        Args:
            db (pymongo.database.Database): Database object

        Returns:
            bool: True if database exist, False otherwise
        """
        db_name = db.name
        return True if db_name in self.client.list_database_names() else False

    def create_database(self, db_name: str):
        """_summary_

        Args:
            db_name (str): Name of database

        Returns:
            pymongo.database.Database: Database object
        """
        return self.client[db_name]

    def __check_collection_exist(self, db: pymongo.database.Database, coll: pymongo.collection.Collection):
        """_summary_

        Args:
            db (pymongo.database.Database): Database object
            coll (pymongo.collection.Collection): Collection object

        Returns:
            bool: True if collection exist, False otherwise
        """
        coll_name = coll.name
        return True if coll_name in db.list_collection_names() else False

    def create_collection(self, collection_name: str, db: pymongo.database.Database):
        """_summary_

        Args:
            db (pymongo.database.Database): Database object
            collection_name (str): Name of collection

        Returns:
            pymongo.collection.Collection: Collection object
        """
        new_coll = db[collection_name]
        return new_coll

    def insert_many(self, data, db: pymongo.database.Database, coll: pymongo.collection.Collection):
        """_summary_

        Args:
            data (__type__): Data to be inserted
            coll (pymongo.collection.Collection): Collection object
        """
        coll.insert_many(data)

    def insert_one(self, data, db: pymongo.database.Database, coll: pymongo.collection.Collection):
        """_summary_

        Args:
            collection_name (str): Name of collection
            data (json): Data to be inserted
        """
        coll.insert_one(data)
