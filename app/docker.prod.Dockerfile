###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.4-slim-bullseye as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y build-essential python3-dev

# lint
RUN pip install --upgrade pip
RUN pip install flake8==3.9.2
COPY . .
RUN flake8 --ignore=E501,F401,W503,W504,F403 .

# install dependencies
COPY ./requirements/* ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r production.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11.4-slim-bullseye

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app


# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


# install dependencies
RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y vim netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/base.txt .
COPY --from=builder /usr/src/app/production.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# copy ./scripts/prod.entrypoint.sh .
RUN chmod +x  $APP_HOME/scripts/base-entrypoint.sh
RUN chmod +x  $APP_HOME/scripts/prod.entrypoint.sh

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/scripts/prod.entrypoint.sh"]
