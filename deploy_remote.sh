#!/bin/bash
# DriftingMe Remote Deployment Script
# Deploys and manages the DriftingMe project on a remote server

set -euo pipefail

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        
        # Validate key format
        if [[ ! "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]]; then
            echo "ERROR: Invalid env var name: $key" >&2
            exit 1
        fi
        
        # Remove quotes and export safely
        value="${value%\"}"
        value="${value#\"}"
        export "$key=$value"
    done < .env
fi

# Configuration
REMOTE_HOST="${REMOTE_HOST:-user@remote-server.com}"
REMOTE_PROJECT_DIR="${REMOTE_PROJECT_DIR:-~/DriftingMe}"
LOCAL_PROJECT_DIR="$(pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check SSH connection
check_ssh_connection() {
    log_info "Testing SSH connection to $REMOTE_HOST..."
    if ssh -o ConnectTimeout=10 -o BatchMode=yes "$REMOTE_HOST" exit 2>/dev/null; then
        log_success "SSH connection successful"
        return 0
    else
        log_error "SSH connection failed. Please ensure:"
        echo "  1. SSH key is set up for passwordless login"
        echo "  2. Host $REMOTE_HOST is accessible"
        echo "  3. You can manually SSH: ssh $REMOTE_HOST"
        return 1
    fi
}

# Function to deploy project files
deploy_project() {
    log_info "Deploying project to $REMOTE_HOST:$REMOTE_PROJECT_DIR..."
    
    # Create project directory on remote
    ssh "$REMOTE_HOST" "mkdir -p $REMOTE_PROJECT_DIR"
    
    # Sync project files (excluding outputs and models that are large)
    rsync -avz --progress \
        --exclude='outputs/' \
        --exclude='models/' \
        --exclude='.git/' \
        --exclude='__pycache__/' \
        --exclude='*.pyc' \
        "$LOCAL_PROJECT_DIR/" "$REMOTE_HOST:$REMOTE_PROJECT_DIR/"
    
    log_success "Project files deployed successfully"
}

# Function to setup remote environment
setup_remote_environment() {
    log_info "Setting up remote environment..."
    
    ssh "$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && bash -s" << 'EOF'
        # Make setup script executable
        chmod +x setup.sh
        
        # Check for Docker
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker not found. Please install Docker and Docker Compose first."
            exit 1
        fi
        
        # Check for NVIDIA Container Toolkit
        if ! docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi &> /dev/null; then
            echo "⚠️  NVIDIA Container Toolkit might not be properly configured"
            echo "   Make sure to install it for GPU support"
        fi
        
        # Create necessary directories
        mkdir -p models/{checkpoints,VAE,RealESRGAN,clip_vision}
        mkdir -p outputs
        mkdir -p config
        mkdir -p art
        mkdir -p custom_nodes
        
        echo "✅ Remote environment setup complete"
EOF
    
    log_success "Remote environment configured"
}

# Function to start services on remote
start_remote_services() {
    log_info "Starting DriftingMe services on remote host..."
    
    ssh "$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && docker compose up -d"
    
    log_success "Services started on remote host"
    log_info "Services will be available at:"
    echo "  - A1111 WebUI: http://$REMOTE_HOST:7860"
    echo "  - ComfyUI: http://$REMOTE_HOST:8188"
}

# Function to stop services on remote
stop_remote_services() {
    log_info "Stopping DriftingMe services on remote host..."
    ssh "$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && docker compose down"
    log_success "Services stopped on remote host"
}

# Function to check service status
check_remote_status() {
    log_info "Checking service status on $REMOTE_HOST..."
    ssh "$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && docker compose ps"
}

# Function to run noir generator remotely
run_remote_noir_generator() {
    local scene_type="${1:-detective}"
    log_info "Running noir generator on remote host (scene: $scene_type)..."
    
    ssh "$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && python3 scripts/noir_generator_remote.py --scene $scene_type"
}

# Function to sync outputs back
sync_outputs() {
    log_info "Syncing outputs from remote host..."
    mkdir -p outputs
    rsync -avz --progress "$REMOTE_HOST:$REMOTE_PROJECT_DIR/outputs/" "./outputs/"
    log_success "Outputs synced to local ./outputs/ directory"
}

# Function to show logs
show_logs() {
    local service="${1:-}"
    if [ -n "$service" ]; then
        ssh "$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && docker compose logs -f $service"
    else
        ssh "$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && docker compose logs -f"
    fi
}

# Main script logic
case "${1:-help}" in
    "deploy")
        check_ssh_connection || exit 1
        deploy_project
        setup_remote_environment
        ;;
    "start")
        check_ssh_connection || exit 1
        start_remote_services
        ;;
    "stop")
        check_ssh_connection || exit 1
        stop_remote_services
        ;;
    "status")
        check_ssh_connection || exit 1
        check_remote_status
        ;;
    "generate")
        check_ssh_connection || exit 1
        run_remote_noir_generator "${2:-detective}"
        ;;
    "sync")
        check_ssh_connection || exit 1
        sync_outputs
        ;;
    "logs")
        check_ssh_connection || exit 1
        show_logs "${2:-}"
        ;;
    "full-deploy")
        check_ssh_connection || exit 1
        deploy_project
        setup_remote_environment
        start_remote_services
        ;;
    "help"|*)
        echo "DriftingMe Remote Deployment Tool"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  deploy        Deploy project files to remote host"
        echo "  start         Start services on remote host"
        echo "  stop          Stop services on remote host"
        echo "  status        Check service status on remote host"
        echo "  generate      Run noir generator remotely [scene_type]"
        echo "  sync          Sync outputs from remote to local"
        echo "  logs          Show service logs [service_name]"
        echo "  full-deploy   Complete deployment (deploy + setup + start)"
        echo "  help          Show this help message"
        echo ""
        echo "Environment Variables:"
        echo "  REMOTE_HOST         Remote SSH host (default: user@remote-server.com)"
        echo "  REMOTE_PROJECT_DIR  Remote project directory (default: ~/DriftingMe)"
        echo ""
        echo "Examples:"
        echo "  $0 full-deploy                    # Complete setup"
        echo "  $0 generate femme_fatale          # Generate noir scene"
        echo "  $0 logs a1111                     # Show A1111 logs"
        ;;
esac