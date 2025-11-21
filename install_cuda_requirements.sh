#!/bin/bash

# DriftingMe CUDA & Requirements Installation Script
# For fresh Linux installations
# Keeps everything containerized with Docker + NVIDIA Container Toolkit

set -e  # Exit on error

echo "============================================"
echo "DriftingMe CUDA & Requirements Setup"
echo "============================================"
echo ""

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VER=$VERSION_ID
    
    # Pop!_OS is based on Ubuntu, use ubuntu for repos
    if [ "$OS" = "pop" ]; then
        echo "Detected Pop!_OS, using Ubuntu repositories"
        OS="ubuntu"
    fi
else
    echo "Cannot detect Linux distribution"
    exit 1
fi

echo "Detected OS: $OS $VER"
echo ""

# Update system packages
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install basic requirements
echo ""
echo "📦 Installing basic requirements..."
sudo apt install -y \
    curl \
    wget \
    git \
    ca-certificates \
    gnupg \
    lsb-release \
    build-essential \
    python3 \
    python3-pip \
    python3-venv

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo ""
    echo "🐳 Installing Docker..."
    
    # Add Docker's official GPG key
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/$OS/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    
    # Add Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$OS \
      $(lsb_release -cs) stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    echo "✅ Docker installed successfully"
else
    echo "✅ Docker already installed"
fi

# Install NVIDIA drivers if not present
if ! command -v nvidia-smi &> /dev/null; then
    echo ""
    echo "🎮 Installing NVIDIA drivers..."
    
    # Add NVIDIA driver PPA
    sudo add-apt-repository -y ppa:graphics-drivers/ppa
    sudo apt update
    
    # Install recommended driver
    sudo apt install -y ubuntu-drivers-common
    sudo ubuntu-drivers autoinstall
    
    echo "✅ NVIDIA drivers installed"
    echo "⚠️  REBOOT REQUIRED for NVIDIA drivers to take effect"
    NEEDS_REBOOT=1
else
    echo "✅ NVIDIA drivers already installed"
    nvidia-smi
fi

# Install NVIDIA Container Toolkit
if ! command -v nvidia-ctk &> /dev/null; then
    echo ""
    echo "🔧 Installing NVIDIA Container Toolkit..."
    
    # Add NVIDIA Container Toolkit repository using new method
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    
    # Use the generic stable deb repository
    echo "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/deb/\$(ARCH) /" | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    
    sudo apt update
    sudo apt install -y nvidia-container-toolkit
    
    # Configure Docker to use NVIDIA runtime
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    
    echo "✅ NVIDIA Container Toolkit installed"
else
    echo "✅ NVIDIA Container Toolkit already installed"
fi

# Test GPU access in Docker
echo ""
echo "🧪 Testing GPU access in Docker..."
if sudo docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
    echo "✅ GPU access in Docker working!"
    sudo docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
else
    echo "⚠️  GPU test failed - may need reboot or driver installation"
fi

# Install Python dependencies for scripts
echo ""
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install requests pillow

echo ""
echo "============================================"
echo "Installation Complete!"
echo "============================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Run the setup script:"
echo "   ./setup.sh"
echo ""
echo "2. Download required models (see docs/Environment_Setup.md)"
echo "   - SDXL Base 1.0 model needed in models/checkpoints/"
echo ""
echo "3. Start the services:"
echo "   docker compose up -d"
echo ""
echo "4. Test the APIs:"
echo "   source venv/bin/activate"
echo "   python3 scripts/test_apis.py"
echo ""

if [ ! -z "$NEEDS_REBOOT" ]; then
    echo "⚠️  IMPORTANT: Reboot required for NVIDIA drivers!"
    echo "   Run: sudo reboot"
    echo ""
fi

if groups $USER | grep -q docker; then
    echo "✅ User is in docker group"
else
    echo "⚠️  Log out and back in for docker group membership to take effect"
    echo "   Or run: newgrp docker"
fi

echo ""
echo "🎬 Ready to create DriftingMe!"
