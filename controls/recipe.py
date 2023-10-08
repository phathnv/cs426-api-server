from utils.database import recipes, users, categories, assets
from models.recipe import Recipe
from models.asset import Asset
from models.category import Category
from models.user import User
from controls.asset import save_asset
from datetime import datetime
from bson import ObjectId
from utils.utils import b64_to_bytes
from controls.ingredient import check_ingredients

def add_user_info(recipe):
    user = User(**users.find_one(recipe['author']))
    recipe['user_avatar'] = user.avatar
    recipe['username'] = user.username
    return recipe

def get_recipe(id):
    data = recipes.find_one(id)
    if data is None:
        raise Exception('Recipe not exist')
    return add_user_info(Recipe(**data).to_json())  

def search_recipe(text):
    result = []
    for x in recipes.find({'name': {'$regex': f".*{text}.*"}}):
        recipe = Recipe(**x)
        result.append({'name': recipe.name, 'id': recipe.id})
    return result

def get_liked_recipes(user):
    result = []
    for id in user.likes:
        result.append(add_user_info(Recipe(**recipes.find_one(id)).to_json()))
    return result

def like_recipe(user, data):
    id = data['recipe_id']
    like = bool(data['like'])
    recipe = recipes.find_one(id)
    if recipe is None:
        raise Exception('Recipe not exist')
    
    recipe = Recipe(**recipe)
    if like:
        if id not in user.likes:
            user.likes.append(id)
            recipe.num_liked = recipe.num_liked + 1
    else:
        if id in user.likes:
            user.likes.remove(id)
            recipe.num_liked = recipe.num_liked - 1

    users.update_one({'_id': user.id}, {'$set': {'likes': user.likes}})
    recipes.update_one({'_id': recipe.id}, {'$set': {'num_liked': recipe.num_liked}})
    return recipe.to_json()

def popular_recipes():
    result = []
    for x in recipes.find({}).sort('num_liked', -1).limit(10):
        result.append(Recipe(**x).id)
    return result

def upload_recipe(user, data):
    recipe = dict()
    recipe['_id'] = str(ObjectId())
    recipe['author'] = user.id
    recipe['num_liked'] = 0
    recipe['name'] = data['name']
    recipe['description'] = data['description']
    recipe['category'] = data['category']
    recipe['details'] = data['details']
    recipe['nutrition'] = data['nutrition']
    recipe['ingredients'] = data['ingredients']
    recipe['directions'] = data['directions']
    recipe['imageId'] = None
    recipe = Recipe(**recipe)
    check_ingredients([ingre['name'] for ingre in recipe.ingredients])

    user.posts.append(recipe.id)

    category = categories.find_one({'name': recipe.category})
    if category is None:
        raise Exception("Category not exist")
    category = Category(**category)
    category.recipes.append(recipe.id)

    asset = None
    if 'image' in data.keys() and data['image'] is not None:
        recipe.imageId = save_asset(b64_to_bytes(data['image']))

    recipes.insert_one(recipe.to_dict())
    users.update_one({'_id': user.id}, {'$set': user.to_dict()})
    categories.update_one({'_id': category.id}, {'$set': category.to_dict()})
    if asset is not None:
        assets.insert_one(asset.to_dict())

    return recipe.to_json()

def update_recipe(user, data):
    recipe = recipes.find_one(data['_id'])
    if recipe is None:
        raise Exception("Recipe not exist")
    if recipe['author'] != user.id:
        raise Exception('Unauthorized access: this recipe is not your own')
    
    old_category = categories.find_one({'name': recipe['category']})
    assert(old_category is not None)
    old_category = Category(**old_category)
    old_category.recipes.remove(recipe['_id'])

    for field in ['name', 'description', 'category', 'details', 'nutrition', 'ingredients', 'directions']:
        recipe[field] = data[field]
    recipe = Recipe(**recipe)
    check_ingredients([ingre['name'] for ingre in recipe.ingredients])

    new_category = categories.find_one({'name': recipe.category})
    if new_category is None:
        raise Exception("Category not exist")
    new_category = Category(**new_category)
    if recipe.id not in new_category.recipes:
        new_category.recipes.append(recipe.id)

    asset = None
    if 'image' in data.keys() and data['image'] is not None:
        recipe.imageId = save_asset(b64_to_bytes(data['image']))

    recipes.update_one({'_id': recipe.id}, {'$set': recipe.to_dict()})
    categories.update_one({'_id': old_category.id}, {'$set': old_category.to_dict()})
    categories.update_one({'_id': new_category.id}, {'$set': new_category.to_dict()})
    if asset is not None:
        assets.insert_one(asset.to_dict())

    return recipe.to_json()

def suggest_recipe(ingredients):
    check_ingredients(ingredients)
    candidates = []
    for recipe in recipes.find({}):
        recipe = Recipe(**recipe)
        s = set()
        for ingre in recipe.ingredients:
            s.add(ingre['name'])
        count = 0
        for ingre in ingredients:
            if ingre in s:
                count = count + 1
        if count > 0:
            candidates.append((count, recipe.num_liked, recipe.id))
    candidates.sort(reverse=True)

    result = []
    for candidate in candidates[:50]:
        _, _, id = candidate
        result.append(id) 
    return result

def delete_recipe(user, recipe_id):
    recipe = recipes.find_one(recipe_id)
    if recipe is None:
        raise Exception("Recipe not exist")
    if recipe['author'] != user.id:
        raise Exception('Unauthorized access: this recipe is not your own')
    recipe = Recipe(**recipe)

    category = categories.find_one({'name': recipe.category})
    assert(category is not None)
    category = Category(**category)

    user.posts.remove(recipe.id)
    category.recipes.remove(recipe.id)

    recipes.delete_one({'_id': recipe.id})
    # remove ref
    users.update_one({'_id': user.id}, {'$set': user.to_dict()})
    categories.update_one({'_id': category.id}, {'$set': category.to_dict()})

    # remove likes
    for u in users.find({'likes': {'$all': [recipe.id]}}):
        u = User(**u)
        u.likes.remove(recipe.id)
        users.update_one({'_id': u.id}, {'$set': u.to_dict()})

    return
