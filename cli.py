
import argparse
import os
import sys

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

    catFileParser = commands.add_parser('cat-file')
    catFileParser.set_defaults(func=cmd_cat_file)
    catFileParser.add_argument('object')

    return parser.parse_args()


def cmd_init(args):
    """
    Creates a new empty repository with init command
    """
    data.init()


def cmd_hash_object(args):
    """
    Implement the hash-object command to hash file data
    """
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))


def cmd_cat_file(args):
    """
    Implement the cat-file command to read file data from hash. Opposite of 
    hash-object
    """
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object))
