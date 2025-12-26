#!/bin/bash
set -euo pipefail

echo "🎬 Starting DriftingMe - Automatic1111 WebUI"
echo "📍 Noir preset settings available in docs/noir_preset_guide.md"

# Validate environment
if [ -z "${CLI_ARGS:-}" ]; then
    echo "ERROR: CLI_ARGS not set" >&2
    exit 1
fi

# Check CUDA availability (warning only, not fatal)
if ! nvidia-smi &>/dev/null; then
    echo "WARNING: NVIDIA GPU not detected" >&2
fi

# Start the WebUI with the original arguments
if ! bash -lc "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 ./webui.sh ${CLI_ARGS}"; then
    echo "ERROR: WebUI failed to start" >&2
    exit 1
fi