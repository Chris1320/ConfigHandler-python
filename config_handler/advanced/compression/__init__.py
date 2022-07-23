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

from config_handler.advanced.compression import lz4
from config_handler.advanced.compression import zlib


def compress(data: bytes, algorithm: str | None) -> bytes:
    """
    Compress <data> using <algorithm>.
    """

    if algorithm is None:
        return data  # Do not modify the data.

    elif algorithm == "zlib":
        return zlib.compress(data)

    elif algorithm == "lz4":
        return lz4.compress(data)

    else:
        raise ValueError(f"Unsupported compression algorithm: {algorithm}")


def decompress(data: bytes, algorithm: str | None) -> bytes:
    """
    Decompress <data> using <algorithm>.
    """

    if algorithm is None:
        return data

    elif algorithm == "zlib":
        return zlib.decompress(data)

    elif algorithm == "lz4":
        return lz4.decompress(data)

    else:
        raise ValueError(f"Unsupported compression algorithm: {algorithm}")
