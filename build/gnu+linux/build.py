import os

def build(python_minor_version: int = 9):
    prevdir = os.getcwd()
    os.chdir('..' + os.sep + '..')

    cmd = f"""
    docker build
        --build-arg PYTHON_MINOR_VERSION={python_minor_version}
        -f build/gnu+linux/Dockerfile
        -t av-syncinator-linux-builder:3.{python_minor_version} .
    """.replace("\n", "")
    print(cmd)
    ret = os.system(cmd)
    if os.name != 'nt': ret = os.WEXITSTATUS(ret)
    if ret != 0: print(f"Non-zero exit code: {ret}"); exit(1)

    pwd = os.getcwd().replace('\\', '/')
    cmd = f"""
    docker run \
        -v {pwd}/build/gnu+linux/dist:/dest
        av-syncinator-linux-builder:3.{python_minor_version}
    """.replace("\n", "")
    print(cmd)
    os.system(cmd)

    os.chdir(prevdir)

if __name__ == '__main__': build()
