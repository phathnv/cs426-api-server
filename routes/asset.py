from flask import Blueprint, send_file
from controls.asset import get_asset
import io

asset_blueprint = Blueprint('asset', __name__)

@asset_blueprint.route('/asset/<id>', methods=['GET'])
def get_asset_endpoint(id):
    try:
        return send_file(
            io.BytesIO(get_asset(id)),
            mimetype='image/jpeg',
            download_name='%s.jpeg' % id)
    except Exception as e:
        return str(e)