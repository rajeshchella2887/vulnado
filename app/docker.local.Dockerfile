# pull official base image
FROM python:3.11.4-slim-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y build-essential python3-dev vim netcat


# copy everything from app folder
COPY . .
COPY ./envs/local.env ./.env

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r ./requirements/local.txt


RUN chmod +x /usr/src/app/scripts/base-entrypoint.sh
RUN chmod +x /usr/src/app/scripts/local.entrypoint.sh


# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/scripts/local.entrypoint.sh"]

