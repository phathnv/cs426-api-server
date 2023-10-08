from flask import Blueprint, request
from controls.ingredient import search_ingredients, get_all_ingredients, detect_ingredient

ingredient_blueprint = Blueprint('ingredient', __name__)

@ingredient_blueprint.route('/ingredients', methods=['GET'])
def all_endpoint():
    return get_all_ingredients()

@ingredient_blueprint.route('/ingredient/<text>', methods=['GET'])
def search_endpoint(text):
    return search_ingredients(text)

@ingredient_blueprint.route('/ingredient/detect', methods=['POST'])
def detect_endpoint():
    try:
        data = request.get_data()
        return {'success': True,
                'message': detect_ingredient(data)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}
