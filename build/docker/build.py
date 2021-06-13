import os

def build(python_minor_version: int = 9):
    prevdir = os.getcwd()
    os.chdir('..' + os.sep + '..')
    cmd = f"""
    docker build
        --build-arg PYTHON_MINOR_VERSION={python_minor_version}
        -f build/docker/Dockerfile
        -t av-syncinator:3.{python_minor_version} .
    """.replace("\n", "")
    print(cmd)
    os.system(cmd)
    os.chdir(prevdir)

if __name__ == '__main__': build()