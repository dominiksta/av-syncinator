ARG PYTHON_MINOR_VERSION=7
FROM python:3.${PYTHON_MINOR_VERSION}-slim-buster

RUN apt-get update && apt-get install -y ffmpeg

ADD /avsyncinator/requirements.txt /
RUN pip3 install -r /requirements.txt

ADD /avsyncinator /avsyncinator

ENTRYPOINT ["python3", "-m", "avsyncinator.cli"]