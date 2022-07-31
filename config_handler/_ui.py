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
import textwrap
from typing import Dict
from typing import List
from typing import Union

from config_handler import info


def _clearScreen() -> None:
    """
    Clears the screen.
    """

    os.system("cls" if os.name == "nt" else "clear")


class Choices:
    """
    Show a menu of choices to the user and return the choice they make.
    """

    def __init__(
        self,
        list_of_choices: Dict[Union[str, None], Union[str, None]],
        title: str = info.title,
        description: Union[str, None] = None,
        minimum_spaces: int = 1,
        margin: int = 4,
        title_fill_char: str = ' ',
        clear_screen: bool = True,
        case_sensitive: bool = False
    ):
        """
        Initialize the Choice() class.

        :param list_of_choices: A dictionary containing the ID and description of each choice.
        :param title: The title of the choice dialog. (default: <info.title>)
        :param description: A description about the choice dialog. (default: None)
        :param minimum_spaces: The minimum number of spaces between the ID and description. (default: 1)
        :param margin: The margin of the description. (default: 4)
        :param title_fill_char: The character to fill the sides of the title with. (default: ' ')
        :param clear_screen: Whether or not to clear the screen before showing the dialog. (default: True)
        :param case_sensitive: Whether or not to ignore case when comparing the user's input to the IDs. (default: False)
        """

        self._list_of_choices = list_of_choices

        self.title = title
        self.description = description
        self.minimum_spaces = minimum_spaces

        self.margin = margin
        self.title_fill_char = title_fill_char
        self.clear_screen = clear_screen
        self.case_sensitive = case_sensitive

    def __call__(self) -> str:
        """
        Show the dialog to the user and return the choice they make.
        """

        while True:
            if self.clear_screen:
                _clearScreen()

            print()
            print(self.title.center(os.get_terminal_size().columns, self.title_fill_char))  # Print the title.
            print()
            if self.description is not None:
                # Print the description.
                for line in textwrap.wrap(
                    self.description,
                    os.get_terminal_size().columns - (self.margin * 2)
                ):
                    print(line.center(os.get_terminal_size().columns))

                print()

            longest_id = max(  # Get the longest key.
                (len(key) if key is not None else 0)
                for key in self._list_of_choices.keys()
            )
            for id, description in self._list_of_choices.items():  # Print the choices.
                if id is None and description is None:
                    print()

                else:
                    spacer = ' ' * (self.minimum_spaces + (longest_id - len(str(id))))
                    print(f"[{id}]{spacer}{description}")

            print()
            choice = input(" >>> ")  # Get the user's choice.
            if self.case_sensitive:
                if choice in self._list_of_choices.keys():
                    return choice

                else:
                    continue

            else:
                if choice.lower() in map(
                    lambda x: x.lower() if type(x) is str else x,  # Convert the keys to lowercase ONLY IF the key is a string.
                    self._list_of_choices.keys()
                ):
                    return choice

                else:
                    continue


    @property
    def list_of_choices(self) -> Dict[Union[str, None], Union[str, None]]:
        return self._list_of_choices

    @list_of_choices.setter
    def list_of_choices(self, new_list: Dict[Union[str, None], Union[str, None]]) -> None:
        """
        Check if the new list of choices is valid.
        Raises a ValueError if any of the pairs are invalid.
        """

        for key, value in new_list.items():
            if any((key, value)) is None and all((key, value)) is not None:
                raise ValueError("Invalid choice.")

        self._list_of_choices = new_list
