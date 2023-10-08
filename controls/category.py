from utils.database import users, categories
from models.category import Category
from functools import cache

@cache
def get_all_category():
    all_cat = categories.find({})
    result = []
    for cat in all_cat:
        result.append(Category(**cat).to_json())
    return result

def get_category_recipes(name):
    cat = categories.find_one({"name" : name})
    if cat == None:
        raise Exception('Category not exists')

    return Category(**cat).recipes
