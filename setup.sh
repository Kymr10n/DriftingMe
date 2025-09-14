#!/bin/bash

# DriftingMe Setup Script
# This script sets up the correct permissions for Docker volume mounts

echo "Setting up DriftingMe environment..."

# Create directories if they don't exist
mkdir -p outputs models config art

# Set correct ownership and permissions for volume mounts
echo "Setting permissions for volume directories..."
sudo chown -R $(whoami):$(whoami) outputs/ models/ config/ art/
chmod -R 755 outputs/ models/ config/ art/

echo "✅ Permissions set successfully!"
echo "You can now run: docker compose up -d"