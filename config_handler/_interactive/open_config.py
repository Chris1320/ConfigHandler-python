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
import shlex
import shutil
from typing import Dict
from typing import Final
from typing import Union

from config_handler import _ui
from config_handler import info
from config_handler.simple import Simple
from config_handler.advanced import Advanced


try:
    import prettytable

except ImportError:
    PRETTYTABLE_SUPPORT: Final[bool] = False

else:
    PRETTYTABLE_SUPPORT: Final[bool] = True


class SimpleConfigManager:
    def __init__(self, config_path: str):
        """
        The initialization method of SimpleConfigManager() class.

        This class handles interactions between the user and ConfigHandler.

        :param config_path: The path to the configuration file to open.
        """

        self.conf: Union[Simple, None] = None
        self.config_path = config_path
        self.config_opts = {
            "prompt": " >>> ",
            "isbase64": False,
            "readonly": False,
            "command_mode": False,
            "encoding": info.defaults["encoding"],
            "browser_items_to_show": info.defaults["browser_items_to_show"]
        }

    def settings(self) -> None:
        """
        Let the user configure the manager.
        """

        while True:  # Show options menu first.
            choice = _ui.Choices(
                list_of_choices = {
                    '1': f"Toggle base64 encoding (Current: {self.config_opts['isbase64']})",
                    '2': f"Toggle read-only mode (Current: {self.config_opts['readonly']})",
                    '3': f"Set encoding ({self.config_opts['encoding']})",
                    '4': f"Number of items per panel in browser (Current: {self.config_opts['browser_items_to_show']})",
                    "97": "Cancel",
                    "98": "Open Configuration File in Command Mode",
                    "99": "Open Configuration File"
                }
            )()

            if choice == "97":
                return

            elif choice == '1':
                self.config_opts["isbase64"] = not self.config_opts["isbase64"]

            elif choice == '2':
                self.config_opts["readonly"] = not self.config_opts["readonly"]

            elif choice == '3':
                new_conf_encoding: str = _ui.InputBox(
                    title = "Enter new encoding to use",
                    description = f"Leave blank for default. ({info.defaults['encoding']})"
                )().replace(' ', '')
                self.config_opts["encoding"] = info.defaults["encoding"]\
                    if new_conf_encoding == ''\
                    else new_conf_encoding

            elif choice == '4':
                while True:
                    try:
                        new_browser_items_to_show: str = _ui.InputBox(
                            title = "Number of items to show per panel in configuration file browser",
                            description = f"Leave blank for default. ({info.defaults['browser_items_to_show']})"
                        )()
                        self.config_opts["browser_items_to_show"] = info.defaults["browser_items_to_show"]\
                            if new_browser_items_to_show == ''\
                            else int(new_browser_items_to_show)

                    except ValueError:
                        continue

                    else:
                        break

            elif choice == "98":
                self.config_opts["command_mode"] = True
                break

            elif choice == "99":
                break

    def startCommandMode(self) -> None:
        """
        Start an interactive session in "command" mode.
        """

        for k, v in self.conf().items():
            print(f"{k}: {v}")

        print()
        if not PRETTYTABLE_SUPPORT:
            print("[!] `prettytable` is not installed.")

        print("[i] Type `help` for more information. Type `quit` to exit.")
        print()
        help_menu = """Available Commands:

load                     Load the configuration file.
save [as]                Save the configuration file. If `as` is added as an argument, ask for a new filepath.
info                     Show information about the configuration file.

get <key>                Get the value of a key.
set <key> <value>        Set the value of a key.
del <key>                Remove an existing key/value pair from the configuration file.
list                     List all existing key/value pairs in the configuration file.

base64                   Toggle base64 encoding of the configuration file.
encoding <encoding>      Change the encoding of the configuration file.

quit | exit              Close the configuration file.
help                     Show this help menu."""
        while True:
            try:
                command = shlex.split(input(self.config_opts["prompt"]))

                if command[0] in {"quit", "exit"}:
                    return

                elif command[0] == "help":
                    print()
                    print(help_menu)
                    print()

                elif command[0] == "load":
                    self.conf.load()

                elif command[0] == "save":
                    try:
                        if command[1] == "as":
                            while True:
                                new_config_filepath = _ui.InputBox(
                                    title=f"{info.title} (Save As)",
                                    description="Enter a new filepath. Press CTRL+C to cancel."
                                )()

                                # Check if file exists
                                if not os.path.isfile(new_config_filepath):
                                    self.conf.config_path = new_config_filepath
                                    self.conf.save()
                                    break

                                else:
                                    # Ask permission for overwrite
                                    if _ui.Choices(
                                        list_of_choices={'Y': "Yes", 'N': "No"},
                                        title=f"{info.title} (Save As)",
                                        description="A file with the same name already exists. Do you want to continue?"
                                    )().lower() == 'y':
                                        self.conf.config_path = new_config_filepath
                                        self.conf.save()
                                        break

                                    continue  # If no, ask for new filename.

                        else:
                            self.conf.save()

                    except IndexError:
                        self.conf.save()  # Save modifications to file. (no `as` argument)

                    except KeyboardInterrupt:
                        pass

                elif command[0] == "info":
                    if PRETTYTABLE_SUPPORT:
                        conf_info = prettytable.PrettyTable(title=info.title, header=False)
                        conf_info.add_rows((self.conf().items()))
                        print(conf_info)

                    else:
                        print(info.title)
                        print()
                        for k, v in self.conf().items():
                            print(f"{k}: {v}")

                        print()

                elif command[0] == "get":
                    print(self.conf[command[1]])

                elif command[0] == "set":
                    self.conf[command[1]] = command[2]

                elif command[0] == "del":
                    del self.conf[command[1]]

                elif command[0] == "list":
                    if PRETTYTABLE_SUPPORT:
                        conf_items = prettytable.PrettyTable(("Key", "Value"))
                        for k, v in self.conf.items():
                            conf_items.add_row((k, v))

                        print(conf_items)

                    else:
                        print("Key: Value")
                        print()
                        for k, v in self.conf.items():
                            print(f"- {k}: {v}")

                        print()

                elif command[0] == "base64":
                    self.conf.isbase64 = not self.conf.isbase64
                    print("Base64 encoding is enabled." if self.conf.isbase64 else "Base64 encoding is disabled.")

                elif command[0] == "encoding":
                    self.conf.encoding = command[1]
                    print(f"Encoding successfully changed to {command[1]}.")

            except Exception as e:
                print(f"[ERROR] {e}")

    def start(self) -> None:
        """
        Start an interactive session.
        """

        # ? Attempt to open configuration file.
        try:
            self.conf = Simple(
                config_path = self.config_path,
                isbase64 = self.config_opts["isbase64"],
                readonly = self.config_opts["readonly"],
                encoding = self.config_opts["encoding"]
            )

        except Exception as e:
            print(f"[ERROR] Cannot open configuration file: {e}")
            _ui.confirm()
            return

        else:
            _ui.clearScreen()
            if self.config_opts["command_mode"]:
                return self.startCommandMode()

            try:
                self.conf.load()

            except Exception as e:
                print(f"[ERROR] Cannot open configuration file: {e}")
                _ui.confirm()
                return

            while True:
                choice = _ui.Choices(
                    list_of_choices = {
                        'a': "Add or modify a key/value pair.",
                        'b': "Browse existing key/value pairs.",
                        'r': "Remove an existing key/value pair.",
                        'q': "Edit configuration file options.",
                        'i': "Show configuration file information",
                        'd': "Discard changes",
                        's': "Save changes",
                        'D': "Discard changes and close",
                        'S': "Save and close"
                    },
                    description = f"You are currently editing `{self.config_path}`. Please choose an action to perform below.",
                    case_sensitive = True
                )()

                if choice == 'D':
                    if _ui.Choices(
                        list_of_choices = {'y': "Yes", 'n': "No"},
                        title = "Discard changes and close",
                        description = "Are you sure?"
                    )() == 'y':
                        return

                elif choice == 'S':
                    self.conf.save()
                    return

                elif choice == 'd':
                    self.conf.load()  # Reload configuration file contents.

                elif choice == 's':
                    self.conf.save()

                elif choice == 'i':
                    _ui.clearScreen()
                    if PRETTYTABLE_SUPPORT:
                        conf_info_table = prettytable.PrettyTable(title="Configuration File Information", header=False)
                        conf_info_table.add_rows((self.conf()))
                        print(conf_info_table)

                    else:
                        print("Configuration File Information:")
                        print()
                        for k, v, in self.conf():
                            print(f"{k}: {v}")

                        print()

                    _ui.confirm()

                elif choice == 'a':
                    try:
                        self.conf.set(
                            _ui.InputBox(description="Enter the key name.")(),
                            _ui.InputBox(description="Enter the key value.")()
                        )

                    except ValueError as e:
                        print(f"[ERROR] {e}")
                        _ui.confirm()

                elif choice == 'b':
                    self.configBrowser()

                elif choice == 'r':
                    self.conf.remove(
                        _ui.InputBox(description="Enter the name of the key to remove.")()
                    )

                elif choice == 'q':
                    self.settings()

    def configBrowser(self) -> None:
        """
        Browse all existing key/value pairs in the configuration file.
        """

        starting_index: int = 0  # Set default value for starting index before the loop.

        while True:
            _ui.clearScreen()
            print(str(
                _ui.InputBox(
                    title = "Configuration File Browser",
                    description = self.conf().get("name", self.conf.config_path)
                )
            ))

            # These variables change depending on the panel number.
            conf_items = self.conf.items()
            maximum_index: int = len(conf_items) - 1  # Max index for whole config
            ending_index: int = (starting_index + self.config_opts["browser_items_to_show"]) - 1  # Max index for panel

            browser_table = prettytable.PrettyTable(
                field_names = ("Item #", "Key", "Value")
            )
            i = starting_index
            while i <= ending_index and i <= maximum_index:
                browser_table.add_row((f"[{i + 1}]", conf_items[i][0], conf_items[i][1]))
                i += 1

            print(browser_table)

            browser_controller_choices = {}
            if starting_index != 0:  # If we are not on the first panel.
                browser_controller_choices["Q"] = "Previous"

            if ending_index < maximum_index:  # If we reached the last panel.
                browser_controller_choices["E"] = "Next"

            browser_controller_choices["W"] = "Go back"

            print()
            print(_ui.Choices(list_of_choices=browser_controller_choices).getChoicesList())
            print()
            operation = input(" >>> ").lower()
            if operation == 'w':
                return

            elif operation == 'q':
                if starting_index != 0:
                    starting_index -= self.config_opts["browser_items_to_show"]

            elif operation == 'e':
                if ending_index < maximum_index:
                    starting_index += self.config_opts["browser_items_to_show"]


