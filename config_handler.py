#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MIT License
Copyright (c) 2020 Chris1320

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
import zlib
import base64
import hashlib

from Cryptodome import Random
from Cryptodome.Cipher import AES

VERSION = "0.0.1.7"

class AES256(object):
    """
    The class that contains methods for working with AES-256.

    Credits to the people from StackOverflow! LMAO

    https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    """

    # This class is from my `Ciphers/aes.py` module.

    def __init__(self, key, encoding="utf-8"):
        """
        The initialization method of AES256() class.

        :param str key: The key/password of the message.
        """

        self.VERSION = "0.0.1.2"

        self.bs = AES.block_size  # The block size
        self.encoding = encoding  # The encoding to be used when calling `encode()` and `decode()`.
        self.key = hashlib.sha256(key.encode(self.encoding)).digest()  # The hashed key

    def encrypt(self, message):
        """
        Encrypt <message> using <self.key> as the key/password.

        :param str message: The message to encrypt.

        :returns bytes: The ciphertext.
        """

        padded_message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        emessage = padded_message.encode(self.encoding)  # Encoded message
        ciphertext = base64.b64encode(iv + cipher.encrypt(emessage))

        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypt <ciphertext> using <self.key> as the key/password.

        :param bytes ciphertext: The ciphertext to decrypt.

        :returns str: The plaintext version of the ciphertext.
        """

        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]  # Get the iv from the ciphertext
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext[AES.block_size:])
        plaintext = self._unpad(decrypted).decode(self.encoding)

        return plaintext

    def _pad(self, s):
        """
        Add a padding to <s>.
        """

        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        """
        Remove padding from <s>.
        """

        return s[:-ord(s[len(s)-1:])]

class Version1():
    """
    The class containing methods to use the version 1 configuration file.
    """

    def __init__(self, config_path="data/config.dat", isbase64=False, encoding="utf-8"):
        """
        The initialization method for ConfigHandler() class.

        :param str config_path: The path of the configuration file to use.
        :param bool isbase64: True if the configuration file is encoded via Base64.
        :param str encoding: The encoding to be used.
        """

        self.VERSION = "0.0.1.1"
        self.config_path = config_path
        self.isbase64 = isbase64
        self.encoding = encoding

    def _open_config_file(self):
        """
        Open the config file.

        :returns str: The configuration file data.
        """

        try:
            with open(self.config_path, 'r') as fopen:
                data = fopen.read()

        except(FileNotFoundError, IOError, EOFError,
                PermissionError, IsADirectoryError):
            raise IOError("Error reading the configuration file!")

        else:
            if self.isbase64 == True:
                try:
                    data = base64.b64decode(data)

                except(TypeError, ValueError, UnicodeDecodeError):
                    raise IOError("The configuration file is corrupt or decrypted!")

                else:
                    try:
                        return str(data.decode(self.encoding))

                    except(TypeError, ValueError,UnicodeDecodeError):
                        raise IOError("The configuration file is corrupt or decrypted!")

            else:
                return data

    def _save_config_file(self, config_data):
        """
        Save the config file.

        :param str config_data: The whole content of the configuration file.

        :returns int: Error code
        """

        try:
            with open(self.config_path, 'w') as fopen:
                fopen.write('')

        except(FileNotFoundError, IOError, EOFError,
               PermissionError, IsADirectoryError):
            raise IOError("Error writing to the configuration file!")

        else:
            try:
                if self.isbase64 == True:
                    with open(self.config_path, 'w') as fopen:
                        fopen.write(base64.b64encode(config_data.encode(self.encoding)).decode(self.encoding))

                else:
                    with open(self.config_path, 'w') as fopen:
                        fopen.write(config_data)

            except(FileNotFoundError, IOError, EOFError,
                   PermissionError, IsADirectoryError):
                raise IOError("Error writing to the configuration file!")

            else:
                return 0

    def get(self, data=None):
        """
        Get data from config file.

        :param str data: The key/name of the value you are looking for.

        :returns bool:
        :returns int:
        :returns float:
        :returns str:
        :returns void:
        """

        contents = self._open_config_file()

        if data is None:
            return None

        else:
            contents = contents.split('\n')

            for content in contents:
                if content.startswith('#'):
                    continue

                elif content.startswith(data + '='):
                    # This if-else statement below is *specially* for booleans.
                    # DEV0001: Might introduce bugs in the future!
                    if content.replace('\n', '').partition('=')[2].lower() == "true":
                        return True

                    elif content.replace('\n', '').partition('=')[2].lower() == "false":
                        return False

                    elif content.replace('\n', '').partition('=')[2].isdigit():
                        try:
                            return int(content.replace('\n', '').partition('=')[2])

                        except ValueError:
                            return content.replace('\n', '').partition('=')[2]

                    elif content.replace('\n', '').partition('=')[2].replace('.', '').isdigit():
                        try:
                            return float(content.replace('\n', '').partition('=')[2])

                        except ValueError:
                            return content.replace('\n', '').partition('=')[2]

                    elif content.replace('\n', '').partition('=')[2] == "None":
                        try:
                            return None

                        except ValueError:
                            return content.replace('\n', '').partition('=')[2]

                    else:
                        return content.replace('\n', '').partition('=')[2]

                else:
                    continue

    def set(self, variable=None, value=None):
        """
        Set a new value for `variable`.

        :param str variable: The variable name/key to modify/add.
        :param str value: The desired value of <variable>.

        :returns int: Error code
        """

        if variable is None or value is None:
            return 11

        else:
            try:
                variable = str(variable)
                value = str(value)

            except(TypeError, ValueError):
                return 11

            else:
                contents = self._open_config_file().split('\n')
                new_config = []
                for content in contents:
                    if content.startswith('#'):
                        new_config.append(content)

                    elif content.startswith(variable + '='):
                        new_config.append(variable + '=' + value)

                    elif content == "":
                        new_config.append('')

                    else:
                        new_config.append(content)

                result = ""
                for line in new_config:
                    if line == "":
                        result += ''

                    else:
                        result += line + '\n'

                try:
                    self._save_config_file(result)

                except Exception as error:
                    print(error)
                    return 1

                else:
                    return 0

    def new(self):
        """
        Create a new configuration file.

        :returns int: Error code
        """

        if os.path.exists(self.config_path):
            print("File already exists")
            return 2651

        new_config = [
            "# ConfigHandler configuration file",
            "# Configuration File Version: 0.0.1.0"
        ]
        result = ""
        for line in new_config:
            if line == "":
                result += ''

            else:
                result += line + '\n'

        try:
            self._save_config_file(result)

        except Exception as error:
            print(error)
            return 1

        else:
            return 0

    def add(self, variable=None, value=None):
        """
        Add a new variable and set value for it.

        :param str variable: The variable name/key to modify/add.
        :param str value: The desired value of <variable>.

        :returns int: Error code
        """

        if variable is None or value is None:
            return 11

        else:
            try:
                variable = str(variable)
                value = str(value)

            except(TypeError, ValueError):
                return 11

            else:
                contents = self._open_config_file().split('\n')
                new_config = []
                for content in contents:
                    if content.startswith('#'):
                        new_config.append(content)

                    elif content.startswith(variable + '='):
                        return 15

                    elif content == "":
                        new_config.append('')

                    else:
                        new_config.append(content)

                new_config.append(variable + '=' + value)

                result = ""
                for line in new_config:
                    if line == "":
                        result += ''

                    else:
                        result += line + '\n'

                try:
                    self._save_config_file(result)

                except Exception as error:
                    print(error)
                    return 1

                else:
                    return 0

class Version2():
    """
    The class containing methods to use the version 2 configuration file.
    """

    def __init__(self, configpath):
        """
        The initialization method of Version2() class.

        :param str configpath: The path of the configuration file to use.
        """

        self.VERSION = "0.0.0.6"

        self.configpath = configpath
        self.__data = {
            "name": None,
            "author": None,
            "version": None,
            "separator": None,
            "compression": None,
            "encryption": None,
            "dictionary": None  # The encrypted form
        }
        self.__dictionary = None  # The decrypted form
        self.encoding = "utf-8"  # ? What if we include this inside config data?

        # A list of supported data types
        self.datatypes = ("str", "int", "float", "bool", "arr", "bin")

        # A list of supported compression algorithms
        self.compressions = ("zlib",)  # `huffman` soon to be supported

        # A list of supported encryption algorithms
        self.encryptions = ("aes256",)

    def __b64encode(self, to_encode):
        """
        Encode <to_encode> using Base64.

        :param str to_encode: The string to encode.*
        :param int to_encode: The integer to encode.*
        :param float to_encode: The decimal to encode.*
        :param bool to_encode: The boolean to encode.*
        :param bytes to_encode: The bytes to encode.*

        *The supported data types (except str and bytes) are converted to str.
        *str data types are converted to bytes.

        :returns str: The string version of the <encoded> (data type `bytes`) variable.
        """

        if type(to_encode) in (str, int, float, bool):
            to_encode = str(to_encode).encode(self.encoding)

        elif type(to_encode) is bytes:
            pass

        else:
            raise ValueError("Unsupported data type.")

        encoded = base64.b64encode(to_encode)
        return str(encoded.decode(self.encoding))

    def __b64decode(self, to_decode):
        """
        Decode <to_decode> using Base64.

        :param str to_decode: The string to decode.
        :param bytes to_decode: The bytes to decode.

        :returns str: The decoded form of <to_decode>.
        """

        if type(to_decode) is str:
            to_decode = to_decode.encode(self.encoding)

        elif type(to_decode) is bytes:
            pass

        else:
            raise ValueError("Unsupported data type.")

        return base64.b64decode(to_decode)

    def __readconfig(self):
        """
        Read the configuration file.

        :returns list: f.readlines()
        """

        with open(self.configpath, 'r') as f:
            return self.__b64decode(f.readlines())

    def __writeconfig(self):
        """
        Replace existing data from <self.configpath> with <self.__data>.

        :returns void:
        """

        # Check if `self.__data` values are valid.
        self._validate_data()

        # Create the long string
        newdata = f"""
