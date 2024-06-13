import os
from tempfile import TemporaryFile
from typing import Any, Generator

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


def _iter_tree_entries(oid) -> Generator[tuple[str, str, str], Any, None]:
    """Generator to yield string values of hashed tree"""
    if not oid:
        return
    
    tree = data.get_object(oid, 'tree')

    for entry in tree.decode().splitlines():
        objType, oid, name = entry.split(' ', 2)
        yield objType, oid, name


def get_tree(oid:str, basePath:str='') -> dict[str, str]:
    """Create a dict containing the contents of a directory tree"""

    result = dict()

    for objType, oid, name in _iter_tree_entries(oid):
        
        if '/' in name:
            raise Exception("Invalid tree path, contains '/'")
        
        if name in ('.', '..'):
            raise Exception("Invalid tree path, contains '.' or '..'")
        
        path = basePath + name

        if objType == 'blob':
            result[path] = oid
        elif objType == 'tree':
            result.update(get_tree(oid, f'{path}/'))
        else:
            raise Exception(f'Unknown tree entry {objType}')
        
    return result


def read_tree(oid:str) -> None:
    """Reconstruct directory from hash trees"""
    _empty_current_dir_()
    for path, oid in get_tree(oid, basePath='./').items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data.get_object(oid))


def _empty_current_dir_() -> None:

    for root, dirNames, fileNames in os.walk('.', topdown=False):
        for fileName in fileNames:
            path = os.path.relpath(f'{root}/{fileName}')
            if is_ignored(path) or os.path.isfile(path):
                continue

        for dirName in dirNames:
            path = os.path.relpath(f'{root}/{dirName}')
            if is_ignored(path) or os.path.isfile(path):
                continue

            try:
                os.rmdir(path)
            except (FileNotFoundError, OSError): 
                # can fail if contains ignored files
                pass