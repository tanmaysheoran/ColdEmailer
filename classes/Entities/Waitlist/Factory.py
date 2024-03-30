from classes.Database.MongoDBManager import MongoDBCollectionManager, MongoDBManager


collection = "Waitlist"
mongoDBManager: MongoDBManager = MongoDBCollectionManager(
).get_mongodb_manager(collection)