name={self.__data["name"]}
author={self.__data["author"]}
version={self.__data["version"]}
separator={self.__data["separator"]}
compression={self.__data["compression"]}
encryption={self.__data["encryption"]}

+|+DICTIONARY+|+
{self.__data["dictionary"]}
"""

        # Write `newdata` to `self.configpath`.
        with open(self.configpath, 'w') as f:
            f.write(self.__b64encode(newdata))

    def _validate_data(self, configdata=None):
        """
        Validate configuration data (data type `dict`).
        Raises `ValueError` if there is an invalid value in the data.
        Raises `TypeError` if `configdata` is invalid.

        :param dict configdata: The dictionary form of configuration data.

        :returns void:
        """

        if configdata is None:
            configdata = self.__data

        else:
            if type(configdata) is dict:
                pass

            else:
                raise TypeError("configdata must be a dictionary.")

        keynames = {
            "name": (str,),
            "author": (str,),
            "version": (int, float),
            "separator": (str,),
            "compression": (str,),
            "encryption": (str,),
            "dictionary": (str,)
        }

        for key in keynames:
            if type(configdata[key]) not in keynames[key]:
                raise ValueError("The key does not have a valid value data type.")

            else:
                continue

    def __readdict(self, dictionary, epass=None):
        """
        Read the dictionary and store it in <self.__dictionary>.

        :param str dictionary: The dictionary in string data type.
        :param bytes dictionary: The dictionary in bytes data type.

        :param str epass: Encryption password.

        :returns void:
        """

        if type(dictionary) is str:
            dictionary = dictionary.encode(self.encoding)

        elif type(dictionary) is bytes:
            pass

        else:
            raise TypeError("Invalid dictionary!")

        # Decompression
        dictionary = self.__b64decode(dictionary.encode(self.encoding))
        if self.__data["compression"] == "None":
            decompressed = dictionary.encode(self.encoding)

        elif self.__data["compression"] == "zlib":
            decompressed = zlib.decompress(dictionary)

        else:
            raise ValueError("Invalid compression algorithm name")

        # Decryption
        decompressed = self.b64decode(decompressed).encode(self.encoding)
        if self.__data["encryption"] == "None":
            decrypted = decompressed

        elif self.__data["encryption"] == "aes256":
            decrypted = AES256(epass).decrypt(decompressed)

        else:
            raise ValueError("Invalid encryption algorithm name")

        plaintext = self.__b64decode(decrypted)

        # parse the plaintext
        i = 0
        result = {}
        # <variable_name>|<datatype>|<value>
        # <variable_name>|<datatype>|<array_datatype>|<array_separator>|<values>
        for line in plaintext.split('\n'):
            line = line.split(self.__data["separator"])
            for column in line:
                if column[1] in self.datatypes:
                    if column[1] == "arr":
                        result[column[0]] = [column[1], column[2], column[3], []]
                        arrayvalues = column[4].split(column[3])
                        for arrayvalue in arrayvalues:
                            if column[2] == "str":
                                arrayvalue = str(arrayvalue)

                            elif column[2] == "int":
                                arrayvalue = int(arrayvalue)

                            elif column[2] == "float":
                                arrayvalue = float(arrayvalue)

                            elif column[2] == "bool":
                                if arrayvalue == 0:
                                    arrayvalue = False

                                elif arrayvalue == 1:
                                    arrayvalue = True

                                else:
                                    raise ValueError("Unknown boolean state")

                            elif column[2] == "bin":
                                arrayvalue = arrayvalue.encode(self.encoding)

                            elif column[2] == "arr":
                                # DEV0004: Should we implement nested arrays?
                                raise ValueError("Nested arrays are not yet implemented.")

                            else:
                                raise ValueError("Invalid array data type")

                            result[column[0]][3].append(arrayvalue)

                    elif column[1] == "str":
                        result[column[0]] = [column[1], column[2]]

                    elif column[1] == "int":
                        result[column[0]] = [column[1], int(column[2])]

                    elif column[1] == "float":
                        result[column[0]] = [column[1], float(column[2])]

                    elif column[1] == "bool":
                        if column[2] == 0:
                            convertedbool = False

                        elif column[2] == 1:
                            convertedbool = True

                        else:
                            raise ValueError("Unknown boolean state")

                        result[column[0]] = [column[1], convertedbool]

                    elif column[1] == "bin":
                        result[column[0]] = [column[1], column[2].encode(self.encoding)]

                    else:
                        raise ValueError("Unknown data type")

        self.__dictionary = result

    def __writedict(self, newdict, epass=None):
        """
        Replace existing data from self.__data["dictionary"] with <newdict>.

        :param str newdict: The whole dictionary to write.
        :param str epass: Encryption password (if self.encryption != None)

        :returns void:
        """

        result = ""

        """
        Python form:
        <variable_name>|<datatype>|<value>

        "variable_name": ["datatype", "value"]

        <variable_name>|<datatype>|<array_datatype>|<array_separator>|<values>

        "variable_name": ["datatype", "array_datatype", "array_separator", ["value1", "value2]]
        """

        # Loop through the new dictionary
        for variable_name in newdict:
            # Get the data type of the value
            datatype = newdict[variable_name][0]
            # Arrays needs more fields.
            if datatype == "arr":
                array_datatype = newdict[variable_name][1]
                array_separator = newdict[variable_name][2]
                values = newdict[variable_name][3]
                result += f'{variable_name}{self.__data["separator"]}{datatype}{self.__data["separator"]}{array_datatype}{self.__data["separator"]}{array_separator}{self.__data["separator"]}'
                _ = 0
                while _ < len(values):
                    result += values[_]
                    if _ < (len(values) - 1):
                        result += '\n'

                    else:
                        result += self.__data["separator"]
                    _ += 1

            else:
                value = newdict[variable_name][1]
                result += f'{variable_name}{self.__data["separator"]}{datatype}{self.__data["separator"]}{value}\n'

        # Encode the result
        eresult = self.__b64encode(result)
        # Encrypt the result
        if self.__data["encryption"] == "None":
            pass

        elif self.__data["encryption"] == "aes256":
            eresult = self.__b64encode(AES256(epass).encrypt(eresult))

        else:
            raise ValueError("Invalid encryption algorithm name")

        # Compress the result
        if self.__data["compression"] == "None":
            cresult = eresult

        elif self.__data["compression"] == "zlib":
            cresult = zlib.compress(eresult)

        else:
            raise ValueError("Invalid compression algorithm name")

        self.__data["dictionary"] = self.__b64encode(cresult)

    def load(self, epass=None, load_dict=True):
        """
        Get the current values of the configuration file.
        This method must be called first to work with the configuration file.

        :param str epass: The encryption password (If the configuration file is encrypted.)
        :param bool load_dict: If True, this method will decrypt and decode the dictionary and store it to `self.__dictionary`.

        :returns void:
        """

        i = 0
        cdata = self.__readconfig()

        # Read configuration file information.
        while i < len(cdata):
            if cdata[i].startswith("name="):
                self.__data["name"] = str(cdata[i].partition('=')[2].replace('\n', ''))

            elif cdata[i].startswith("author="):
                self.__data["author"] = str(cdata[i].partition('=')[2].replace('\n', ''))

            elif cdata[i].startswith("version="):
                self.__data["version"] = float(cdata[i].partition('=')[2].replace('\n', ''))

            elif cdata[i].startswith("separator="):
                self.__data["separator"] = str(cdata[i].partition('=')[2].replace('\n', ''))

            elif cdata[i].startswith("compression="):
                self.__data["compression"] = str(cdata[i].partition('=')[2].replace('\n', ''))

            elif cdata[i].startswith("encryption="):
                self.__data["encryption"] = str(cdata[i].partition('=')[2].replace('\n', ''))

            elif cdata[i] == "+|+DICTIONARY+|+\n":
                self.__data["dictionary"] = cdata[i + 1].replace('\n', '').encode(self.encoding)
                if load_dict:
                    self.__readdict(self.__data["dictionary"], epass)

                else:
                    self.__dictionary = None

            else:
                i += 1
                continue

    def info(self):
        """
        Return information about the configuration file.

        :returns dict:
        """

        return self.__data.pop("dictionary")

    def get(self, key):
        """
        Get the value of <key>.

        :param str key: The name/key of the value you are looking for.

        :returns str: Returns type(str) if the <key>'s datatype is `str`.
        :returns int: Returns type(int) if the <key>'s datatype is `int`.
        :returns float: Returns type(float) if the <key>'s datatype is `float`.
        :returns bool: Returns type(bool) if the <key>'s datatype is `bool`.
        :returns list: Returns type(list) if the <key>'s datatype is `arr`.
        :returns bytes: Returns type(bytes) if the <key>'s datatype is `bin`.
        """

        if self.__dictionary is None:
            raise ValueError("The dictionary is not yet loaded!")

        elif type(self.__dictionary) is dict:
            value = self.__dictionary[key]
            if value[0] == "str":
                value = str(value[1])

            elif value[0] == "int":
                value = int(value[1])

            elif value[0] == "float":
                value = float(value[1])

            elif value[0] == "bool":
                if int(value[1]) == 0:
                    value = False

                elif int(value[1]) == 1:
                    value = True

                else:
                    raise ValueError("Unknown boolean state")

            elif value[0] == "arr":
                # result[column[0]] = [column[1], column[2], column[3], []]
                newvalue = value[3].split(value[2])
                valuearrdatatype = value[1]
                value = []
                for _ in newvalue:
                    if valuearrdatatype == "str":
                        value.append(str(_))

                    elif valuearrdatatype == "int":
                        value.append(int(_))

                    elif valuearrdatatype == "float":
                        value.append(float(_))

                    elif valuearrdatatype == "bool":
                        if int(_) == 0:
                            value.append(False)

                        elif int(_) == 1:
                            value.append(True)

                        else:
                            raise ValueError("Unknown boolean state")

                    elif valuearrdatatype == "bin":
                        value.append(_.encode(self.encoding))

                    else:
                        raise ValueError("Invalid data type")

            elif value[0] == "bin":
                value = value[1].encode(self.encoding)

            else:
                raise ValueError("Invalid data type")

        else:
            raise ValueError("Invalid dictionary")

    def add(self, key, valuetype, value, array_datatype=None, array_separator=None):
        """
        Add a new variable.

        :param str key: The variable name/key.
        :param str valuetype: The data type of the variable.
                              Available valuetypes:
                                  - str
                                  - int
                                  - float
                                  - bool
                                  - arr (list)
                                  - bin (binary)
        :param str value: The value of <key>.
        :param str array_datatype: [OPTIONAL; If your valuetype is `arr`, this is required] The data type of the array objects (`arr` not supported)
        :param str array_separator: [OPTIONAL; If your valuetype is `arr`, this is required] The separator for the array
        """

        # <variable_name>|<datatype>|<value>
        # <variable_name>|<datatype>|<array_datatype>|<array_separator>|<values>

        if self.__dictionary is None:
            raise ValueError("The dictionary is not yet loaded!")

        if self.__dictionary.get(key, None) is None:
            # Some lazy security checks
            if self.__data["separator"] in value:
                raise ValueError("value must not contain the separator!")

            if self.__data["separator"] in key:
                raise ValueError("key must not contain the separator!")

            # Add to the dictionary
            if valuetype in self.datatypes:
                if valuetype == "arr":
                    if array_datatype is None or array_separator is None:
                        raise ValueError("array_datatype and array_separator is required to create an array!")

                    keyvalue = [valuetype, array_datatype, array_separator, []]
                    # Check the list
                    if type(value) in (tuple, list):
                        for _ in value:
                            if keyvalue[1] == "str":
                                keyvalue[3].append(str(_))

                            elif keyvalue[1] == "int":
                                keyvalue[3].append(int(_))

                            elif keyvalue[1] == "float":
                                keyvalue[3].append(float(_))

                            elif keyvalue[1] == "bool":
                                if int(_) == 0:
                                    keyvalue[3].append(False)

                                elif int(_) == 1:
                                    keyvalue[3].append(True)

                                else:
                                    raise ValueError("Unknown boolean state")

                            elif keyvalue[1] == "bin":
                                if type(_) is bytes:
                                    keyvalue[3].append(_)

                                else:
                                    raise("array object is not in bytes data type")

                    else:
                        raise TypeError("value must be a tuple or list when creating an array.")

                else:
                    if valuetype == "str":
                        self.__dictionary[key] = [valuetype, str(value)]

                    elif valuetype == "int":
                        self.__dictionary[key] = [valuetype, int(value)]

                    elif valuetype == "float":
                        self.__dictionary[key] = [valuetype, float(value)]

                    elif valuetype == "bool":
                        if value:
                            self.__dictionary[key] = [valuetype, 1]

                        else:
                            self.__dictionary[key] = [valuetype, 0]

                    elif valuetype == "bin":
                        if type(value) is bytes:
                            self.__dictionary[key] = [valuetype, value]

                        else:
                            raise ValueError("value is not in bytes data type")

                    else:
                        raise ValueError("Unsupported data type")

            else:
                raise ValueError("Unsupported data type")

        else:
            ValueError("A value is already assigned to the key. Use update() instead.")

    def update(self, key, value):
        """
        Update an existing variable.

        :param str key: The variable name/key to update.
        :param str value: The new value of <key>.
        """

        # <variable_name>|<datatype>|<value>
        # <variable_name>|<datatype>|<array_datatype>|<array_separator>|<values>
        # ! TODO: DEV0003
        oldkeyvalue = self.get(key)
        if oldkeyvalue[0] == "str":
            newkeyvalue = [oldkeyvalue[0], str(value)]

        elif oldkeyvalue[0] == "int":
            newkeyvalue = [oldkeyvalue[0], int(value)]

        elif oldkeyvalue[0] == "float":
            newkeyvalue = [oldkeyvalue[0], float(value)]

        elif oldkeyvalue[0] == "bool":
            newkeyvalue = [oldkeyvalue[0], int(value)]

        elif oldkeyvalue[0] == "arr":
            newkeyvalue = [oldkeyvalue[0], int(value)]

        elif oldkeyvalue[0] == "bin":
            newkeyvalue = [oldkeyvalue[0], int(value)]

    def remove(self, key):
        """
        Remove an existing variable.

        :param key: The key to remove.
        """

    def new(self, name, author=None, separator="|", compression=None, encryption=None):
        """
        Create a new configuration file.
        """