# ConfigHandler

## Description

Create, update, and remove values from a configuration file made by ConfigHandler.

## Usage

- Version 1:

  ```python

  from config_handler import Version1

  # Setup
  config_path = "config.dat"  # This is our configuration file.
  config = config_handler.Version1(config_path, False)

  # Creating a new configuration file
  config.new()  # Create a new configuration file.

  # Adding new variables
  config.add("sampleVariable", "sampleValue")
  config.add("another variable", 123456789)
  config.add("decimals", 1234.5678)
  config.add("lazymode", True)

  # Getting variables
  print(config.get("sampleVariable"))
  print(config.get("decimals") + 987654321)
  if config.get("lazymode"):
      print("The value of `lazymode` is True.")

  else:
      print("You're not lazy.")

  # Updating existing variables
  print("This is the old value: {0}".format(config.get("sampleVariable")))
  config.set("sampleVariable", "NewValue")
  print("This is the new value: {0}".format(config.get("sampleVariable")))
  ```

- Version 2:

  ```python

  from config_handler import Version2

  # "config.conf" is the configuration file path.
  config = Version2("config.conf")
  ```

## Configuration File Structure

- Version 1
  - Dictionary [Base64 encoded (optional)]
- Version 2
  - File info (config name, author, version, etc.) [Base64 encoded]
  - Dictionary [Compressed]

## Configuration Files Documentation

- Version 1:
  The version 1 of the configuration file is pretty straightforward.
  It only contains the main key/value pairs with optional comments
  represented by `#` symbols.

  ```plaintext
  # This is a comment.
  # This returns "value1" as a string.
  key1=value1
  # This automatically converts to an integer.
  aVariable=1234
  # This automatically converts to a float.
  s0m3thing=3.14
  # This automatically converts to a boolean.
  booleans=true
  ```

  - Dictionary:
    The dictionary contains the key/value pairs of the configuration file.
    The dictionary can be optionally encoded using Base64.
- Version 2:
  The version 2 of the configuration file contains more information about
  itself. It contains the configuration file's name, author, version, and
  the actual dictionary. Everything is encoded using Base64 and the dictionary
  is compressed or even be encrypted. `#` symbols represent comments. Comments
  are not allowed inside the dictionary.

  ```plaintext
  # This is a decoded and decompressed version of the configuration file.

  # The configuration info is formatted the same way as the version 1 configuration file format.
  name=Sample Configuration file
  author=Christopher Andrei Tayao
  version=2
  separator=|

  # The values below tells the module what compression and encryption algorithms
  # are used to store the dictionary.
  # Of course we did not compress anything here.
  compression=Huffman
  encryption=None

  # This is the line where the dictionary starts.
  # We will decode and decrypt the dictionary to make it readable.
  # This time, comments are allowed inside the dictionary.
  +|+DICTIONARY+|+
  # <variable_name>|<datatype>|<value>
  value1|str|Hello, world!
  aVariable|str|Some things here...
  anInt215|int|1452
  1Float|float|3.14
  # 0 = False, 1 = True
  isItTRUE|bool|0
  # The array below consists only of strings. Mixed data types are currently unavailable. (DEV0004)
  # <variable_name>|<datatype>|<array_datatype>|<array_separator>|<values>
  anArrayIGuess|arr|str|:;:|value1:;:Hello again!:;:Hola:;:Bonjour:;:anothing string of text.
  ```

  - Configuration Name:
    The configuration name is identified by the `name` key. This piece of
    information is used when Version2().info() is called.
  - Configuration Author:
    The configuration author is identified by the `author` key.
    It contains the name of the author/creator of the configuration file.
    This is optional.
  - Configuration Version:
    The configuration version is identified by the `version` key. It is **NOT**
    to be manually modified.
  - Dictionary Separator:
    The dictionary separator is identified by the `separator` key. It contains
    the separator used in the dictionary. Dictionary keys/values must not contain
    the dictionary separator.
  - Dictionary Compression Alogrithm:
    The dictionary compression algorithm is identified by the `compression` key.
    It contains the compression algorithm name used to compress the dictionary.
  - Dictionary Encryption Algorithm:
    The dictionary encryption algorithm is identified by the `encryption` key.
    It contains the encryption algorithm name used to encrypt the dictionary.
  - Dictionary
    The dictionary is the last part of the configuration file. ConfigHandler knows
    the position of the dictionary by looking for the constant string `+|+DICTIONARY+|+`.
    The dictionary contains the key/value pairs of the configuration file.
    It can also be optionally encrypted. Currently, the supported data types
    are strings (str), integers (int), decimals (float), booleans (bool),
    arrays (arr), and binary (bin).

    - Dictionary key/value pair Example (For strings, integers, decimals, booleans, and binary; Separator in this case is `|`):

      ```plaintext
      <variable_name>|<datatype>|<value>
      ```

    - Dictionary key/value pair Example (For arrays; Separator in this case is `|`):

      ```plaintext
      <variable_name>|<datatype>|<array_datatype>|<array_separator>|<values>
      ```
