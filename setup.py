"""
Package configuration for taski.

Installs the taski CLI as a globally accessible command using setuptools.
Run once from the project root to register the command:

    pip install -e .

The -e flag installs in editable mode, meaning code changes take effect
immediately without needing to reinstall.

After installation, the CLI is available as:

    taski <command> [args]

Run 'taski help' for usage and examples.
"""

from setuptools import setup

setup(
    name="taski",
    version="1.0",
    py_modules=["taski", "engine", "db", "entity", "state_machine", "exceptions", "logger"],
    entry_points={
        "console_scripts": [
            # Maps the 'taski' shell command to the main() function in taski.py
            "taski=taski:main",
        ],
    },
)