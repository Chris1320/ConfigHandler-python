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
        print(f"Program Version:           v{'.'.join([str(v) for v in info.version])}")
        print(f"Program Release:           {info.release}")
        print(f"Current Working Directory: {os.getcwd()}")
        print()

    def createNewConfig(self) -> None:
        """
        Create a new configuration file.
        """

        # Ask for the filepath of the new configuration file.
        while True:
            try:
                config_path: str = _ui.InputBox(
                    title = "Create A New Configuration File",
                    description = "Please enter the filepath of the new configuration file. CTRL+C to cancel."
                )()
                if _ui.Choices(
                    list_of_choices = {
                        'y': "Yes",
                        'n': "No"
                    },
                    description = f"Is this correct? `{config_path}`",
                    case_sensitive = False
                )() == 'y':
                    break

                else:
                    continue

            except (KeyboardInterrupt, EOFError):
                return  # Cancel configuration file creation.

        # Ask for the type of the new configuration file.
        config_type: str = _ui.Choices(
            list_of_choices = {
                '1': "Simple Configuration File",
                '2': "Advanced Configuration File",
                '99': "Cancel"
            }
        )()

        if config_type == '99':
            return  # Cancel configuration file creation.

        elif config_type == '1':
            config_opts = {
                "base64": False,
                "encoding": info.defaults["encoding"]
            }
            while True:
                _ui.clearScreen()
                config_opts_action: str = _ui.Choices(
                    list_of_choices = {
                        '1': f"Encode to Base64 (Current: {config_opts['base64']})",
                        '2': f"Set encoding     (Current: {config_opts['encoding']})",
                        "98": "Cancel",
                        "99": "Create Configuration File"
                    },
                    description = "Set configuration file options",
                    case_sensitive = False
                )()

                if config_opts_action == "98":
                    return  # Cancel configuration file creation.

                elif config_opts_action == '1':
                    config_opts["base64"] = not config_opts["base64"]

                elif config_opts_action == '2':
                    new_conf_encoding: str = _ui.InputBox(
                        title = "Enter new encoding to use",
                        description = f"Leave blank for default. ({info.defaults['encoding']})"
                    )().replace(' ', '')
                    config_opts["encoding"] = info.defaults["encoding"] if new_conf_encoding == '' else new_conf_encoding

                elif config_opts_action == "99":
                    print("Creating new configuration file...")

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

            except (KeyboardInterrupt, EOFError):
                print("\nForce exiting...")
                sys.exit(2)

            except Exception as e:
                print(f"[CRITICAL] An unhandled exception occured: {e}")
                print()
                return 1


if __name__ == "__main__":
    sys.exit(Main().main())
