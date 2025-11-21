#!/usr/bin/env python3
"""
DriftingMe Noir Generator
Advanced script for generating noir-style images using A1111 API with optimized settings.
"""

import requests
import json
import base64
import os
import argparse
from datetime import datetime
from config import get_config

# API Configuration
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
    "crime_scene": {
        "prompt": """Police investigation scene in a dimly lit room, evidence scattered on a desk, harsh lighting from a desk lamp, shadows on the wall. Film noir crime scene, black and white, dramatic lighting, 1940s detective story, moody atmosphere, investigative drama.""",
        "aspect": "landscape"
    }
}

NOIR_NEGATIVE = """
color, bright colors, cheerful, sunny, daylight, happy, cartoonish, anime, 
low quality, blurry, distorted, modern, contemporary, digital, neon colors,
rainbow, pastel colors, cute, kawaii, child-like
"""

# Optimized settings for noir generation
NOIR_SETTINGS = {
    "steps": 30,
    "cfg_scale": 8.0,
    "sampler_name": "DPM++ 2M Karras",
    "scheduler": "Karras",
    "restore_faces": False,  # Disabled until face restoration models are loaded
    "enable_hr": False,  # Disabled for now, can enable after testing
    # "hr_scale": 1.5,
    # "hr_upscaler": "R-ESRGAN 4x+",
    # "hr_second_pass_steps": 15,
}

def get_dimensions(aspect_ratio):
    """Get optimal dimensions based on aspect ratio"""
    if aspect_ratio == "portrait":
        return 512, 768
    elif aspect_ratio == "landscape":
        return 768, 512
    else:
        return 512, 512

def generate_noir_image(scene_type, custom_prompt=None, seed=-1, output_dir="outputs"):
    """Generate a noir-style image using A1111 API"""
    
    if scene_type not in NOIR_SCENES and not custom_prompt:
        raise ValueError(f"Unknown scene type: {scene_type}. Available: {list(NOIR_SCENES.keys())}")
    
    # Setup prompt and dimensions
    if custom_prompt:
        prompt = custom_prompt
        width, height = 512, 512
        scene_name = "custom"
    else:
        scene = NOIR_SCENES[scene_type]
        prompt = scene["prompt"]
        width, height = get_dimensions(scene["aspect"])
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
            
            # Save the generated image
            if result['images']:
                image_data = base64.b64decode(result['images'][0])
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"noir_{scene_name}_{timestamp}.png"
                filepath = os.path.join(output_dir, filename)
                
                os.makedirs(output_dir, exist_ok=True)
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                # Print results
                info = json.loads(result['info'])
                print(f"✅ Generation successful!")
                print(f"💾 Saved: {filename}")
                print(f"🎯 Final seed: {info['seed']}")
                print(f"⚙️  Model: {info['sd_model_name']}")
                print(f"⏱️  Steps: {info['steps']}")
                
                return {
                    'success': True,
                    'filename': filename,
                    'filepath': filepath,
                    'seed': info['seed'],
                    'info': info
                }
            else:
                print("❌ No images generated")
                return {'success': False, 'error': 'No images in response'}
                
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(response.text)
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return {'success': False, 'error': str(e)}

def main():
    parser = argparse.ArgumentParser(description="Generate noir-style images")
    parser.add_argument("--scene", choices=list(NOIR_SCENES.keys()), 
                       help="Predefined scene type")
    parser.add_argument("--prompt", type=str, 
                       help="Custom prompt (overrides scene)")
    parser.add_argument("--seed", type=int, default=-1,
                       help="Seed for reproducible generation")
    parser.add_argument("--output", type=str, default="outputs",
                       help="Output directory")
    parser.add_argument("--batch", type=int, default=1,
                       help="Number of images to generate")
    parser.add_argument("--all-scenes", action="store_true",
                       help="Generate all predefined scenes")
    
    args = parser.parse_args()
    
    print("🎬 DriftingMe Noir Generator")
    print("=" * 50)
    
    results = []
    
    if args.all_scenes:
        print("🎯 Generating all noir scenes...")
        for scene_type in NOIR_SCENES.keys():
            for i in range(args.batch):
                print(f"\n📷 Scene {scene_type} ({i+1}/{args.batch})")
                result = generate_noir_image(scene_type, seed=args.seed, 
                                           output_dir=args.output)
                results.append(result)
    
    elif args.scene or args.prompt:
        for i in range(args.batch):
            print(f"\n📷 Generation {i+1}/{args.batch}")
            result = generate_noir_image(args.scene, custom_prompt=args.prompt,
                                       seed=args.seed, output_dir=args.output)
            results.append(result)
    else:
        print("❌ Please specify --scene, --prompt, or --all-scenes")
        return
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n🎯 Generation Summary:")
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"📁 Output directory: {args.output}")
    
    if successful > 0:
        print("\n🎉 Noir images generated successfully!")
        print("💡 Tips:")
        print("   - Use the same seed to reproduce images")
        print("   - Try different scenes for variety")
        print("   - Check the noir preset guide for manual settings")

if __name__ == "__main__":
    main()