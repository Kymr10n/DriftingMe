#!/usr/bin/env python3
"""
DriftingMe Character Generator - REFINED CLOSE-UPS
Clean noir comic character with clear, defined features - NOT abstract/Picasso style
"""

import requests
import json
import base64
from datetime import datetime
import os

# API Configuration
A1111_URL = "http://localhost:7860"

# REFINED Character Prompts - Clear Features, Not Abstract
REFINED_CHARACTER_PROMPTS = {
    "character_closeup_clear": {
        "prompt": """
        noir comic book close-up portrait, clean black and white illustration,
        handsome male face with clear defined features, strong jawline, well-defined nose,
        realistic proportions but simplified clean lines, classic comic book style,
        clear eyes with defined pupils, masculine eyebrows, clean hair outline,
        venetian blind shadows across face creating geometric patterns,
        high contrast black and white, bold clean outlines, graphic novel style,
        clear facial structure, no abstract distortion, recognizable human features
        """,
        "negative": "abstract art, picasso style, cubist, distorted features, surreal, weird eyes, deformed face, multiple eyes, abstract facial features, fragmented face, artistic distortion, avant-garde",
        "style_note": "Clear, defined close-up with recognizable human features"
    },
    
    "character_profile_clear": {
        "prompt": """
        noir comic book side profile, clean black and white illustration,
        masculine male profile with clear defined nose, strong jaw, clean hairline,
        realistic facial proportions, classic comic book character design,
        clear outline of face, well-defined ear, clean neck line,
        venetian blind shadows creating stripe patterns, high contrast lighting,
        bold clean lines, graphic novel aesthetic, no facial distortion,
        recognizable human profile, clean geometric shadows
        """,
        "negative": "abstract profile, picasso style, cubist, distorted nose, weird proportions, fragmented face, surreal features, artistic distortion, deformed profile",
        "style_note": "Clean side profile with clear human proportions"
    },
    
    "character_eyes_clear": {
        "prompt": """
        noir comic book extreme close-up of male eyes, clean black and white,
        clearly defined human eyes with realistic proportions, clean eyebrows,
        expression of confusion and awakening, venetian blind shadow stripes,
        bold clean outlines around eyes, well-defined pupils and iris,
        classic comic book eye design, high contrast black and white,
        clean geometric shadows, no abstract distortion, recognizable human eyes,
        graphic novel style illustration, clear facial features
        """,
        "negative": "abstract eyes, picasso style, cubist eyes, weird eye shapes, distorted pupils, surreal eyes, fragmented eyes, artistic distortion, multiple pupils",
        "style_note": "Clear, realistic eyes with geometric shadow patterns"
    },
    
    "character_awakening_clear": {
        "prompt": """
        noir comic book medium shot of man waking up, clean black and white,
        clear masculine face with defined features, confused expression,
        realistic facial proportions, strong jawline, clear nose and mouth,
        venetian blind shadows creating geometric patterns across clear features,
        classic comic book character design, bold clean outlines,
        recognizable human face, high contrast lighting, graphic novel style,
        clean hair design, well-proportioned features, no abstract distortion
        """,
        "negative": "abstract face, picasso style, cubist, distorted features, weird proportions, surreal face, fragmented features, artistic distortion, deformed face",
        "style_note": "Clear awakening scene with defined human features"
    },
    
    "character_face_front_clear": {
        "prompt": """
        noir comic book front view portrait, clean black and white illustration,
        handsome masculine male face, clear defined features and proportions,
        strong symmetrical jawline, well-defined nose, clear mouth,
        realistic human facial structure, classic comic book hero style,
        clean hair outline, defined eyebrows, clear facial geometry,
        venetian blind shadows in geometric patterns, high contrast,
        bold clean character design, graphic novel aesthetic, no distortion,
        recognizable human features, clean professional comic art
        """,
        "negative": "abstract portrait, picasso style, cubist face, asymmetrical weird features, distorted proportions, surreal face, fragmented face, artistic distortion",
        "style_note": "Clean front-facing portrait with clear human features"
    },
    
    "character_expression_clear": {
        "prompt": """
        noir comic book close-up of male face showing confusion,
        clean black and white illustration with clear human features,
        realistic facial proportions, well-defined confused expression,
        clear eyes showing uncertainty, defined eyebrows, clean jawline,
        venetian blind geometric shadows across recognizable face,
        classic comic book emotional expression, bold clean outlines,
        high contrast black and white, graphic novel character design,
        no abstract distortion, clear human facial structure
        """,
        "negative": "abstract expression, picasso style, cubist emotion, weird facial distortion, surreal expression, fragmented face, artistic distortion, deformed features",
        "style_note": "Clear emotional expression with defined human features"
    }
}

# Adjusted parameters for clearer character work
CLEAR_CHARACTER_PARAMS = {
    "width": 768,
    "height": 1024,
    "steps": 30,  # More steps for cleaner definition
    "cfg_scale": 6.0,  # Lower CFG for less AI interpretation
    "sampler_name": "Euler a",  # Different sampler for cleaner lines
    "scheduler": "normal",
    "seed": -1,
    "batch_size": 1,
    "n_iter": 3,
}

def create_clear_character_prompt(base_prompt):
    """Enhanced prompt for clear, defined character features"""
    character_modifiers = """
    professional comic book art, clear character design, defined human features,
    realistic proportions, clean illustration, classic comic book style,
    """
    
    return f"{character_modifiers} {base_prompt}"

def create_clear_negative(base_negative):
    """Strong negative to prevent abstract/Picasso-style distortion"""
    distortion_prevention = """
    abstract art, cubism, picasso, surrealism, distorted anatomy, weird proportions,
    fragmented features, artistic distortion, deformed face, multiple features,
    avant-garde art, experimental style, unrealistic anatomy, bizarre features,
    """
    
    return f"{base_negative}, {distortion_prevention}"

def generate_clear_character(prompt_key, custom_seed=None):
    """Generate clear, defined character features"""
    if prompt_key not in REFINED_CHARACTER_PROMPTS:
        print(f"Unknown character prompt: {prompt_key}")
        return False
    
    char_data = REFINED_CHARACTER_PROMPTS[prompt_key]
    
    # Enhanced prompts for clear character work
    prompt = create_clear_character_prompt(char_data["prompt"])
    negative = create_clear_negative(char_data["negative"])
    
    # Prepare payload
    payload = {
        **CLEAR_CHARACTER_PARAMS,
        "prompt": prompt,
        "negative_prompt": negative,
    }
    
    if custom_seed:
        payload["seed"] = custom_seed
    
    print(f"\n👤 Generating CLEAR Character: {prompt_key}")
    print(f"🎭 Style Note: {char_data['style_note']}")
    print(f"🚫 Anti-Picasso: Strong distortion prevention active")
    
    try:
        response = requests.post(f"{A1111_URL}/sdapi/v1/txt2img", json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            
            # Save generated images
            for i, image_data in enumerate(result['images']):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"clear_char_{prompt_key}_{timestamp}_v{i+1}.png"
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
            print(f"🔄 Sampler: {payload['sampler_name']}")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False

def generate_clear_character_set():
    """Generate complete set of clear character studies"""
    print("👤 DRIFTINGME - CLEAR Character Studies (Anti-Picasso)")
    print("=" * 60)
    
    # Key clear character studies
    clear_studies = [
        "character_face_front_clear",
        "character_profile_clear", 
        "character_closeup_clear",
        "character_awakening_clear"
    ]
    
    success_count = 0
    for study in clear_studies:
        if generate_clear_character(study):
            success_count += 1
        print("-" * 40)
    
    print(f"\n📊 Clear Character Studies Complete:")
    print(f"✅ Successfully generated: {success_count}/{len(clear_studies)} clear characters")

def main():
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "clear-set":
            generate_clear_character_set()
        elif command == "all-clear":
            print("Generating all clear character studies...")
            success = 0
            for key in REFINED_CHARACTER_PROMPTS.keys():
                if generate_clear_character(key):
                    success += 1
            print(f"Generated {success}/{len(REFINED_CHARACTER_PROMPTS)} clear characters")
        elif command in REFINED_CHARACTER_PROMPTS:
            custom_seed = None
            if "seed:" in " ".join(sys.argv):
                seed_arg = [arg for arg in sys.argv if arg.startswith("seed:")][0]
                custom_seed = int(seed_arg.split(":")[1])
            
            generate_clear_character(command, custom_seed)
        else:
            print(f"Unknown command: {command}")
    else:
        print("👤 DriftingMe CLEAR Character Generator (Anti-Picasso)")
        print("\nAvailable clear character studies:")
        for key, data in REFINED_CHARACTER_PROMPTS.items():
            print(f"  • {key}: {data['style_note']}")
        print(f"\nCommands:")
        print(f"  clear-set               - Generate core clear character set")
        print(f"  all-clear              - Generate all clear character studies")
        print(f"  <study_name>           - Generate specific clear character")
        print(f"  <study_name> seed:123  - Use custom seed")

if __name__ == "__main__":
    main()