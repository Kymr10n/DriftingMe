#!/usr/bin/env python3
"""
DriftingMe API Test Script
Demonstrates programmatic access to both ComfyUI API for noir image generation.
"""

import os
import logging
from datetime import datetime
from config import get_config
from comfyui_api import generate_image, check_server_status

# API endpoints
COMFYUI_URL = get_config('COMFYUI_URL')
COMFYUI_URL = get_config('COMFYUI_URL')

# Noir-style prompt based on the preset guide
NOIR_PROMPT = """
A dramatic black and white noir scene featuring a detective in a fedora and trench coat, 
standing under a flickering street lamp in a rain-soaked alley. Deep shadows, harsh lighting, 
cinematic composition, 1940s film noir aesthetic, high contrast, moody atmosphere, 
dramatic silhouettes, urban setting, mystery and intrigue.
"""

NEGATIVE_PROMPT = """
color, bright colors, cheerful, sunny, daylight, happy, cartoonish, anime, 
low quality, blurry, distorted
"""

def test_a1111_api():
    """Test A1111 txt2img API with noir parameters"""
    logger.info("🎬 Testing A1111 API...")
    
    payload = {
        "prompt": NOIR_PROMPT,
        "negative_prompt": NEGATIVE_PROMPT,
        "steps": 20,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 768,  # Portrait aspect for classic noir
        "sampler_name": "DPM++ 2M Karras",
        "seed": -1,
        "save_images": True
    }
    
    try:
        logger.info("📡 Sending request to A1111...")
        response = requests.post(f"{COMFYUI_URL}/sdapi/v1/txt2img", json=payload, timeout=60)
        
        if images:
            logger.info("✅ A1111 API successful!")
            logger.info(f"Generated {len(result['images'])} image(s)")
            
            # Save the first image
            if result['images']:
                image_data = base64.b64decode(result['images'][0])
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"noir_a1111_{timestamp}.png"
                filepath = os.path.join("outputs", filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                logger.info(f"💾 Image saved: {filename}")
                
            # Generation complete
            logger.info(f"🎯 Seed: {info['seed']}")
            logger.info(f"⚙️  Model: {info['sd_model_name']}")
            logger.info(f"🔧 Sampler: {info['sampler_name']}")
            
            return True
        else:
            logger.info(f"❌ A1111 API failed: {response.status_code}")
            logger.info(response.text)
            return False
            
    except TimeoutError:
        logger.info(f"❌ A1111 API timeout")
        return False
    except ConnectionError as e:
        logger.info(f"❌ A1111 API connection error: {e}")
        return False
    except Exception as e:
        logger.info(f"❌ A1111 API request error: {e}")
        return False
    except Exception as e:
        logger.info(f"❌ A1111 API error: {e}")
        return False

def test_comfyui_api():
    """Test ComfyUI API system status"""
    logger.info("\n🎨 Testing ComfyUI API...")
    
    try:
        # Test system stats
        response = requests.get(f"{COMFYUI_URL}/system_stats")
        
        if response.status_code == 200:
            stats = response.json()
            logger.info("✅ ComfyUI API accessible!")
            logger.info(f"🖥️  ComfyUI Version: {stats['system']['comfyui_version']}")
            logger.info(f"🐍 Python: {stats['system']['python_version']}")
            logger.info(f"🔥 PyTorch: {stats['system']['pytorch_version']}")
            
            # GPU info
            if stats['devices']:
                gpu = stats['devices'][0]
                vram_total_gb = gpu['vram_total'] / (1024**3)
                vram_free_gb = gpu['vram_free'] / (1024**3)
                logger.info(f"🎮 GPU: {gpu['name']}")
                logger.info(f"💾 VRAM: {vram_free_gb:.1f}GB free / {vram_total_gb:.1f}GB total")
            
            return True
        else:
            logger.info(f"❌ ComfyUI API failed: {response.status_code}")
            return False
            
    except TimeoutError:
        logger.info(f"❌ ComfyUI API timeout")
        return False
    except ConnectionError as e:
        logger.info(f"❌ ComfyUI API connection error: {e}")
        return False
    except Exception as e:
        logger.info(f"❌ ComfyUI API request error: {e}")
        return False
    except Exception as e:
        logger.info(f"❌ ComfyUI API error: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🎬 DriftingMe API Test Suite")
    logger.info("=" * 50)
    
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)
    
    # Test both APIs
    a1111_success = test_a1111_api()
    comfyui_success = test_comfyui_api()
    
    logger.info("\n" + "=" * 50)
    logger.info("📊 Test Results:")
    logger.info(f"🎯 A1111 API: {'✅ Working' if a1111_success else '❌ Failed'}")
    logger.info(f"🎨 ComfyUI API: {'✅ Working' if comfyui_success else '❌ Failed'}")
    
    if a1111_success and comfyui_success:
        logger.info("\n🎉 Both APIs are ready for noir image generation!")
        logger.info("📍 Next steps:")
        logger.info("   - Create workflow scripts for automated generation")
        logger.info("   - Implement ComfyUI workflows for advanced processing")
        logger.info("   - Build batch processing for episode content")
    else:
        logger.info("\n⚠️  Some APIs need attention before proceeding")

if __name__ == "__main__":
    main()