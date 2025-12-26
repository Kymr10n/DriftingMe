#!/usr/bin/env python3
"""
Environment configuration loader for DriftingMe scripts
"""

import os
import re
import logging
from pathlib import Path
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
MODEL_DIR = PROJECT_ROOT / "models"

# Allowed environment variables for security
ALLOWED_ENV_VARS = {
    'A1111_URL', 'COMFYUI_URL', 'REMOTE_HOST', 
    'REMOTE_PROJECT_DIR', 'LOG_LEVEL'
}

# Default configuration
DEFAULTS = {
    'A1111_URL': 'http://localhost:7860',
    'COMFYUI_URL': 'http://localhost:8188',
    'REMOTE_HOST': 'user@remote-server.com',
    'REMOTE_PROJECT_DIR': '~/DriftingMe'
}

def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return False
        if not parsed.netloc:
            return False
        # Prevent injection
        if any(char in url for char in ['`', '$', ';', '|', '&', '\n', '\r']):
            return False
        return True
    except Exception:
        return False

def validate_env_value(key: str, value: str) -> str:
    """Validate environment variable value"""
    if key.endswith('_URL'):
        if not validate_url(value):
            raise ValueError(f"Invalid URL format for {key}: {value}")
    elif key == 'REMOTE_HOST':
        # Validate SSH host format (user@host or just host)
        if not re.match(r'^([\w\.-]+@)?[\w\.-]+$', value):
            raise ValueError(f"Invalid host format for {key}: {value}")
    
    # Prevent command injection
    if any(char in value for char in ['`', '$', ';', '&', '\n', '\r']):
        raise ValueError(f"Invalid characters in {key}")
    
    return value

def load_env():
    """Securely load environment variables from .env file"""
    env_file = PROJECT_ROOT / '.env'
    
    if not env_file.exists():
        logger.debug(".env file not found, using defaults")
        return
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Check for = separator
                if '=' not in line:
                    logger.warning(f"Invalid line {line_num} in .env: missing '='")
                    continue
                
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                # Only allow whitelisted variables
                if key not in ALLOWED_ENV_VARS:
                    logger.warning(f"Unknown env var '{key}' in .env, ignoring")
                    continue
                
                # Validate value
                try:
                    value = validate_env_value(key, value)
                    os.environ[key] = value
                    logger.debug(f"Loaded env var: {key}")
                except ValueError as e:
                    logger.error(f"Invalid env var {key}: {e}")
                    raise
                    
    except Exception as e:
        logger.critical(f"Failed to load .env: {e}")
        raise

def get_config(key: str, default=None) -> str:
    """Get configuration value with fallback to defaults"""
    return os.environ.get(key, default or DEFAULTS.get(key))

def get_output_path(filename: str) -> Path:
    """Get validated output path, preventing path traversal"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / filename
    
    # Prevent path traversal attacks
    try:
        filepath.resolve().relative_to(OUTPUT_DIR.resolve())
    except ValueError:
        raise ValueError(f"Invalid output path: {filename}")
    
    return filepath

def validate_configuration():
    """Validate all configuration at startup"""
    errors = []
    
    # Validate URLs
    for url_var in ['COMFYUI_URL']:
        url = get_config(url_var)
        if not validate_url(url):
            errors.append(f"{url_var} has invalid URL: {url}")
    
    # Validate directories exist/can be created
    for directory in [OUTPUT_DIR, MODEL_DIR]:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create directory {directory}: {e}")
    
    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join(errors))

# Auto-load when module is imported
load_env()

# Validate configuration
try:
    validate_configuration()
except ValueError as e:
    logger.error(f"Configuration validation failed: {e}")
    # Don't raise - allow scripts to run with defaults