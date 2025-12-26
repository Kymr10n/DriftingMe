#!/usr/bin/env python3
"""
DriftingMe Integrated Scene Generator
Combines character design with clean environment style for complete scene generation
"""

import logging
from datetime import datetime
from config import get_config, get_output_path
from comfyui_api import generate_image, check_server_status
from utils import validate_seed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# API Configuration
COMFYUI_URL = get_config('COMFYUI_URL')


# Integrated Scene Prompts - Character + Environment
INTEGRATED_SCENES = {
    "scene1_awakening_integrated": {
        "prompt": """
        noir comic book illustration, clean black and white art style,
        medium shot of masculine male protagonist jolting awake in bed,
        clear defined facial features, strong jawline, confused expression,
        woman sleeping beside him with clear human proportions,
        venetian blind shadows casting geometric patterns across the scene,
        clean bedroom interior, bold outlines, high contrast lighting,
        classic comic book style, minimal details but clear human features,
        graphic novel aesthetic, no abstract distortion, realistic proportions
        """,
        "negative": "cross-hatching, film grain, gritty texture, noise, rough lines, sketchy, photorealistic, color, soft shadows, abstract art, picasso style, cubist, distorted features",
        "style_note": "Complete Scene 1 with clear character features"
    },
    
    "scene1_closeup_integrated": {
        "prompt": """
        noir comic book close-up of male protagonist's face, clean black and white,
        handsome masculine face with clear defined features, strong jawline,
        confused expression with clear eyes, well-defined nose and eyebrows,
        venetian blind shadow stripes across recognizable human features,
        classic comic book character design, bold clean outlines,
        high contrast lighting, graphic novel style, clean facial structure,
        no abstract distortion, realistic proportions, professional comic art
        """,
        "negative": "cross-hatching, texture, photorealistic, soft shadows, color, gritty, sketchy lines, abstract art, picasso style, cubist, distorted features, weird proportions",
        "style_note": "Clear character close-up with environmental shadow integration"
    },
    
    "scene1_silhouette_integrated": {
        "prompt": """
        clean noir comic book illustration, male protagonist geometric silhouette sitting on bed edge,
        minimalist black and white art, venetian blind shadows creating stripe patterns,
        architectural bedroom interior, bold clean silhouette against geometric room,
        abstract body proportions, stylized interior forms, high contrast lighting,
        vector-like illustration style, graphic novel aesthetic, clean geometric composition,
        no texture or cross-hatching, pure shadow play with architectural precision
        """,
        "negative": "detailed anatomy, cross-hatching, texture, photorealistic, soft shadows, color, gritty, realistic proportions",
        "style_note": "Character silhouette integrated with clean room design"
    },
    
    "scene1_room_with_figure": {
        "prompt": """
        clean minimalist noir comic illustration, wide shot of geometric bedroom interior,
        male protagonist figure in bed, geometric stylized forms, woman beside him,
        venetian blind shadows creating precise architectural patterns,
        simplified furniture with bold geometric forms, high contrast silhouettes,
        vector-like art style, graphic novel aesthetic, minimal details,
        dramatic window lighting with sharp geometric shadows, clean ink illustration,
        abstract interior design, no texture or grain
        """,
        "negative": "cross-hatching, gritty, film grain, texture, noise, detailed objects, photorealistic, color, soft shadows, cluttered details",
        "style_note": "Wide establishing shot with integrated character presence"
    },
    
    "scene1_hands_awakening": {
        "prompt": """
        clean noir comic book style, close-up of geometric male protagonist's hands,
        minimalist black and white illustration, stylized hand forms against bed sheets,
        venetian blind shadow stripes across hands and bedding, bold clean lines,
        abstract finger shapes, architectural precision in hand design,
        vector-like art style, graphic novel aesthetic, no texture or cross-hatching,
        dramatic lighting with sharp geometric shadows, clean ink illustration
        """,
        "negative": "detailed skin texture, cross-hatching, photorealistic hands, soft shadows, color, gritty, sketchy lines, realistic anatomy",
        "style_note": "Character hands detail integrated with scene elements"
    },
    
    "scene1_shadow_character": {
        "prompt": """
        abstract noir comic book style, geometric male protagonist silhouette,
        venetian blind shadow patterns creating prison bar effect across figure,
        minimalist composition, high contrast geometric shapes, clean black silhouette,
        stylized human form behind precise shadow lines, graphic design aesthetic,
        vector-like illustration, no facial details visible, pure geometric shadow play,
        architectural shadow composition, clean ink art style, dramatic abstract design
        """,
        "negative": "detailed features, cross-hatching, texture, gritty, photorealistic, color, soft edges, realistic anatomy",
        "style_note": "Abstract character integration with symbolic shadow patterns"
    }
}

# Generation parameters optimized for integrated scenes
INTEGRATED_PARAMS = {
    "width": 768,
    "height": 1024,
    "steps": 25,
    "cfg_scale": 7.0,
    "sampler_name": "DPM++ 2M",
    "scheduler": "karras", 
    "seed": -1,
    "batch_size": 1,
    "n_iter": 2,
}

def create_integrated_prompt(base_prompt):
    """Enhanced prompt for integrated character + environment"""
    style_modifiers = """
    masterpiece, best quality, clean vector illustration, geometric character design,
    architectural interior design, bold graphic style, consistent visual language,
    """
    
    return f"{style_modifiers} {base_prompt}"

