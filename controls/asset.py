from utils.database import assets
from utils.utils import is_image
from bson import ObjectId
from functools import cache

@cache
def get_asset(id):
    result = assets.find_one({'_id': id})
    if result is None:
        raise Exception("Image not found")
    else:
        return result['data']

def save_asset(data):
    if not is_image(data):
        raise Exception('Data is not an image')
    id = str(ObjectId())
    assets.insert_one({'_id': id, 'data': data})
    return id