from classes.Database.MongoDBManager import MongoDBCollectionManager, MongoDBManager


collection = "Users"
mongoDBManager: MongoDBManager = MongoDBCollectionManager(
).get_mongodb_manager(collection)
