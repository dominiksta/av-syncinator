import os
import shutil

def build(python_minor_version: int = 9):

    # Build the appimagetool container
    # ----------------------------------------------------------------------

    cmd = """
    docker build
        -f Dockerfile.appimagetool
        -t av-syncinator-appimagetoool:latest .
    """.replace("\n", "")
    print(cmd)
    ret = os.system(cmd)
    if os.name != 'nt': ret = os.WEXITSTATUS(ret)
    if ret != 0: print(f"Non-zero exit code: {ret}"); exit(1)

    # Build builder container
    # ----------------------------------------------------------------------

    prevdir = os.getcwd()
    os.chdir('..' + os.sep + '..')

    cmd = f"""
    docker build
        --build-arg PYTHON_MINOR_VERSION={python_minor_version}
        -f build/gnu_linux/Dockerfile
        -t av-syncinator-linux-builder:3.{python_minor_version} .
    """.replace("\n", "")
    print(cmd)
    ret = os.system(cmd)
    if os.name != 'nt': ret = os.WEXITSTATUS(ret)
    if ret != 0: print(f"Non-zero exit code: {ret}"); exit(1)

    os.chdir(prevdir)

    # build the application
    # ----------------------------------------------------------------------

    pwd = os.getcwd().replace('\\', '/')
    cmd = f"""
    docker run \
        -v {pwd}/tmp/:/dest
        av-syncinator-linux-builder:3.{python_minor_version}
    """.replace("\n", "")
    print(cmd)
    ret = os.system(cmd)
    if os.name != 'nt': ret = os.WEXITSTATUS(ret)
    if ret != 0: print(f"Non-zero exit code: {ret}"); exit(1)

    shutil.rmtree('tmp' + os.sep + 'av-syncinator.AppDir' + os.sep + 'app'
                  + os.sep + 'av-syncinator', ignore_errors=True)
    shutil.move('tmp' + os.sep + 'av-syncinator',
                'tmp' + os.sep + 'av-syncinator.AppDir' + os.sep + 'app')
    shutil.rmtree('tmp' + os.sep + 'av-syncinator-cli.AppDir' + os.sep + 'app'
                  + os.sep + 'av-syncinator-cli', ignore_errors=True)
    shutil.move('tmp' + os.sep + 'av-syncinator-cli',
                'tmp' + os.sep + 'av-syncinator-cli.AppDir' + os.sep + 'app')

    # package it as an appimage
    # ----------------------------------------------------------------------

    pwd = os.getcwd().replace('\\', '/')
    cmd = f"""
    docker run \
        -v {pwd}/tmp:/app
        av-syncinator-appimagetool
        /usr/local/bin/appimagetool av-syncinator.AppDir
    """.replace("\n", "")
    print(cmd)
    ret = os.system(cmd)
    if os.name != 'nt': ret = os.WEXITSTATUS(ret)
    if ret != 0: print(f"Non-zero exit code: {ret}"); exit(1)

    shutil.move('tmp' + os.sep + 'AV-Syncinator-x86_64.AppImage',
                'dist' + os.sep + 'AV-Syncinator.AppImage')

    cmd = f"""
    docker run \
        -v {pwd}/tmp:/app
        av-syncinator-appimagetool
        /usr/local/bin/appimagetool av-syncinator-cli.AppDir
    """.replace("\n", "")
    print(cmd)
    ret = os.system(cmd)
    if os.name != 'nt': ret = os.WEXITSTATUS(ret)
    if ret != 0: print(f"Non-zero exit code: {ret}"); exit(1)

    shutil.move('tmp' + os.sep + 'AV-Syncinator-x86_64.AppImage',
                'dist' + os.sep + 'av-syncinator-cli.AppImage')


if __name__ == '__main__': build()
