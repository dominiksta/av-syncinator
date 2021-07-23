import os
import sys
from . import build

def run_tests(python_minor_version: int = 9):
    build.build(python_minor_version)

    prevdir = os.getcwd()
    os.chdir('..' + os.sep + '..')

    pwd = os.getcwd()
    cmd = f"""
    docker run
        -v {pwd}/data:/data
        --entrypoint "/usr/local/bin/python3"
        av-syncinator:3.{python_minor_version}
        -m avsyncinator.test.code
    """.replace("\n", "")
    print(cmd)
    ret = os.system(cmd)
    if os.name != 'nt': ret = os.WEXITSTATUS(ret)

    os.chdir(prevdir)
    if ret != 0: exit(ret)

if __name__ == '__main__':
    if len(sys.argv) >= 2: run_tests(int(sys.argv[1]))
    else: run_tests()