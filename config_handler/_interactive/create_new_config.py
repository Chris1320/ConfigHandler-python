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

from getpass import getuser

from config_handler import _ui
from config_handler import info
from config_handler import simple
from config_handler import advanced
from config_handler.advanced import encryption as adv_encryption
from config_handler.advanced import compression as adv_compression
from config_handler._interactive.utils import getConfigurationFilePassword


def createNewConfig() -> None:
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
            )().lower() == 'y':
                break

            else:
                continue

        except (KeyboardInterrupt, EOFError):
            return  # Cancel configuration file creation.

    while True:
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
                    simple.Simple(
                        config_path = config_path,
                        isbase64 = config_opts["base64"],
                        encoding = config_opts["encoding"]
                    ).save()
                    return

                else:
                    continue

        elif config_type == '2':
            config_opts = {
                "encoding": info.defaults["encoding"],
                "name": "New Configuration File",
                # Author is defined below
                "compression": None,
                "encryption": None
            }
            try:
                config_opts["author"] = getuser()

            except Exception:  # I don't think it is documented what is the exact exception raised. See line 167 of `getpass.py`
                config_opts["author"] = None

            while True:
                _ui.clearScreen()
                list_of_choices = {
                    '1': f"Set encoding                  (Current: {config_opts['encoding']})",
                    '2': f"Set configuration file name   (Current: {config_opts['name']})",
                    '3': f"Set configuration file author (Current: {config_opts['author']})",
                    '4': f"Set compression               (Current: {config_opts['compression']})",
                    '5': f"Set encryption                (Current: {config_opts['encryption']})",
                    "98": "Cancel",
                    "99": "Create Configuration File"
                }

                config_opts_action: str = _ui.Choices(
                    list_of_choices = list_of_choices,
                    description = "Set configuration file options",
                    case_sensitive = False
                )()

                if config_opts_action == "98":
                    return

                elif config_opts_action == '1':
                    new_conf_encoding: str = _ui.InputBox(
                        title = "Enter new encoding to use",
                        description = f"Leave blank for default. ({info.defaults['encoding']})"
                    )().replace(' ', '')
                    config_opts["encoding"] = info.defaults["encoding"] if new_conf_encoding == '' else new_conf_encoding

                elif config_opts_action == '2':
                    config_opts["name"] = _ui.InputBox(title="Enter Configuration File Name")()

                elif config_opts_action == '3':
                    config_opts["author"] = _ui.InputBox(title="Enter Configuration File Author")()

                elif config_opts_action == '4':
                    # Create a dictionary containing a list of supported compression algorithms.
                    supported_compression: dict = {}
                    i = 1
                    for compression in advanced.Advanced.supported_compression:
                        supported_compression[str(i)] = compression
                        i += 1

                    new_conf_compression: str = supported_compression[
                        _ui.Choices(
                            list_of_choices = supported_compression,
                            title = "Choose Compression to Use",
                            clear_screen = True,
                            case_sensitive = False
                        )()
                    ]
                    if adv_compression.isAvailable(new_conf_compression):
                        config_opts["compression"] = new_conf_compression

                    else:
                        print("[E] The selected compression is not available.")
                        _ui.confirm()

                elif config_opts_action == '5':
                    # Create a dictionary containing a list of supported encryption algorithms
                    supported_encryption: dict = {}
                    i = 1
                    for encryption in advanced.Advanced.supported_encryption:
                        supported_encryption[str(i)] = encryption
                        i += 1

                    new_conf_encryption = supported_encryption[
                        _ui.Choices(
                            list_of_choices = supported_encryption,
                            title = "Choose Encryption to Use",
                            clear_screen = True,
                            case_sensitive = False
                        )()
                    ]
                    if adv_encryption.isAvailable(new_conf_encryption):
                        config_opts["encryption"] = new_conf_encryption

                    else:
                        print("[E] The selected encryption is not available.")
                        _ui.confirm()

                elif config_opts_action == "99":
                    print("Creating new configuration file...")
                    new_advanced_config = advanced.Advanced(
                        config_path = config_path,
                        config_pass = getConfigurationFilePassword() if config_opts["encryption"] is not None else None,
                        encoding = config_opts["encoding"]
                    )
                    new_advanced_config.new(
                        name = config_opts["name"],
                        author = config_opts["author"],
                        compression = config_opts["compression"],
                        encryption = config_opts["encryption"]
                    )
                    try:
                        new_advanced_config.save()

                    except ValueError as e:
                        print(f"[ERROR] {e}")
                        _ui.confirm()

                    else:
                        print("Done!")
                        _ui.confirm()
                        return
