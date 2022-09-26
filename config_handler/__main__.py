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
import sys

from config_handler import _ui
from config_handler import info


class Main:
    def __init__(self):
        pass

    def showProgramInformation(self) -> None:
        """
        Show the program information.
        """

        print()
        print(info.title)
        print()
        print(f"Program Version: v{'.'.join([str(v) for v in info.version])}")
        print(f"Program Release: {info.release}")
        print()
        print(f"Current Working Directory: `{os.getcwd()}`")
        print()

    def createNewConfig(self) -> None:
        """
        Create a new configuration file.
        """

        config_path = _ui.InputBox(
            title = "Create A New Configuration File",
            description = "Please enter the filepath of the new configuration file."
            # WIP
        )

    def main(self) -> int:
        while True:
            try:
                menu_action: int = int(_ui.Choices(
                    list_of_choices = {
                        "1": "Open An Existing Configuration File",
                        "2": "Create A New Configuration File",
                        "3": "Open Settings",
                        "98": "About",
                        "99": "Quit"
                    },
                    description = "Enter the number of the operation you want to perform.",
                    case_sensitive = False
                )())

                if menu_action == 99:
                    print("Exiting...")
                    return 0

                elif menu_action == 1:
                    _ui.confirm()

                elif menu_action == 2:
                    self.createNewConfig()

                elif menu_action == 3:
                    print("Settings")
                    _ui.confirm()

                elif menu_action == 98:
                    self.showProgramInformation()
                    _ui.confirm()

                else:
                    print("THIS SHOULD NOT HAPPEN!") # DEV0005: This is temporary.
                    _ui.confirm()

            except KeyboardInterrupt:
                continue  # Ignore CTRL+C


if __name__ == "__main__":
    sys.exit(Main().main())
