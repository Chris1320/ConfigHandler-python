#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MIT License
Copyright (c) 2020-2023 Chris1320

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
from typing import Union
from importlib import import_module

from config_handler import info
from config_handler.advanced.compression import lz4
from config_handler.advanced.compression import zlib


def isAvailable(compression_name: Union[str, None]) -> bool:
    """
    Check if <compression_name> is available in the user's machine.
    """

    if compression_name is None:
        return True  # This means that no compression is needed.

    parent_import_path = "config_handler.advanced.compression"

    return getattr(import_module(f"{parent_import_path}.{compression_name}"), "available")


def compress(data: str, algorithm: Union[str, None], encoding: str = info.defaults["encoding"]) -> str:
    """
    Compress <data> using <algorithm>.
    Return the base64-encoded result as a string.
    """

    if algorithm is None:
        return data  # Do not modify the data.

    elif algorithm == "zlib":
        return base64.b64encode(zlib.compress(data.encode(encoding))).decode(encoding)

    elif algorithm == "lz4":
        return base64.b64encode(lz4.compress(data.encode(encoding))).decode(encoding)

    else:
        raise ValueError(f"Unsupported compression algorithm: {algorithm}")


def decompress(data: str, algorithm: Union[str, None], encoding: str = info.defaults["encoding"]) -> str:
    """
    Decompress <data> using <algorithm>.
    """

    if algorithm is None:
        return data

    elif algorithm == "zlib":
        return zlib.decompress(base64.b64decode(data)).decode(encoding)

    elif algorithm == "lz4":
        return lz4.decompress(base64.b64decode(data)).decode(encoding)

    else:
        raise ValueError(f"Unsupported compression algorithm: {algorithm}")
