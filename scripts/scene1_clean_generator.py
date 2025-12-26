#!/usr/bin/env python3
"""
DriftingMe Scene 1 Generator - REFINED VERSION
Clean noir comic book style with crisp lines and geometric shadows
"""

from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# API Configuration
COMFYUI_URL = "http://localhost:8188"

# REFINED Scene 1 Prompts - Clean Abstract Noir Style
SCENE_1_PROMPTS = {
    "awakening_medium_shot": {
        "prompt": """
        clean noir comic book illustration, minimalist black and white art style,
        sharp geometric shadows, bold clean lines, high contrast silhouettes,
        medium shot of man waking in bed, venetian blind creating precise geometric shadow patterns,
        abstract noir style, minimal details, strong black and white contrast,
        clean ink illustration, graphic novel aesthetic, stylized composition,
        dramatic lighting with hard edges, architectural shadows, no texture or grain
        """,
        "negative": "cross-hatching, film grain, gritty texture, noise, rough lines, sketchy, detailed rendering, photorealistic, color, soft shadows, blurred edges",
        "style_note": "Clean medium shot with geometric venetian blind shadows"
    },
    
    "close_up_eyes": {
        "prompt": """
        clean noir comic book style, minimalist black and white illustration,
        extreme close-up of man's eyes, bold geometric shadow patterns across face,
        sharp clean lines, high contrast silhouettes, venetian blind shadows,
        abstract noir aesthetic, minimal detailing, pure black and white,
        graphic novel style, stylized facial features, dramatic lighting with hard edges,
        no texture or cross-hatching, clean ink art
        """,
        "negative": "cross-hatching, film grain, gritty, texture, noise, detailed skin, photorealistic, color, soft lighting, sketchy lines",
        "style_note": "Clean close-up with geometric shadow patterns"
    },
    
    "room_overview": {
        "prompt": """
        clean minimalist noir comic illustration, abstract black and white interior,
        geometric venetian blind shadows creating precise patterns,
        simplified bedroom with bold architectural forms, high contrast silhouettes,
        clean lines, minimal details, graphic novel aesthetic,
        dramatic window lighting with sharp geometric shadows,
        stylized furniture forms, pure black and white contrast, no texture
        """,
        "negative": "cross-hatching, gritty, film grain, texture, noise, detailed objects, photorealistic, color, soft shadows, cluttered details",
        "style_note": "Clean architectural establishing shot with geometric shadows"
    },
    
    "shadow_bars": {
        "prompt": """
        abstract noir comic book style, geometric venetian blind shadow patterns,
        clean black and white illustration, bold stripe shadows creating prison bar effect,
        minimalist composition, high contrast geometric shapes,
        stylized silhouette behind precise shadow lines, graphic design aesthetic,
        sharp edges, no texture, pure geometric forms, clean ink art style,
        dramatic abstract composition with bold contrasts
        """,
        "negative": "cross-hatching, texture, gritty, film grain, noise, detailed rendering, photorealistic, color, soft edges, sketchy",
        "style_note": "Abstract geometric shadow composition"
    },
    
    # NEW: Even cleaner, more abstract versions
    "minimal_awakening": {
        "prompt": """
        ultra-minimalist noir comic style, clean vector-like illustration,
        simple geometric forms, man in bed with venetian shadow stripes,
        bold black shapes on white background, graphic design approach,
        abstract geometric composition, minimal line art, high contrast,
        stylized silhouettes, architectural shadow patterns, clean modern comic style
        """,
        "negative": "detailed faces, cross-hatching, texture, gritty, photorealistic, color, soft gradients, noise, sketchy lines",
        "style_note": "Ultra-clean minimal geometric approach"
    },
    
    "architectural_shadows": {
        "prompt": """
        architectural noir illustration, clean geometric shadow study,
        venetian blind casting precise parallel lines, minimalist interior space,
        bold black and white graphic design, abstract geometric forms,
        clean modernist aesthetic, sharp architectural shadows,
        stylized geometric composition, no human figures, pure shadow play
        """,
        "negative": "people, faces, cross-hatching, texture, gritty, detailed objects, photorealistic, color, organic shapes",
        "style_note": "Pure architectural shadow study"
    }
}

# UPDATED Generation parameters for cleaner output
GENERATION_PARAMS = {
    "width": 768,
    "height": 1024,
    "steps": 25,  # Fewer steps for cleaner results
    "cfg_scale": 7.0,  # Lower CFG for less over-processing
    "sampler_name": "DPM++ 2M",  # Cleaner sampler
    "scheduler": "karras",
    "seed": -1,
    "batch_size": 1,
    "n_iter": 2,
}

