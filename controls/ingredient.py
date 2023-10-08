from utils.database import ingredients
from models.ingredient import ListIngredient
from ml.yolo import detect_ingredients
from functools import cache

def update_ingredients(a):
    list_ingredient = ListIngredient(**ingredients.find_one('all')).list
    for ingredient in a:
        try:
            name = ingredient['name']
            if name not in list_ingredient:
                list_ingredient.append(name)
        except:
            pass
    ingredients.update_one({'_id': 'all'}, {'$set': {'list': list_ingredient}})

def search_ingredients(text):
    list_ingredient = ListIngredient(**ingredients.find_one('all')).list
    result = []
    for ingredient in list_ingredient:
        if text in ingredient:
            result.append(ingredient)
    return result

@cache
def get_all_ingredients():
    list_ingredient = ListIngredient(**ingredients.find_one('all')).list
    return list_ingredient

def check_ingredients(ingres):
    list_ingredient = ListIngredient(**ingredients.find_one('all')).list
    for ingre in ingres:
        if ingre not in list_ingredient:
            raise Exception(f'Invalid ingredient: {ingre}')
    return

def detect_ingredient(data):
    return detect_ingredients(data)
