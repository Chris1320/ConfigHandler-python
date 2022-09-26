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
import base64
from typing import Any
from typing import List
from typing import Final
from typing import Tuple
from typing import Union

from config_handler import info


class Simple:
    r"""
    A class that creates and manipulates a "simple" configuration file.

    - Comments are supported by appending a hash (#) at the beginning of the line.
    - Each line of the file contains one key-value pair separated by an equal (=) sign.
    - Keys must follow the constraints below:
        - Keys must be a string.
        - Keys must not start with a hash (#).
        - Keys must not contain a newline (\n).
        - Keys must not contain an equal (=) sign.
    - Values must be any string, integer, float, or boolean.
    - Values must not contain a newline (\n).
    """

    parser_version: Final[Tuple[int, int, int]] = (0, 5, 0)  # Parser version
    _separator: Final[str] = '='
    _comment_char: Final[str] = '#'

    def __init__(
        self,
        config_path: str,
        isbase64: bool = False,
        readonly: bool = False,
        encoding: str = info.defaults["encoding"]
    ):
        """
        :param config_path: The path of the configuration file to open or create.
        :param isbase64: True if the configuration file is encoded via Base64.
        :param readonly: True if the configuration file is read-only.
        :param encoding: The encoding to use.

        Read-only mode allows manipulation but not writing to the configuration file.
        """

        self.config_path = config_path
        self.isbase64 = isbase64
        self.readonly = readonly
        self.encoding = encoding

        self.__data = {}  # The configuration file contents.

    def __contains__(self, key: str) -> bool:
        """
        Check if <key> exists in the configuration file.
        """

        return key in self.__data

    def __delitem__(self, key: str) -> None:
        """
        Remove a key from the configuration file.
        """

        del self.__data[key]

    def __setitem__(self, key: str, value: Union[str, int, float, bool]) -> None:
        """
        Set a key-value pair in the configuration file.
        Raises a `ValueError` if the key or value has invalid characters.

        :param key: The key of the pair.
        :param value: The value of the key.
        """

        if not self._parseKey(key):
            raise ValueError("Key contains invalid characters.")

        if not self._parseValue(value):
            raise ValueError("Value contains invalid characters.")

        self.__data[key] = value

    def __getitem__(self, key: str) -> Union[str, int, float, bool]:
        """
        Get the value of <key>.
        """

        return self.__data[key]

    def __repr__(self) -> str:
        """
        Return a string representation of the configuration file.
        """

        return f"<Simple config file at {self.config_path}>"

    def __len__(self) -> int:
        """
        Return the number of pairs present in the configuration file.
        """

        return len(self.__data)

    def __call__(self) -> dict:
        """
        Return information about the configuration file in type<dict>.
        """

        return {
            "parser_version": self.parser_version,
            "config_path": self.config_path,
            "isbase64": self.isbase64,
            "readonly": self.readonly,
            "encoding": self.encoding,
            "dict_size": len(self.__data)
        }

    @property
    def config_path(self) -> str:
        return self._config_path

    @config_path.setter
    def config_path(self, new_path: str):
        self._config_path = os.path.abspath(new_path)

    @property
    def exists(self) -> bool:
        """
        Check if the configuration file exists in the file system.
        """

        return os.path.isfile(self.config_path)

    @property
    def _forbidden_key_chars(self) -> Tuple[str, ...]:
        return (
            self._separator,
            '\n'
        )

    def _parseKey(self, key: str) -> bool:
        """
        Check if the key is valid.
        """

        if type(key) is not str:
            return False

        elif key.startswith(self._comment_char):
            return False

        elif any(char in key for char in self._forbidden_key_chars):
            return False

        else:
            return True

    def _parseValue(self, value: Any) -> bool:
        """
        Check if the value is valid.
        """

        if type(value) not in (str, int, float, bool):  # Check if data type is accepted.
            return False

        elif type(value) is str:  # Perform checks when the value is a string.
            if '\n' in value:
                return False

            else:
                return True

        else:  # Return True when no additional checks are needed.
            return True

    def load(self) -> None:
        """
        Load the configuration file contents to memory.
        Call this method when you want to read the configuration file.
        If `self.save()` is called without calling this method, the configuration file
        will be overwritten.
        """

        # Open in `rb` mode if self.isbase64 is True.
        with open(self.config_path, "rb" if self.isbase64 else 'r') as f:
            # Decode from Base64 if self.base64 is True.
            config_data = base64.b64decode(f.read()).decode(self.encoding) if self.isbase64 else f.read()

        # Parse the configuration file contents
        for line in config_data.splitlines():
            if line.startswith(self._comment_char):
                continue  # Skip comments.

            data = line.partition(self._separator)

            if data[2].isdigit():  # Check if the value is an int.
                self.__data[data[0]] = int(data[2])

            elif data[2].lower() in ("true", "false"):  # Check if the value is a bool.
                if data[2].lower() == "true":
                    self.__data[data[0]] = True

                elif data[2].lower() == "false":
                    self.__data[data[0]] = False

                else:
                    raise ValueError("Key value has unknown boolean state.")

            elif data[2].partition('.')[0].isdigit() and data[2].partition('.')[2].isdigit():  # Check if the value is a float.
                self.__data[data[0]] = float(data[2])

            else:  # If none of the above is true, the value is a string.
                self.__data[data[0]] = data[2]

    def save(self) -> None:
        """
        Save the configuration file to <self.config_path>.
        This method raises a `PermissionError` if the configuration file is read-only.
        """

        if self.readonly:
            raise PermissionError("The configuration file is read-only.")

        config_data = ""  # The string to be written to file.
        for key in self.__data:
            config_data += f"{key}={self.__data[key]}\n"  # Write the key-value pair to the config file.

        # Open in `wb` mode if self.isbase64 is True.
        with open(self.config_path, "wb" if self.isbase64 else 'w') as f:
            # Encode to Base64 if self.base64 is True.
            f.write(base64.b64encode(config_data.encode(self.encoding)) if self.isbase64 else config_data)

    def setdefault(self, key: str, default: Any = None) -> Any:
        """
        Set the value of <key> to <default> if it does not exist.
        Raises a `ValueError` if the key or value has invalid characters.

        :returns: The value of <key> if it exists, otherwise <default>.
        """

        if not self._parseKey(key):
            raise ValueError("Key contains invalid characters.")

        if not self._parseValue(default):
            raise ValueError("Default value contains invalid characters.")

        return self.__data.setdefault(key, default)

    def set(self, key: str, value: Union[str, int, float, bool]) -> None:
        """
        Set a key-value pair in the configuration file.
        Raises a `ValueError` if the key or value has invalid characters.

        :param key: The key of the pair.
        :param value: The value of the key.
        """

        if not self._parseKey(key):
            raise ValueError("Key contains invalid characters.")

        if not self._parseValue(value):
            raise ValueError("Value contains invalid characters.")

        self.__data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get the value of <key> or <default> if the key does not exist.
        """

        return self.__data.get(key, default)

    def remove(self, key: str) -> None:
        """
        Remove a key from the configuration file.
        """

        del self.__data[key]

    def pop(self, key: str, default: Any = None) -> Any:
        """
        Remove and return the value of <key>. <default> is returned if the key does not exist.
        """

        return self.__data.pop(key, default)

    def popitem(self) -> Tuple[str, Any]:
        """
        Pop a key-pair value from the configuration file.
        """

        return self.__data.popitem()

    def items(self) -> List[Tuple[str, Any]]:
        """
        Return a list of key-value pairs of the configuration file.
        """

        return list(self.__data.items())

    def keys(self) -> List[str]:
        """
        Return existing keys in the configuration file.
        """

        return list(self.__data.keys())

    def values(self) -> List[Any]:
        """
        Return a list of values in the configuration file.
        """

        return list(self.__data.values())

    def clear(self) -> None:
        """
        Clear all key-value pairs in the configuration file.
        """

        self.__data.clear()
