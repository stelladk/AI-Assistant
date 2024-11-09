import os
import sys

__BASEDIR = os.path.abspath(os.path.dirname(__file__))
__EXECUTABLE = sys.executable

def basedir():
    if "python" in __EXECUTABLE.split("/")[-1]:
        return __BASEDIR
    else:
        return os.path.abspath(os.path.dirname(__EXECUTABLE))