class AdvancedConfigManager:
    def __init__(self, config_path: str):
        """
        The initialization method of AdvancedConfigHandler() class.

        This class handles interactions between the user and ConfigHandler.

        :param config_path: The path to the configuration file to open.
        """

        self.conf = None
        self.config_path = config_path
        self.config_opts = {
            "prompt": " >>> ",
            "strict": True,
            "readonly": False,
            "encoding": info.defaults["encoding"],
            "command_mode": False
        }

    def settings(self):
        """
        Let the user configure the manager.
        """

        while True:
            choice = _ui.Choices(
                list_of_choices = {
                    '1': f"Toggle strict mode (Current: {self.config_opts['strict']})",
                    '2': f"Toggle read-only mode (Current: {self.config_opts['readonly']})",
                    '3': f"Set encoding ({self.config_opts['encoding']})",
                    "97": "Cancel",
                    "98": "Open Configuration File in Command Mode",
                    "99": "Open Configuration File"
                }
            )()

            if choice == "97":
                return

            elif choice == '1':
                self.config_opts["strict"] = not self.config_opts["strict"]

            elif choice == '2':
                self.config_opts["readonly"] = not self.config_opts["readonly"]

            elif choice == '3':
                new_conf_encoding: str = _ui.InputBox(
                    title="Enter new encoding to use",
                    description=f"Leave blank for default. ({info.defaults['encoding']})"
                )().replace(' ', '')
                self.config_opts["encoding"] = info.defaults["encoding"]\
                    if new_conf_encoding == ''\
                    else new_conf_encoding

            elif choice == "98":
                self.config_opts["command_mode"] = True
                break

            elif choice == "99":
                break

    def startCommandMode(self):
        """
        Start an interactive session in "command" mode.
        """

    def start(self):
        """
        Start an interactive session.
        """


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

            if config_type == "99":
                return

            elif config_type == '1':
                config_manager = SimpleConfigManager(config_path)

            elif config_type == '2':
                config_manager = AdvancedConfigManager(config_path)

            config_manager.settings()
            config_manager.start()

        except (KeyboardInterrupt, EOFError):
            pass

        finally:
            return
