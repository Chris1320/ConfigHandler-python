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
import shlex
from typing import Final

from config_handler import _ui
from config_handler import info
from config_handler import simple
from config_handler._interactive.utils import showProgramInformation
from config_handler._interactive.create_new_config import createNewConfig

try:
    import prettytable

except ImportError:
    PRETTYTABLE_SUPPORT: Final[bool] = False

else:
    PRETTYTABLE_SUPPORT: Final[bool] = True


def openConfig() -> None:
    """
    Open an existing configuration file.

    This function only asks the user for the filepath and
    the config kind (simple or advanced) and calls another
    function for that kind of configuration file.
    """

    while True:
        try:
            config_path: str = _ui.InputBox(
                title = "Open an Existing Configuration File",
                description = "Please enter the filepath of an existing configuration file. CTRL+C to cancel."
            )()
            if _ui.Choices(
                list_of_choices = {
                    'y': "Yes",
                    'n': "No"
                },
                description = f"Is this correct? `{config_path}`",
                case_sensitive = False
            )().lower() == 'y':
                break

            else:
                continue

        except (KeyboardInterrupt, EOFError):
            return

    while True:
        try:
            config_type: str = _ui.Choices(
                list_of_choices = {
                    '1': "Simple Configuration File",
                    '2': "Advanced Configuration File",
                    "99": "Cancel"
                }
            )()

            if config_type == '1':
                openSimpleConfig(config_path)
                return

            elif config_type == '2':
                openAdvancedConfig(config_path)
                return

            elif config_type == "99":
                return

        except (KeyboardInterrupt, EOFError):
            return


def openSimpleConfig(config_path: str) -> None:
    """
    Open a simple configuration file.
    """

    config_opts = {
        "isbase64": False,
        "readonly": False,
        "command_mode": False,
        "encoding": info.defaults["encoding"]
    }
    while True:  # Show options menu first.
        choice = _ui.Choices(
            list_of_choices = {
                '1': f"Toggle base64 encoding (Current: {config_opts['isbase64']})",
                '2': f"Toggle read-only mode (Current: {config_opts['readonly']})",
                '3': f"Set encoding ({config_opts['encoding']})",
                "97": "Cancel",
                "98": "Open Configuration File in Command Mode",
                "99": "Open Configuration File"
            }
        )()

        if choice == "97":
            return

        elif choice == '1':
            config_opts["isbase64"] = not config_opts["isbase64"]

        elif choice == '2':
            config_opts["readonly"] = not config_opts["readonly"]

        elif choice == '3':
            new_conf_encoding: str = _ui.InputBox(
                title = "Enter new encoding to use",
                description = f"Leave blank for default. ({info.defaults['encoding']})"
            )().replace(' ', '')
            config_opts["encoding"] = info.defaults["encoding"] if new_conf_encoding == '' else new_conf_encoding

        elif choice == "98":
            config_opts["command_mode"] = True
            break

        elif choice == "99":
            break

    # ? Attempt to open configuration file.
    try:
        conf = simple.Simple(
            config_path = config_path,
            isbase64 = config_opts["isbase64"],
            readonly = config_opts["readonly"],
            encoding = config_opts["encoding"]
        )

    except Exception as e:
        print(f"[ERROR] Cannot open configuration file: {e}")
        _ui.confirm()
        return

    else:
        _ui.clearScreen()
        if config_opts["command_mode"]:
            for k, v in conf().items():
                print(f"{k}: {v}")

            print()
            print("[i] Type `help` for more information. Type `quit` to exit.")
            print()
            help_menu = """Available Commands:

load                     Load the configuration file.
save [as]                Save the configuration file. If `as` is added as an argument, ask for a new filepath.
info                     Show information about the configuration file.

get <key>                Get the value of a key.
set <key> <value>        Set the value of a key.
list                     List all existing key/value pairs in the configuration file.

quit                     Close the configuration file.
help                     Show this help menu."""
            while True:
                try:
                    command = shlex.split(input(" >>> "))

                    if command[0] == "quit":
                        return

                    elif command[0] == "help":
                        print()
                        print(help_menu)
                        print()

                    elif command[0] == "load":
                        conf.load()

                    elif command[0] == "save":
                        try:
                            if command[1] == "as":
                                while True:
                                    new_config_filepath = _ui.InputBox(
                                        title = f"{info.title} (Save As)",
                                        description = "Enter a new filepath. Press CTRL+C to cancel."
                                    )()

                                    # Check if file exists
                                    if not os.path.isfile(new_config_filepath):
                                        conf.config_path = new_config_filepath
                                        conf.save()
                                        break

                                    else:
                                        # Ask permission for overwrite
                                        if _ui.Choices(
                                            list_of_choices = {'Y': "Yes", 'N': "No"},
                                            title = f"{info.title} (Save As)",
                                            description = "A file with the same name already exists. Do you want to continue?"
                                        )().lower() == 'y':
                                            conf.config_path = new_config_filepath
                                            conf.save()
                                            break

                                        continue  # If no, ask for new filename.

                            else:
                                conf.save()

                        except IndexError:
                            conf.save()  # Save modifications to file. (no `as` argument)

                        except KeyboardInterrupt:
                            pass

                    elif command[0] == "info":
                        if PRETTYTABLE_SUPPORT:
                            conf_info = prettytable.PrettyTable(title = info.title)
                            conf_info.add_rows((conf().items()))
                            print(conf_info)

                        else:
                            print(info.title)
                            print()
                            for k, v in conf().items():
                                print(f"{k}: {v}")

                            print()

                    elif command[0] == "get":
                        print(conf[command[1]])

                    elif command[0] == "set":
                        conf[command[1]] = command[2]

                    elif command[0] == "list":
                        if PRETTYTABLE_SUPPORT:
                            conf_items = prettytable.PrettyTable(("Key", "Value"))
                            for k, v in conf.items():
                                conf_items.add_row((k, v))

                            print(conf_items)

                        else:
                            print("Key: Value")
                            print()
                            for k, v in conf.items():
                                print(f"- {k}: {v}")

                            print()

                except Exception as e:
                    print(f"[ERROR] {e}")


def openAdvancedConfig(config_path: str) -> None:
    """
    Open an advanced configuration file.
    """


def main() -> int:
    """
    The main function of the program.

    :returns: The exit code.
    """

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
                openConfig()

            elif menu_action == 2:
                createNewConfig()

            elif menu_action == 98:
                showProgramInformation()
                _ui.confirm()

            else:
                print("THIS SHOULD NOT HAPPEN!")  # DEV0005: This is temporary.
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
