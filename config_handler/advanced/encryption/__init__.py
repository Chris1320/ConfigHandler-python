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

from config_handler.advanced.encryption import aes256


def encrypt(data: bytes, algorithm: str | None, key: str | None = None) -> bytes:
    """
    Encrypt <data> using <algorithm> as the encryption algorithm and <key> as the key.
    """

    if algorithm is None:
        return data  # Do not modify the data.

    if key is None:
        raise ValueError("Configuration password is not set but encryption is on.")

    elif algorithm == "aes256":
        return aes256.encrypt(data, key)

    else:
        raise ValueError(f"Unsupported encryption algorithm: {algorithm}")


def decrypt(data: bytes, algorithm: str | None, key: str | None = None) -> bytes:
    """
    Decrypt <data> using <algorithm> as the encryption algorithm and <key> as the key.
    """

    if algorithm is None:
        return data

    if key is None:
        raise ValueError("Configuration password is not set but encryption is on.")

    if algorithm == "aes256":
        return aes256.decrypt(data, key)

    else:
        raise ValueError(f"Unsupported encryption algorithm: {algorithm}")
