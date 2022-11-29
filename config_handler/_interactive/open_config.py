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
from typing import Any
from typing import Final

from config_handler import _ui
from config_handler import info
from config_handler.simple import Simple

try:
    import prettytable

except ImportError:
    _PRETTYTABLE_SUPPORT: Final[bool] = False

else:
    _PRETTYTABLE_SUPPORT: Final[bool] = True

_VALUE_TYPES: Final = {
    str: "String",
    int: "Integer",
    float: "Float",
    bool: "Boolean"
}


def parseValue(value: str) -> Any:
    """
    Check if user explicitly states a value type and convert if necessary.
    This function raises a ValueError if it is unable to convert the value.

    :param value: The value to check for conversion.
    """

    if type(value) is not str:
        return value  # Do not do anything with <value> if it is not a string.
        # ? We will still accept non-string datatypes because values can also be an int, float, or bool.

    if value.startswith("str:"):
        return str(value.partition("str:")[2])

    elif value.startswith("int:"):
        return int(value.partition("int:")[2])

    elif value.startswith("float:"):
        return float(value.partition("float:")[2])

    elif value.startswith("bool:"):
        parsed_bool = value.partition("bool:")[2].lower()
        if parsed_bool in {"true", "false"}:
            return parsed_bool == "true"

        elif parsed_bool.isdigit():  # This will accept any positive integers. (0-n)
            return int(parsed_bool) != 0  # 0 is False; True otherwise.

        else:
            raise ValueError("Invalid value for a boolean value datatype.")

    else:
        return value  # Do not do anything with value if none of the above are true.


class SimpleConfigManager:
    def __init__(self, config_path: str):
        """
        The initialization method of SimpleConfigManager() class.
        This class handles interactions between the user and ConfigHandler.

        :param config_path: The path to the configuration file to open.
        """

        self.config_path = config_path
        self.command_mode = False
        self.prompt = " >>> "
        self.browser_items_to_show = info.defaults["browser_items_to_show"]
        self.conf = Simple(
            config_path=self.config_path,
            isbase64=False,
            readonly=False,
            encoding=info.defaults["encoding"]
        )
        self.do_not_reload = False
        self.exit = False

    def __call__(self) -> None:
        """
        Start interactive session with the configuration file.
        """

        self.settings(True)  # Ask user for settings before creating a new Simple() object.
        while not self.exit:
            if self.command_mode:
                self.startCommandMode()

            else:
                self.start()

    def settings(self, open_wizard: bool = False) -> None:
        """
        Let the user configure the manager.

        :param open_wizard: Show "open configuration file" options instead of "go back" options.
        """

        while True:  # Show options menu first.
            available_options = {
                'b': f"Toggle base64 encoding (Current: {self.conf.isbase64})",
                'r': f"Toggle read-only mode (Current: {self.conf.readonly})",
                'e': f"Set encoding ({self.conf.encoding})",
                'p': f"Number of items per panel in browser (Current: {self.browser_items_to_show})"
            }
            # Add options depending on <open_wizard> state.
            if open_wizard:
                available_options['C'] = "Cancel"
                available_options['O'] = "Open Configuration File in Command Mode"
                available_options['o'] = "Open Configuration File"

            else:
                available_options['o'] = f"Toggle Command Mode (Current: {self.command_mode})"
                available_options['w'] = "Go Back"

            # Show the menu to the user.
            choice = _ui.Choices(
                list_of_choices=available_options,
                case_sensitive=True
            )()

            if choice == 'C' and open_wizard:
                self.exit = True  # Cancel management of configuration file; return to main menu.
                return

            elif choice == 'O' and open_wizard:
                self.command_mode = True
                return

            elif choice == 'o':  # This option is present in both <open_wizard> statements.
                if open_wizard:
                    return  # ? The default value for <self.command_mode> is False anyway.

                self.command_mode = not self.command_mode
                self.do_not_reload = True

            elif choice == 'w' and not open_wizard:
                return

            elif choice == 'b':
                self.conf.isbase64 = not self.conf.isbase64

            elif choice == 'r':
                self.conf.readonly = not self.conf.readonly

            elif choice == 'e':
                new_conf_encoding: str = _ui.InputBox(
                    title="Enter new encoding to use",
                    description=f"Leave blank for default. ({info.defaults['encoding']})"
                )().lstrip().rstrip()
                # Set default encoding when encoding is blank.
                self.conf.encoding = info.defaults["encoding"] \
                    if new_conf_encoding == '' \
                    else new_conf_encoding

            elif choice == 'p':
                try:
                    # ? do not convert to int immediately for us to be able to accept empty inputs.
                    new_browser_items_to_show: str = _ui.InputBox(
                        title="Number of items to show per panel in configuration file browser",
                        description=f"Leave blank for default. ({info.defaults['browser_items_to_show']})"
                    )()
                    # Set default number of items if empty.
                    self.browser_items_to_show = info.defaults["browser_items_to_show"] \
                        if new_browser_items_to_show == '' \
                        else int(new_browser_items_to_show)

                except ValueError:
                    print("[E] Invalid number.")
                    _ui.confirm()

    def startCommandMode(self) -> None:
        """
        Start an interactive session in "command" mode.
        """

        for k, v in self.conf().items():
            print(f"{k}: {v if k != 'parser_version' else 'v'.format('.'.join(map(str, v)))}")

        print()
        if not _PRETTYTABLE_SUPPORT:
            print("[!] `prettytable` is not installed.")
            print()

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
readonly                 Toggle read-only mode of the configuration file.

