FROM nvidia/cuda:11.3.0-cudnn8-runtime-ubuntu20.04
LABEL maintainer="EnlightAI"
LABEL repository="upsampler"

ENV DEBIAN_FRONTEND=interactive

# Copy the local file to the file in the container.
# We also develop in the code folder.

RUN apt update && \
    apt install -y bash \
                   build-essential \
                   git \
                   git-lfs \
                   curl \
                   ca-certificates \
                   python3.8 \
                   python3-pip \
                   python3.8-venv && \
    rm -rf /var/lib/apt/lists

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# make sure to use venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN git clone https://github.com/xinntao/Real-ESRGAN.git
# go to the code folder
WORKDIR /app/Real-ESRGAN

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir torch==1.12.1+cu113 \
        torchvision==0.13.1+cu113 torchaudio==0.12.1 \
        --extra-index-url https://download.pytorch.org/whl/cu113 && \
    python3 -m pip install --no-cache-dir -r requirements.txt && \
    python3 setup.py develop

WORKDIR /app