import sys
import os
import shutil

VERSION='0.0.1'

MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


FFMPEG = None
APPDIR = 'avsyncinator' + os.sep
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
        os.environ['PATH'] = os.environ['PATH'] + ';' + APPDIR

    global FFMPEG
    FFMPEG = APPDIR + 'ffmpeg.exe' if os.path.exists(APPDIR + 'ffmpeg.exe') \
        else shutil.which('ffmpeg')
    if FFMPEG == None: raise Exception("ffmpeg not found in PATH")