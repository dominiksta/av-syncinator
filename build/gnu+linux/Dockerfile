ARG PYTHON_MINOR_VERSION=9
FROM python:3.${PYTHON_MINOR_VERSION}-buster
# The slim version of python does not seem to include tkinter

# wget: download static ffmpeg
# xz-utils: extract static ffmpeg
# binutils: dependency of pyinstaller
RUN apt-get update && apt-get install -y wget xz-utils binutils

ADD /avsyncinator/requirements.txt /
RUN pip3 install -r /requirements.txt

WORKDIR /tmp
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
RUN tar xf ffmpeg-release-amd64-static.tar.xz
RUN mv /tmp/ffmpeg-*/ffmpeg /tmp/ffmpeg

ADD / /src
WORKDIR /src/build/gnu+linux
ENTRYPOINT ["bash", "build.sh", "both"]
