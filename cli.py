
import argparse
import os

from . import data


def main() -> None:
    args = parse_args()
    args.func(args)


def parse_args() -> argparse.Namespace:
    """Parser for commands"""
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    initParser = commands.add_parser('init')
    initParser.set_defaults(func=cmd_init)

    return parser.parse_args()


def cmd_init(args):
    """Creates a new empty repository"""
    data.init()
