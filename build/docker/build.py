import os

def build():
    prevdir = os.getcwd()
    os.chdir('..' + os.sep + '..')
    cmd = 'docker build -f build/docker/Dockerfile -t av-syncinator:latest .'
    print(cmd)
    os.system(cmd)
    os.chdir(prevdir)

if __name__ == '__main__': build()