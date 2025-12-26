#!/usr/bin/env python3
"""
DriftingMe Character Generator - Main Protagonist
Clean geometric noir style character development system
"""

import logging
from datetime import datetime
from config import get_config, get_output_path
from utils import validate_prompt_key, validate_seed
from comfyui_api import generate_image, check_server_status

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# API Configuration
COMFYUI_URL = get_config('COMFYUI_URL')

# Main Character Development Prompts
CHARACTER_PROMPTS = {
    "character_profile_front": {
        "prompt": """
        clean noir comic book character design, minimalist black and white illustration,
        front view portrait of male protagonist, geometric stylized features,
        bold clean lines, high contrast silhouettes, abstract facial structure,
        simple geometric hair design, strong jawline, minimalist eye design,
        vector-like illustration style, graphic novel aesthetic, no texture or grain,
        dramatic lighting with hard edges, stylized masculine features,
        clean ink art style, architectural precision in facial structure
        """,
        "negative": "cross-hatching, texture, gritty, photorealistic, detailed skin, hair texture, soft shadows, color, anime, cartoon, sketchy lines",
        "style_note": "Front-facing character design sheet"
    },
    
    "character_profile_side": {
        "prompt": """
        clean noir comic book character design, side profile view of male protagonist,
        minimalist black and white illustration, geometric stylized silhouette,
        bold clean lines, strong profile with angular features, abstract nose and jaw design,
        simple geometric hair form, high contrast lighting, vector-like art style,
        graphic novel aesthetic, no texture or cross-hatching, architectural facial structure,
        dramatic side lighting with sharp shadows, clean ink illustration
        """,
        "negative": "cross-hatching, texture, detailed hair, photorealistic, soft gradients, color, sketchy, gritty, anime",
        "style_note": "Side profile character reference"
    },
    
    "character_awakening_closeup": {
        "prompt": """
        clean noir comic book style, extreme close-up of male protagonist's face waking up,
        minimalist black and white illustration, geometric facial features,
        eyes wide with confusion and disorientation, venetian blind shadow stripes across face,
        bold clean lines, high contrast silhouettes, abstract stylized expression,
        vector-like illustration, graphic novel aesthetic, dramatic geometric shadows,
        no texture or grain, sharp architectural lighting, clean ink art style
        """,
        "negative": "cross-hatching, texture, detailed skin, photorealistic, soft shadows, color, gritty, sketchy lines, anime",
        "style_note": "Character in awakening scene - emotional close-up"
    },
    
    "character_silhouette_bed": {
        "prompt": """
        clean noir comic book illustration, male protagonist silhouette sitting on bed edge,
        minimalist black and white art, geometric human form, bold clean silhouette,
        venetian blind shadows creating stripe patterns across figure,
        abstract body proportions, stylized masculine form, high contrast lighting,
        vector-like illustration style, no facial details visible, pure geometric shadow play,
        graphic novel aesthetic, architectural precision, clean ink art
        """,
        "negative": "detailed anatomy, cross-hatching, texture, photorealistic, soft shadows, color, gritty, sketchy",
        "style_note": "Character silhouette in bed scene"
    },
    
    "character_standing_shadow": {
        "prompt": """
        clean noir comic book style, full body silhouette of male protagonist standing,
        minimalist black and white illustration, geometric human proportions,
        venetian blind shadow stripes across entire figure, bold clean silhouette,
        abstract stylized body form, high contrast lighting, vector-like art style,
        dramatic geometric shadow patterns, no facial features visible,
        graphic novel aesthetic, architectural shadow composition, clean ink illustration
        """,
        "negative": "detailed clothing, cross-hatching, texture, photorealistic, soft shadows, color, realistic anatomy, sketchy",
        "style_note": "Full body character silhouette study"
    },
    
    "character_hands_geometric": {
        "prompt": """
        clean noir comic book style, close-up of male hands in geometric style,
        minimalist black and white illustration, stylized hand forms,
        bold clean lines, abstract finger shapes, high contrast shadows,
        venetian blind shadow stripes across hands, vector-like art style,
        graphic novel aesthetic, no texture or cross-hatching, geometric precision,
        dramatic lighting with sharp edges, clean ink illustration style
        """,
        "negative": "detailed skin texture, cross-hatching, photorealistic hands, soft shadows, color, gritty, sketchy lines",
        "style_note": "Character hands detail study"
    },
    
    "character_eyes_geometric": {
        "prompt": """
        clean noir comic book style, extreme close-up of protagonist's eyes,
        minimalist black and white illustration, geometric stylized eye design,
        bold clean lines, abstract eye shapes, high contrast pupils and iris,
        venetian blind shadow stripes across eye area, vector-like art style,
        dramatic expression of confusion and disorientation, graphic novel aesthetic,
        no texture or cross-hatching, sharp architectural shadows, clean ink art
        """,
        "negative": "realistic eyes, detailed eyelashes, cross-hatching, texture, photorealistic, soft shadows, color, sketchy",
        "style_note": "Character eyes - emotional expression study"
    },
    
    "character_consistent_test": {
        "prompt": """
        clean noir comic book character sheet, same male protagonist in multiple poses,
        minimalist black and white illustration, consistent geometric facial features,
        front view, side view, and three-quarter view of same character,
        bold clean lines, stylized masculine features, vector-like art style,
        high contrast lighting, graphic novel aesthetic, no texture or grain,
        character consistency study, architectural precision in design, clean ink illustration
        """,
        "negative": "different people, cross-hatching, texture, photorealistic, soft shadows, color, inconsistent features, sketchy",
        "style_note": "Character consistency reference sheet"
    }
}

