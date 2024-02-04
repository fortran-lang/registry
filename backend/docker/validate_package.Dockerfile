FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

RUN apk add --no-cache \
    bash \
    bash-completion \
    bash-doc \
    gfortran \
    git \
    musl-dev \
    tar \
    wget

USER root
WORKDIR /home/registry

# Set up fpm
RUN wget https://github.com/fortran-lang/fpm/releases/download/v0.9.0/fpm-0.9.0-linux-x86_64 -4 -O fpm && \
    chmod u+x fpm


WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .


CMD ["python3", "validate.py"]