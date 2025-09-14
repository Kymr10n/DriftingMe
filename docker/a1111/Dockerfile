FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y --no-install-recommends git wget curl ca-certificates python3 python3-venv python3-pip libglib2.0-0 libsm6 libxrender1 libxext6 libtcmalloc-minimal4 libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
# Add user with UID 1000 and proper entry in /etc/passwd
RUN useradd -m -u 1000 user && echo 'user:x:1000:1000::/home/user:/bin/bash' >> /etc/passwd
WORKDIR /opt
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui webui
WORKDIR /opt/webui
RUN python3 -m venv /opt/webui/venv
ENV VIRTUAL_ENV=/opt/webui/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN git config --global --add safe.directory /opt/webui
RUN pip install --upgrade pip && pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio
# Install CUDA-compatible xformers
RUN pip install xformers --index-url https://download.pytorch.org/whl/cu121
# Fix permissions for user
RUN chown -R user:user /opt/webui /opt/webui/venv
USER user
EXPOSE 7860
ENV CLI_ARGS="--listen --port 7860 --xformers --medvram"
CMD bash -lc "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 ./webui.sh ${CLI_ARGS}"
