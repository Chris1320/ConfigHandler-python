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
from typing import Any
from typing import Final

from config_handler.simple import Simple


class TestSimpleConfigHandler:
    _tests_folder: Final[str] = os.path.join(os.getcwd(), "tests_data", "simple")
    simple_configpath: Final[str] = os.path.join(_tests_folder, "test.conf")
    simple_base64_configpath: Final[str] = os.path.join(_tests_folder, "base64_test.conf")

    bulk_ops_range: Final[int] = 10000

    key_value_pairs: Final[dict[str, Any]] = {
        "foo": "bar",
        "nums": 123,
        "dec": 3.14,
        "Aboolean": True,
        "unintentional variable!": "unintentional value."
    }
    forbidden_chars_in_key: Final[dict[Any, Any]] = {
        "=": "equal sign",
        "#": "hash",
        "\n": "newline",
        "c=a+b": "equation is the key",
        "#something": "comment",
        "foo\nbar": "newline in key",
        123: "number",
        3.14: "pi",
        False: "boolean"
    }
    forbidden_chars_in_value: Final[dict[str, Any]] = {
        "foo": ("b", "a", "r"),
        "newline": "something\nhere"
    }
    if not os.path.exists(_tests_folder):
        os.makedirs(_tests_folder)

    # Remove configuration files if they exist.
    if os.path.exists(simple_configpath):
        os.remove(simple_configpath)

    if os.path.exists(simple_base64_configpath):
        os.remove(simple_base64_configpath)

    def testNewConfig(self):
        """
        Create a new configuration file.
        """

        config = Simple(self.simple_configpath)

        # Set the key-value pairs.
        for key, value in self.key_value_pairs.items():
            config[key] = value

        assert len(config) == len(self.key_value_pairs)

        # Remove a key-value pair.
        del config["unintentional variable!"]

        config.save()  # Save the configuration file.

        # Check if the contents of the configuration file are in the expected format.
        with open(self.simple_configpath, 'r') as f:
            assert f.read() == "foo=bar\nnums=123\ndec=3.14\nAboolean=True\n"

    def testLoadConfig(self):
        """
        Load a configuration file.
        """

        if not os.path.exists(self.simple_configpath):
            # Create test file if it does not exist.
            with open(self.simple_configpath, "w") as f:
                f.write("foo=bar\nnums=123\ndec=3.14\nAboolean=True\n")

        config = Simple(self.simple_configpath)
        config.load()  # Load the configuration file.

        assert config["foo"] == "bar"
        try:
            config["unintentional variable!"]

        except KeyError:
            pass  # This is expected.

        else:
            assert False  # KeyError should've been raised.

        config["foo"] = "barred"  # Change value of existing key.
        config["new key"] = "new value"  # Add new key-value pair.

        assert config["foo"] == "barred"
        assert config["new key"] == "new value"

        config.save()  # Save the configuration file.

        # Check if the contents of the configuration file are in the expected format.
        with open(self.simple_configpath, "r") as f:
            assert f.read() == "foo=barred\nnums=123\ndec=3.14\nAboolean=True\nnew key=new value\n"

    def testNewBase64Config(self):
        """
        Create a new configuration file with base64 encoding.
        """

        config = Simple(self.simple_base64_configpath, isbase64=True)

        # Set the key-value pairs.
        for key, value in self.key_value_pairs.items():
            config[key] = value

        assert len(config) == len(self.key_value_pairs)

        # Remove a key-value pair.
        del config["unintentional variable!"]

        config.save()  # Save the configuration file.

        # Check if the contents of the configuration file are in the expected format.
        with open(self.simple_base64_configpath, 'rb') as f:
            assert f.read() == b"Zm9vPWJhcgpudW1zPTEyMwpkZWM9My4xNApBYm9vbGVhbj1UcnVlCg=="

    def testLoadBase64Config(self):
        """
        Load a configuration file with base64 encoding.
        """

        if not os.path.exists(self.simple_base64_configpath):
            # Create test file if it does not exist.
            with open(self.simple_base64_configpath, "wb") as f:
                f.write(b"Zm9vPWJhcgpudW1zPTEyMwpkZWM9My4xNApBYm9vbGVhbj1UcnVlCg==")

        config = Simple(self.simple_base64_configpath, isbase64=True)
        config.load()

        assert config["foo"] == "bar"
        try:
            config["unintentional variable!"]

        except KeyError:
            pass  # This is expected.

        else:
            assert False  # KeyError should've been raised.

        config["foo"] = "barred"  # Change value of existing key.
        config["new key"] = "new value"  # Add new key-value pair.

        config.save()

        # Check if the contents of the configuration file are in the expected format.
        with open(self.simple_base64_configpath, "rb") as f:
            assert f.read() == b"Zm9vPWJhcnJlZApudW1zPTEyMwpkZWM9My4xNApBYm9vbGVhbj1UcnVlCm5ldyBrZXk9bmV3IHZhbHVlCg=="

    def testDunderMethods(self):
        """
        Test dunder methods of the simple ConfigHandler object.
        """

        with open(self.simple_configpath, 'w') as f:
            f.write("foo=bar\nnums=123\ndec=3.14\nAboolean=True\n")

        config = Simple(self.simple_configpath)
        config.load()
        assert "foo" in config
        del config["foo"]
        assert "foo" not in config
        assert str(config) == f"<Simple config file at {os.path.abspath(self.simple_configpath)}>"
        assert len(config) == 3
        assert config.setdefault("foo", "boo") == "boo"
        assert len(config) == 4

        config_info = config()
        for key, value in config_info.items():
            if key == "parser_version":
                continue

            elif key == "config_path":
                assert value == os.path.abspath(self.simple_configpath)

            elif key == "isbase64":
                assert value is False

            elif key == "readonly":
                assert value is False

            elif key == "encoding":
                assert value == "utf-8"

            elif key == "dict_size":
                assert value == 4

            else:
                raise AssertionError(f"Unknown key: {key}")

    def testForbiddenCharsInKey(self):
        """
        Test if forbidden characters are detected in the key.
        """

        config = Simple(self.simple_configpath)
        old_config_items = config.items()

        for key, value in self.forbidden_chars_in_key.items():
            try:
                config[key] = value

            except ValueError:
                pass

            else:
                assert False  # ValueError should've been raised.

        assert old_config_items == config.items()

    def testForbiddenCharsInValue(self):
        """
        Test if forbidden characters are detected in the value.
        """

        config = Simple(self.simple_configpath)
        old_config_items = config.items()

        for key, value in self.forbidden_chars_in_value.items():
            try:
                config[key] = value

            except ValueError:
                pass

            else:
                assert False  # ValueError should've been raised.

        assert old_config_items == config.items()

    def testConvertToBase64(self):
        """
        Test if the module can convert a non-base64 configuration file to a base64 configuration file
        by setting `config.isbase64` to `True`.
        """

        with open(self.simple_base64_configpath, 'w') as f:
            f.write("foo=bar\nnums=123\ndec=3.14\nAboolean=True\n")

        config = Simple(self.simple_base64_configpath)
        config.load()

        assert config["foo"] == "bar"
        assert config["nums"] == 123
        assert config["dec"] == 3.14
        assert config["Aboolean"] is True
        config.isbase64 = True
        config.save()

        # Check if the contents of the configuration file are in the expected format.
        with open(self.simple_base64_configpath, "rb") as f:
            assert f.read() == b"Zm9vPWJhcgpudW1zPTEyMwpkZWM9My4xNApBYm9vbGVhbj1UcnVlCg=="

    def testConvertFromBase64(self):
        """
        Test if the module can convert a base64 configuration file to a non-base64 configuration file
        by setting `config.isbase64` to `False`.
        """

        with open(self.simple_configpath, 'wb') as f:
            f.write(b"Zm9vPWJhcgpudW1zPTEyMwpkZWM9My4xNApBYm9vbGVhbj1UcnVlCg==")

        config = Simple(self.simple_configpath, isbase64=True)
        config.load()

        assert config["foo"] == "bar"
        assert config["nums"] == 123
        assert config["dec"] == 3.14
        assert config["Aboolean"] is True
        config.isbase64 = False
        config.save()

        # Check if the contents of the configuration file are in the expected format.
        with open(self.simple_configpath, "r") as f:
            assert f.read() == "foo=bar\nnums=123\ndec=3.14\nAboolean=True\n"

    def testReadOnlyMode(self):
        """
        Test read-only mode of simple ConfigHandler.
        """

        with open(self.simple_configpath, 'w') as f:
            f.write("foo=bar\nnums=123\ndec=3.14\nAboolean=True\n")

        config = Simple(self.simple_configpath, readonly=True)
        config.load()

        assert "foo" in config
        del config["foo"]
        assert "foo" not in config

        config["another key"] = "another value"

        try:
            config.save()

        except PermissionError:
            pass  # This is expected.

        else:
            assert False  # PermissionError should've been raised because readonly is True.

    def testBulkWriteOperations(self, benchmark):
        """
        Perform many write operations using simple ConfigHandler.
        This also benchmarks the performance of its `save()` method.
        """

        config = Simple(self.simple_configpath)

        for index, value in enumerate(range(0, self.bulk_ops_range)):
            config[f"key_{index}"] = value

        benchmark(config.save)

    def testBulkLoadOperations(self, benchmark):
        """
        Load the configuration file made by `self.testBulkWriteOperations()`.
        This also benchmarks the performance of its `load()` method.
        """

        config = Simple(self.simple_configpath)
        benchmark(config.load)

        assert len(config) == self.bulk_ops_range
