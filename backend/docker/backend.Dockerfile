# Prod environment
FROM --platform=$BUILDPLATFORM python:3.10.13-bookworm AS builder

WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,mode=0777,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

CMD ["python3", "server.py"]

