#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='gyt',
    version='1.0',
    packages=['gyt'],
    entry_points={
        'console_scripts': [
            'gyt = gyt.cli:main'
        ]
    }
)