FROM nvidia/cuda:12.1.0-devel-ubuntu22.04
ENV PYTHONUNBUFFERED 1

# Setting up basic repo 
ARG DEBIAN_FRONTEND noninteractive
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV TZ Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV CUDA_SUPPORT True

# Setting up working directory
ADD ./ services/
WORKDIR /services

# Install prerequisites
RUN apt-get update && apt-get install -y apt-utils \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && apt-get install -y \
    make build-essential wget curl git nano ffmpeg libsm6 libxext6 \
    p7zip-full p7zip-rar \
    python3.10 python3.10-distutils python3.10-dev python3.10-venv \
    && apt-get clean -y

# Create venv
RUN if [ ! -d "venv" ]; \
    then \
    python3.10 -m venv venv; \
    fi

# Setup
RUN /bin/bash install.sh

# Command for starting entrypoint script
CMD ["/bin/bash", "run.sh"]