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

import sys

from config_handler import _ui
from config_handler._interactive import utils
from config_handler._interactive import open_config
from config_handler._interactive import create_new_config


def main() -> int:
    """
    The main function of the program.

    :returns: The exit code.
    """

    while True:
        try:
            menu_action: str = _ui.Choices(
                list_of_choices = {
                    "E": "Open An Existing Configuration File",
                    "C": "Create A New Configuration File",
                    "I": "About",
                    "Q": "Quit"
                },
                description = "Choose the operation you want to perform.",
                case_sensitive = False
            )().lower()

            if menu_action == 'q':
                print("Exiting...")
                return 0

            elif menu_action == 'e':
                open_config.openConfig()

            elif menu_action == 'c':
                create_new_config.createNewConfig()

            elif menu_action == 'i':
                utils.showProgramInformation()
                _ui.confirm()

        except (KeyboardInterrupt, EOFError):
            print("\nForce exiting...")
            sys.exit(2)

        except Exception as e:
            print(f"[CRITICAL] An unhandled exception occurred: {e}")
            print()
            return 1


if __name__ == "__main__":
    sys.exit(main())
