import errno
import os
from qiniustorage.backends import QiniuStorage

__all__ = ('cloud_storage')
cloud_storage = QiniuStorage()

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured