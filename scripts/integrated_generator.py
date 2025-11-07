#!/usr/bin/env python3
"""
DriftingMe Integrated Scene Generator
Combines character design with clean environment style for complete scene generation
"""

import requests
import json
import base64
from datetime import datetime
import os

# API Configuration
A1111_URL = "http://localhost:7860"

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
    if scene_key not in INTEGRATED_SCENES:
        print(f"Unknown integrated scene: {scene_key}")
        return False
    
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
    
    print(f"\n🎬👤 Generating Integrated Scene: {scene_key}")
    print(f"🎭 Style Note: {scene_data['style_note']}")
    print(f"🎯 Integration: Character + Environment")
    
    try:
        response = requests.post(f"{A1111_URL}/sdapi/v1/txt2img", json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            
            # Save generated images
            for i, image_data in enumerate(result['images']):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"integrated_{scene_key}_{timestamp}_v{i+1}.png"
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
            print(f"🎯 CFG Scale: {payload['cfg_scale']}")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False

def generate_complete_scene1():
    """Generate complete Scene 1 with integrated character design"""
    print("🎬👤 DRIFTINGME - Scene 1 Complete Integration")
    print("=" * 60)
    
    # Key integrated scenes for Scene 1
    scene1_shots = [
        "scene1_awakening_integrated",
        "scene1_closeup_integrated", 
        "scene1_room_with_figure",
        "scene1_shadow_character"
    ]
    
    success_count = 0
    for shot in scene1_shots:
        if generate_integrated_scene(shot):
            success_count += 1
        print("-" * 40)
    
    print(f"\n📊 Scene 1 Integration Complete:")
    print(f"✅ Successfully generated: {success_count}/{len(scene1_shots)} integrated scenes")

def main():
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "scene1":
            generate_complete_scene1()
        elif command == "all":
            print("Generating all integrated scenes...")
            success = 0
            for key in INTEGRATED_SCENES.keys():
                if generate_integrated_scene(key):
                    success += 1
            print(f"Generated {success}/{len(INTEGRATED_SCENES)} integrated scenes")
        elif command in INTEGRATED_SCENES:
            custom_seed = None
            if "seed:" in " ".join(sys.argv):
                seed_arg = [arg for arg in sys.argv if arg.startswith("seed:")][0]
                custom_seed = int(seed_arg.split(":")[1])
            
            generate_integrated_scene(command, custom_seed)
        else:
            print(f"Unknown command: {command}")
    else:
        print("🎬👤 DriftingMe Integrated Scene Generator")
        print("\nAvailable integrated scenes:")
        for key, data in INTEGRATED_SCENES.items():
            print(f"  • {key}: {data['style_note']}")
        print(f"\nCommands:")
        print(f"  scene1                  - Generate complete Scene 1 integration")
        print(f"  all                     - Generate all integrated scenes")  
        print(f"  <scene_name>            - Generate specific integrated scene")
        print(f"  <scene_name> seed:12345 - Use custom seed")

if __name__ == "__main__":
    main()