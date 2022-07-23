#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MIT License
Copyright (c) 2020-2022 Chris1320

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

try:
    from Cryptodome import Random
    from Cryptodome.Cipher import AES
    from Cryptodome.Protocol.KDF import PBKDF2
    from Cryptodome.Util.Padding import pad
    from Cryptodome.Util.Padding import unpad
    available: bool = True

except ModuleNotFoundError:
    available: bool = False  # There is no supported cryptography module available.


def encrypt(data: bytes, key: bytes | str) -> bytes:
    """
    Encrypt <data> using <key> as key.

    :param data: The data to encrypt.
    :param key: The key to use.
    """

    key_size = 32
    salt_size = 16
    block_size = AES.block_size

    salt = Random.new().read(salt_size)  # Generate a random 16-byte salt.
    key_hash: bytes = PBKDF2(key, salt, dkLen=key_size, count=50000)  # type: ignore
    iv: bytes = Random.new().read(AES.block_size)  # Generate a random 16-bytes initialization vector.

    aes = AES.new(key_hash, AES.MODE_CBC, iv=iv)  # Create a new AES object.
    return salt + iv + aes.encrypt(pad(data, block_size))  # Encrypt the data.


def decrypt(data: bytes, key: bytes | str) -> bytes:
    """
    Decrypt <data> using <key> as key.

    :param data: The data to decrypt.
    :param key: The key to use.
    """

    key_size = 32
    salt_size = 16
    block_size = AES.block_size

    iv = data[salt_size:salt_size + block_size]  # Get the iv of the ciphertext.
    salt = data[:salt_size]  # Get the first 16 bytes of the data as the salt used.
    enc_data = data[salt_size + block_size:]  # Get the encrypted data.

    key_hash : bytes = PBKDF2(key, salt, dkLen=key_size, count=50000)  # type: ignore

    aes = AES.new(key_hash, AES.MODE_CBC, iv=iv)

    return unpad(aes.decrypt(enc_data), block_size)
