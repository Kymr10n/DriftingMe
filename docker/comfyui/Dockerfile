FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y --no-install-recommends git wget curl ca-certificates python3 python3-venv python3-pip && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 comfyuser

WORKDIR /home/comfyuser
RUN git clone https://github.com/comfyanonymous/ComfyUI.git
WORKDIR /home/comfyuser/ComfyUI
RUN python3 -m venv /home/comfyuser/ComfyUI/venv
ENV VIRTUAL_ENV=/home/comfyuser/ComfyUI/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip && pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio && pip install -r requirements.txt || true

# Fix permissions
RUN chown -R comfyuser:comfyuser /home/comfyuser/ComfyUI

USER comfyuser
EXPOSE 8188
CMD bash -lc "python main.py --listen 0.0.0.0 --port 8188"
