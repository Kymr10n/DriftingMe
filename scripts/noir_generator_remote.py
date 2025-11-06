#!/usr/bin/env python3
"""
DriftingMe Remote Noir Generator
Advanced script for generating noir-style images using A1111 API on remote host.
"""

import requests
import json
import base64
import os
import argparse
from datetime import datetime
from config import get_config

# Remote API Configuration 
A1111_URL = get_config('A1111_URL')

# Noir presets based on the guide
NOIR_SCENES = {
    "detective": {
        "prompt": """A mysterious detective in a classic fedora and dark trench coat, standing in the shadows of a rain-soaked city street. Dramatic lighting from a single street lamp creates harsh shadows across his face. Film noir cinematography, black and white, high contrast, 1940s aesthetic, moody atmosphere, urban decay, mystery and intrigue.""",
        "aspect": "portrait"
    },
    "alley": {
        "prompt": """Dark narrow alley between tall buildings, wet cobblestones reflecting neon signs, deep shadows, single light source creating dramatic contrast. Film noir setting, black and white, atmospheric fog, urban decay, mysterious atmosphere, cinematic composition.""",
        "aspect": "landscape"
    },
    "femme_fatale": {
        "prompt": """Elegant woman in 1940s attire, dramatic lighting casting shadows across her face, cigarette smoke curling in the air, mysterious expression. Classic film noir portrait, black and white, high contrast, dramatic shadows, vintage Hollywood glamour, dangerous beauty.""",
        "aspect": "portrait"
    },
    "nightclub": {
        "prompt": """Smoky jazz club interior, dim lighting, silhouettes of patrons, neon signs casting colored light through smoke. Film noir atmosphere, black and white with selective color, 1940s nightclub, mysterious ambiance, dramatic shadows.""",
        "aspect": "landscape"
    },
    "car_chase": {
        "prompt": """High-speed car chase through rain-soaked city streets at night, headlights cutting through darkness, reflections on wet asphalt. Film noir action scene, black and white, dramatic motion blur, urban setting, 1940s automobiles.""",
        "aspect": "landscape"
    }
}

# Optimized settings for noir generation
NOIR_SETTINGS = {
    "steps": 30,
    "cfg_scale": 7.5,
    "sampler_name": "DPM++ 2M Karras",
    "scheduler": "karras",
    "denoising_strength": 0.75,
    "restore_faces": True,
    "tiling": False,
    "do_not_save_samples": False,
    "do_not_save_grid": False,
    "enable_hr": True,
    "hr_scale": 1.5,
    "hr_upscaler": "R-ESRGAN 4x+",
    "hr_second_pass_steps": 15,
    "hr_denoising_strength": 0.4
}

# Negative prompt optimized for noir
NOIR_NEGATIVE = """cartoon, anime, 3d render, painting, drawing, illustration, bright colors, colorful, cheerful, happy, modern, contemporary, digital art, low quality, blurry, distorted, deformed, bad anatomy, bad hands, extra fingers, missing fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed face, ugly, bad proportions, extra limbs, extra arms, extra legs, disfigured, long neck, cross-eyed"""

def get_aspect_dimensions(aspect, base_size=1024):
    """Get width and height based on aspect ratio"""
    if aspect == "portrait":
        return base_size, int(base_size * 1.3)  # 4:5 ratio
    elif aspect == "landscape":
        return int(base_size * 1.3), base_size  # 5:4 ratio
    else:  # square
        return base_size, base_size

