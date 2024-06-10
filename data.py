import os
import hashlib

GIT_DIR = '.gyt'

def init() -> None:
    os.makedirs(GIT_DIR)


def hash_object(data:bytes) -> str:
    """
    Hash contents of file, store file contents under the hash
    """
    oid = hashlib.sha1(data).hexdigest()

    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as f:
        f.write(data)

    return oid


def get_object(oid:str):
    """
    Get the contents of a file from hash
    """
    with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        contents = f.read()
        return contents