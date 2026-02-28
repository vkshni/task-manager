from setuptools import setup

setup(
    name="taski",
    version="1.0",
    py_modules=["taski", "engine", "db", "entity", "state_machine"],
    entry_points={
        "console_scripts": [
            "taski=taski:main",
        ],
    },
)
