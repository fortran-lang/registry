FROM alpine:latest

# Install system dependencies
RUN apk add --no-cache \
    bash \
    bash-completion \
    bash-doc \
    gfortran \
    git \
    musl-dev \
    wget

# Create a non-root user
RUN adduser -D registry
USER registry
WORKDIR /home/registry

# Set up fpm
RUN wget https://github.com/fortran-lang/fpm/releases/download/v0.6.0/fpm-0.6.0-linux-x86_64 -4 -O fpm && \
    chmod u+x fpm

RUN git checkout stdlib-fpm
WORKDIR /home/registry
