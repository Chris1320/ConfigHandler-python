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

import json
import zlib
import base64

from hashlib import blake2b

from config_handler import exceptions

try:
    import lz4.frame
    lz4_support = True

except ImportError:
    lz4_support = False

from . import ciphers


class Advanced():
    """
    A class that creates and manipulates an "advanced" configuration file.

    This mode is for storing any datatype supported by the JSON data format.
    """

    VERSION = (1, 0, 0)  # Parser version

    # All compression and encryption methods must accept and return `bytes` type.
    SUPPORTED = {
        "compression": ("zlib", "lz4"),
        "encryption": ("aes256",),
        "valuetypes": (str, int, float, bool, list, tuple, dict)
    }

    def __init__(self, config_path: str, epass: str = None, readonly: bool = False):
        """
        The initialization method of Advanced() class.

        :param str config_path: The path of the configuration file to use.
        :param str epass: The encryption password.
        :param bool readonly: True if the configuration file is read-only.
        """

        self.config_path = config_path
        self.epass = epass
        self.__readonly = readonly

        self.__metadata = {}  # Metadata of the configuration file.
        self.__dictionary = {}  # The actual data of the configuration file.

    def __compress(self, data: bytes) -> bytes:
        """
        Compress <data>. Raises ValueError if the compression method is not supported.

        :param bytes data: The data to compress.

        :returns str: Unmodified data if compression is None.
        :returns bytes: The compressed data.
        """

        if self.__metadata["compression"] == "zlib":
            return zlib.compress(data)

        elif self.__metadata["compression"] == "lz4":
            if not lz4_support:
                raise ValueError("LZ4 compression is not supported in this system.")

            return lz4.frame.compress(data)

        else:
            raise ValueError(f"Unsupported compression type `{self.__metadata['compression']}`")

    def __decompress(self, data: bytes) -> bytes:
        """
        Decompress <data>. Raises ValueError if the compression method is not supported.

        :param bytes data: The data to decompress.

        :returns str: Unmodified data if compression is None.
        :returns bytes: The decompressed data.
        """

        if self.__metadata["compression"] == "zlib":
            return zlib.decompress(data)

        elif self.__metadata["compression"] == "lz4":
            if not lz4_support:
                raise ValueError("LZ4 compression is not supported in this system.")

            return lz4.frame.decompress(data)

        else:
            raise ValueError(f"Unsupported compression type `{self.__metadata['compression']}`")

    def __encrypt(self, data: bytes) -> bytes:
        """
        Encrypt <data>. Raises ValueError if the encryption method is not supported.

        :param bytes data: The data to be encrypted.

        :returns bytes: The encrypted data.
        """

        if self.__metadata["encryption"] == "aes256":
            if not ciphers.cryptodome_support:
                raise ValueError("AES256 encryption is not supported in this system.")

            return ciphers.AES256(self.epass).encrypt(base64.b64encode(data).decode(self.__metadata["encoding"]))

        else:
            raise ValueError(f"Unsupported encryption type `{self.__metadata['encryption']}`")

    def __decrypt(self, data: bytes) -> bytes:
        """
        Decrypt <data>. Raises ValueError if the encryption method is not supported.

        :param bytes data: The data to decrypt.

        :returns bytes: The decrypted data.
        """

        if self.__metadata["encryption"] == "aes256":
            if not ciphers.cryptodome_support:
                raise ValueError("AES256 encryption is not supported in this system.")

            return base64.b64decode(ciphers.AES256(self.epass).decrypt(data))

        else:
            raise ValueError(f"Unsupported encryption type `{self.__metadata['encryption']}`")

    def _checkKey(self, key: str) -> bool:
        """
        Returns True if key is valid. Otherwise, raise ValueError.

        :param str key: The key to check

        :returns bool: True if key is valid.
        """

        if type(key) is not str:
            raise ValueError(f"Invalid key `{key}`")

        return True

    def _generateChecksum(self, data: bytes) -> str:
        """
        Generate a BLAKE2 hash of <data>.

        :param bytes data: The data to hash.

        :returns str: The BLAKE2 hash of the data. If <data> is None, returns ''.
        """

        return blake2b(data, digest_size=8).hexdigest() if data is not None else ''

    def new(self, name: str, author: str = None, compression: str = None, encryption: str = None, encoding: str = "utf-8") -> None:
        """
        Create a new configuration file.

        This method sets the metadata of the current configuration file.

        :param str name: The name of the configuration file.
        :param str author: The author of the configuration file.
        :param str compression: The compression method to use.
        :param str encryption: The encryption method to use.
        :param str encoding: The encoding to use when writing the configuration file.
        """

        if self.__readonly:
            raise PermissionError("The configuration file is read-only.")

        assert compression in Advanced.SUPPORTED["compression"] or compression is None
        assert encryption in Advanced.SUPPORTED["encryption"] or encryption is None
        assert "encoding test".encode(encoding)  # Check if the encoding is valid.

        self.__metadata["name"] = name
        self.__metadata["author"] = author
        self.__metadata["compression"] = compression
        self.__metadata["encryption"] = encryption
        self.__metadata["encoding"] = encoding
        self.__metadata["version"] = Advanced.VERSION
        self.__metadata["dictionary"] = ''
        self.__metadata["checksum"] = ''

        self.__dictionary = {}

        self.save()  # Save the new configuration file to `self.config_path`.

    def load(self, strict: bool = True) -> None:
        """
        Load the configuration file.

        :param bool strict: If True, raise `exceptions.ChecksumError` if the dictionary checksum does not match.

        Raises a `json.decoder.JSONDecodeError` if the AES encryption password is incorrect,
        or the configuration file is corrupt.
        Raises a `ValueError` if the password is not provided and the configuration file is encrypted.
        """

        # ? Decode (Base64)
        # ? Decompress
        # ? Decrypt
        # ? Integrity check
        # ? json to dict.decode()

        # * Step 1: Load metadata.
        with open(self.config_path, 'r') as fopen:
            self.__metadata = json.load(fopen)

        # check if self.epass is not None.
        if self.epass is None and self.__metadata["encryption"] is not None:
            raise ValueError("The configuration file is encrypted but no password is provided.")

        # * Step 2: Decode dictionary.
        dictionary = base64.b64decode(self.__metadata["dictionary"].encode(self.__metadata["encoding"]))

        # * Step 3: If compression is used, decompress dictionary.
        if self.__metadata["compression"] is not None:
            dictionary = self.__decompress(dictionary)

        # * Step 4: If encryption is used, decrypt dictionary.
        if self.__metadata["encryption"] is not None:
            dictionary = self.__decrypt(dictionary)

        # * Step 5: Check dictionary checksum if strict mode is enabled.
        if strict:
            # Check if `checksum` exists in `self.__metadata`.
            if "checksum" not in self.__metadata and self.__metadata["version"][0] < 1:
                # If the configuration file is made by Advanced mode parser v0.x.x, generate a new checksum value.
                self.__metadata["checksum"] = self._generateChecksum(dictionary)

            else:
                # Evaluate the checksum of the dictionary.
                if (self.__metadata["checksum"] != self._generateChecksum(dictionary)):
                    raise exceptions.ChecksumError()

        # * Step 6: Convert JSON to dictionary.
        self.__dictionary = json.loads(dictionary.decode(self.__metadata["encoding"]))

        return

    def save(self) -> None:
        """
        Save the configuration file.
        """

        # ? dict to json.encode()
        # ? Generate checksum
        # ? Encrypt
        # ? Compress
        # ? Encode (Base64)

        # self.__metadata will be updated.
        self.__metadata["version"] = Advanced.VERSION

        # * Step 1: Convert the dictionary to JSON.
        dictionary = json.dumps(self.__dictionary).encode(self.__metadata["encoding"])

        # * Step 2: Calculate BLAKE2 checksum of the dictionary in JSON format.
        self.__metadata["checksum"] = self._generateChecksum(dictionary)

        # * Step 3: If encryption is enabled, encrypt the dictionary.
        if self.__metadata["encryption"] is not None:
            dictionary = self.__encrypt(dictionary)

        # * Step 4: If compression is enabled, compress the dictionary.
        if self.__metadata["compression"] is not None:
            dictionary = self.__compress(dictionary)

        # * Step 5: Encode the dictionary to Base64.
        self.__metadata["dictionary"] = base64.b64encode(dictionary).decode(self.__metadata["encoding"])

        # * Step 6: Write metadata to file.
        with open(self.config_path, 'w') as fopen:
            fopen.write(json.dumps(self.__metadata, indent=4))

        return

    def set(self, key, value) -> None:
        """
        Set value of a key on `self.__dictionary`.
        """

        self._checkKey(key)
        self.__dictionary[key] = value

    def get(self, key):
        """
        Get the value of <key>. Raises a KeyError if the key is not found.
        """

        return self.__dictionary[key]

    def remove(self, key) -> None:
        """
        Remove a key from `self.__dictionary`.
        """

        self.__dictionary.pop(key)

    def keys(self) -> list:
        """
        Get all the keys in `self.__dictionary`.

        :returns list: The list of keys.
        """

        return self.__dictionary.keys()

    def metadata(self) -> dict:
        """
        Return the metadata of the configuration file.
        """

        metadata = self.__metadata.copy()
        metadata.pop("dictionary")
        metadata["dictionary_size"] = len(self.__dictionary)
        return metadata
