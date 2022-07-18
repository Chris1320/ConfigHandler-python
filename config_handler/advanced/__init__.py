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

import os
from typing import Final
from hashlib import blake2b


class Advanced:
    r"""
    A class that creates and manipulates an "advanced" configuration file.

    This type configuration file uses the JSON format.
    """

    parser_version: Final[tuple[int, int, int]] = (2, 0, 0)

    def __init__(
        self,
        config_path: str,
        readonly: bool,
        encoding: str = "utf-8"
    ):
        """
        :param config_path: The path of the configuration file to open or create.
        :param readonly: True if the configuration file is read-only.
        :param encoding: The encoding to use.

        Read-only mode allows manipulation but not writing to the configuration file.
        """

        self.config_path = config_path
        self.readonly = readonly
        self.encoding = encoding

        self.__initialized = False  # Is `self.load()` or `self.new()` called?
        self.__data = {}  # The configuration file contents.

    @property
    def config_path(self) -> str:
        return self._config_path

    @config_path.setter
    def config_path(self, new_path: str):
        self._config_path = os.path.abspath(new_path)

    @property
    def compression(self) -> str | None:
        return self._compression

    @compression.setter
    def compression(self, compression: str | None):
        self._compression = compression  # TODO: Check if the compression name is valid.

    @property
    def encryption(self) -> str | None:
        return self._encryption

    @encryption.setter
    def encryption(self, encryption: str | None):
        self._encryption = encryption  # TODO: Check if the encryption name is valid.

    @property
    def exists(self) -> bool:
        """
        Check if the configuration file exists in the file system.
        """

        return os.path.isfile(self.config_path)

    def _generateChecksum(self, data: bytes) -> str:
        """
        Generate a BLAKE2 hash of <data>.
        """

        return blake2b(data, digest_size=8).hexdigest()

    def new(
        self,
        name: str = __name__,
        author: str | None = None,
        compression: str | None = None,
        encryption: str | None = None
    ):
        """
        Create a new configuration file to <self.config_path>.
        This method raises a `PermissionError` if the configuration file is read-only.

        :param name: The name of the configuration file. (default: <__name__>)
        :param author: The author of the configuration file. (default: None)
        :param compression: The compression algorithm to use. (default: None)
        :param encryption: The encryption algorithm to use. (default: None)
        """

        self.name = name
        self.author = author
        self.compression = compression  # TODO: Check if the compression name is valid.
        self.encryption = encryption  # TODO: Check if the encryption name is valid.

    def load(self):
        """
        Load the configuration file contents to memory.
        Call this method when you want to read the configuration file.
        If `self.save()` is called without calling this method, the configuration file
        will be overwritten.
        """

        # TODO

    def save(self):
        """
        Save the configuration file to <self.config_path>.
        This method raises a `PermissionError` if the configuration file is read-only.
        """

        # TODO
