# ##############################################################################
# build this image:
# 
# docker build \
#   --build-arg UID=$(id -u) \
#   --build-arg GID=$(id -g) \
#   -t extract:1.0 .
# 
# Run this image
# 
# docker run --rm -v $(pwd):/home/docker extract:1.0 <zip_filename>
# ##############################################################################

FROM ubuntu:18.04

LABEL maintainer "Frank Junior <frankcbjunior@gmail.com>"

RUN apt-get update && apt-get install -y \
  --no-install-recommends \
  bash \
  zip \
  gzip \
  unzip \
  bzip2 \
  tar \
  xz-utils \
  unrar \
  p7zip-full \
  cabextract

RUN	apt-get clean -y && rm -rf /var/lib/apt/lists/*

# PS: this block is necessary to create file with the same host user (non-root user)
# --------------------------------------------------------------------------------
ARG USER=docker
# default password for user
ARG PW=docker

# this values come from "docker build"
ARG UID
ARG GID

RUN useradd -m ${USER} --uid=${UID} && echo "${USER}:${PW}" | chpasswd

USER ${UID}:${GID}
WORKDIR /home/${USER}
# --------------------------------------------------------------------------------

COPY extract.sh /home/${USER}/extract.sh

ENTRYPOINT [ "./extract.sh" ]