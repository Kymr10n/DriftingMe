#!/usr/bin/env python3
"""
DriftingMe Scene 1 Generator - "The Awakening"
Specialized script for generating noir comic book panels based on the opening scene.
"""

import requests
import json
import base64
from datetime import datetime
import os

# API Configuration
A1111_URL = "http://localhost:7860"
COMFYUI_URL = "http://localhost:8188"

# Scene 1 Prompts based on the script
SCENE_1_PROMPTS = {
    "awakening_medium_shot": {
        "prompt": """
        noir comic book style, black and white illustration, high contrast chiaroscuro lighting,
        medium shot of a man jolting awake in bed, woman sleeping beside him partially visible,
        venetian blind shadows casting hard geometric patterns across the scene,
        dim bedroom before dawn, soft blue-gray light filtering through rain-streaked windows,
        cross-hatching technique, film grain texture, gritty ink rendering,
        dramatic shadows like prison bars across his face, disorientation and unease,
        classic noir atmosphere, introspective mood, heavy contrast between black and white
        """,
        "negative": "color, bright lighting, cheerful, clean lines, cartoon, anime, soft shadows, daylight",
        "style_note": "Medium shot - man in bed, woman half-seen, venetian blind shadows"
    },
    
    "close_up_eyes": {
        "prompt": """
        noir comic book style, extreme close-up of a man's eyes wide awake in the darkness,
        black and white illustration, high contrast lighting, cross-hatched shading,
        fear and confusion in his expression, venetian blind shadows across his face,
        gritty ink rendering, film noir atmosphere, dramatic chiaroscuro,
        heavy shadows, introspective and tense mood
        """,
        "negative": "color, bright lighting, cartoon, anime, soft shadows, cheerful expression",
        "style_note": "Close-up - eyes reflecting confusion and disorientation"
    },
    
    "room_overview": {
        "prompt": """
        noir comic book style, wide shot of unfamiliar bedroom interior before dawn,
        black and white illustration, venetian blind shadows creating geometric patterns,
        rain-streaked windows with soft blue-gray light filtering through,
        rumpled bed sheets, mysterious atmosphere, cross-hatching technique,
        film grain texture, gritty ink rendering, heavy contrast,
        noir cinematography style, moody and atmospheric
        """,
        "negative": "color, bright lighting, clean modern room, daylight, cartoon style",
        "style_note": "Establishing shot - unfamiliar room setting the noir mood"
    },
    
    "shadow_bars": {
        "prompt": """
        noir comic book style, dramatic shot of venetian blind shadows creating prison bar effect,
        black and white illustration, man's silhouette behind geometric shadow patterns,
        high contrast chiaroscuro lighting, cross-hatching shading technique,
        metaphorical prison bars of light and shadow, gritty ink rendering,
        film noir atmosphere, psychological tension, heavy dramatic contrast
        """,
        "negative": "color, soft lighting, clean lines, bright atmosphere, cartoon style",
        "style_note": "Symbolic shot - shadows as metaphorical prison bars"
    }
}

# Generation parameters optimized for noir style
GENERATION_PARAMS = {
    "width": 768,
    "height": 1024,  # Portrait orientation for comic panels
    "steps": 30,
    "cfg_scale": 8.5,
    "sampler_name": "Euler",
    "scheduler": "normal",
    "seed": -1,  # Random seed for variation
    "batch_size": 1,
    "n_iter": 2,  # Generate 2 variations per prompt
}

def generate_scene_1_panel(prompt_key, custom_seed=None):
    """Generate a specific panel for Scene 1"""
    if prompt_key not in SCENE_1_PROMPTS:
        print(f"Unknown prompt key: {prompt_key}")
        return False
    
    scene_data = SCENE_1_PROMPTS[prompt_key]
    
    # Prepare payload
    payload = {
        **GENERATION_PARAMS,
        "prompt": scene_data["prompt"],
        "negative_prompt": scene_data["negative"],
    }
    
    if custom_seed:
        payload["seed"] = custom_seed
    
    print(f"\n🎬 Generating Scene 1 Panel: {prompt_key}")
    print(f"📝 Style Note: {scene_data['style_note']}")
    print(f"🎯 Prompt: {scene_data['prompt'][:100]}...")
    
    try:
        response = requests.post(f"{A1111_URL}/sdapi/v1/txt2img", json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            
            # Save generated images
            for i, image_data in enumerate(result['images']):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scene1_{prompt_key}_{timestamp}_v{i+1}.png"
                filepath = os.path.join("/home/alex/Projects/DriftingMe/outputs", filename)
                
                # Decode and save
                image_bytes = base64.b64decode(image_data)
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
                
                file_size = len(image_bytes) / 1024
                print(f"✅ Saved: {filename} ({file_size:.1f}KB)")
            
            # Print generation info
            info = json.loads(result['info'])
            print(f"🔧 Model: {info.get('sd_model_name', 'Unknown')}")
            print(f"⚙️  Seed: {info.get('seed', 'Unknown')}")
            print(f"⏱️  Time: ~{info.get('job_timestamp', 'Unknown')}")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False

def generate_complete_scene_1():
    """Generate all panels for Scene 1 - The Awakening"""
    print("🎭 DRIFTINGME - Scene 1: The Awakening")
    print("=" * 50)
    
    success_count = 0
    total_panels = len(SCENE_1_PROMPTS)
    
    for prompt_key in SCENE_1_PROMPTS.keys():
        if generate_scene_1_panel(prompt_key):
            success_count += 1
        print("-" * 30)
    
    print(f"\n📊 Scene 1 Generation Complete:")
    print(f"✅ Successfully generated: {success_count}/{total_panels} panels")
    
    if success_count == total_panels:
        print("🎉 All Scene 1 panels generated successfully!")
    else:
        print("⚠️  Some panels failed to generate. Check API status.")

def main():
    import sys
    
    if len(sys.argv) > 1:
        panel_name = sys.argv[1]
        if panel_name == "all":
            generate_complete_scene_1()
        else:
            generate_scene_1_panel(panel_name)
    else:
        print("🎭 DriftingMe Scene 1 Generator")
        print("\nAvailable panels:")
        for key, data in SCENE_1_PROMPTS.items():
            print(f"  • {key}: {data['style_note']}")
        print(f"\nUsage:")
        print(f"  python3 {sys.argv[0]} <panel_name>")
        print(f"  python3 {sys.argv[0]} all")

if __name__ == "__main__":
    main()