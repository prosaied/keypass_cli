import os
from Crypto.Cipher import AES
import base64
import click
import sys
import getpass

@click.group()

def keypass():
    """Simple command-line tool for managing your password securely."""
    pass

@keypass.command()
@click.option('-k', '--key_name', required=True)
@click.option('-p', '--key_pass', '--password', required=True, prompt=True, hide_input=True, confirmation_prompt=True)
def create_key(key_name, key_pass):
    safe_password = encode_password(key_pass)
    kpath = os.environ['HOME'] + "/" + key_name
    f = open(kpath, "wb+")
    f.write(safe_password)
    f.close()
    print("Your key was created.")


@keypass.command()
@click.option('-k', '--key_name', required=True)
def show_key(key_name):
    if key_exists(key_name) == 0:
        print("Key no exist.")
    else:
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

@keypass.command()
def create_secret():
    secret = os.urandom(16)
    spath = os.environ['HOME'] + "/secret_file"
    f = open(spath, "wb+")
    f.write(secret)
    f.close()
    print("Your Secret file is now created in your home directory, Keep It Safe !!!!")



if '__main__':
    keypass()