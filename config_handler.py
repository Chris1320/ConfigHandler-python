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
import base64

from hashlib import sha256

try:
    from Cryptodome import Random
    from Cryptodome.Cipher import AES
    aes_support = True

except ModuleNotFoundError:
    try:  # Try to use the alternative library.
        from Crypto import Random
        from Crypto.Cipher import AES
        aes_support = True

    except ModuleNotFoundError:
        aes_support = False


VERSION = (0, 3, 0)

if aes_support:  # Initialize Cipher() class only if Cryptodome module is available.
    class AES256():
        """
        The class that contains methods for working with AES-256.

        Found this solution from StackOverflow.
        https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
        """

        def __init__(self, key: str, encoding: str = "utf-8"):
            """
            The initialization method of AES256() class.

            :param str key: The key/password of the message.
            :param str encoding: The encoding of the message.
            """

            self.VERSION = (0, 1, 2)

            self.bs = AES.block_size  # The block size
            self.encoding = encoding  # The encoding to be used when calling `encode()` and `decode()`.
            self.key = sha256(key.encode(self.encoding)).digest()  # The hashed key

        def encrypt(self, message: str) -> bytes:
            """
            Encrypt <message> using <self.key> as the key/password. Overridable method.

            :param str message: The message to encrypt.

            :returns bytes: The ciphertext.
            """

            padded_message = self._pad(message)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)

            emessage = padded_message.encode(self.encoding)  # Encoded message
            ciphertext = base64.b64encode(iv + cipher.encrypt(emessage))

            return ciphertext

        def decrypt(self, ciphertext: bytes) -> str:
            """
            Decrypt <ciphertext> using <self.key> as the key/password. Overridable method.

            :param bytes ciphertext: The ciphertext to decrypt.

            :returns str: The plaintext version of the ciphertext.
            """

            ciphertext = base64.b64decode(ciphertext)
            iv = ciphertext[:AES.block_size]  # Get the iv from the ciphertext
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext[AES.block_size:])
            plaintext = self._unpad(decrypted).decode(self.encoding)

            return plaintext

        def _pad(self, s):
            """
            Add a padding to <s>.
            """

            return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

        @staticmethod
        def _unpad(s):
            """
            Remove padding from <s>.
            """

            return s[:-ord(s[len(s) - 1:])]


class Simple():
    """
    A class the creates and manipulates a "simple" configuration file.

    + This mode is for storing string, integer, and decimals only.
    + Comments are supported by appending `#` at the beginning of the line.
    + Each line of the file contains one key-value pair separated by an equal (=) sign.
    """

    def __init__(self, config_path: str, isbase64: bool = False, encoding: str = "utf-8", readonly: bool = False):
        """
        The initialization method for Simple() class.

        :param str config_path: The path of the configuration file to use.
        :param bool isbase64: True if the configuration file is encoded via Base64.
        :param str encoding: The encoding to be used.
        :param bool readonly: True if the configuration file is read-only.
        """

        self.VERSION = (0, 2, 0)  # Parser version

        self.isbase64 = isbase64
        self.encoding = encoding

        self._config_path = config_path
        self.__readonly = readonly
        self.__data = {}  # We will put the contents of the configuration file here.

    def _parse_key(self, key: str) -> None:
        """
        Check if the key is valid. Raises a ValueError if the key is invalid.

        :param str key: The key to check.
        """

        if type(key) is not str:  # Separate this check from other checks to avoid TypeError when key is not a str.
            raise ValueError(f"Invalid key `{key}`")

        if '=' in key or key.startswith('#') or '\n' in key:
            raise ValueError(f"Invalid key `{key}`")

        return

    def load(self) -> None:
        """
        Read the config file and store it to self.__data as a dictionary.
        Call this method when you want to read the configuration file.
        If you save without calling load(), the configuration file will be overwritten.

        :returns void:
        """

        with open(self._config_path, 'r') as fopen:
            if self.isbase64:  # Decode data if it is Base64 encoded.
                config_data = base64.b64decode(fopen.read()).decode(self.encoding)

            else:
                config_data = fopen.read()

        for line in config_data.splitlines():
            if line.startswith('#'):
                continue  # Skip comments.

            data = line.partition('=')  # * data[0] is the key, data[1] is the separator, data[2] is the value.

            # Write the key-value pair to `self.__data`.
            if data[2].partition('.')[0].isdigit() and data[2].partition('.')[2].isdigit():
                self.__data[data[0]] = float(data[2])

            elif data[2].isdigit():
                self.__data[data[0]] = int(data[2])

            elif data[2].lower() in ("true", "false"):
                if data[2].lower() == "true":
                    self.__data[data[0]] = True

                else:
                    self.__data[data[0]] = False

            else:
                self.__data[data[0]] = str(data[2])

    def save(self) -> None:
        """
        Save the config file. Raises a PermissionError if the configuration file is read-only.

        :returns void:
        """

        if self.__readonly:
            raise PermissionError("The configuration file is read-only.")

        config_data = ""  # Let's initialize it as an empty string first.
        for key in self.__data:
            config_data += f"{key}={self.__data[key]}\n"  # Write the key-value pair to the config file.

        with open(self._config_path, 'w') as fopen:
            if self.isbase64:
                fopen.write(base64.b64encode(config_data.encode(self.encoding)).decode(self.encoding))

            else:
                fopen.write(config_data)

        return

    def get(self, key: str) -> str:
        """
        Get the value of <key> from `self.__data`.
        """

        return self.__data[key]  # Will raise a KeyError exception if the key is not found.

    def set(self, key: str, value) -> None:
        """
        Add or update a new key-value pair to `self.__data`.

        :param str key: The key to add.
        :param value: The value to add.
        """

        self._parse_key(key)  # Check if the key is valid.
        self.__data[key] = value
        return

    def remove(self, key: str) -> None:
        """
        Remove a key-value pair from `self.__data`.

        :param str key: The key to remove.
        """

        self.__data.pop(key)
        return

    def keys(self) -> list:
        """
        Get all the keys in `self.__data`.

        :returns list: The list of keys.
        """

        return self.__data.keys()


