#!/bin/bash

# Create presets directory with proper permissions
mkdir -p /opt/webui/presets
chmod 755 /opt/webui/presets

# Copy noir preset to WebUI presets directory if it exists
if [ -f "/opt/webui/config/noir_preset.json" ]; then
    cp /opt/webui/config/noir_preset.json /opt/webui/presets/ 2>/dev/null || echo "Note: Could not copy preset (permission issue)"
    if [ -f "/opt/webui/presets/noir_preset.json" ]; then
        echo "✅ Copied noir_preset.json to WebUI presets directory"
    else
        echo "ℹ️  noir_preset.json available in /opt/webui/config/ directory"
    fi
else
    echo "ℹ️  No noir_preset.json found in config directory"
fi

# Start the WebUI with the original arguments
bash -lc "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 ./webui.sh ${CLI_ARGS}"