FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y ffmpeg

ADD /src/requirements.txt /
RUN pip3 install -r /requirements.txt

ADD /src /src

ENTRYPOINT ["python3", "/src/app/cli.py"]