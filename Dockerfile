FROM python:3.10-slim
WORKDIR /work

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# no apt prompts
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y install libgtk-3-0

# alias "python" to "python3"
RUN ln -s /usr/bin/python3 /usr/bin/python

# install python3 dependencies
RUN pip3 install --upgrade pip

COPY . .
RUN pip3 install .
