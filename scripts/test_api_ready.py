#!/usr/bin/env python3
"""
Simple script to test if A1111 API is ready and generate a quick test image
"""

import time
import sys
import os
import logging

# Load config if available
try:
    from config import get_config
    from comfyui_api import generate_image, check_server_status
    DEFAULT_URL = get_config('COMFYUI_URL')
except ImportError:
    DEFAULT_URL = os.environ.get('COMFYUI_URL', 'http://localhost:8188')

def wait_for_api(url=None, max_attempts=20):
    if url is None:
        url = DEFAULT_URL
    """Wait for A1111 API to be ready"""
    logger.info(f"🔄 Waiting for A1111 API at {url}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{url}/sdapi/v1/options", timeout=5)
            if response.status_code == 200:
                logger.info("✅ A1111 API is ready!")
                return True
        except TimeoutError:
            pass
        except ConnectionError:
            pass
        except Exception:
            pass
        except Exception as e:
            logger.info(f"⚠️  Unexpected error: {e}")
        
        logger.info(f"⏳ Attempt {attempt + 1}/{max_attempts} - waiting 15s...")
        time.sleep(15)
    
    logger.info(f"❌ A1111 API not ready after {max_attempts * 15} seconds")
    return False

def test_generation(url=None):
    if url is None:
        url = DEFAULT_URL
    """Test a simple image generation"""
    logger.info("🎬 Testing simple image generation...")
    
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
            logger.info("✅ Test generation successful!")
            return True
        else:
            logger.info(f"❌ Generation failed with status {response.status_code}")
            logger.info(f"Response: {response.text}")
            return False
    except TimeoutError:
        logger.info("❌ Generation timed out")
        return False
    except ConnectionError as e:
        logger.info(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        logger.info(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        logger.info(f"❌ Generation failed: {e}")
        return False

if __name__ == "__main__":
    if wait_for_api():
        if test_generation():
            logger.info("🎉 A1111 is ready for noir generation!")
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)