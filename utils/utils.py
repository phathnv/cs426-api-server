import jwt
import os
from hashlib import sha256
import base64
import random
from PIL import Image
import io

def hash_password(data): 
    return sha256(jwt.encode(data, os.getenv('SECRET'), algorithm="HS256").encode()).hexdigest()

def gen_token(): 
    #data['random'] = os.urandom(8).hex()
    #return hash_password(data)
    return sha256(os.urandom(16).hex().encode()).hexdigest()

def gen_reset_pwd_code():
    return '{:08d}'.format(random.randint(0, 99999999))

def datetime_to_str(date):
    return date.strftime(os.getenv('DATETIME_FORMAT'))

def b64_to_bytes(s):
    return base64.b64decode(str(s))

def bytes_to_b64(bytes):
    return base64.b64encode(bytes).decode()

def is_image(data):
    try:
        image = Image.open(io.BytesIO(data))
        return True
    except:
        return False