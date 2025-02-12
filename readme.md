# SecureFE (free) (python encryptor & obfuscate only)

>SecureFE is a Python-based tool designed to encrypt, obfuscate, and compress Python code, making it harder to reverse-engineer and unauthorized access. The tool uses AES encryption with RSA key wrapping to securely protect your Python code. Additionally, it obfuscates the code by renaming functions and modifying critical parts to make analysis more difficult.

## Features

- **RSA Key Pair Generation**: Generates an RSA key pair to securely encrypt the AES key used for encrypting your Python code.
- **AES Encryption**: Uses AES-GCM encryption to encrypt the Python code, ensuring both confidentiality and integrity.
- **Code Obfuscation**: Obfuscates the code by modifying function names and adding randomization to make reverse engineering more difficult.
- **Compression**: Compresses the encrypted bytecode using LZMA to reduce the size of the final output.
- **File Integrity Check**: Computes and logs the integrity hash of the encrypted output file using SHA-256.
- **Access Control**: Includes a custom access denied message that is also encrypted, ensuring that only authorized users can execute the code.

## How It Works

1. **Key Generation**:
   The user provides a password, which is used to generate a secure AES key via the PBKDF2 key derivation function. This AES key is used to encrypt the Python code.

2. **RSA Encryption**:
   The AES key is then encrypted with an RSA public key, ensuring that the AES key can only be decrypted by someone with the corresponding private key.

3. **Code Obfuscation**:
   The Python code is obfuscated by modifying function names and replacing keywords to make it more difficult for an attacker to understand the code. Additionally, a watermark is added to the code to mark it as being encrypted by CPScripts.

4. **Encryption & Compression**:
   The obfuscated code is compiled to bytecode, padded, and encrypted using AES-GCM. After encryption, the bytecode is compressed using LZMA to minimize the size of the output file.

5. **Output**:
   The encrypted code, along with the encrypted AES key and decryption logic, is saved in a new Python file. The file can only be executed after the AES key is decrypted using the RSA private key.

## Prerequisites

Before running the script, you need to install the following dependencies:

`pip install pycryptodome lzma`


## Usage

1. **Prepare Your Python Script**:
   Write the Python code you want to encrypt and save it in a `.py` file.

2. **Run the Encryptor**:
   Execute the script using the following command:

```
python encryptor.py
```


3. **Input File**:
   The tool will prompt you to enter the filename of the Python file you want to encrypt.

4. **Generate Secure Key**:
   You will be asked to input a password. This password will be used to generate a secure AES key.

5. **Encrypted Output**:
   The encrypted and obfuscated Python code will be saved in a new file with the `_encrypted.py` suffix. The file contains everything necessary to decrypt and execute the code, including the encrypted AES key, the RSA-encrypted key, and decryption logic.

6. **Decryption and Execution**:
   To run the encrypted code, simply execute the generated output Python file. It will automatically decrypt the AES key using the RSA private key, decrypt the encrypted code, and then execute the original Python code.

   > **Important**: The RSA private key must be kept secure. Without the private key, the encrypted code cannot be decrypted and executed.

## Example

```
[user-input] -- [Enter File Name (ex: main.py)]: example.py
[user-input] -- [Enter a password to generate a secure key]: examplePassword

Encrypted file has been saved as: example_encrypted.py File integrity hash: a4f36e134b6c517ea0a5b74680e0e5f50d7c6198397fcb424f53e2dcb65b2537
```


## Security Considerations

- **Encryption**: AES-GCM ensures the confidentiality and integrity of the code, while RSA encryption secures the AES key.
- **Obfuscation**: Function name randomization and other obfuscation techniques make it harder for attackers to reverse-engineer the code.
- **RSA Key Security**: The RSA private key must be securely stored to ensure only authorized users can decrypt the AES key.

## Disclaimer

While this tool provides an additional layer of security, no encryption or obfuscation method is entirely foolproof atleast not this free versions. It is still possible for determined attackers with access to the environment (e.g., through physical access or other means) to eventually reverse-engineer or bypass these protections.
