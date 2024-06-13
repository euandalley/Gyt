
from argparse import Namespace, ArgumentParser
import os
import sys

from gyt import data, base


def main() -> None:
    args = parse_args()
    args.func(args)


def parse_args() -> Namespace:
    """
    Parser for commands
    """
    parser: ArgumentParser = ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    initParser: ArgumentParser = commands.add_parser('init')
    initParser.set_defaults(func=cmd_init)

    hashObjParser: ArgumentParser = commands.add_parser('hash-object')
    hashObjParser.set_defaults(func=cmd_hash_object)
    hashObjParser.add_argument('file')

    catFileParser: ArgumentParser = commands.add_parser('cat-file')
    catFileParser.set_defaults(func=cmd_cat_file)
    catFileParser.add_argument('object')

    writeTreeParser: ArgumentParser = commands.add_parser('write-tree')
    writeTreeParser.set_defaults(func=cmd_write_tree)

    readTreeParser: ArgumentParser = commands.add_parser('read-tree')
    readTreeParser.set_defaults(func=cmd_read_tree)
    readTreeParser.add_argument('tree')

    return parser.parse_args()


def cmd_init(args) -> None:
    """
    Creates a new empty repository with init command
    """
    data.init()


def cmd_hash_object(args) -> None:
    """
    Implement the hash-object command to hash file data
    """
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))


def cmd_cat_file(args) -> None:
    """
    Implement the cat-file command to read file data from hash. Opposite of 
    hash-object
    """
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object, expected=None)) # type: ignore


def cmd_write_tree(args) -> None:
    """Encode state of current directory"""
    print(base.write_tree())


def cmd_read_tree(args) -> None:
    """Restore a tree from it's id"""
    base.read_tree(args.tree)