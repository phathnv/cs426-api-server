from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

client = MongoClient(os.getenv('DATABASE_URI'), server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    database = client.get_database('recipe-app')
    users = database.get_collection('users')
    categories = database.get_collection('categories')
    assets = database.get_collection('assets')
    recipes = database.get_collection('recipes')
    ingredients = database.get_collection('ingredients')
    sessions = database.get_collection('sessions')
except Exception as e:
    print(e)
