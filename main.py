import os
from Crypto.Cipher import AES
import base64
import sys
import getpass


def create_key(key_name, key_pass):
    safe_password = encode_password(key_pass)
    kpath = os.environ['HOME'] + "/" + key_name
    f = open(kpath, "wb+")
    f.write(safe_password)
    f.close()
    print("Your key was created.")


def show_key(key_name):
    secret = read_secret()
    kpath = os.environ['HOME'] + "/" + key_name
    f = open(kpath, "r")
    encoded = f.read()
    decoded = decode_password(encoded)
    print(decoded.decode("utf-8"))
    f.close()


def key_exists(key_name):
    kpath = os.environ['HOME'] + "/" + key_name
    try:
        f = open(kpath)
        f.close()
    except FileNotFoundError:
        return 0
    return 1


def secret_exist():
    spath = os.environ['HOME'] + "/secret_file"
    try:
        f = open(spath)
        f.close()
    except FileNotFoundError:
        return 0
    return 1


def create_secret():
    secret = os.urandom(16)
    spath = os.environ['HOME'] + "/secret_file"
    f = open(spath, "wb+")
    f.write(secret)
    f.close()
    print("Your Secret file is now created in your home directory, Keep It Safe !!!!")


def read_secret():
    spath = os.environ['HOME'] + "/secret_file"
    f = open(spath, "rb")
    secret = f.read()
    f.close()
    return secret


def encode_password(key_pass):
    secret = read_secret()
    msg_text = key_pass.rjust(32)
    cipher = AES.new(secret, AES.MODE_ECB)
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded


def decode_password(encoded):
    secret = read_secret()
    cipher = AES.new(secret, AES.MODE_ECB)
    decoded = cipher.decrypt(base64.b64decode(encoded))
    return decoded.strip()


# if sys.argv[1] == "--create-secret":
#     create_secret()
#
# if sys.argv[1] == "--create-key":
#     if secret_exist() == 0:
#         print("You have not already created your secret file!, run --create-secret")
#         sys.exit()
#     key_name = input('Enter your key: ')
#     if key_exists(key_name) == 1:
#         print("You already created a key with this name !")
#         sys.exit()
#     key_pass = getpass.getpass('Enter your password: ')
#     create_key(key_name, key_pass)
#
# if sys.argv[1] == "--show-key":
#     key_name = input('Enter your key: ')
#     show_key(key_name)


