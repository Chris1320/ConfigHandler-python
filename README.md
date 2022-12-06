# ConfigHandler

## Description

Create, update, and remove values from a configuration file made by ConfigHandler.

+ ***Simple Mode***: Store simple data (e.g., version, program statistics, etc.) in a single file.
+ ***Advanced Mode***: Store configuration data using JSON data format. Supports metadata, encryption, and compression.

## Installation

+ via pip: `pip install ConfigHandler-python`
+ as a Git submodule: `git submodule add https://github.com/Chris1320/ConfigHandler-python.git`

### Requirements

The following modules are optional:

+ `pycryptodomex`: AES256 encryption
+ `prettytable`: Prettier layout in interactive mode
+ `lz4`: LZ4 compression support

## Usage

### Simple Mode

**[QuickStart]** Creating a New Configuration File

```python

    from config_handler.simple import Simple

    config = Simple("test.conf")  # Create a new Simple ConfigHandler object.

    # Add key-value pairs to the configuration file.
    config["foo"] = "bar"  # "foo" is the key, "bar" is the value.
    config["nums"] = 123
    config["dec"] = 3.14
    config["Aboolean"] = True
    config["unintentional variable!"] = "unintentional value."

    # Remove values
    del config["unintentional variable!"]

    print(config.exists)  # It will print `False` because the file does not exist yet.
    config.save()  # Save the data to the file.
    print(config.exists)  # It is now True.

```

**[QuickStart]** Loading an Existing Configuration File

```python

    from config_handler.simple import Simple

    config = Simple("test.conf")

    config.load()  # Load the data from the file.

    # Get values from the loaded data.
    print(config["foo"])  # "foo" is the key.

    config["foo"] = "barred"  # Change value of a key.
    config["new_key"] = "new_value"  # Add a new key-value pair.

    config.isbase64 = True  # Encode configuration file to Base64.

    # Save changes
    config.save()

```

A key can be any string, but must not start with a `#`, include a `=`, or include a `\n`.
A value can be any string, integer, float, or boolean.

### Advanced Mode

**[QuickStart]** Creating a New Configuration File

```python

    from config_handler.advanced import Advanced

    config = Advanced("test.conf", "p4ssw0rd")  # Password is required when encryption is not None.

    config.new(  # Initialize a new configuration file.
        name="Advanced Mode Test",
        author="Chris1320",
        compression="zlib",
        encryption="aes256"
    )

    # Add key-value pairs to configuration file.
    config["foo"] = "bar"  # "foo" is the key, "bar" is the value.
    config["nums"] = 123
    config["dec"] = 3.14
    config["Aboolean"] = True
    config["unintentional variable!"] = "unintentional value."

    # Remove values
    del config["unintentional variable!"]

    config.save()  # Save the data to the file.

```

**[QuickStart]** Loading an Existing Configuration File

```python

    from config_handler.advanced import Advanced

    config = Advanced("test.conf", "p4ssw0rd")  # Password is required when encryption is not None.

    # Load the data from the file.
    config.load()

    # Get values from the loaded data.
    print(config["foo"])  # "foo" is the key.

    config["foo"] ="barred"  # Change value of a key.
    config["new_key"] = "new_value"  # Add a new key-value pair.

    config()  # Get metadata of the configuration file.
              # This is formerly called as `config.metadata()`.

    config.save()  # Save changes

```
