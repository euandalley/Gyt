import os
import hashlib

GIT_DIR = '.gyt'
NULL = b'\x00'

def init() -> None:
    os.makedirs(GIT_DIR)


def hash_object(data:bytes, objType='blob') -> str:
    """
    Hash contents of file, store file contents under the hash, return the hash
    """
    obj = objType.encode() + NULL + data
    oid: str = hashlib.sha1(obj).hexdigest()

    objectsPath = os.path.dirname(f'{GIT_DIR}/objects/')

    if not os.path.isdir(objectsPath):
        os.makedirs(objectsPath)

    with open(os.path.join(objectsPath, oid), 'wb') as f:
        f.write(data)
        f.write(obj)

    return oid


def get_object(oid:str, expected='blob') -> bytes:
    """
    Get the contents of a file from hash
    """
    with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj: bytes = f.read()

    objType, _, content = obj.partition(NULL)
    objType = objType.decode()

    if expected is not None:
        if objType != expected:
            raise Exception(f'Expected {expected}, got {objType}')

    return content


def set_HEAD(oid:str) -> None:
    """
    Head is the id of the most recent commit
    """
    with open(f'{GIT_DIR}/HEAD', 'w') as f:
        f.write(oid)


def get_HEAD() -> str | None:
    """
    Get the id of the most recent commit
    """
    headDir = f'{GIT_DIR}/HEAD'
    if os.path.isfile(headDir):
        with open(headDir) as f:
            return f.read().strip()
    else:
        return None