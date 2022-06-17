from database import db_manager

import os
import hashlib
import base64
from cryptography.fernet import Fernet

def create_salt():
    return os.urandom(32)

def hash_file(username, password, created):
    if created == True:
        salt_verification = db_manager.read_record(username, "verification")[0][1]
        pass_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_verification, 100000)
    else:
        salt_verification = create_salt()
        pass_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_verification, 100000)
    return pass_key, salt_verification

def hash_to_encrypt(username, password, created):
    if created == True:
        salt_encrypt = db_manager.read_record(username, "credentials")[0][1]
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_encrypt, 100000)
    else:
        salt_encrypt = create_salt()
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_encrypt, 100000)
    return hash_encode_key(hashed_password), salt_encrypt

def hash_encode_key(hashed_password):
    key = base64.b64encode(hashed_password)
    fernet = Fernet(key)
    return fernet

def encrypt_value(decPass, fernet, type):
    encPass = None
    if decPass is not None:
        if type == 'password':
            encPass = fernet.encrypt(decPass.encode())
        else:
            encPass = fernet.encrypt(decPass)
    return encPass

def decrypt_value(encPass, fernet, type):
    decPass = None
    if encPass is not None:
        if type == 'password':
            decPass = fernet.decrypt(encPass).decode()
        else:
            decPass = fernet.decrypt(encPass)
    return decPass