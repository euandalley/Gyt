import os

from gyt import data


def write_tree(directory:str='.'):
    """
    Store the current working directory in the object database by scanning the directory recursively
    """
    entries = list()

    with os.scandir(directory) as dirs:
        for dir in dirs:
            fullDir = f'{directory}/{dir.name}'

            if is_ignored(fullDir):
                continue
            
            if dir.is_file(follow_symlinks=False):
                objType = 'blob'
                with open(fullDir, 'rb') as f:
                    oid = data.hash_object(f.read())

            elif dir.is_dir(follow_symlinks=False):
                objType = 'tree'
                oid = write_tree(fullDir)

            entry = (dir.name, oid, objType)
            entries.append(entry)

    tree = ''
    for name, oid, onjType in sorted(entries):
        tree.join(f'{objType} {oid} {name}')
    
    return data.hash_object(tree.encode(), 'tree')


def is_ignored(path:str) -> bool:
    """Ignore files in .gyt as not part of project"""
    return '.gyt' in path.split('/')