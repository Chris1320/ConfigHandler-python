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

import sys
import json
import shlex
import pathlib

from getpass import getpass

from . import info
from . import simple
from . import advanced
from . import exceptions

try:
    import prettytable
    prettytable_support = True

except ImportError:
    prettytable_support = False


def promptGenerator(open_configfile: str = None) -> str:
    """
    Changes the prompt if a configuration file is open.

    :param str open_configfile: The name of the configuration file.

    :returns str: The prompt string.
    """

    return ">>> " if open_configfile is None else f"{open_configfile} >>> "


def helpMenu(config_file: str = None) -> None:
    """
    Show a help menu.

    :param str config_file: The filename of the configuration file opened.
    """

    print()
    print("help                   Show this help menu.")
    print("status                 Show current configuration.")
    print()
    print("base64                 Toggle base64 encoding. (Only for `simple` mode.)")
    print("encoding <encoding>    Set encoding to use.")
    print("password               Set password. (Only for encrypted config files in `advanced` mode.)")
    print("clrpw                  Remove set password.")
    print("readonly               Toogle read-only mode.")
    print("strict                 Toggle strict mode. (Only for `advanced` mode.)")
    print()
    if config_file is None:
        print("mode <mode>            Change the config handler.")
        print("    simple             Simple mode.")
        print("    advanced           Advanced mode.")
        print("open <filename>        Open a configuration file.")

    else:
        print("new                    Create a new configuration file. (Only for `advanced` mode.)")
        print("close                  Close the current configuration file.")
        print("save                   Save the current configuration file.")
        print("get <key>              Get a value from the configuration file.")
        print("set <key> <value>      Set a value in the configuration file.")
        print("remove <key>           Remove a value from the configuration file.")
        print("keys                   Show all available keys in the configuration file.")
        print("list                   Show all available keys and values in the configuration file.")
        print("metadata               Show the metadata of the configuration file.")

    print()
    print("exit                   Exit the program.")
    print()
    print('=' * 40)
    print()
    print("When setting a value, you can explicitly convert them using the following:")
    print("    + str:<value>       Convert <value> to a string.")
    print("    + int:<value>       Convert <value> to an integer.")
    print("    + float:<value>     Convert <value> to a float.")
    print("    + bool:<value>      Convert <value> to a boolean.")
    print()


def parse(data: str) -> str:
    """
    Check if <data> needs explicit conversion.

    :param str data: The data to check.

    :returns str|int|float|bool: The parsed data in a new type.
    """

    if data.startswith("str:"):
        return str(data.partition('str:')[2])

    elif data.startswith("int:"):
        return int(data.partition('int:')[2])

    elif data.startswith("float:"):
        return float(data.partition('float:')[2])

    elif data.startswith("bool:"):
        if data.partition("bool:")[2].lower() == "true":
            return True

        elif data.partition("bool:")[2].lower() == "false":
            return False

        else:
            raise ValueError("[E] Invalid boolean value.")

    else:
        return data  # If nothing matched, do not modify the data.


