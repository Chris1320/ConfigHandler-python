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
from getpass import getpass

from config_handler import info


def showProgramInformation() -> None:
    """
    Show the program information.
    """

    print()
    print(info.title)
    print()
    print(f"Program Version:           v{'.'.join([str(v) for v in info.version])}")
    print(f"Program Release:           {info.release}")
    print(f"Current Working Directory: {os.getcwd()}")
    print()


def getConfigurationFilePassword(
    *,
    prompt: str = "Enter configuration file password: ",
    confirmation_prompt: str = "Re-enter configuration file password: ",
    set_new_pass: bool = True
) -> str:
    """
    Ask the user for the configuration file password.

    :param prompt: The prompt to show.
    :param confirmation_prompt: The confirmation prompt to show.
    :param set_new_pass: True if user is setting a new password. (Will show confirmation prompt)
    """

    # ? https://security.stackexchange.com/questions/29019/are-passwords-stored-in-memory-safe
    if not set_new_pass:
        return getpass(prompt)

    while True:
        first_input: str = getpass(prompt)
        confirm_input: str = getpass(confirmation_prompt)
        if first_input == confirm_input:
            return confirm_input

        else:
            print("[E] Passwords do not match.")
            continue
