from flask import Blueprint, jsonify, request
from models.user import User
from datetime import datetime
from controls.user import create_user, login, auth_user, update_profile, change_password, get_user, forgot_password, reset_password, logout

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/user/<user_id>', methods=['GET'])
def user_endpoint(user_id):
    try:
        user = get_user(user_id)
        return user.to_json()
    except Exception as e:
        return str(e)

@user_blueprint.route('/user/register', methods=['POST'])
def register_endpoint():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = create_user(email, password)
        return {'success': True,
                'message': 'Register successfully'}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}

@user_blueprint.route('/user/login', methods=['POST'])
def login_endpoint():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        token = login(email, password)
        return {'success': True,
                'auth_token': token}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}
    
@user_blueprint.route('/user/logout', methods=['POST'])
def logout_endpoint():
    try:
        data = request.get_json()
        token = data['auth_token']
        logout(token)
        return {'success': True,
                'message': 'Logout successfully'}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}

@user_blueprint.route('/user/changepassword', methods=['POST'])
def changepassword_endpoint():
    try:
        data = request.get_json()
        user = auth_user(request)
        oldpwd = data['old_password']
        newpwd = data['new_password']
        change_password(user, oldpwd, newpwd)
        return {'success': True,
                'message': 'Password changed'}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}

@user_blueprint.route('/user/profile', methods=['GET', 'POST'])
def profile_endpoint():
    try:
        user = auth_user(request)
        if request.method == 'GET':
            return user.to_json()
        else: 
            user = update_profile(user, request.get_json())
            return {
                'success': True,
                'data': user.to_json()
            }
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}

@user_blueprint.route('/user/forgotpassword', methods=['POST'])
def forgot_password_endpoint():
    try:
        data = request.get_json()
        forgot_password(data['email'])
        return {'success': True,
                'message': 'Email sent successfully'}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}

@user_blueprint.route('/user/resetpassword', methods=['POST'])
def reset_password_endpoint():
    try:
        data = request.get_json()
        reset_password(data['email'], data['code'], data['password'])
        return {'success': True,
                'message': 'Reset password successfully'}
    except KeyError as e:
        return {'success': False,
                'message': 'missing ' + str(e)}
    except Exception as e:
        return {'success': False,
                'message': str(e)}
