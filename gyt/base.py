import os

from . import data


def write_tree(directory:str='.'):
    """
    Store the current working directory in the object database by scanning the directory recursively
    """
    with os.scandir(directory) as dirs:
        for dir in dirs:
            fullDir = f'{directory}/{dir.name}'
            
            if dir.is_file(follow_symlinks=False):
                print(fullDir)
            elif dir.is_dir(follow_symlinks=False):
                write_tree(fullDir)