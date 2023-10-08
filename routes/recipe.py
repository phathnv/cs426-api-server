from flask import Blueprint, request
from models.user import User
from datetime import datetime
from controls.recipe import get_recipe, search_recipe, get_liked_recipes, like_recipe, popular_recipes, upload_recipe, update_recipe, delete_recipe, suggest_recipe
from controls.user import auth_user

recipe_blueprint = Blueprint('recipe', __name__)

@recipe_blueprint.route('/recipes', methods=['GET'])
def popular_endpoint():
    return popular_recipes()

@recipe_blueprint.route('/recipe/<recipe_id>', methods=['GET'])
def recipe_endpoint(recipe_id):
    try:
        recipe = get_recipe(recipe_id)
        return recipe
    except Exception as e:
        return str(e)
    
@recipe_blueprint.route('/recipe/search/<text>', methods=['GET'])
def search_endpoint(text):
    try:
        return search_recipe(text)
    except Exception as e:
        return str(e)
    
@recipe_blueprint.route('/recipe/like', methods=['GET', 'POST'])
def like_endpoint():
    try:
        user = auth_user(request)
        if request.method == 'GET':
            return get_liked_recipes(user)
        else:
            return {'success': True,
                    'data': like_recipe(user, request.get_json())}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}
    

@recipe_blueprint.route('/recipe/upload', methods=['POST'])
def upload_endpoint():
    try:
        user = auth_user(request)
        return {'success': True,
                'data': upload_recipe(user, request.get_json())}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}
    
@recipe_blueprint.route('/recipe/update', methods=['POST'])
def update_endpoint():
    try:
        user = auth_user(request)
        return {'success': True,
                'data': update_recipe(user, request.get_json())}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}
    
@recipe_blueprint.route('/recipe/delete/<recipe_id>', methods=['POST'])
def delete_endpoint(recipe_id):
    try:
        user = auth_user(request)
        delete_recipe(user, recipe_id)
        return {'success': True,
                'message': 'delete successfully'}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}

    
@recipe_blueprint.route('/suggestrecipe', methods=['POST'])
def suggest_endpoint():
    try:
        return suggest_recipe(request.get_json()['ingredients'])
    except KeyError as e:
        return 'Missing ' + str(e)
    except Exception as e:
        return str(e)
