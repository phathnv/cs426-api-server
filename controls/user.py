from utils.database import users, sessions
from utils.utils import hash_password, gen_token, datetime_to_str, gen_reset_pwd_code, b64_to_bytes
from utils.gmail import send_reset_code
from models.user import User
from models.session import Session
from controls.asset import get_asset, save_asset
from datetime import datetime, timedelta
from bson import ObjectId
import os

def get_user(id):
    data = users.find_one(id)
    if data is None:
        raise Exception('User not found')
    return User(**data)

def create_user(email, password):
    if users.find_one({'email': email}) != None:
        raise Exception('Email is already registered for other account')
    time = datetime_to_str(datetime.utcnow().date())
    user = User(
        _id = str(ObjectId()),
        _token = None,
        _pwd = hash_password({'time': time, 'password': password}),
        email = email,
        created_at = time,
        username = None,
        avatar = None,
        dob = None,
        country = None,
        posts = [],
        likes = [],
    )
    users.insert_one(user.to_dict())
    return user

def login(email, password):
    user = users.find_one({'email': email})
    if user == None:
        raise Exception('Email not exists')
    
    user['_id'] = str(user['_id'])
    user = User(**user)
    if user.pwd == hash_password({'time': datetime_to_str(user.created_at), 'password': password}):
        token = gen_token()
        session = Session(_id = str(ObjectId()), token = token, user_id = user.id, exp_time = datetime.utcnow() + timedelta(days = 1))
        sessions.insert_one(session.to_dict())
        return token
    else:
        raise Exception('Incorrect password')

def logout(token):
    sessions.delete_one({'token': token})

def auth_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        raise Exception('Authorization required')

    session = sessions.find_one({'token': token})
    if session is None:
        raise Exception('Unauthorized access: Invalid token')
    session = Session(**session)
    if session.exp_time < datetime.utcnow():
        raise Exception('Unauthorized access: Session expired')
    session.exp_time = datetime.utcnow() + timedelta(days = 1)
    sessions.update_one({'_id': session.id}, {'$set': session.to_dict()})
    user = users.find_one(session.user_id)
    assert(user is not None)
    return User(**user)

def change_password(user, oldpwd, newpwd):
    # check old
    if user.pwd != hash_password({'time': datetime_to_str(user.created_at), 'password': oldpwd}):
        raise Exception('Incorrect password')
    # update
    pwd = hash_password({'time': datetime_to_str(user.created_at), 'password': newpwd})
    users.update_one({"_id": user.id}, {"$set": {"_pwd": pwd}})
    sessions.delete_many({'user_id': user.id})
    return

def update_profile(user, data):
    updatedata = dict()
    for field in ['dob', 'country']:
        if field in data.keys():
            updatedata[field] = data[field]
    if 'avatar' in data.keys():
        updatedata['avatar'] = save_asset(b64_to_bytes(data['avatar']))
    if 'username' in data.keys():
        new = data['username']
        old = user.username
        if new != old and users.find_one({'username': new}) is not None:
            raise Exception('Username already exists')
        updatedata['username'] = new
    if 'email' in data.keys():
        new = data['email']
        old = user.email
        if new != old and users.find_one({'email': new}) is not None:
            raise Exception('Email already exists')
        updatedata['email'] = new
    users.update_one({"_id": user.id}, {"$set": updatedata})
    user = users.find_one({"_id": user.id})
    user['_id'] = str(user['_id'])
    return User(**user)

def forgot_password(email):
    user = users.find_one({'email': email})
    if user == None:
        raise Exception('Email not exists')
    
    user = User(**user)
    user.code = gen_reset_pwd_code()
    user.code_exp = datetime.utcnow() + timedelta(minutes=10)
    send_reset_code(user.email, user.username if user.username is not None else 'guest', user.code)
    users.update_one({'_id': user.id}, {'$set': user.to_dict()})
    return

def reset_password(email, code, password):
    user = users.find_one({'email': email})
    if user == None:
        raise Exception('Email not exists')
    user = User(**user)
    if user.code != code:
        raise Exception('Incorrect code')
    if user.code_exp < datetime.utcnow():
        raise Exception('Code expired, plese request a new one')    

    user.code = None
    user.code_exp = None
    user.pwd = hash_password({'time': datetime_to_str(user.created_at), 'password': password})
    users.update_one({'_id': user.id}, {'$set': user.to_dict()})
    sessions.delete_many({'user_id': user.id})
    return