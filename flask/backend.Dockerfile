# # This is a multi-stage build, so we can use the same Dockerfile for dev and prod environments
# Prod environment
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

CMD ["python3", "server.py"]


# Dev environment 
# FROM builder as dev-envs  

# RUN <<EOF
# apk update
# apk add git
# EOF

# RUN <<EOF
# addgroup -S docker
# adduser -S --shell /bin/bash --ingroup docker vscode
# EOF

# # install Docker tools (cli, buildx, compose)
# COPY --from=gloursdocker/docker / /

# CMD ["python3", "server.py"]
