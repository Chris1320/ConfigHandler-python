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

import builtins

from config_handler import _ui


def testConfigHandlerUIInputBox(monkeypatch):
    test_inputs = (
        "The quick brown fox jumps over the lazy dog.",
        "Integer vehicula dignissim fermentum. Nullam.",
        "Pellentesque massa dui, volutpat sed."
    )
    input_box = _ui.InputBox(
        title = "Test Input Box",
        description = "This is just a test.",
        clear_screen = False,
        title_fill_char = '-',
        margin = 4
    )

    for test_input in test_inputs:
        monkeypatch.setattr(builtins, "input", lambda *args, **kwargs: test_input)
        monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)
        assert input_box() == test_input

    input_box = _ui.InputBox()
    for test_input in test_inputs:
        monkeypatch.setattr(builtins, "input", lambda *args, **kwargs: test_input)
        monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)
        assert input_box() == test_input


def testConfigHandlerUIChoices(monkeypatch):
    test_choices = {
        '1': "Option #1",
        '2': "Option #2",
        '3': "Option #3",
        "Q": "Option Q",
        "h": "Option h"
    }
    choices_dialog = _ui.Choices(
        list_of_choices = test_choices,
        title = "Test Choices Dialog",
        description = "This is just a test.",
    )

    for choice_key in test_choices:
        monkeypatch.setattr(builtins, "input", lambda *args, **kwargs: choice_key)
        monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)
        assert choices_dialog() == choice_key
