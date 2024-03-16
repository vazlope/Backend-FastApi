from pymongo import MongoClient
from DB.user_info.db_credentials import MongoUser

#! Base de datos local
#db_client = MongoClient().local

#! Base de datos en la nube MongoDB
cloud = MongoUser()
URL = f"mongodb+srv://{cloud.user}:{cloud.pass_db}@{cloud.cluster}.ib1npyu.mongodb.net/?retryWrites=true&w=majority&appName={cloud.cluster}"
print(URL)
db_client = MongoClient(URL).test

# user: pablovazquezlopez
# password: user