def main() -> int:
    """
    Start an interactive console.

    :returns int: The exit code.
    """

    print(info.title)
    print()
    print(f"Running on: `{pathlib.Path().cwd()}`")
    print()
    print("Type `help` for help.")
    print()
    if not advanced.ciphers.cryptodome_support:
        print("[!] An encryption module is not installed on this system.")
        print("[!] Advanced mode won't be able to encrypt or decrypt.")
        print()

    if not prettytable_support:
        print("[!] `prettytable` is not installed on this system.")
        print()

    config_file = None
    password = None
    mode = "simple"  # The default mode.
    encoding = "utf-8"  # The default encoding.
    readonly = False  # The default read-only mode.
    strict = True  # The default strict mode.
    base64 = False  # The default base64 encoding mode.

    while True:
        try:
            command = str(input(promptGenerator(config_file)))
            if command == "help":
                helpMenu(config_file)
                continue

            elif command == "status":
                print()
                print("Current Configuration File: ", config_file)
                print("Config Mode:                ", mode)
                print("Encoding:                   ", encoding)
                print("Read-only:                  ", readonly)
                print("Strict Mode:                ", strict)
                print("Base64:                     ", base64)
                print()
                print("Password:                   ", ("*" * 12 if password is not None else "None"))
                print()
                continue

            elif command == "readonly":
                readonly = not readonly
                print("Read-only mode {0}.".format("enabled" if readonly else "disabled"))
                continue

            elif command == "password":
                password = getpass("Enter password: ")
                print("[i] Password set.")

            elif command == "clrpw":
                password = None
                print("[i] Password removed.")

            elif command == "base64":
                base64 = not base64
                print("Base64 encoding {0}.".format("enabled" if base64 else "disabled"))
                continue

            elif command.startswith("encoding"):
                if command.partition(' ')[2] != '':
                    encoding = command.partition(' ')[2]
                    print(f"Encoding set to `{encoding}`.")
                    continue

                helpMenu(config_file)  # Show help menu if no encoding is given.

            elif command == "strict":
                strict = not strict
                print("Strict mode {0}.".format("enabled" if strict else "disabled"))
                continue

            elif command == "exit":
                print("[!] Quitting...")
                return 0

            elif config_file is None:
                if command.startswith("open"):
                    config_file = command.partition(' ')[2]
                    if config_file == '':
                        helpMenu(config_file)
                        config_file = None
                        continue

                    try:
                        if mode == "simple":
                            config = simple.Simple(config_file, base64, encoding, readonly)
                            print("[i] Configuration file opened.")
                            continue

                        elif mode == "advanced":
                            config = advanced.Advanced(config_file, password, readonly)
                            print("[i] Configuration file opened.")
                            continue

                        else:
                            config_file = None
                            print("[E] Unkown mode is set!")

                    except json.decoder.JSONDecodeError:
                        print("[E] The configuration file might be corrupted or you have entered an incorrect password.")
                        config_file = None

                    except ValueError:
                        print("[E] You must set a password before opening the configuration file.")
                        config_file = None

                elif command.startswith("mode"):
                    command_option = command.partition(' ')[2]
                    if command_option == '':
                        print(f"[i] You are currently using `{mode}` mode.")

                    elif command_option == "simple":
                        mode = "simple"
                        print("mode is set to `simple`.")

                    elif command_option == "advanced":
                        mode = "advanced"
                        print("mode is set to `advanced`.")

                    else:
                        print(f"[E] Unknown mode `{command_option}`.")

                    continue

                else:
                    print(f"[E] Unknown command `{command}`.")
                    continue

            else:
                if command == "close":
                    config_file = None
                    config = None
                    print("[i] Configuration file closed.")
                    continue

                elif command == "load":
                    try:
                        config.load(strict)

                    except exceptions.ChecksumError as e:
                        print("[E]", e)
                        print("[i] Disable strict mode to bypass this error.")
                        continue

                    else:
                        print("[i] Configuration file loaded.")
                        continue

                elif command == "keys":
                    print("Available keys:")
                    for k in config.keys():
                        print("+", k)

                    continue

                elif command == "list":
                    if prettytable_support:
                        table = prettytable.PrettyTable()
                        table.field_names = ["Key", "Value", "Type"]
                        for key in config.keys():
                            table.add_row([key, config.get(key), type(config.get(key))])

                        print(table)

                    else:
                        print("Key=Value (Type)\n")
                        for key in config.keys():
                            print(f"+ {key}={config.get(key)} ({type(config.get(key))})")

                        print()

                elif command == "new":
                    if mode != "advanced":
                        print("[E] You can only call `new` in advanced mode.")
                        continue

                    else:
                        if password is None:
                            print("[i] You must set a password before creating an encrypted configuration file.")
                            print()

                        config_name: str = input("Configuration File Name (Blank for None): ")
                        config_author: str = input("Configuration File Author (Blank for None): ")
                        config_compression: str = input("Configuration File Compression (Blank for None): ")
                        while config_compression not in advanced.Advanced.SUPPORTED["compression"]:
                            if config_compression == '':
                                break

                            for available_compression_algorithm in advanced.Advanced.SUPPORTED["compression"]:
                                print("+", available_compression_algorithm)

                            print()
                            config_compression: str = input("Configuration File Compression (Blank for None): ")

                        if password is not None:
                            config_encryption: str = input("Configuration File Encryption (Blank for None): ")
                            while config_encryption not in advanced.Advanced.SUPPORTED["encryption"]:
                                if config_encryption == '':
                                    break

                                for available_encryption_algorithm in advanced.Advanced.SUPPORTED["encryption"]:
                                    print("+", available_encryption_algorithm)

                                print()
                                config_encryption: str = input("Configuration File Encryption (Blank for None): ")

                        else:
                            config_encryption = ''  # Set to blank if no password is set.

                        config_name = None if config_name == '' else config_name
                        config_author = None if config_author == '' else config_author
                        config_compression = None if config_compression == '' else config_compression
                        config_encryption = None if config_encryption == '' else config_encryption

                        print("Creating configuration file...")
                        try:
                            config.new(
                                config_name,
                                config_author,
                                config_compression,
                                config_encryption,
                                encoding
                            )

                        except AssertionError:
                            print("[E] An assertion error occured.")

                        continue

                elif command.startswith("save"):
                    try:
                        config.save()
                        print("[i] Configuration file saved.")

                    except Exception as e:
                        print("[E] An error occured:", e)

                    finally:
                        continue

                elif command.startswith("set"):
                    commands = shlex.split(command)
                    try:
                        key = commands[1]
                        try:
                            value = parse(commands[2])

                        except ValueError as e:
                            print(e)

                    except IndexError:
                        helpMenu(config_file)

                    else:
                        config.set(key, value)

                    finally:
                        del commands

                elif command.startswith("get"):
                    try:
                        print(config.get(shlex.split(command)[1]))

                    except(IndexError, KeyError):
                        helpMenu(config_file)

                elif command.startswith("remove"):
                    try:
                        config.remove(shlex.split(command)[1])
                        print("Key removed.")

                    except(IndexError, KeyError):
                        helpMenu(config_file)

                elif command.startswith("metadata"):
                    if mode != "advanced":
                        print("[E] You can only call `metadata` in advanced mode.")
                        continue

                    try:
                        metadata = config.metadata()

                    except KeyError:
                        print("[E] The configuration file is not yet loaded or created.")
                        continue

                    if prettytable_support:
                        table = prettytable.PrettyTable()
                        table.field_names = ["Key", "Value"]
                        for key in metadata:
                            if key == "version":
                                table.add_row([key, '.'.join(map(str, metadata[key]))])

                            elif key == "dictionary_size":
                                table.add_row(["Number of Entries in The Dictionary", metadata[key]])

                            elif key == "checksum":
                                table.add_row(["Dictionary Checksum", metadata[key]])

                            else:
                                table.add_row([key, metadata[key]])

                        print(table)
                        print()

                    else:
                        for key in metadata:
                            if key == "version":
                                print(f"+ {key}: {'.'.join(map(str, metadata[key]))}")

                            elif key == "dictionary_size":
                                print(f"+ There are `{metadata[key]}` entries in the dictionary.")

                            elif key == "checksum":
                                print(f"+ Dictionary Checksum: {metadata[key]}")

                            else:
                                print(f"+ {key}: {metadata[key]}")

                        print()

                else:
                    print(f"[E] Unknown command `{command}`.")
                    continue

        except KeyboardInterrupt:
            print("\n[!] Forcing to quit...")
            return 2

        except Exception as e:
            print("\n[E] An unexpected error occurred:", e)
            input("Press enter to continue...")
            return 1


if __name__ == "__main__":
    sys.exit(main())
