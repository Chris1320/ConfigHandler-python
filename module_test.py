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
import base64
from config_handler.simple import Simple
from config_handler.advanced import Advanced


class TestClass:
    simple_configpath = "./simple_test.conf"
    advanced_configpath = "./advanced_test.conf"

    def test_simple_new(self):
        config = Simple(TestClass.simple_configpath)
        key_value_pairs = {
            "foo": "bar",
            "nums": 123,
            "dec": 3.14,
            "Aboolean": True,
            "unintentional variable!": "unintentional value."
        }
        for key, value in key_value_pairs.items():
            config.set(key, value)

        config.remove("unintentional variable!")
        config.save()
        with open(TestClass.simple_configpath, 'r') as f:
            assert f.read() == "foo=bar\nnums=123\ndec=3.14\nAboolean=True\n"

        for key in config.keys():
            assert config.get(key) == key_value_pairs[key]

    def test_simple_load(self):
        if not os.path.exists(TestClass.simple_configpath):
            # Create test file if it does not exist.
            with open(TestClass.simple_configpath, "w") as f:
                f.write("foo=bar\nnums=123\ndec=3.14\nAboolean=True\n")

        config = Simple(TestClass.simple_configpath)
        config.load()
        assert config.get("foo") == "bar"
        try:
            config.get("new_key")

        except KeyError:
            pass  # Test passed

        else:
            raise AssertionError("KeyError not raised.")

        config.set("foo", "barred")
        config.set("new_key", "new_value")

        assert config.get("foo") == "barred"
        assert config.get("new_key") == "new_value"

        config.isbase64 = True
        config.save()

        with open(TestClass.simple_configpath, "r") as f:
            assert base64.b64decode(f.read().encode("utf-8")).decode() == "foo=barred\nnums=123\ndec=3.14\nAboolean=True\nnew_key=new_value\n"

    def test_simple_load_base64(self):
        with open(TestClass.simple_configpath, "w") as f:
            f.write("Zm9vPWJhcnJlZApudW1zPTEyMwpkZWM9My4xNApBYm9vbGVhbj1UcnVlCm5ld19rZXk9bmV3X3ZhbHVlCg==")

        config = Simple(TestClass.simple_configpath, True)
        config.load()

        assert list(config.keys()) == ["foo", "nums", "dec", "Aboolean", "new_key"]

    def test_advanced_new(self):
        config = Advanced(TestClass.advanced_configpath, "p4ssw0rd")
        config.new(
            name="Advanced Mode Test",
            author="Chris1320",
            compression="zlib",
            encryption="aes256"
        )

        # Create a new configuration file by assigning key-value pair.
        key_value_pairs = {
            "foo": "bar",  # "foo" is the key, "bar" is the value.
            "nums": 123,
            "dec": 3.14,
            "Aboolean": True,
            "unintentional variable!": "unintentional value."
        }
        for key, value in key_value_pairs.items():
            config.set(key, value)

        # Remove values
        config.remove("unintentional variable!")
        config.save()  # Save the data to the file.
        config_keys = key_value_pairs.copy()
        config_keys.pop("unintentional variable!")
        config_checksum = config._generateChecksum(json.dumps(config_keys).encode("utf-8"))

        assert config.epass == "p4ssw0rd"
        assert config.config_path == TestClass.advanced_configpath
        assert list(config.keys()) == ["foo", "nums", "dec", "Aboolean"]
        assert config.metadata() == {
            "name": "Advanced Mode Test",
            "author": "Chris1320",
            "compression": "zlib",
            "encryption": "aes256",
            "encoding": "utf-8",
            "version": Advanced.VERSION,
            "checksum": config_checksum,
            "dictionary_size": 4
        }

    def test_advanced_load(self):
        config = Advanced(TestClass.advanced_configpath, "p4ssw0rd")
        if not os.path.exists(TestClass.advanced_configpath):
            config.new(
                name="Advanced Mode Test",
                author="Chris1320",
                compression="zlib",
                encryption="aes256"
            )

        config.load()
        config.get("foo")
        config.set("foo", "barred")
        config.set("new_key", "new_value")
        config.metadata()
        config.save()  # Save changes
        config_keys = {}
        for key in config.keys():
            config_keys[key] = config.get(key)

        config_checksum = config._generateChecksum(json.dumps(config_keys).encode("utf-8"))
        assert config.metadata() == {
            "name": "Advanced Mode Test",
            "author": "Chris1320",
            "compression": "zlib",
            "encryption": "aes256",
            "encoding": "utf-8",
            "version": Advanced.VERSION,
            "checksum": config_checksum,
            "dictionary_size": len(config_keys)
        }
