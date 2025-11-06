#!/usr/bin/env python3
"""
Environment configuration loader for DriftingMe scripts
"""

import os
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent.parent / '.env'
    
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key] = value

# Auto-load when module is imported
load_env()

# Default configuration
DEFAULTS = {
    'A1111_URL': 'http://localhost:7860',
    'COMFYUI_URL': 'http://localhost:8188',
    'REMOTE_HOST': 'user@remote-server.com',
    'REMOTE_PROJECT_DIR': '~/DriftingMe'
}

def get_config(key, default=None):
    """Get configuration value with fallback to defaults"""
    return os.environ.get(key, default or DEFAULTS.get(key))