settings                 Open the interactive settings menu.
quit | exit              Close the configuration file.
help                     Show this help menu.



EXPLICITLY DECLARING A VALUE TYPE

    When setting a value, you can add the following prefixes to explicitly
state its type:

| Prefix | Type    | Example Value         |
| str:   | string  | str:This is a string. |
| int:   | integer | int:1024              |
| float: | float   | float:3.1415          |
| bool:  | boolean | bool:true             |

When the value you entered cannot be converted, the program will raise an error."""

        while True:
            try:
                command = shlex.split(input(self.prompt))

                if command[0] in {"quit", "exit"}:
                    self.exit = True
                    return

                elif command[0] == "settings":
                    return self.settings()

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
                                    description="Enter a new filepath. Press CTRL+C to cancel.",
                                    input_prompt="filepath > "
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
                        continue

                    print("[i] Configuration file saved.")

                elif command[0] == "info":
                    self.showConfigInfo()

                elif command[0] == "get":
                    print(self.conf[command[1]])

                elif command[0] == "set":
                    self.conf[command[1]] = parseValue(command[2])

                elif command[0] == "del":
                    del self.conf[command[1]]

                elif command[0] == "list":
                    if _PRETTYTABLE_SUPPORT:
                        conf_items = prettytable.PrettyTable(("Key", "Value", "Data Type"))
                        for k, v in self.conf.items():
                            conf_items.add_row((k, v, _VALUE_TYPES[type(v)]))

                        print(conf_items)

                    else:
                        print("Key: Value")
                        print()
                        for k, v in self.conf.items():
                            print(f"- {k}: {v} ({_VALUE_TYPES[type(v)]})")

                        print()

                elif command[0] == "base64":
                    self.conf.isbase64 = not self.conf.isbase64
                    print("Base64 encoding is enabled." if self.conf.isbase64 else "Base64 encoding is disabled.")

                elif command[0] == "encoding":
                    self.conf.encoding = command[1]
                    print(f"Encoding successfully changed to {command[1]}.")

                elif command[0] == "readonly":
                    self.conf.readonly = not self.conf.readonly
                    print(
                        "Configuration file is now read-only."
                        if self.conf.readonly
                        else "Read-only mode is now disabled."
                    )

            except Exception as e:
                print(f"[ERROR] {e}")

    def start(self) -> None:
        """
        Start an interactive session.
        """

        try:
            if not self.do_not_reload:
                self.conf.load()

        except Exception as e:
            print(f"[ERROR] Cannot open configuration file: {e}")
            self.exit = True
            _ui.confirm()
            return

        while True:
            try:
                choice = _ui.Choices(
                    list_of_choices={
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
                    description=f"You are currently editing:\n`{self.config_path}`",
                    case_sensitive=True
                )()

                if choice == 'D':
                    if _ui.Choices(
                        list_of_choices={'y': "Yes", 'n': "No"},
                        title="Discard changes and close",
                        description="Are you sure?"
                    )() == 'y':
                        self.exit = True
                        return

                elif choice == 'S':
                    self.conf.save()
                    self.exit = True
                    return

                elif choice == 'd':
                    self.conf.load()  # Reload configuration file contents.

                elif choice == 's':
                    self.conf.save()

                elif choice == 'i':
                    _ui.clearScreen()
                    self.showConfigInfo()
                    _ui.confirm()

                elif choice == 'a':
                    try:
                        self.conf.set(
                            _ui.InputBox(
                                title="Add or modify a key/value pair.",
                                description="Enter the key name. (CTRL+C to cancel)"
                            )(),
                            parseValue(
                                _ui.InputBox(
                                    title="Add or modify a key/value pair.",
                                    description="Enter the key value. (CTRL+C to cancel)"
                                )()
                            )
                        )

                    except ValueError as e:
                        print(f"[ERROR] {e}")
                        _ui.confirm()

                    except KeyboardInterrupt:
                        pass

                elif choice == 'b':
                    self.configBrowser()

                elif choice == 'r':
                    self.conf.remove(
                        _ui.InputBox(
                            title="Remove an existing key/value pair.",
                            description="Enter the name of the key to remove. (CTRL+C to cancel)"
                        )()
                    )

                elif choice == 'q':
                    return self.settings()

            except KeyboardInterrupt:
                pass

    def showConfigInfo(self) -> None:
        """
        Print self.conf information
        """

        if _PRETTYTABLE_SUPPORT:
            conf_info_table = prettytable.PrettyTable(title="Configuration File Information", header=False)
            for k, v in self.conf().items():
                conf_info_table.add_row(
                    (
                        k,
                        v if k != "parser_version" else "v{}".format('.'.join(map(str, v)))
                    )
                )

            print(conf_info_table)

        else:
            print("Configuration File Information:")
            print()
            for k, v, in self.conf():
                print(f"{k}: {v}")

            print()

    def configBrowser(self) -> None:
        """
        Browse all existing key/value pairs in the configuration file.
        """

        starting_index: int = 0  # Set default value for starting index before the loop.
        while True:
            try:
                _ui.clearScreen()
                print(  # Print only the header.
                    str(
                        _ui.InputBox(
                            title="Configuration File Browser",
                            description=self.conf().get("name", self.conf.config_path)
                        )
                    )
                )

                # These variables change depending on the panel number.
                conf_items = self.conf.items()
                maximum_index: int = len(conf_items) - 1  # Max index for whole config
                ending_index: int = (starting_index + self.browser_items_to_show) - 1  # Max index for panel

                browser_table = prettytable.PrettyTable(field_names=("Item #", "Key", "Value", "Data Type"))
                i = starting_index
                while i <= ending_index and i <= maximum_index:
                    browser_table.add_row(
                        (
                            f"[{i + 1}]",
                            conf_items[i][0],
                            conf_items[i][1],
                            _VALUE_TYPES[type(conf_items[i][1])]
                        )
                    )
                    i += 1

                print(browser_table)

                browser_controller_choices = {}
                if starting_index != 0:  # If we are not on the first panel.
                    browser_controller_choices['Q'] = "First"
                    browser_controller_choices['q'] = "Previous"

                if ending_index < maximum_index:  # If we reached the last panel.
                    browser_controller_choices['E'] = "Last"
                    browser_controller_choices['e'] = "Next"

                browser_controller_choices['w'] = "Go back"

                print()
                print(_ui.Choices(list_of_choices=browser_controller_choices).getChoicesList())
                print()
                operation = input(" >>> ").lstrip().rstrip()
                if operation == 'w':
                    return

                elif operation == 'Q':
                    starting_index = 0

                elif operation == 'q':
                    starting_index = 0 \
                        if starting_index < self.browser_items_to_show \
                        else starting_index - self.browser_items_to_show

                elif operation == 'E':
                    starting_index = (maximum_index - self.browser_items_to_show) + 1

                elif operation == 'e':
                    # ? Print the last panel if
                    starting_index = (maximum_index - self.browser_items_to_show) + 1 \
                        if starting_index + self.browser_items_to_show >= maximum_index - self.browser_items_to_show \
                        else starting_index + self.browser_items_to_show

                elif operation in map(str, tuple(range(starting_index + 1, min(ending_index, maximum_index) + 2))):
                    while True:
                        key_to_edit = int(operation) - 1
                        key_to_edit_operation = _ui.Choices(
                            list_of_choices={
                                'E': "Edit value",
                                'R': "Remove key/value pair",
                                'W': "Go Back"
                            },
                            description="{0}\n{1}\n{2}".format(
                                f"Key: `{conf_items[key_to_edit][0]}`",
                                f"Value: `{conf_items[key_to_edit][1]}`",
                                f"Value Type: {_VALUE_TYPES[type(conf_items[key_to_edit][1])]}"
                            )
                        )().lower()

                        if key_to_edit_operation == 'w':
                            break

                        elif key_to_edit_operation == 'e':
                            self.conf[conf_items[key_to_edit][0]] = parseValue(
                                _ui.InputBox(
                                    description=f"Please enter the new value for key `{conf_items[key_to_edit][0]}`."
                                )()
                            )
                            conf_items = self.conf.items()

                        elif key_to_edit_operation == 'r':
                            del self.conf[conf_items[key_to_edit][0]]
                            print("Pair deleted.")
                            _ui.confirm()
                            break

            except KeyboardInterrupt:
                pass


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
                title="Open an Existing Configuration File",
                description="Please enter the filepath of an existing configuration file.\n(CTRL+C to cancel)"
            )()
            if _ui.Choices(
                list_of_choices={
                    'y': "Yes",
                    'n': "No"
                },
                description=f"Is this correct?\n`{config_path}`",
                case_sensitive=False
            )().lower() == 'y':
                break

            else:
                continue

        except (KeyboardInterrupt, EOFError):
            return

    while True:
        try:
            config_type: str = _ui.Choices(
                list_of_choices={
                    's': "Simple Configuration File",
                    'a': "Advanced Configuration File",
                    "c": "Cancel"
                }
            )().lower()

            if config_type == "c":
                return

            elif config_type == 's':
                SimpleConfigManager(config_path)()
                return

            elif config_type == 'a':
                # TODO
                # AdvancedConfigManager(config_path)()
                print("WIP")
                _ui.confirm()
                return

        except (KeyboardInterrupt, EOFError):
            pass
