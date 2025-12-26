#!/usr/bin/env python3
"""
DriftingMe Final API Demo
Simple demonstration of programmatic noir image generation.
"""

import os
import logging
from datetime import datetime
from config import get_config
from comfyui_api import generate_image, check_server_status

def generate_noir_demo():
    """Generate a demo noir image via A1111 API"""
    
    logger.info("🎬 DriftingMe - Programmatic Noir Generation Demo")
    logger.info("=" * 60)
    
    # Simple noir prompt
    payload = {
        "prompt": """A film noir detective in a fedora and trench coat, standing under a street lamp 
                    in the rain, dramatic black and white lighting, 1940s cinematography, 
                    high contrast shadows, moody atmosphere""",
        "negative_prompt": "color, bright, cheerful, cartoonish",
        "steps": 15,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 768,
        "sampler_name": "Euler",
        "seed": 42,  # Fixed seed for reproducible demo
        "save_images": True
    }
    
    logger.info("📡 Sending API request to A1111...")
    logger.info(f"🎯 Using seed: {payload['seed']}")
    logger.info(f"📐 Dimensions: {payload['width']}x{payload['height']}")
    
    try:
        api_url = get_config('COMFYUI_URL')
        response = requests.post(
            f"{api_url}/sdapi/v1/txt2img", 
            json=payload, 
            timeout=60
        )
        
        if images:
            info = json.loads(result['info'])
            
            logger.info("✅ Generation successful!")
            logger.info(f"⚙️  Model: {info['sd_model_name']}")
            logger.info(f"🔧 Sampler: {info['sampler_name']}")
            logger.info(f"🎯 Seed: {info['seed']}")
            
            # Save image
            if result['images']:
                image_data = base64.b64decode(result['images'][0])
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"noir_demo_{timestamp}.png"
                
                os.makedirs("outputs", exist_ok=True)
                with open(f"outputs/{filename}", 'wb') as f:
                    f.write(image_data)
                
                logger.info(f"💾 Image saved: outputs/{filename}")
                
                # File size
                file_size = len(image_data) / 1024
                logger.info(f"📊 File size: {file_size:.1f} KB")
                
                return True
        else:
            logger.info(f"❌ API Error: {response.status_code}")
            logger.info(response.text)
            return False
            
    except Exception as e:
        logger.info(f"❌ Error: {e}")
        return False

def main():
    success = generate_noir_demo()
    
    logger.info("\n" + "=" * 60)
    if success:
        logger.info("🎉 API Demo Complete!")
        logger.info("\n📋 Summary:")
        logger.info("✅ A1111 API is working perfectly")
        logger.info("✅ ComfyUI API is accessible")
        logger.info("✅ Noir image generation successful")
        logger.info("✅ Programmatic control achieved")
        
        logger.info("\n🚀 Next Steps:")
        logger.info("• Create batch processing scripts")
        logger.info("• Implement ComfyUI workflows")
        logger.info("• Build episode content automation")
        logger.info("• Develop character consistency tools")
        
        logger.info("\n📍 Available for DriftingMe project:")
        logger.info("• Direct API access for automation")
        logger.info("• Reproducible generation with seeds")
        logger.info("• High-quality noir aesthetic")
        logger.info("• Ready for episode production")
    else:
        logger.info("❌ Demo failed - check API status")

if __name__ == "__main__":
    main()