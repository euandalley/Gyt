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