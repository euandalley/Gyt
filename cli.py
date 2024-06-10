
import argparse
import os

from . import data


def main() -> None:
    args = parse_args()
    args.func(args)


def parse_args() -> argparse.Namespace:
    """
    Parser for commands
    """
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    initParser = commands.add_parser('init')
    initParser.set_defaults(func=cmd_init)

    hashObjParser = commands.add_parser('hash-object')
    hashObjParser.set_defaults(func=cmd_hash_object)
    hashObjParser.add_argument('file')

    return parser.parse_args()


def cmd_init(args):
    """
    Creates a new empty repository with init command
    """
    data.init()


def cmd_hash_object(args):
    """
    Implement the hash-object command
    """
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))