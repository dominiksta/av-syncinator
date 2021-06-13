import os
import build

def run_tests():
    build.build()

    prevdir = os.getcwd()
    os.chdir('..' + os.sep + '..')

    cmd = """
    docker run
        -v {pwd}/data:/data
        --entrypoint "/usr/local/bin/python3"
        av-syncinator:latest
        /src/test/code.py
    """.format(pwd = os.getcwd()).replace("\n", "")

    print(cmd)
    os.system(cmd)
    os.chdir(prevdir)

if __name__ == '__main__': run_tests()