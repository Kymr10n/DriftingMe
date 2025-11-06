# DriftingMe Remote Deployment Guide

This guide will help you deploy and use the DriftingMe project on a remote machine via SSH.

## Prerequisites

### Local Machine (Your Current Machine)
- SSH client
- rsync (usually included with SSH)
- Git (to clone the repository)

### Remote Machine
- SSH server running
- Docker and Docker Compose installed
- NVIDIA Container Toolkit (for GPU support)
- NVIDIA GPU with at least 8GB VRAM
- 16GB+ system RAM
- 50GB+ free disk space

## Configuration

### 1. Environment Setup
Copy the environment template and configure for your setup:
```bash
cp .env.template .env
# Edit .env with your specific configuration
```

Example `.env` configuration:
```bash
# Your remote server details
REMOTE_HOST=user@your-server.com
REMOTE_PROJECT_DIR=~/DriftingMe

# API URLs (usually localhost when tunneling)
A1111_URL=http://localhost:7860
COMFYUI_URL=http://localhost:8188
```

## Quick Start

### 1. Make Deployment Scripts Executable
```bash
chmod +x deploy_remote.sh ssh_tunnel.sh
```

### 2. Complete Remote Deployment
```bash
# Deploy everything in one command
./deploy_remote.sh full-deploy
```

This will:
- Deploy project files to the remote server
- Set up the remote environment
- Start the Docker services

### 3. Set Up SSH Tunnels (Optional)
If you want to access the web interfaces locally:
```bash
# In a separate terminal
./ssh_tunnel.sh start
```

Then access:
- **A1111 WebUI**: http://localhost:7860
- **ComfyUI**: http://localhost:8188

## Step-by-Step Deployment

### 1. Deploy Project Files
```bash
./deploy_remote.sh deploy
```

### 2. Start Services on Remote
```bash
./deploy_remote.sh start
```

### 3. Check Status
```bash
./deploy_remote.sh status
```

## Using the Remote Noir Generator

### Generate a Noir Scene
```bash
# Generate a detective scene
./deploy_remote.sh generate detective

# Generate a femme fatale scene
./deploy_remote.sh generate femme_fatale

# Generate an alley scene
./deploy_remote.sh generate alley
```

### Sync Generated Images Back
```bash
./deploy_remote.sh sync
```

This downloads all generated images from the remote `outputs/` directory to your local `outputs/` directory.

## Manual SSH Commands

If you prefer to work directly on the remote machine:

### SSH into Remote Machine
```bash
ssh $REMOTE_HOST  # Uses your .env configuration
cd ~/DriftingMe
```

### Run Commands Remotely
```bash
# Check service status
docker-compose ps

# Generate noir image directly
python3 scripts/noir_generator_remote.py --scene detective

# View logs
docker-compose logs -f a1111
```

## Remote API Access

The noir generator script automatically detects the remote environment. You can also set the API URL manually:

```bash
# On the remote machine
export A1111_URL="http://localhost:7860"
python3 scripts/noir_generator_remote.py --scene detective
```

### Environment Configuration

All configuration is managed through the `.env` file. Available variables:

- `REMOTE_HOST`: SSH hostname for your remote server
- `REMOTE_PROJECT_DIR`: Remote project directory (default: `~/DriftingMe`) 
- `A1111_URL`: A1111 API URL (default: `http://localhost:7860`)
- `COMFYUI_URL`: ComfyUI API URL (default: `http://localhost:8188`)
- `LOCAL_A1111_PORT`: Local tunnel port for A1111 (default: 7860)
- `LOCAL_COMFYUI_PORT`: Local tunnel port for ComfyUI (default: 8188)

### Custom Configuration
Edit your `.env` file:
```bash
# Example .env
REMOTE_HOST=user@your-server.com
REMOTE_PROJECT_DIR=/opt/driftingme
A1111_URL=http://localhost:7860
```

## Available Commands

### Deployment Script (`./deploy_remote.sh`)
- `deploy` - Deploy project files to remote
- `start` - Start services on remote
- `stop` - Stop services on remote  
- `status` - Check service status
- `generate [scene]` - Generate noir image remotely
- `sync` - Sync outputs from remote to local
- `logs [service]` - Show service logs
- `full-deploy` - Complete deployment

### SSH Tunnel Script (`./ssh_tunnel.sh`)
- `start` - Create SSH tunnels (default)
- `stop` - Stop all SSH tunnels
- `status` - Show tunnel status

## Troubleshooting

### SSH Connection Issues
```bash
# Test SSH connection
ssh $REMOTE_HOST exit

# If password is required, set up SSH keys:
ssh-copy-id $REMOTE_HOST
```

### Docker Issues on Remote
```bash
# SSH to remote and check Docker
ssh $REMOTE_HOST

# Check Docker daemon
sudo systemctl status docker

# Check NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### Service Not Starting
```bash
# Check logs
./deploy_remote.sh logs

# Check specific service
./deploy_remote.sh logs a1111
```

### Port Conflicts with SSH Tunnels
```bash
# Stop existing tunnels
./ssh_tunnel.sh stop

# Check what's using the port
lsof -i :7860

# Kill specific process if needed
kill -9 <PID>
```

## Model Management

Models are stored in `~/DriftingMe/models/` on the remote server. The first time you start the services, they will download required models automatically.

### Required Models Location
- `models/checkpoints/` - Main model files
- `models/VAE/` - VAE models  
- `models/RealESRGAN/` - Upscaling models
- `models/clip_vision/` - CLIP models

## Performance Notes

- The first generation will take longer as models are loaded
- Subsequent generations are much faster
- Use `--seed` parameter for reproducible results
- Monitor GPU memory usage with `nvidia-smi` on the remote machine

## Security Considerations

- Services are bound to localhost on remote (only accessible via SSH tunnel or from remote machine)
- No external network access to A1111/ComfyUI interfaces
- All communication over encrypted SSH

## Next Steps

1. **Generate your first noir image**: `./deploy_remote.sh generate detective`
2. **Set up SSH tunnels**: `./ssh_tunnel.sh start` (in separate terminal)
3. **Access web interface**: Visit http://localhost:7860
4. **Sync results**: `./deploy_remote.sh sync`

Happy generating! 🎬✨