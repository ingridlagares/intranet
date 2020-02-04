# Pull the base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Setup workdir
RUN mkdir /code
WORKDIR /code

# Upgrade pip
RUN pip install pip -U
ADD requirements.txt /code/

#Install dependencies
RUN apt-get update
RUN apt-get install netcat python3-dev default-libmysqlclient-dev  -y
RUN pip install -r requirements.txt

# Add source files
ADD . /code/
