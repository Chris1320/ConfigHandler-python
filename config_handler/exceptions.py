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


class ChecksumError(Exception):
    """
    Exception raised when the checksum of the dictionary is invalid.
    """

    def __init__(self, message: str = "The checksum of the dictionary does not match the previous checksum."):
        super().__init__(message)


class ConfigFileNotInitializedError(Exception):
    """
    Exception raised when the configuration file has not yet been initialized.
    """

    def __init__(self, message: str = "The configuration file has not yet been initialized."):
        super().__init__(message)


class InvalidConfigurationFileError(Exception):
    """
    Exception raised when the configuration file is unable to be loaded.
    """

    def __init__(self, message: str = "The configuration file is invalid or corrupted."):
        super().__init__(message)
