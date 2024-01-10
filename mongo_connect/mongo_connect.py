import pymongo
from pymongo.mongo_client import MongoClient
from collections.abc import MutableMapping

config = {
    'server': '130.193.52.52',
    'port': '27017',
    'bd_name': 'int',
    'user': 'modul',
    'psw': 'krendel'
}
myclient = MongoClient(f"mongodb://{config['user']}:{config['psw']}@{config['server']}:{config['port']}")


database_names = myclient.list_database_names()
print(database_names)