import imp
from urllib.request import HTTPPasswordMgrWithDefaultRealm
from cryptography.fernet import Fernet
import bcrypt
from .models import Expenses


def create_encrypt_key():
    key = Fernet.generate_key()
    encrypted_key = key
    return encrypted_key

def encrypt(message, encrypt_key):
    msg = message.encode()
    cipher_suite = Fernet(encrypt_key)
    cipher_text = cipher_suite.encrypt(msg)
    return cipher_text

def decrypt(cipher_text, encrypt_key):
    cipher_suite = Fernet(encrypt_key)
    # decryptected_msg = cipher_suite.decrypt(cipher_text).decode()
    decrypted = cipher_suite.decrypt(cipher_text)
    decryptected_msg = decrypted.decode()
    return decryptected_msg

# encrypt_key = create_encrypt_key()

# encryptedmsg = encrypt('prueba de encriptado', encrypt_key)
# print(encryptedmsg)
# print(encrypt_key)
# decryptedmsg = decrypt(encryptedmsg, encrypt_key)
# print(decryptedmsg)


# password =b'prueba'

# hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# print(hashed)

# if bcrypt.checkpw(password, hashed):
#     print('Password correct')
# else:
#     print('Password incorrect')


def encrypt_password(password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

def validate_password(password, hashed):
    if bcrypt.hashpw(password, hashed) == hashed:
        print('Password correct')
        return True
    else:
        print('Password incorrect')
        return False


# password = 'prueba'
# encrypted_password = encrypt_password(password)
# print(encrypted_password)

# passwordp = 'prueba2'

# validate_password(passwordp, encrypted_password)
# validate_password(password, encrypted_password)


def generate_expenses_id():
    id = 1
    if Expenses.objects.filter(id=id).exists():
        new_id = generate_expenses_id()+1
        return new_id
    else:
        return id


# for i in range(10):
#     id = generate_expenses_id()
#     print(id)
#     Expenses.objects.create(id=id, description='prueba', amount=100)
