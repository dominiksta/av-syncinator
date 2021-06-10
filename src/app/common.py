import sys
import os
import shutil

APPDIR = '..' + os.sep
TEMPDIR = (os.getenv("TMP") if os.name == 'nt' else '/tmp') + os.sep \
    + "_AVSyncinator" + os.sep


def dirsetup():
    _pyinstchdir()
    if not os.path.exists(TEMPDIR): os.mkdir(TEMPDIR)


def dirteardown():
    if os.path.exists(TEMPDIR): shutil.rmtree(TEMPDIR)


def _pyinstchdir():
    """
    When running from a pyinstaller bundle, set the cwd so that data files like
    icons can be used as if we were running outside of a pyinstaller bundle.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        global APPDIR
        APPDIR = sys._MEIPASS + os.sep
