#!/bin/bash

echo "🎬 Starting DriftingMe - Automatic1111 WebUI"
echo "📍 Noir preset settings available in docs/noir_preset_guide.md"

# Start the WebUI with the original arguments
bash -lc "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 ./webui.sh ${CLI_ARGS}"