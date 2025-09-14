FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y --no-install-recommends git wget curl ca-certificates python3 python3-venv python3-pip && rm -rf /var/lib/apt/lists/*
WORKDIR /root
RUN git clone https://github.com/comfyanonymous/ComfyUI.git
WORKDIR /root/ComfyUI
RUN python3 -m venv /root/ComfyUI/venv
ENV VIRTUAL_ENV=/root/ComfyUI/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip && pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio && pip install -r requirements.txt || true
EXPOSE 8188
CMD bash -lc "python main.py --listen 0.0.0.0 --port 8188"