# Character-specific generation parameters
CHARACTER_PARAMS = {
    "width": 768,
    "height": 1024,
    "steps": 25,
    "cfg_scale": 6.5,  # Slightly lower for character work
    "sampler_name": "DPM++ 2M",
    "scheduler": "karras",
    "seed": -1,
    "batch_size": 1,
    "n_iter": 3,  # More variations for character development
}

def create_character_prompt(base_prompt):
    """Enhanced prompt for character consistency"""
    character_modifiers = """
    masterpiece, best quality, character design sheet, clean vector illustration,
    geometric character design, consistent facial features, bold graphic style,
    """
    
    return f"{character_modifiers} {base_prompt}"

def create_character_negative(base_negative):
    """Enhanced negative for clean character design"""
    character_prevention = """
    multiple people, inconsistent features, realistic proportions, detailed anatomy,
    cross-hatching, texture, gritty art, photorealistic, soft gradients,
    complex shading, watercolor, painting style, sketchy lines, anime, cartoon,
    """
    
    return f"{base_negative}, {character_prevention}"

def generate_character_study(prompt_key, custom_seed=None, use_fixed_seed=False):
    """Generate character studies with optional seed consistency"""
    # Validate inputs
    if not validate_prompt_key(prompt_key):
        raise ValueError(f"Invalid prompt key format: {prompt_key}")
    
    if prompt_key not in CHARACTER_PROMPTS:
        raise KeyError(f"Unknown character prompt: {prompt_key}")
    
    custom_seed = validate_seed(custom_seed)
    
    char_data = CHARACTER_PROMPTS[prompt_key]
    
    # Enhanced prompts for character work
    prompt = create_character_prompt(char_data["prompt"])
    negative = create_character_negative(char_data["negative"])
    
    # Determine seed
    if custom_seed:
        seed = custom_seed
    elif use_fixed_seed:
        seed = 12345678  # Fixed seed for consistency
    else:
        seed = -1  # Random
    
    logger.info(f"\n👤 Generating Character Study: {prompt_key}")
    logger.info(f"🎭 Style Note: {char_data['style_note']}")
    logger.info(f"🎯 Seed Mode: {'Fixed' if use_fixed_seed else 'Custom' if custom_seed else 'Random'}")
    
    try:
        # Generate using ComfyUI
        images = generate_image(
            prompt=prompt,
            negative_prompt=negative,
            width=CHARACTER_PARAMS["width"],
            height=CHARACTER_PARAMS["height"],
            steps=CHARACTER_PARAMS["steps"],
            cfg_scale=CHARACTER_PARAMS["cfg_scale"],
            sampler_name=CHARACTER_PARAMS["sampler_name"],
            scheduler=CHARACTER_PARAMS["scheduler"].lower(),
            seed=seed,
            batch_size=CHARACTER_PARAMS["n_iter"],
            timeout=300
        )
        
        # Save generated images
        for i, image_data in enumerate(images):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"character_{prompt_key}_{timestamp}_v{i+1}.png"
            filepath = get_output_path(filename)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            file_size = len(image_data) / 1024
            logger.info(f"✅ Saved: {filename} ({file_size:.1f}KB)")
        
        logger.info(f"🔧 Images generated: {len(images)}")
        logger.info(f"⚙️  Seed: {seed if seed != -1 else 'random'}")
        logger.info(f"🎯 CFG Scale: {CHARACTER_PARAMS['cfg_scale']}")
        
        return True
        
    except TimeoutError:
        logger.error(f"API request timed out after 300s")
        return False
    except Exception as e:
        logger.error(f"Generation Error: {e}")
        return False
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        return False

