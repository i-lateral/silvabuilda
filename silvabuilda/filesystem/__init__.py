__author__="morven"
__date__ ="$07-Jul-2011 23:37:05$"

# Filesystem deals with the core manipulations of related to downloading,
# extracting and copying remotes and local files into your project directory

import os
import shutil

def rm_existing(loc):
    """
    Used to check if a location already exists, if it does, delete it and
    return true

    """
    if os.path.isdir(loc):
        shutil.rmtree(loc)
        return True
    else:
        return False
    
def fix_path(path):
    """
    Use this to check if a path to a directory is ended with a "/". If not, then
    add it
    """
    if not path.endswith(os.sep):
        return path + os.sep
    else:
        return path
