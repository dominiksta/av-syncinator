import os
import importlib
from shutil import rmtree
from os.path import join
from argparse import ArgumentParser

parser = ArgumentParser(description='Build AV-Syncinator')
parser.add_argument('target', help='The target to build', choices=[
    'windows', 'gnu_linux', 'docker', 'clean', 'test_docker'
])
try: args = parser.parse_args()
except: exit(1)

prevdir = os.getcwd()


def _main():
    if args.target == 'windows': build_windows()
    if args.target == 'gnu_linux': build_gnu_linux()
    if args.target == 'docker': build_docker()
    if args.target == 'clean': clean()


def clean():
    # windows:
    _rm('build', 'windows', 'dist', 'av-syncinator-cli.exe')
    _rm('build', 'windows', 'dist', 'av-syncinator.exe')
    _rmdir('build', 'windows', 'tmp')
    _mkdir('build', 'windows', 'tmp')
    _touch('build', 'windows', 'tmp', '.gitkeep')
    # gnu_linux:
    _rm('build', 'gnu_linux', 'dist', 'AV-Syncinator.AppImage')
    _rm('build', 'gnu_linux', 'dist', 'av-syncinator-cli.AppImage')
    _rmdir('build', 'gnu_linux', 'tmp', 'av-syncinator.AppDir',
           'app', 'av-syncinator')
    _rmdir('build', 'gnu_linux', 'tmp', 'av-syncinator-cli.AppDir',
           'app', 'av-syncinator-cli')
    # These should not exits, but to be sure:
    _rmdir('build', 'gnu_linux', 'tmp', 'av-syncinator')
    _rmdir('build', 'gnu_linux', 'tmp', 'av-syncinator-cli')
    

def build_windows():
    if os.name != 'nt':
        print("Windows builds can currently only be built on windows")
        exit(1)

    os.chdir('build' + os.sep + 'windows')
    ret = os.system('build-all.bat')
    if ret != 0:
        print(f'Non-zero exit code: {ret}'); exit(1)
    os.chdir(prevdir)


def build_gnu_linux():
    mod = importlib.import_module('build.gnu_linux.build')
    os.chdir('build' + os.sep + 'gnu_linux')
    mod.build()
    os.chdir(prevdir)


def build_docker():
    mod = importlib.import_module('build.docker.build')
    os.chdir('build' + os.sep + 'docker')
    mod.build()
    os.chdir(prevdir)


def _rm(*path):
    if os.path.exists(join(*path)): os.remove(join(*path))
def _rmdir(*path): rmtree(join(*path), ignore_errors=True)
def _touch(*path): open(join(*path), 'a').close()
def _mkdir(*path): os.mkdir(join(*path))

if __name__ == '__main__': _main()
