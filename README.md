# DriftingMe

A Docker-based Stable Diffusion environment featuring both Automatic1111 WebUI and ComfyUI for AI image generation.

## Features

- **Automatic1111 WebUI**: Full-featured web interface for Stable Diffusion
- **ComfyUI**: Node-based interface for advanced workflows
- **CUDA Support**: GPU acceleration for faster generation
- **Docker Compose**: Easy deployment and management
- **Volume Mounts**: Persistent storage for models, outputs, and configurations

## Prerequisites

- Docker and Docker Compose
- NVIDIA GPU with CUDA support
- NVIDIA Container Toolkit

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/DriftingMe.git
cd DriftingMe
```

2. Configure environment (optional):
```bash
cp .env.template .env
# Edit .env with your specific configuration
```

3. Set up permissions (required for Docker volume mounts):
```bash
./setup.sh
```

4. Start the services:
```bash
docker compose up -d
```

5. Access the interfaces:
   - **Automatic1111 WebUI**: http://localhost:7860 (configurable via A1111_URL)
   - **ComfyUI**: http://localhost:8188 (configurable via COMFYUI_URL)

## Directory Structure

```
DriftingMe/
├── docker/
│   ├── a1111/          # Automatic1111 Dockerfile
│   └── comfyui/        # ComfyUI Dockerfile
├── models/             # AI models storage
├── outputs/            # Generated images
├── config/             # Configuration files
├── art/                # Project artwork and references
├── scripts/            # Project scripts and documentation
└── docs/               # Documentation
```

## Configuration

- Models are stored in `./models/` and shared between both services
- Generated outputs are saved to `./outputs/`
- Configuration files can be placed in `./config/`

## Models

Place your Stable Diffusion models in the appropriate directories:
- Checkpoints: `models/checkpoints/` or `models/Stable-diffusion/`
- LoRA: `models/Lora/` or `models/loras/`
- VAE: `models/vae/` or `models/VAE/`

## Docker Services

### Automatic1111 WebUI
- Port: 7860
- Features: SDXL support, xformers, dark theme
- GPU: Full GPU access

### ComfyUI
- Port: 8188
- Features: Node-based workflow interface
- GPU: Full GPU access

## Development

To rebuild the containers:
```bash
docker compose build --no-cache
```

To view logs:
```bash
docker compose logs -f
```

## Troubleshooting

### Permission Errors
If you encounter permission errors like "Permission denied: 'outputs/txt2img-images'":
```bash
# Run the setup script to fix permissions
./setup.sh

# Or manually fix permissions
sudo chown -R $(whoami):$(whoami) outputs/ models/ config/ art/
chmod -R 755 outputs/ models/ config/ art/
```

### xFormers Issues
The containers are configured with CUDA-compatible xFormers. If you see xFormers warnings, the containers will automatically fall back to standard attention mechanisms.

## Configuration & Security

### Environment Variables
All sensitive configuration is managed through the `.env` file (not tracked in git):
- Copy `.env.template` to `.env` and customize for your setup
- Never commit `.env` files to version control
- For remote deployment, see `docs/Remote_Deployment.md`

### Available Configuration
- `A1111_URL`: API URL for Automatic1111 
- `COMFYUI_URL`: API URL for ComfyUI
- `REMOTE_HOST`: SSH host for remote deployment
- `REMOTE_PROJECT_DIR`: Remote project directory

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