def generate_character_sheet():
    """Generate complete character reference sheet"""
    print("👤 DRIFTINGME - Character Development Sheet")
    print("=" * 50)
    
    # Core character studies
    core_studies = [
        "character_profile_front",
        "character_profile_side", 
        "character_awakening_closeup",
        "character_silhouette_bed"
    ]
    
    success_count = 0
    for study in core_studies:
        try:
            if generate_character_study(study, use_fixed_seed=True):
                success_count += 1
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to generate {study}: {e}")
        print("-" * 30)
    
    print(f"\n📊 Character Sheet Complete:")
    print(f"✅ Successfully generated: {success_count}/{len(core_studies)} studies")

def generate_character_details():
    """Generate detailed character feature studies"""
    print("🔍 DRIFTINGME - Character Detail Studies")
    print("=" * 50)
    
    detail_studies = [
        "character_hands_geometric",
        "character_eyes_geometric",
        "character_consistent_test"
    ]
    
    success_count = 0
    for study in detail_studies:
        try:
            if generate_character_study(study, use_fixed_seed=True):
                success_count += 1
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to generate {study}: {e}")
        print("-" * 30)
    
    print(f"\n📊 Detail Studies Complete:")
    print(f"✅ Successfully generated: {success_count}/{len(detail_studies)} studies")

def main():
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "sheet":
            generate_character_sheet()
        elif command == "details":
            generate_character_details()
        elif command == "all":
            generate_character_sheet()
            print("\n" + "="*50)
            generate_character_details()
        elif command in CHARACTER_PROMPTS:
            # Check for seed options
            fixed_seed = "fixed" in sys.argv
            custom_seed = None
            if "seed:" in " ".join(sys.argv):
                seed_arg = [arg for arg in sys.argv if arg.startswith("seed:")][0]
                try:
                    custom_seed = int(seed_arg.split(":")[1])
                except ValueError as e:
                    logger.error(f"Invalid seed value: {e}")
                    sys.exit(1)
            
            try:
                generate_character_study(command, custom_seed, fixed_seed)
            except (ValueError, KeyError) as e:
                logger.error(f"Generation failed: {e}")
                sys.exit(1)
        else:
            print(f"Unknown command: {command}")
    else:
        print("👤 DriftingMe Character Generator")
        print("\nAvailable character studies:")
        for key, data in CHARACTER_PROMPTS.items():
            print(f"  • {key}: {data['style_note']}")
        print(f"\nCommands:")
        print(f"  sheet                   - Generate core character reference sheet")
        print(f"  details                 - Generate detailed feature studies")
        print(f"  all                     - Generate complete character development")
        print(f"  <study_name>            - Generate specific study")
        print(f"  <study_name> fixed      - Use fixed seed for consistency")
        print(f"  <study_name> seed:12345 - Use custom seed")

if __name__ == "__main__":
    main()