def wait_for_api_ready(max_attempts=30, delay=10):
    """Wait for the A1111 API to be ready"""
    import time
    
    print(f"🔄 Waiting for A1111 API at {A1111_URL}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{A1111_URL}/sdapi/v1/options", timeout=5)
            if response.status_code == 200:
                print("✅ A1111 API is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"⏳ Attempt {attempt + 1}/{max_attempts} - waiting {delay}s...")
        time.sleep(delay)
    
    print(f"❌ A1111 API not ready after {max_attempts * delay} seconds")
    return False

def generate_noir_image(scene_type="detective", seed=-1, custom_prompt=None):
    """Generate a noir-style image"""
    
    if not wait_for_api_ready():
        return None
    
    # Get scene configuration
    if scene_type in NOIR_SCENES:
        scene_config = NOIR_SCENES[scene_type]
        prompt = custom_prompt or scene_config["prompt"]
        width, height = get_aspect_dimensions(scene_config["aspect"])
        scene_name = scene_type
    else:
        # Custom scene
        prompt = custom_prompt or scene_type
        width, height = get_aspect_dimensions("portrait")  # Default to portrait
        scene_name = scene_type
    
    # Create payload
    payload = {
        "prompt": prompt,
        "negative_prompt": NOIR_NEGATIVE,
        "width": width,
        "height": height,
        "seed": seed,
        **NOIR_SETTINGS
    }
    
    print(f"🎬 Generating noir scene: {scene_name}")
    print(f"📐 Dimensions: {width}x{height}")
    print(f"🎯 Seed: {seed if seed != -1 else 'random'}")
    
    try:
        response = requests.post(f"{A1111_URL}/sdapi/v1/txt2img", json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            
            # Save the image
            if result['images']:
                # Decode base64 image
                image_data = base64.b64decode(result['images'][0])
                
                # Create filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"noir_{scene_name}_{timestamp}.png"
                filepath = os.path.join("outputs", filename)
                
                # Ensure outputs directory exists
                os.makedirs("outputs", exist_ok=True)
                
                # Save image
                with open(filepath, "wb") as f:
                    f.write(image_data)
                
                print(f"✅ Image saved: {filepath}")
                
                # Save generation info
                info_file = filepath.replace('.png', '_info.json')
                generation_info = {
                    "scene_type": scene_name,
                    "prompt": prompt,
                    "negative_prompt": NOIR_NEGATIVE,
                    "settings": NOIR_SETTINGS,
                    "dimensions": {"width": width, "height": height},
                    "seed": result.get('parameters', {}).get('seed', seed),
                    "timestamp": timestamp,
                    "api_url": A1111_URL
                }
                
                with open(info_file, 'w') as f:
                    json.dump(generation_info, f, indent=2)
                
                print(f"📄 Generation info saved: {info_file}")
                return filepath
            else:
                print("❌ No images returned from API")
                return None
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The image generation might be taking longer than expected.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate noir-style images using A1111 API")
    parser.add_argument("--scene", "-s", 
                       choices=list(NOIR_SCENES.keys()) + ["custom"],
                       default="detective",
                       help="Noir scene type to generate")
    parser.add_argument("--prompt", "-p",
                       help="Custom prompt (use with --scene custom)")
    parser.add_argument("--seed", "-seed",
                       type=int, default=-1,
                       help="Seed for reproducible generation (-1 for random)")
    parser.add_argument("--api-url", "-u",
                       default="http://localhost:7860",
                       help="A1111 API URL")
    parser.add_argument("--list-scenes", "-l",
                       action="store_true",
                       help="List available scene types")
    
    args = parser.parse_args()
    
    # Update API URL from argument or environment
    global A1111_URL
    A1111_URL = os.environ.get('A1111_URL', args.api_url)
    
    if args.list_scenes:
        print("Available noir scenes:")
        for scene, config in NOIR_SCENES.items():
            print(f"  {scene}: {config['aspect']} aspect")
        return
    
    if args.scene == "custom" and not args.prompt:
        print("❌ Custom scene requires --prompt argument")
        return
    
    # Generate the image
    scene_input = args.prompt if args.scene == "custom" else args.scene
    result = generate_noir_image(scene_input, args.seed, args.prompt if args.scene != "custom" else None)
    
    if result:
        print(f"🎉 Generation completed successfully!")
        print(f"📁 File: {result}")
    else:
        print("💀 Generation failed")

if __name__ == "__main__":
    main()