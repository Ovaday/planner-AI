# Imports and functions
import os

from pathlib import Path

from helpers.tokenHelpers import get_token
from os import listdir
from os.path import isfile, join
from cryptography.fernet import Fernet
from builtins import open


def listFiles(resourcesPath, is_encrypt):
    if is_encrypt:
        # Return only files with the ".enc" extension
        return [f for f in listdir(resourcesPath) if
                isfile(join(resourcesPath, f)) and f.endswith(".enc") and f != 'resourcesPacker.ipynb']
    else:
        # Return all files except 'resourcesPacker.ipynb'
        return [f for f in listdir(resourcesPath) if isfile(join(resourcesPath, f)) and f != 'resourcesPacker.ipynb']


def handleExtension(filename, is_encrypt):
    if not is_encrypt:
        # Remove the ".enc" extension from the filename
        if filename.endswith(".enc"):
            filename = filename[:-4]
    else:
        # Append the ".enc" extension to the filename
        if not filename.endswith(".enc"):
            filename += ".enc"
    return filename


def encrypt(filename_origin, filename_destination, key):
    f = Fernet(key)
    with open(filename_origin, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    filename_destination = handleExtension(filename_destination, True)
    # write the encrypted file
    with open(filename_destination, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename_origin, filename_destination, key):
    decrypted_data, f = read_encrypted(filename_origin, key)
    filename_destination = handleExtension(filename_destination, False)
    # write the original file
    with open(filename_destination, "wb") as file:
        file.write(decrypted_data)

def read_encrypted(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data, f

def get_fernet_key():
    return bytes(str(get_token('COMMON_KEY')), 'utf-8')

root_file_path = Path(__file__).resolve().parent.parent
basedir_extracted = os.path.join(root_file_path, 'resources/extracted/')
basedir_packed = os.path.join(root_file_path, 'resources/')

# Unpack resources using the key
def unpack_resources():
    key = get_fernet_key()
    files = listFiles(basedir_packed, True)
    for filename in files:
        decrypt(basedir_packed + filename, basedir_extracted + filename, key)

def pack_resources():
    print(basedir_extracted)
    key = get_fernet_key()
    files = listFiles(basedir_extracted, False)
    for filename in files:
        encrypt(basedir_extracted + filename, basedir_packed + filename, key)