#!/bin/bash

set -e

pushd . && cd ../../

mkdir -p /dist
mkdir -p /tmp/buildtmp


build() {
    pyinstaller \
        --onedir -y \
        --add-data "avsyncinator/res/logo/logo.ico:res/logo" \
        --add-data "/tmp/ffmpeg:." \
        --workpath "/tmp/buildtmp" \
        --distpath "/dest" \
        --name $EXENAME \
        $SCRIPTFILE
    rm "$EXENAME.spec"
}


case $1 in
    cli)
        EXENAME=av-syncinator-cli
        SCRIPTFILE=avsyncinator/cli.py
        build
        ;;
    gui)
        EXENAME=av-syncinator
        SCRIPTFILE=avsyncinator/gui.py
        build
        ;;
    both)
        EXENAME=av-syncinator-cli
        SCRIPTFILE=avsyncinator/cli.py
        build
        EXENAME=av-syncinator
        SCRIPTFILE=avsyncinator/gui.py
        build
        ;;
    *)
        echo "Missing argument"; exit 1
esac

popd