class Advanced():
    """
    A class that creates and manipulates an "advanced" configuration file.

    + This mode is for storing any datatype supported by the JSON data format.
    """

    def __init__(self, config_path: str, epass: str = None, readonly: bool = False):
        """
        The initialization method of Advanced() class.

        :param str config_path: The path of the configuration file to use.
        :param str epass: The encryption password.
        :param bool readonly: True if the configuration file is read-only.
        """

        self.VERSION = (0, 2, 0)  # Parser version

        self.config_path = config_path
        self.__readonly = readonly

        self.__metadata = {}  # Metadata of the configuration file.
        self.__dictionary = {}  # The actual data of the configuration file.

        self.supported = {
            "compression": ("zlib",),
            "encryption": ("aes256",),
            "valuetypes": (str, int, float, bool, list, tuple, dict)
        }

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

        assert compression in self.supported["compression"] or compression is None
        assert encryption in self.supported["encryption"] or encryption is None
        assert "encoding test".encode(encoding)  # Check if the encoding is valid.

        self.__metadata["name"] = name
        self.__metadata["author"] = author
        self.__metadata["compression"] = compression
        self.__metadata["encryption"] = encryption
        self.__metadata["encoding"] = encoding
        self.__metadata["version"] = self.VERSION
        self.__metadata["dictionary"] = {}

        self.save()  # Save the new configuration file to `self.config_path`.

    def load(self) -> None:
        """
        Load the configuration file.
        """

        with open(self.config_path, 'r') as fopen:
            self.__metadata = self.json.load(fopen)

        self.__dictionary = base64.b64decode(self.__metadata["dictionary"]).decode(self.__metadata["encoding"])

        # ? I don't think this is necessary.
        # self.__metadata.pop("dictionary")

        return

    def save(self) -> None:
        """
        Save the configuration file.
        """

        # self.__metadata will be updated.
        self.__data["version"] = self.VERSION
        self.__data["dictionary"] = base64.b64encode(self.__dictionary.encode(self.__data["encoding"])).decode(self.__data["encoding"])
        with open(self.config_path, 'r') as fopen:
            fopen.write(self.json.dumps(self.__data, indent=4))

        return

    # def verify(self, value) -> bool:
    #     """
    #     Check if the type of <value> is valid. Raises a TypeError if its type is not supported.

    #     :param value: The value to check.

    #     :returns bool: True if the type of <value> is valid.
    #     """

    #     if type(value) not in self.supported["valuetypes"]:
    #         raise TypeError(f"The type of <value> is not supported.")

    #     return True

    def set(self, key, value) -> None:
        """
        Set value of a key on `self.__dictionary`.
        """

        self.__dictionary[key] = value

    def get(self, key):
        """
        Get the value of <key>. Raises a KeyError if the key is not found.
        """

        return self.__dictionary[key]
