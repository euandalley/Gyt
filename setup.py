
from importlib.metadata import entry_points
from setuptools import setup

setup(
    name='gyt',
    version='1.0',
    packages=['gyt'],
    entry_points={
        'console_scripts': [
            'gyt = gyt.cli.main'
        ]
    }
)