def create_integrated_negative(base_negative):
    """Enhanced negative for clean integrated scenes"""
    prevention_terms = """
    inconsistent art styles, mixed techniques, realistic photography, detailed textures,
    complex shading, watercolor, painting style, soft gradients, anime, cartoon,
    """
    
    return f"{base_negative}, {prevention_terms}"

def generate_integrated_scene(scene_key, custom_seed=None):
    """Generate integrated character + environment scenes"""
    # Validate inputs
    if not validate_prompt_key(scene_key):
        raise ValueError(f"Invalid scene key format: {scene_key}")
    
    if scene_key not in INTEGRATED_SCENES:
        raise KeyError(f"Unknown integrated scene: {scene_key}")
    
    custom_seed = validate_seed(custom_seed)
    
    scene_data = INTEGRATED_SCENES[scene_key]
    
    # Enhanced prompts
    prompt = create_integrated_prompt(scene_data["prompt"])
    negative = create_integrated_negative(scene_data["negative"])
    
    payload = {
        **INTEGRATED_PARAMS,
        "prompt": prompt,
        "negative_prompt": negative,
    }
    
    if custom_seed:
        payload["seed"] = custom_seed
    
    logger.info(f"\n🎬👤 Generating Integrated Scene: {scene_key}")
    logger.info(f"🎭 Style Note: {scene_data['style_note']}")
    logger.info(f"🎯 Integration: Character + Environment")
    
    try:
        images = generate_image(
            prompt=payload["prompt"],
            negative_prompt=payload["negative_prompt"],
            width=payload["width"],
            height=payload["height"],
            steps=payload["steps"],
            cfg_scale=payload["cfg_scale"],
            sampler_name=payload["sampler_name"],
            scheduler=payload["scheduler"].lower(),
            seed=payload.get("seed", -1),
            batch_size=payload.get("n_iter", 1),
            timeout=300
        )
        
        if images:
            
            # Save generated images
            for i, image_data in enumerate(images):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_{timestamp}_v{i+1}.png"
                filepath = get_output_path(filename)
                
                # Save image
                image_bytes = image_data
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
                
                file_size = len(image_bytes) / 1024
                logger.info(f"✅ Saved: {filename} ({file_size:.1f}KB)")
            
            # Generation complete
            
            logger.info(f"⚙️  Seed: {info.get('seed', 'Unknown')}")
            logger.info(f"🎯 CFG Scale: {payload['cfg_scale']}")
            
            return True
            
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return False
            
    except TimeoutError:
        logger.error(f"API request timed out after 120s")
        return False
    except ConnectionError as e:
        logger.error(f"Connection Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Request Error: {e}")
        return False
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        return False

def generate_complete_scene1():
    """Generate complete Scene 1 with integrated character design"""
    logger.info("🎬👤 DRIFTINGME - Scene 1 Complete Integration")
    logger.info("=" * 60)
    
    # Key integrated scenes for Scene 1
    scene1_shots = [
        "scene1_awakening_integrated",
        "scene1_closeup_integrated", 
        "scene1_room_with_figure",
        "scene1_shadow_character"
    ]
    
    success_count = 0
    for shot in scene1_shots:
        try:
            if generate_integrated_scene(shot):
                success_count += 1
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to generate {shot}: {e}")
        logger.info("-" * 40)
    
    logger.info(f"\n📊 Scene 1 Integration Complete:")
    logger.info(f"✅ Successfully generated: {success_count}/{len(scene1_shots)} integrated scenes")

def main():
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "scene1":
            generate_complete_scene1()
        elif command == "all":
            logger.info("Generating all integrated scenes...")
            success = 0
            for key in INTEGRATED_SCENES.keys():
                try:
                    if generate_integrated_scene(key):
                        success += 1
                except (ValueError, KeyError) as e:
                    logger.error(f"Failed to generate {key}: {e}")
            logger.info(f"Generated {success}/{len(INTEGRATED_SCENES)} integrated scenes")
        elif command in INTEGRATED_SCENES:
            custom_seed = None
            if "seed:" in " ".join(sys.argv):
                seed_arg = [arg for arg in sys.argv if arg.startswith("seed:")][0]
                try:
                    custom_seed = int(seed_arg.split(":")[1])
                except ValueError as e:
                    logger.error(f"Invalid seed value: {e}")
                    sys.exit(1)
            
            try:
                generate_integrated_scene(command, custom_seed)
            except (ValueError, KeyError) as e:
                logger.error(f"Generation failed: {e}")
                sys.exit(1)
        else:
            logger.info(f"Unknown command: {command}")
    else:
        logger.info("🎬👤 DriftingMe Integrated Scene Generator")
        logger.info("\nAvailable integrated scenes:")
        for key, data in INTEGRATED_SCENES.items():
            logger.info(f"  • {key}: {data['style_note']}")
        logger.info(f"\nCommands:")
        logger.info(f"  scene1                  - Generate complete Scene 1 integration")
        logger.info(f"  all                     - Generate all integrated scenes")  
        logger.info(f"  <scene_name>            - Generate specific integrated scene")
        logger.info(f"  <scene_name> seed:12345 - Use custom seed")

if __name__ == "__main__":
    main()