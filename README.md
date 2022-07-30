# ConfigHandler

## Description

Create, update, and remove values from a configuration file made by ConfigHandler.

+ ***Simple Mode***: Store simple data (e.g., version, program statistics, etc.) in a single file.
+ ***Advanced Mode***: Store configuration data using JSON data format. Supports metadata, encryption, and compression.

## Installation

+ via pip: `pip install confighandler-python`
+ as a Git submodule: `git submodule add https://github.com/Chris1320/ConfigHandler-python.git`

### Requirements

The following modules are optional:

+ `pycryptodomex`: AES-256 encryption
+ `prettytable`: Prettier layout in interactive mode
+ `lz4`: LZ4 compression support

## Usage

### Simple Mode

**[QuickStart]** Creating a New Configuration File

```python

from config_handler.simple import Simple

config = Simple("test.conf")

# Create a new configuration file by assigning key-value pair.
config.set("foo", "bar")  # "foo" is the key, "bar" is the value.
config.set("nums", 123)
config.set("dec", 3.14)
config.set("Aboolean", True)
config.set("unintentional variable!", "unintentional value.")

# Remove values
config.remove("unintentional variable!")

config.save()  # Save the data to the file.

```

**[QuickStart]** Loading an Existing Configuration File

```python

from config_handler.simple import Simple

config = Simple("test.conf")

config.load()  # Load the data from the file.

# Get values from the loaded data.
config.get("foo")  # "foo" is the key.

config.set("foo", "barred")  # Change value of a key.
config.set("new_key", "new_value")  # Add a new key-value pair.

config.isbase64 = True  # Encode configuration file to Base64.

# Save changes
config.save()

```

A key can be any string, but must not start with a `#`, include a `=`, or include a `\n`.
A value can be any string, integer, or float.

### Advanced Mode

**[QuickStart]** Creating a New Configuration File

```python

from config_handler.advanced import Advanced

config = Advanced("test.conf", "p4ssw0rd")  # Password is required when encryption is not None.

config.new(
    name="Advanced Mode Test",
    author="Chris1320",
    compression="zlib",
    encryption="aes256"
)

# Create a new configuration file by assigning key-value pair.
config.set("foo", "bar")  # "foo" is the key, "bar" is the value.
config.set("nums", 123)
config.set("dec", 3.14)
config.set("Aboolean", True)
config.set("unintentional variable!", "unintentional value.")

# Remove values
config.remove("unintentional variable!")

config.save()  # Save the data to the file.

```

**[QuickStart]** Loading an Existing Configuration File

```python

from config_handler.advanced import Advanced

config = Advanced("test.conf", "p4ssw0rd")  # Password is required when encryption is not None.

# Load the data from the file.
config.load()

# Get values from the loaded data.
config.get("foo")  # "foo" is the key.

config.set("foo", "barred")  # Change value of a key.
config.set("new_key", "new_value")  # Add a new key-value pair.

config.metadata()  # Get metadata of the configuration file.

config.save()  # Save changes

```
