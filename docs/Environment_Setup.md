# DriftingMe Environment Setup

## Prerequisites

### Hardware Requirements
- NVIDIA GPU with at least 8GB VRAM (tested with RTX 3080 10GB)
- 16GB+ system RAM recommended
- 50GB+ free disk space for models

### Software Requirements
- Docker and Docker Compose
- NVIDIA Container Toolkit
- Linux (tested on Ubuntu 22.04)

## Initial Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd DriftingMe
```

### 2. Model Downloads
The following models need to be downloaded manually and placed in their respective directories:

#### Required Models
- **SDXL Base 1.0**: `models/checkpoints/sd_xl_base_1.0.safetensors`
  - Download from: [Hugging Face](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
  - Size: ~6.9GB
  - Note: Automatically symlinked to `models/Stable-diffusion/` for A1111 compatibility

#### Optional Enhancement Models
These will be automatically downloaded by the containers on first run:
- **RealESRGAN x4**: `models/RealESRGAN/RealESRGAN_x4plus.pth` (~67MB)
- **CLIP Vision**: `models/clip_vision/clip_vision_g.safetensors` (~3.7GB)
- **CodeFormer**: Face restoration models
- **GFPGAN**: Face enhancement models

### 3. Start Services
```bash
docker compose up -d
```

**Important**: If models appear missing in ComfyUI after first startup, restart the containers:
```bash
docker compose down
docker compose up -d
```
This ensures proper volume mounting of large model files.

### 4. Verify Setup
Wait for containers to fully start (2-3 minutes), then test:
```bash
python3 scripts/test_apis.py
```

## Service URLs
- **A1111 WebUI**: http://localhost:7860
- **A1111 API**: http://localhost:7860/sdapi/v1/
- **ComfyUI**: http://localhost:8188
- **ComfyUI API**: http://localhost:8188/

## Environment Variables
No environment variables currently required. Configuration is handled through:
- `docker-compose.yml` for container settings
- `config/` directory for application configs (auto-generated)

## Troubleshooting

### GPU Issues
If you get CUDA errors:
```bash
# Check NVIDIA driver
nvidia-smi

# Check Docker NVIDIA support
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### Memory Issues
- Reduce batch size in generation scripts
- Close other GPU applications
- Restart Docker if containers become unresponsive

### Model Loading
If models fail to load:
- Check file sizes match expected values
- Verify file integrity (not corrupted downloads)
- Ensure sufficient disk space

## Development Notes
- Generated images saved to `outputs/` (gitignored)
- API scripts in `scripts/` directory
- Model files are gitignored (too large for repository)
- Configuration files in `config/default/` are gitignored (auto-generated)

## Production Considerations
- Use volume mounts for persistent model storage
- Consider model caching strategies for faster startup
- Monitor GPU memory usage during batch operations
- Implement proper error handling for API timeouts