# NEW: Enhanced prompt with style emphasis
def create_enhanced_prompt(base_prompt):
    """Add consistent style modifiers to ensure clean output"""
    style_modifiers = """
    masterpiece, best quality, clean illustration, vector art style,
    bold geometric shapes, minimal noise, sharp clean edges,
    """
    
    quality_boost = """
    professional comic book art, graphic design quality,
    """
    
    return f"{style_modifiers} {base_prompt} {quality_boost}"

def create_enhanced_negative(base_negative):
    """Enhanced negative prompt to prevent noise and texture"""
    noise_prevention = """
    noise, grain, texture, cross-hatching, sketchy lines, rough art,
    low quality, blurry, soft edges, watercolor, painting style,
    photorealistic, detailed rendering, complex shading,
    """
    
    return f"{base_negative}, {noise_prevention}"

def generate_scene_1_panel(prompt_key, custom_seed=None, use_enhanced=True):
    """Generate a specific panel for Scene 1 with optional enhanced prompts"""
    if prompt_key not in SCENE_1_PROMPTS:
        logger.info(f"Unknown prompt key: {prompt_key}")
        return False
    
    scene_data = SCENE_1_PROMPTS[prompt_key]
    
    # Optionally enhance prompts for cleaner output
    if use_enhanced:
        prompt = create_enhanced_prompt(scene_data["prompt"])
        negative = create_enhanced_negative(scene_data["negative"])
    else:
        prompt = scene_data["prompt"]
        negative = scene_data["negative"]
    
    # Prepare payload
    payload = {
        **GENERATION_PARAMS,
        "prompt": prompt,
        "negative_prompt": negative,
    }
    
    if custom_seed:
        payload["seed"] = custom_seed
    
    logger.info(f"\n🎨 Generating CLEAN Scene 1 Panel: {prompt_key}")
    logger.info(f"📐 Style Note: {scene_data['style_note']}")
    logger.info(f"✨ Enhanced Prompts: {'Yes' if use_enhanced else 'No'}")
    
    try:
        response = requests.post(f"{COMFYUI_URL}/sdapi/v1/txt2img", json=payload, timeout=120)
        
        if images:
            
            # Save generated images
            for i, image_data in enumerate(result['images']):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                prefix = "clean_" if use_enhanced else "orig_"
                filename = f"{prefix}scene1_{prompt_key}_{timestamp}_v{i+1}.png"
                filepath = os.path.join("/home/alex/Projects/DriftingMe/outputs", filename)
                
                # Decode and save
                image_bytes = base64.b64decode(image_data)
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
                
                file_size = len(image_bytes) / 1024
                logger.info(f"✅ Saved: {filename} ({file_size:.1f}KB)")
            
            # Generation complete
            
            logger.info(f"⚙️  Seed: {info.get('seed', 'Unknown')}")
            logger.info(f"🎯 CFG Scale: {payload['cfg_scale']}")
            logger.info(f"🔄 Sampler: {payload['sampler_name']}")
            
            return True
            
        else:
            logger.info(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.info(f"❌ Connection Error: {e}")
        return False

def generate_clean_comparison():
    """Generate clean versions of key panels for comparison"""
    logger.info("🎭 DRIFTINGME - Clean Style Comparison")
    logger.info("=" * 50)
    
    # Test with the most important panels
    test_panels = ["awakening_medium_shot", "minimal_awakening", "architectural_shadows"]
    
    success_count = 0
    for prompt_key in test_panels:
        if generate_scene_1_panel(prompt_key, use_enhanced=True):
            success_count += 1
        logger.info("-" * 30)
    
    logger.info(f"\n📊 Clean Style Test Complete:")
    logger.info(f"✅ Successfully generated: {success_count}/{len(test_panels)} panels")

def main():
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "clean":
            generate_clean_comparison()
        elif command == "all-clean":
            logger.info("Generating all panels with clean style...")
            success = 0
            for key in SCENE_1_PROMPTS.keys():
                if generate_scene_1_panel(key, use_enhanced=True):
                    success += 1
            logger.info(f"Generated {success}/{len(SCENE_1_PROMPTS)} clean panels")
        elif command in SCENE_1_PROMPTS:
            # Enhanced by default, add "raw" for original
            enhanced = "raw" not in sys.argv
            generate_scene_1_panel(command, use_enhanced=enhanced)
        else:
            logger.info(f"Unknown command: {command}")
    else:
        logger.info("🎨 DriftingMe CLEAN Scene 1 Generator")
        logger.info("\nAvailable panels:")
        for key, data in SCENE_1_PROMPTS.items():
            logger.info(f"  • {key}: {data['style_note']}")
        logger.info(f"\nCommands:")
        logger.info(f"  clean                    - Test clean style with key panels")
        logger.info(f"  all-clean               - Generate all panels with clean style")
        logger.info(f"  <panel_name>            - Generate specific panel (enhanced)")
        logger.info(f"  <panel_name> raw        - Generate specific panel (original)")

if __name__ == "__main__":
    main()