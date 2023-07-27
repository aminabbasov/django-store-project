ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim-bullseye AS base
# Why not alpine? Because it uses *musl* that can cause strange issues.
# https://pythonspeed.com/articles/alpine-docker-python/

LABEL maintainer="aminabbasov@proton.me"

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# Disables an automatic check for pip updates each time.

ENV PYTHONDONTWRITEBYTECODE 1
# Python will not try to write ".pyc" files.

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get --no-install-recommends install -y build-essential nano \
    && rm -rf /var/lib/apt/lists/*
    # Last line to delete apt cache and reduce dockerfile size

RUN pip install --upgrade pip

FROM base AS prod

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
# No cache to make dockerfile smaller

WORKDIR /src
COPY src /src
# name "/srv" would be also suitable

USER nobody

FROM base AS dev
# This syntax requires to have Docker Engine v23.0 or later

COPY dev-requirements.txt /
RUN pip install --no-cache-dir -r /dev-requirements.txt
# No cache to make dockerfile smaller

WORKDIR /src
COPY src /src
# TODO: think how to remove repetition

EXPOSE 8000
# Expose the port that the application listens on

CMD python3 manage.py runserver 8000
# Run the application
