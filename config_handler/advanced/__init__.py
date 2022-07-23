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
import json
from typing import Final
from hashlib import blake2b

from config_handler import exceptions
from config_handler.advanced import encryption
from config_handler.advanced import compression

class Advanced:
    """
    A class that creates and manipulates an "advanced" configuration file.

    This type of configuration file uses the JSON format.
    """

    parser_version: Final[tuple[int, int, int]] = (2, 0, 0)
    supported_compression: Final[tuple] = (
        None,
        "zlib",
        "lz4"
    )
    supported_encryption: Final[tuple] = (
        None,
        "aes256"
    )

    def __init__(
        self,
        config_path: str,
        config_pass: str | None = None,
        readonly: bool = False,
        encoding: str = "utf-8"
    ):
        """
        :param config_path: The path of the configuration file to open or create.
        :param config_pass: The configuration file encryption password. (Default: `None`)
        :param readonly: True if the configuration file is read-only. (Default: `False`)
        :param encoding: The encoding to use. (Default: `utf-8`)

        Read-only mode allows manipulation but not writing to the configuration file.
        """

        self.config_path = config_path
        self.config_pass = config_pass
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
        """
        Check if the compression algorithm is supported first before setting.
        """

        if compression in self.supported_compression:
            self._compression = compression

        else:
            raise ValueError(f"Unsupported compression algorithm: {compression}")

    @property
    def encryption(self) -> str | None:
        return self._encryption

    @encryption.setter
    def encryption(self, encryption: str | None):
        """
        Check if the encryption algorithm is supported first before setting.
        """

        if encryption in self.supported_encryption:
            self._encryption = encryption

        else:
            raise ValueError(f"Unsupported encryption algorithm: {encryption}")

    @property
    def exists(self) -> bool:
        """
        Check if the configuration file exists in the file system.
        """

        return os.path.isfile(self.config_path)

    def _generateChecksum(self, data: bytes, digest_size: int = 8) -> str:
        """
        Generate a BLAKE2 hash of <data>.

        :param data: The data to hash.
        :param digest_size: The size of the hash. (default: 8; 64 bits)
        """

        return blake2b(data, digest_size=digest_size).hexdigest()

    def _pack(self, data: bytes) -> bytes:
        """
        Perform compression and encryption to <data> if needed.
        """

        if self.compression is None:
            pass

        elif self.compression == "zlib":
            data = compression.zlib.compress(data)

        elif self.compression == "lz4":
            data = compression.lz4.compress(data)

        else:
            raise ValueError(f"Unsupported compression algorithm: {self.compression}")

        if self.encryption is None:
            pass  # Do nothing to data if encryption is None.

        elif self.encryption == "aes256":
            if self.config_pass is None:
                raise ValueError("Configuration password is not set but encryption is on.")

            data = encryption.aes256.encrypt(self.config_pass, data)

        else:
            raise ValueError(f"Unsupported encryption algorithm: {self.encryption}")

        return data

    def new(
        self,
        name: str = __name__,
        author: str | None = None,
        compression: str | None = None,
        encryption: str | None = None
    ) -> None:
        """
        Create a new configuration file to <self.config_path>.
        This method raises a `PermissionError` if the configuration file is read-only.

        :param name: The name of the configuration file. (default: <__name__>)
        :param author: The author of the configuration file. (default: None)
        :param compression: The compression algorithm to use. (default: None)
        :param encryption: The encryption algorithm to use. (default: None)
        """

        if self.readonly:
            raise PermissionError("Configuration file is read-only.")

        self.name = name
        self.author = author
        self.compression = compression
        self.encryption = encryption

        self.__initialized = True
        self.__data = {}

        self.save()

    def load(self) -> None:
        """
        Load the configuration file contents to memory.
        Call this method when you want to read the configuration file.
        If `self.save()` is called without calling this method, the configuration file
        will be overwritten.
        """

        # TODO

    def save(self) -> None:
        """
        Save the configuration file to <self.config_path>.
        This method raises a `PermissionError` if the configuration file is read-only.
        This method raises a `ConfigFileNotInitializedError` if the configuration file is
        not initialized.
        """

        # Check if the configuration file is not initialized or is read-only.

        if self.readonly:
            raise PermissionError("Configuration file is read-only.")

        if not self.__initialized:
            raise exceptions.ConfigFileNotInitializedError

        # ? dict to json.encode()
        # ? Generate checksum
        # ? Encrypt
        # ? Compress
        # ? Encode (Base64)

        dictionary = json.dumps(self.__data).encode(self.encoding)

        # Step 1: Create the JSON data.
        to_write = {
            "name": self.name,
            "author": self.author,

            "compression": self.compression,
            "encryption": self.encryption,
            "encoding": self.encoding,

            "parser": {
                "version": self.parser_version
            },

            "checksum": self._generateChecksum(dictionary),
            "data": self._pack(dictionary)
        }
