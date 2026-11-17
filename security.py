import os
import hashlib
import hmac
import base64
from cryptography.fernet import Fernet



def hash_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:

    if salt is None:
        salt = os.urandom(16)

    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key, salt

def verify_password(stored_hash: bytes, stored_salt: bytes, provided_password: str) -> bool:

    new_hash, _ = hash_password(provided_password, stored_salt)
    return hmac.compare_digest(stored_hash, new_hash)

def get_fernet_key(master_password: str, salt: bytes) -> Fernet:
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode('utf-8'), salt, 100000)
    url_safe_key = base64.urlsafe_b64encode(key)
    return Fernet(url_safe_key)


def encrypt_password(password: str, fernet: Fernet) -> str:
    encrypted_bytes = fernet.encrypt(password.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_password(password: str, fernet: Fernet) -> str:
    try:
        decrypted_bytes = fernet.decrypt(password.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        return str(e)