FROM nvidia/cuda:11.7.0-cudnn8-devel-ubuntu20.04
LABEL maintainer="EnlightAI"
LABEL repository="dreambooth"

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

# make sure to use venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# pre-install the heavy dependencies (these can later be overridden by the deps from setup.py)
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
        torch \
        torchvision \
        torchaudio \
        --extra-index-url https://download.pytorch.org/whl/cu117 && \
    python3 -m pip install --no-cache-dir \
        accelerate \
        datasets \
        hf-doc-builder \
        huggingface-hub \
        modelcards \
        numpy \
        scipy \
        tensorboard \
        transformers && \
    # install the diffusers for dreambooth
    python3 -m pip install --no-cache-dir \
        'git+https://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@github.com/Enlight-AI/diffuser.git@master' \
        ftfy \
        tensorboard \
        bitsandbytes-cuda117 \
        modelcards\
        ninja \
        'git+https://github.com/facebookresearch/xformers.git@main#egg=xformers'

RUN python3 -m pip install triton==2.0.0.dev20221120
    
CMD ["/bin/bash"]