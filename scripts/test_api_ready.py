#!/usr/bin/env python3
"""
Simple script to test if A1111 API is ready and generate a quick test image
"""

import requests
import time
import sys
import os

# Load config if available
try:
    from config import get_config
    DEFAULT_URL = get_config('A1111_URL')
except ImportError:
    DEFAULT_URL = os.environ.get('A1111_URL', 'http://localhost:7860')

def wait_for_api(url=None, max_attempts=20):
    if url is None:
        url = DEFAULT_URL
    """Wait for A1111 API to be ready"""
    print(f"🔄 Waiting for A1111 API at {url}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{url}/sdapi/v1/options", timeout=5)
            if response.status_code == 200:
                print("✅ A1111 API is ready!")
                return True
        except Exception as e:
            pass
        
        print(f"⏳ Attempt {attempt + 1}/{max_attempts} - waiting 15s...")
        time.sleep(15)
    
    print(f"❌ A1111 API not ready after {max_attempts * 15} seconds")
    return False

def test_generation(url=None):
    if url is None:
        url = DEFAULT_URL
    """Test a simple image generation"""
    print("🎬 Testing simple image generation...")
    
    payload = {
        "prompt": "a simple test image, black and white",
        "negative_prompt": "color, colorful",
        "width": 512,
        "height": 512,
        "steps": 10,
        "cfg_scale": 7,
        "sampler_name": "Euler a",
    }
    
    try:
        response = requests.post(f"{url}/sdapi/v1/txt2img", json=payload, timeout=60)
        if response.status_code == 200:
            print("✅ Test generation successful!")
            return True
        else:
            print(f"❌ Generation failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False

if __name__ == "__main__":
    if wait_for_api():
        if test_generation():
            print("🎉 A1111 is ready for noir generation!")
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)