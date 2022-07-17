from setuptools import setup

from config_handler import info

with open("README.md", "r") as f:
    README = f.read()  # Read the contents of `README.md` file.

print(info.title)
print()

setup(
    name="confighandler-python",
    version='.'.join(map(str, info.version)),  # Get the program version from the package.
    description="Create, update, and remove values from a configuration file made by ConfigHandler.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Chris1320/ConfigHandler-python",
    author="Chris1320",
    author_email="chris1320is@protonmail.com",
    license="MIT",
    classifiers=[  # https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7"
    ],
    packages=["config_handler"],
    include_package_data=True,
    install_requires=[],  # Required packages
    extras_require={  # Optional packages for optional features
        "AES Encryption": ["pycryptodomex"],
        "Pretty Table": ["prettytable"],
        "LZ4 Compression": ["lz4"],
    },
    entry_points={
        "console_scripts": [
            "config_handler=config_handler.__main__:main",
        ]
    }
)
