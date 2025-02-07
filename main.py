import os
import sys
import base64
import random
import marshal
import hashlib
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt, PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import lzma
import gzip
import bz2
import zlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_aes_key_with_rsa(aes_key, rsa_public_key):
    rsa_key = RSA.import_key(rsa_public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    return encrypted_key

def key_gen(password: str, salt: bytes) -> bytes:
    return PBKDF2(password.encode(), salt, dklen=32, count=1000000)

def encrypt(code, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    
    watermark = 'CPScripts AES encryptor'
    code_with_watermark = f'''{code}\n# encrypted and obfuscated using: {watermark}'''
    compiled_code = compile(code_with_watermark, '<string>', 'exec')
    bytecode = marshal.dumps(compiled_code)
    
    padded_bytecode = pad(bytecode, AES.block_size)
    ciphertext, tag = cipher.encrypt_and_digest(padded_bytecode)
    
    return base64.b64encode(iv + tag + ciphertext).decode('utf-8')

def encrypt_msg(message, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    
    padded_message = pad(message.encode(), AES.block_size)
    ciphertext, tag = cipher.encrypt_and_digest(padded_message)
    
    return base64.b64encode(iv + tag + ciphertext).decode('utf-8')

def obfuscate(code):
    code = code.replace('exec', 'x_x_e_c')
    code = code.replace('def ', 'def ' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8)) + ' ')
    return code

def compress(bytecode):
    compressed = lzma.compress(bytecode)
    return base64.b64encode(compressed).decode('utf-8')

def check(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_hash = hashlib.sha256(file_data).hexdigest()
            logging.info(f"Integrity hash of the file: {file_hash}")
            return file_hash
    except FileNotFoundError:
        logging.error("File not found for integrity check.")
        return None

def main():
    os.system('clear')
    print(" • Creator: CPScript\n")

    input_file = input(' [user-input] -- [Enter File Name (ex: main.py)]: ')

    try:
        with open(input_file, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        logging.error("File not found.")
        return

    password = input(" [user-input] -- Enter a password to generate a secure key: ")
    salt = get_random_bytes(16)
    key = key_gen(password, salt)

    obfuscated = obfuscate(code)
    encrypted = encrypt(obfuscated, key)
    
    access_denied_message = "Cannot run: Credit has been removed, access denied"
    encrypted_msg = encrypt_msg(access_denied_message, key)

    compressed_encrypted_code = compress(base64.b64decode(encrypted))

    output_file = input_file.split('.')[0] + "_encrypted.py"

    private_key, public_key = generate_rsa_key_pair()
    encrypted_aes_key = encrypt_aes_key_with_rsa(key, public_key)

    with open(output_file, 'w') as file:
        file.write(f"import base64\n")
        file.write(f"from Crypto.Cipher import AES, PKCS1_OAEP\n")
        file.write(f"from Crypto.PublicKey import RSA\n")
        file.write(f"from Crypto.Util.Padding import unpad\n")
        file.write(f"import marshal, sys\n")
        file.write(f"encrypted_aes_key = '{base64.b64encode(encrypted_aes_key).decode('utf-8')}'\n")
        file.write(f"encrypted_code = '{compressed_encrypted_code}'\n")
        file.write(f"def decrypt():\n")
        file.write(f"    encrypted_aes_key_bytes = base64.b64decode(encrypted_aes_key)\n")
        file.write(f"    rsa_private_key = RSA.import_key(b'''{private_key.decode('utf-8')}''')\n")
        file.write(f"    cipher_rsa = PKCS1_OAEP.new(rsa_private_key)\n")
        file.write(f"    aes_key = cipher_rsa.decrypt(encrypted_aes_key_bytes)\n")
        file.write(f"    encrypted_bytes = base64.b64decode(encrypted_code)\n")
        file.write(f"    iv = encrypted_bytes[:AES.block_size]\n")
        file.write(f"    tag = encrypted_bytes[AES.block_size:AES.block_size + AES.block_size]\n")
        file.write(f"    ciphertext = encrypted_bytes[AES.block_size + AES.block_size:]\n")
        file.write(f"    cipher = AES.new(aes_key, AES.MODE_GCM, iv)\n")
        file.write(f"    decrypted = unpad(cipher.decrypt_and_verify(ciphertext, tag), AES.block_size)\n")
        file.write(f"    code = marshal.loads(decrypted)\n")
        file.write(f"    exec(code)\n")
        file.write(f"try:\n")
        file.write(f"    decrypt()\n")
        file.write(f"except Exception as e:\n")
        file.write(f"    print('Error during execution:', e)\n")
        file.write(f"    sys.exit(1)\n")

    file_hash = check(output_file)

    logging.info(f"Encrypted file has been saved as: {output_file}")
    logging.info(f"File integrity hash: {file_hash}")

if __name__ == "__main__":
    main()
