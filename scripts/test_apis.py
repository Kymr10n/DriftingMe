#!/usr/bin/env python3
"""
DriftingMe API Test Script
Demonstrates programmatic access to both A1111 and ComfyUI APIs for noir image generation.
"""

import requests
import json
import base64
import os
from datetime import datetime

# API endpoints
A1111_URL = "http://localhost:7860"
COMFYUI_URL = "http://localhost:8188"

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
    print("🎬 Testing A1111 API...")
    
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
        print("📡 Sending request to A1111...")
        response = requests.post(f"{A1111_URL}/sdapi/v1/txt2img", json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ A1111 API successful!")
            print(f"Generated {len(result['images'])} image(s)")
            
            # Save the first image
            if result['images']:
                image_data = base64.b64decode(result['images'][0])
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"noir_a1111_{timestamp}.png"
                filepath = f"/home/alex/Projects/DriftingMe/outputs/{filename}"
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                print(f"💾 Image saved: {filename}")
                
            # Print generation info
            info = json.loads(result['info'])
            print(f"🎯 Seed: {info['seed']}")
            print(f"⚙️  Model: {info['sd_model_name']}")
            print(f"🔧 Sampler: {info['sampler_name']}")
            
            return True
        else:
            print(f"❌ A1111 API failed: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ A1111 API error: {e}")
        return False

def test_comfyui_api():
    """Test ComfyUI API system status"""
    print("\n🎨 Testing ComfyUI API...")
    
    try:
        # Test system stats
        response = requests.get(f"{COMFYUI_URL}/system_stats")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ ComfyUI API accessible!")
            print(f"🖥️  ComfyUI Version: {stats['system']['comfyui_version']}")
            print(f"🐍 Python: {stats['system']['python_version']}")
            print(f"🔥 PyTorch: {stats['system']['pytorch_version']}")
            
            # GPU info
            if stats['devices']:
                gpu = stats['devices'][0]
                vram_total_gb = gpu['vram_total'] / (1024**3)
                vram_free_gb = gpu['vram_free'] / (1024**3)
                print(f"🎮 GPU: {gpu['name']}")
                print(f"💾 VRAM: {vram_free_gb:.1f}GB free / {vram_total_gb:.1f}GB total")
            
            return True
        else:
            print(f"❌ ComfyUI API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ComfyUI API error: {e}")
        return False

def main():
    """Main test function"""
    print("🎬 DriftingMe API Test Suite")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs("/home/alex/Projects/DriftingMe/outputs", exist_ok=True)
    
    # Test both APIs
    a1111_success = test_a1111_api()
    comfyui_success = test_comfyui_api()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"🎯 A1111 API: {'✅ Working' if a1111_success else '❌ Failed'}")
    print(f"🎨 ComfyUI API: {'✅ Working' if comfyui_success else '❌ Failed'}")
    
    if a1111_success and comfyui_success:
        print("\n🎉 Both APIs are ready for noir image generation!")
        print("📍 Next steps:")
        print("   - Create workflow scripts for automated generation")
        print("   - Implement ComfyUI workflows for advanced processing")
        print("   - Build batch processing for episode content")
    else:
        print("\n⚠️  Some APIs need attention before proceeding")

if __name__ == "__main__":
    main()