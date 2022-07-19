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

import base64
from hashlib import sha256

try:
    from Cryptodome import Random
    from Cryptodome.Cipher import AES
    available: bool = True

except ModuleNotFoundError:
    try:  # Try to use the alternative library.
        from Crypto import Random
        from Crypto.Cipher import AES
        available: bool = True

    except ModuleNotFoundError:
        available: bool = False  # There is no supported cryptography module available.


def _pad(data: bytes) -> bytes:
    """
    Add padding to <data>.
    """

    # return s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)
    pass  # TODO


def _unpad(data: bytes) -> bytes:
    """
    Remove padding from <data>.
    """

    # return s[:-ord(s[len(s) - 1:])]
    pass  # TODO


def encrypt(key: bytes, data: bytes, encoding: str = "utf-8") -> bytes:
    """
    Encrypt <data> using <key> as key.

    :param key: The key to use.
    :param data: The data to encrypt.
    :param encoding: The encoding to use.
    """

    key: bytes = sha256(key).digest()  # Get the SHA-256 hash of the key so we have a 32-bytes key.
    iv: bytes = Random.new().read(AES.block_size)  # Generate a random 16-bytes initialization vector.
    aes = AES().new(key, AES.MODE_CBC, iv=iv)  # Create a new AES object.


def decrypt(key: str, data: bytes):
    """
    Decrypt <data> using <key> as key.
    """
