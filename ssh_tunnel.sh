#!/bin/bash
set -euo pipefail

# SSH Tunnel Script for DriftingMe Remote Access
# Creates SSH tunnels to access remote web interfaces locally

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        
        # Validate key format (alphanumeric and underscore only)
        if [[ ! "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]]; then
            echo "WARNING: Invalid env var name: $key" >&2
            continue
        fi
        
        # Remove quotes and export safely
        value="${value%\"}"
        value="${value#\"}"
        export "$key=$value"
    done < .env
fi

REMOTE_HOST="${REMOTE_HOST:-user@remote-server.com}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚇 Setting up SSH tunnels to $REMOTE_HOST${NC}"

# Function to check if port is already in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $port is already in use${NC}"
        return 1
    fi
    return 0
}

# Function to create tunnel
create_tunnel() {
    local local_port=$1
    local remote_port=$2
    local service_name=$3
    local max_attempts=5
    
    if ! check_port $local_port; then
        echo -e "${YELLOW}⏭️  Skipping $service_name tunnel (port $local_port already in use)${NC}"
        return 1
    fi
    
    echo -e "${GREEN}🔗 Creating tunnel for $service_name: localhost:$local_port -> $REMOTE_HOST:$remote_port${NC}"
    
    # Start tunnel in background
    ssh -N -L "$local_port:localhost:$remote_port" "$REMOTE_HOST" &
    local pid=$!
    echo "$pid" > "/tmp/driftingme_tunnel_${service_name}.pid"
    
    # Verify tunnel established
    for i in $(seq 1 $max_attempts); do
        sleep 2
        if kill -0 "$pid" 2>/dev/null && command -v nc >/dev/null 2>&1 && nc -z localhost "$local_port" 2>/dev/null; then
            echo -e "${GREEN}✅ $service_name tunnel verified${NC}"
            return 0
        fi
    done
    
    # Cleanup failed tunnel
    if kill -0 "$pid" 2>/dev/null; then
        kill "$pid" 2>/dev/null || true
    fi
    rm -f "/tmp/driftingme_tunnel_${service_name}.pid"
    echo -e "${RED}❌ $service_name tunnel failed to establish${NC}"
    return 1
}

# Function to stop tunnels
stop_tunnels() {
    echo -e "${BLUE}🛑 Stopping SSH tunnels...${NC}"
    for service in comfyui; do
        pidfile="/tmp/driftingme_tunnel_${service}.pid"
        if [ -f "$pidfile" ]; then
            pid=$(cat "$pidfile")
            if ps -p $pid > /dev/null 2>&1; then
                kill $pid
                echo -e "${GREEN}✅ Stopped $service tunnel (PID: $pid)${NC}"
            fi
            rm -f "$pidfile"
        fi
    done
}

# Function to show tunnel status
show_status() {
    echo -e "${BLUE}📊 Tunnel Status:${NC}"
    for service in comfyui; do
        pidfile="/tmp/driftingme_tunnel_${service}.pid"
        if [ -f "$pidfile" ]; then
            pid=$(cat "$pidfile")
            if ps -p $pid > /dev/null 2>&1; then
                case $service in
                    "comfyui")
                        echo -e "${GREEN}✅ ComfyUI: http://localhost:8188 (PID: $pid)${NC}"
                        ;;
                esac
                esac
            else
                echo -e "${YELLOW}❌ $service tunnel not running${NC}"
                rm -f "$pidfile"
            fi
        else
            echo -e "${YELLOW}❌ $service tunnel not active${NC}"
        fi
    done
}

# Main script logic
case "${1:-start}" in
    "start")
        # Set trap to cleanup on script exit
        trap stop_tunnels EXIT INT TERM
        
        # Create tunnels
        create_tunnel 7860 7860 "a1111"
        create_tunnel 8188 8188 "comfyui"
        
        echo ""
        echo -e "${GREEN}🎉 SSH tunnels established!${NC}"
        echo -e "${BLUE}Access your services at:${NC}"
        echo -e "  📱 A1111 WebUI: http://localhost:7860"
        echo -e "  🎨 ComfyUI: http://localhost:8188"
        echo ""
        echo -e "${YELLOW}💡 Press Ctrl+C to stop tunnels${NC}"
        
        # Keep script running
        wait
        ;;
    "stop")
        stop_tunnels
        ;;
    "status")
        show_status
        ;;
    "help"|*)
        echo "SSH Tunnel Manager for DriftingMe"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  start    Create SSH tunnels (default)"
        echo "  stop     Stop all SSH tunnels"
        echo "  status   Show tunnel status"
        echo "  help     Show this help message"
        echo ""
        echo "Environment Variables:"
        echo "  REMOTE_HOST  Remote SSH host (default: user@remote-server.com)"
        ;;
esac