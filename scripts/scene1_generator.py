#!/usr/bin/env python3
"""
DriftingMe Scene 1 Generator - "The Awakening"
Specialized script for generating noir comic book panels based on the opening scene.
"""

import logging
from datetime import datetime
from config import get_config, get_output_path
from comfyui_api import generate_image, check_server_status

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# API Configuration
COMFYUI_URL = get_config('COMFYUI_URL')


# Shared style components for consistent visual language
STYLE_PREFIX = """black and white comic book art, clean ink drawing, simple style,"""

STYLE_SUFFIX = """clear image, not abstract, not messy"""

# Shared negative prompt - blocks all unwanted styles
SHARED_NEGATIVE = """photorealistic, photo, 3d, render, painting, watercolor, oil, pastel, soft shading, gradient shading, color, colored,
anime, manga, cartoonish, chibi, exaggerated proportions,
abstract, surreal, incoherent, messy, chaotic lines, sketch, rough sketch, scribble, low contrast,
blurry, out of focus, motion blur, noise, grainy, jpeg artifacts,
text, watermark, logo, signature, speech bubble text,
deformed, disfigured, mutated, bad anatomy, extra limbs, extra fingers, missing fingers, bad hands, bad face,
low detail, unreadable face, faceless, distorted eyes"""


# Scene 1 Panel Specifications
SCENE_1_PROMPTS = {
    "awakening_medium_shot": {
        "panel_spec": """two people in a bed, man sitting up awake, woman lying down sleeping, bedroom interior, bed with blanket and pillows, window with venetian blinds in background, shadow stripes on wall""",
        "style_note": "Medium shot - man in bed, woman half-seen, venetian blind shadows"
    },
    
    "close_up_eyes": {
        "panel_spec": """man's face, eyes wide open, worried expression""",
        "style_note": "Close-up - eyes reflecting confusion and disorientation"
    },
    
    "room_overview": {
        "panel_spec": """bedroom, bed, window, simple furniture""",
        "style_note": "Establishing shot - unfamiliar room setting the noir mood"
    },
    
    "shadow_bars": {
        "panel_spec": """dramatic composition, camera angle from side, man's silhouette profile against wall,
        venetian blind creating strong horizontal shadow bars like prison bars,
        man standing or sitting in shadow, only outline visible, geometric light and shadow pattern dominates,
        symbolic metaphor of imprisonment or being trapped, strong graphic design, minimalist background""",
        "style_note": "Symbolic shot - shadows as metaphorical prison bars"
    }
}

# Generation parameters optimized for clean line-art
GENERATION_PARAMS = {
    "width": 768,
    "height": 1024,  # Portrait orientation for comic panels
    "steps": 25,  # Balanced steps
    "cfg_scale": 6.5,  # Balanced CFG - not too high, not too low
    "sampler_name": "DPM++ 2M",  # Better structure control
    "scheduler": "karras",  # Karras for quality
    "seed": -1,  # Random seed for variation
    "batch_size": 1,
    "n_iter": 2,  # Generate 2 variations per prompt
}

def generate_scene_1_panel(prompt_key, custom_seed=None):
    """Generate a specific panel for Scene 1"""
    if prompt_key not in SCENE_1_PROMPTS:
        logger.error(f"Unknown prompt key: {prompt_key}")
        return False
    
    scene_data = SCENE_1_PROMPTS[prompt_key]
    
    # Build complete prompt with prefix + panel spec + suffix
    full_prompt = f"{STYLE_PREFIX} {scene_data['panel_spec']} {STYLE_SUFFIX}"
    
    # Use custom seed if provided, otherwise use default from params
    seed = custom_seed if custom_seed is not None else GENERATION_PARAMS["seed"]
    
    logger.info(f"\n🎬 Generating Scene 1 Panel: {prompt_key}")
    logger.info(f"📝 Style Note: {scene_data['style_note']}")
    logger.info(f"🎯 Panel Spec: {scene_data['panel_spec'][:100]}...")
    
    try:
        images = generate_image(
            prompt=full_prompt,
            negative_prompt=SHARED_NEGATIVE,
            width=GENERATION_PARAMS["width"],
            height=GENERATION_PARAMS["height"],
            steps=GENERATION_PARAMS["steps"],
            cfg_scale=GENERATION_PARAMS["cfg_scale"],
            sampler_name=GENERATION_PARAMS["sampler_name"],
            scheduler=GENERATION_PARAMS["scheduler"],
            seed=seed,
            batch_size=GENERATION_PARAMS["n_iter"],
            timeout=300
        )
        
        if images:
            # Save generated images
            for i, image_data in enumerate(images):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scene1_{prompt_key}_{timestamp}_v{i+1}.png"
                filepath = get_output_path(filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                file_size = len(image_data) / 1024
                logger.info(f"✅ Saved: {filename} ({file_size:.1f}KB)")
            
            return True
            
        else:
            logger.error("❌ No images returned from API")
            return False
            
    except Exception as e:
        logger.error(f"❌ Generation error: {e}")
        return False

def generate_complete_scene_1():
    """Generate all panels for Scene 1 - The Awakening"""
    logger.info("🎭 DRIFTINGME - Scene 1: The Awakening")
    logger.info("=" * 50)
    
    success_count = 0
    total_panels = len(SCENE_1_PROMPTS)
    
    for prompt_key in SCENE_1_PROMPTS.keys():
        if generate_scene_1_panel(prompt_key):
            success_count += 1
        logger.info("-" * 30)
    
    logger.info(f"\n📊 Scene 1 Generation Complete:")
    logger.info(f"✅ Successfully generated: {success_count}/{total_panels} panels")
    
    if success_count == total_panels:
        logger.info("🎉 All Scene 1 panels generated successfully!")
    else:
        logger.warning("⚠️  Some panels failed to generate. Check API status.")

def main():
    import sys
    
    if len(sys.argv) > 1:
        panel_name = sys.argv[1]
        if panel_name == "all":
            generate_complete_scene_1()
        else:
            if not generate_scene_1_panel(panel_name):
                sys.exit(1)
    else:
        logger.info("🎭 DriftingMe Scene 1 Generator")
        logger.info("\nAvailable panels:")
        for key, data in SCENE_1_PROMPTS.items():
            logger.info(f"  • {key}: {data['style_note']}")
        logger.info(f"\nUsage:")
        logger.info(f"  python3 {sys.argv[0]} <panel_name>")
        logger.info(f"  python3 {sys.argv[0]} all")

if __name__ == "__main__":
    main()