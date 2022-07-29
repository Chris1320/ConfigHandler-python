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

from config_handler import exceptions
from config_handler.advanced import Advanced


class TestAdvancedConfigHandler:
    _tests_folder: Final[str] = os.path.join(os.getcwd(), "tests_data", "advanced")
    advanced_configpath: Final[str] = os.path.join(_tests_folder, "test.conf")

    bulk_ops_range: Final[int] = 10000

    key_value_pairs: Final[dict[str, Any]] = {
        "foo": "bar",
        "nums": 123,
        "dec": 3.14,
        "Aboolean": True,
        "unintentional variable!": "unintentional value."
    }
    if not os.path.exists(_tests_folder):
        os.makedirs(_tests_folder)

    # Remove configuration files if they exist.
    if os.path.exists(advanced_configpath):
        os.remove(advanced_configpath)

    def testNewConfig(self):
        config = Advanced(self.advanced_configpath)
        try:
            config["test"]

        except exceptions.ConfigFileNotInitializedError:
            pass

        else:
            raise AssertionError("ConfigFileNotInitializedError should've been raised.")

        try:
            assert config.get("uninitialized", "expected_value") == "expected_value"

        except exceptions.ConfigFileNotInitializedError:
            pass

        else:
            raise AssertionError("ConfigFileNotInitializedError should've been raised.")

        assert not config.exists

        config.new()  # Initialize configuration file.

        assert not config.exists

        config.save()  # Save to file.

        assert config.exists
        assert config.get("non-existent", "expected_value") == "expected_value"

        # Set the key-value pairs.
        for key, value in self.key_value_pairs.items():
            config[key] = value

        assert len(config) == len(self.key_value_pairs)

        # Remove a key-value pair.
        del config["unintentional variable!"]

        config.save()  # Save the configuration file.

    def testLoadConfig(self):
        config = Advanced(self.advanced_configpath)
        assert config.exists
        try:
            config["test"]

        except exceptions.ConfigFileNotInitializedError:
            pass

        else:
            raise AssertionError("ConfigFileNotInitializedError should've been raised.")

        config.load()

        assert config.name == "config_handler.advanced"
        assert config.author is None
        assert config["foo"] == "bar"
        assert config.get("non-existent", "expected_value") == "expected_value"
        config.set("foo", "bar2")
        assert config["foo"] == "bar2"

    def testCompression(self):
        pass

    def testEncryption(self):
        pass

    def testCompressionAndEncryption(self):
        pass

    def testDunderMethods(self):
        pass
