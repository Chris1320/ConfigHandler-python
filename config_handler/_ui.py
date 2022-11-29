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
import shutil
import textwrap
from typing import Dict
from typing import Union

from config_handler import info


def clearScreen() -> None:
    """
    Clears the screen.
    """

    os.system("cls" if os.name == "nt" else "clear")


def confirm(message: str = "Press enter to continue...") -> None:
    """
    Wait for user input.

    :param message: The message to show to the user.
    """

    input(message)


class InputBox:
    """
    Show an input box to the user and return their input.
    """

    def __init__(
        self,
        title: str = info.title,
        description: Union[str, None] = None,
        margin: int = 4,
        title_fill_char: str = ' ',
        clear_screen: bool = True,
        input_prompt: str = " >>> "
    ):
        """
        Initialize the InputBox() class.

        :param title: The title of the input box. (default: <info.title>)
        :param description: The description of the input box. (default: None)
        :param margin: The margin of the description. (default: 4)
        :param title_fill_char: The character to fill the sides of the title with. (default: ' ')
        :param clear_screen: Whether to clear the screen before showing the dialog. (default: True)
        :param input_prompt: The prompt to show beside the user's input field. (default: " >>> ")
        """

        self.title = title
        self.description = description
        self.margin = margin
        self.title_fill_char = title_fill_char
        self.clear_screen = clear_screen
        self.input_prompt = input_prompt

    def __call__(self) -> str:
        """
        Show the dialog to the user and return their input.

        :returns: The input of the user.
        """

        if self.clear_screen:
            clearScreen()

        print(self.__buildDialog())
        return input(self.input_prompt)

    def __str__(self) -> str:
        """
        Get a string representation of the dialog.
        This will not clear the screen nor ask for the user's input.

        :returns: The string representation of the dialog.
        """

        return self.__buildDialog()

    def __buildDialog(self) -> str:
        """
        Build the dialog.

        :returns: The dialog.
        """

        # Center and add the title.
        result: str = f"\n{self.title.center(shutil.get_terminal_size().columns, self.title_fill_char)}\n\n"
        if self.description is not None:  # Center and add the description.
            for desc_line in self.description.split('\n'):
                for line in textwrap.wrap(
                    desc_line,
                    shutil.get_terminal_size().columns - (self.margin * 2)
                ):
                    result += f"{line.center(shutil.get_terminal_size().columns)}\n"

            result += '\n'

        return result


class Choices:
    """
    Show a menu of choices to the user and return the choice they make.
    """

    def __init__(
        self,
        list_of_choices: Dict[str, str],
        title: str = info.title,
        description: Union[str, None] = None,
        minimum_spaces: int = 1,
        margin: int = 4,
        title_fill_char: str = ' ',
        clear_screen: bool = True,
        case_sensitive: bool = False,
        input_prompt: str = " >>> "
    ):
        """
        Initialize the Choice() class.

        :param list_of_choices: A dictionary containing the ID and description of each choice.
        :param title: The title of the choice dialog. (default: <info.title>)
        :param description: A description about the choice dialog. (default: None)
        :param minimum_spaces: The minimum number of spaces between the ID and description. (default: 1)
        :param margin: The margin of the description. (default: 4)
        :param title_fill_char: The character to fill the sides of the title with. (default: ' ')
        :param clear_screen: Whether to clear the screen before showing the dialog. (default: True)
        :param case_sensitive: Whether to ignore case when comparing the user's input to the IDs. (default: False)
        :param input_prompt: The prompt to show beside the user's input field. (default: " >>> ")
        """

        self.list_of_choices = list_of_choices

        self.title = title
        self.description = description
        self.minimum_spaces = minimum_spaces

        self.margin = margin
        self.title_fill_char = title_fill_char
        self.clear_screen = clear_screen
        self.case_sensitive = case_sensitive
        self.input_prompt = input_prompt

    def __call__(self) -> str:
        """
        Show the dialog to the user and return the choice they make.

        :returns: The choice the user made.
        """

        while True:
            if self.clear_screen:
                clearScreen()

            print(self.__buildDialog())
            choice = input(self.input_prompt)  # Get the user's choice.
            if self.case_sensitive:
                if choice in self.list_of_choices.keys():
                    return choice

            else:
                if choice.lower() in [  # Convert the keys to lowercase ONLY IF the key is a string.
                    key.lower() if type(key) is str else key
                    for key in self.list_of_choices.keys()
                ]:
                    return choice

    def __str__(self) -> str:
        """
        Get a string representation of the dialog.
        This will not clear the screen nor ask for the user's input.

        :returns: The string representation of the dialog.
        """

        return self.__buildDialog()

    def __buildDialog(self) -> str:
        """
        Build the dialog.
        """

        # Center and add title.
        result: str = f"\n{self.title.center(shutil.get_terminal_size().columns, self.title_fill_char)}\n\n"

        if self.description is not None:  # Center and add description.
            for desc_line in self.description.split('\n'):
                for line in textwrap.wrap(
                    desc_line,
                    shutil.get_terminal_size().columns - (self.margin * 2)
                ):
                    result += f"{line.center(shutil.get_terminal_size().columns)}\n"

            result += '\n'

        result += self.getChoicesList()
        result += '\n'
        return result

    def getChoicesList(self) -> str:
        """
        Return a string containing the formatted choices list without the title and description.
        """

        result: str = ""

        # Get the longest key; to be used in formatting the choices.
        longest_id = max(
            (len(key) if key is not None else 0)
            for key in self.list_of_choices.keys()
        )

        # Format and add choices to result.
        for choice_id, choice_description in self.list_of_choices.items():
            spacer = ' ' * (self.minimum_spaces + (longest_id - len(str(choice_id))))
            result += f"[{choice_id}]{spacer}{choice_description}\n"

        return result
