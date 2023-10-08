from flask import Blueprint, jsonify, request
from models.category import Category
from datetime import datetime
from controls.category import get_all_category, get_category_recipes

category_blueprint = Blueprint('category', __name__)


@category_blueprint.route('/categories', methods=['GET'])
def all_cat_endpoint():
    return get_all_category()

@category_blueprint.route('/category/<name>', methods=['GET'])
def cat_endpoint(name):
    try:
        return get_category_recipes(name)
    except Exception as e:
        return str(e)