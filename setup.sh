#!/bin/bash
set -euo pipefail

# DriftingMe Setup Script
# This script sets up the correct permissions for Docker volume mounts

echo "Setting up DriftingMe environment..."

# Validate we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "ERROR: Must run from project root directory" >&2
    exit 1
fi

# Create directories if they don't exist
for dir in outputs models config art; do
    mkdir -p "$dir"
done

# Check if we actually need sudo
need_sudo=false
for dir in outputs models config art; do
    if [ ! -w "$dir" ]; then
        need_sudo=true
        break
    fi
done

if [ "$need_sudo" = false ]; then
    echo "✅ Directories already writable, no sudo needed"
else
    echo "🔒 Setting permissions (requires sudo)..."
    sudo chown -R "$(whoami):$(whoami)" outputs/ models/ config/ art/
fi

# Set permissions for current user
chmod -R 755 outputs/ models/ config/ art/

echo "✅ Permissions set successfully!"
echo "You can now run: docker compose up -d"