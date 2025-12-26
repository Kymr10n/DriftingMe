#!/usr/bin/env python3
"""
ComfyUI API Helper Module
Provides simplified interface for text-to-image generation via ComfyUI API
"""

import json
import uuid
import time
import urllib.request
import urllib.parse
import logging
from typing import Dict, Any, Optional, List
from config import get_config

logger = logging.getLogger(__name__)

# API Configuration
COMFYUI_URL = get_config('COMFYUI_URL')

def create_basic_workflow(
    prompt: str,
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    steps: int = 20,
    cfg_scale: float = 8.0,
    sampler_name: str = "euler",
    scheduler: str = "normal",
    seed: int = -1,
    batch_size: int = 1
) -> Dict[str, Any]:
    """
    Create a basic text-to-image workflow for ComfyUI
    
    This creates a simple workflow with:
    - CLIP Text Encode for positive/negative prompts
    - KSampler for generation
    - VAE Decode for final image
    - Save Image node
    """
    
    # Generate random seed if not provided
    if seed == -1:
        seed = int(time.time() * 1000) % 2**32
    
    # Map common sampler names to ComfyUI format
    sampler_mapping = {
        "dpm++ 2m karras": "dpmpp_2m",
        "dpm++ 2m": "dpmpp_2m",
        "euler a": "euler_ancestral",
        "euler": "euler",
    }
    sampler_name = sampler_mapping.get(sampler_name.lower(), "euler")
    
    workflow = {
        "3": {
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg_scale,
                "sampler_name": sampler_name,
                "scheduler": scheduler,
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler",
            "_meta": {"title": "KSampler"}
        },
        "4": {
            "inputs": {
                "ckpt_name": "v1-5-pruned-emaonly.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {"title": "Load Checkpoint"}
        },
        "5": {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": batch_size
            },
            "class_type": "EmptyLatentImage",
            "_meta": {"title": "Empty Latent Image"}
        },
        "6": {
            "inputs": {
                "text": prompt,
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "CLIP Text Encode (Prompt)"}
        },
        "7": {
            "inputs": {
                "text": negative_prompt,
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "CLIP Text Encode (Negative)"}
        },
        "8": {
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            },
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"}
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": ["8", 0]
            },
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"}
        }
    }
    
    return workflow


def queue_prompt(workflow: Dict[str, Any], client_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Queue a workflow for execution in ComfyUI
    
    Args:
        workflow: The workflow dictionary
        client_id: Optional client ID for websocket tracking
        
    Returns:
        Response data including prompt_id
    """
    if client_id is None:
        client_id = str(uuid.uuid4())
    
    payload = {
        "prompt": workflow,
        "client_id": client_id
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        logger.error(f"Failed to queue prompt: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error queueing prompt: {e}")
        raise


def get_history(prompt_id: str) -> Dict[str, Any]:
    """
    Get the execution history for a prompt
    
    Args:
        prompt_id: The prompt ID to query
        
    Returns:
        History data for the prompt
    """
    req = urllib.request.Request(f"{COMFYUI_URL}/history/{prompt_id}")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        logger.error(f"Failed to get history: {e}")
        raise


def get_image(filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
    """
    Download an image from ComfyUI
    
    Args:
        filename: Name of the image file
        subfolder: Subfolder within the output directory
        folder_type: Type of folder (output, input, temp)
        
    Returns:
        Image data as bytes
    """
    params = {
        "filename": filename,
        "subfolder": subfolder,
        "type": folder_type
    }
    
    url = f"{COMFYUI_URL}/view?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read()
    except urllib.error.URLError as e:
        logger.error(f"Failed to download image: {e}")
        raise


def wait_for_completion(prompt_id: str, timeout: int = 300, poll_interval: int = 2) -> Dict[str, Any]:
    """
    Wait for a prompt to complete execution
    
    Args:
        prompt_id: The prompt ID to wait for
        timeout: Maximum time to wait in seconds
        poll_interval: How often to check for completion
        
    Returns:
        Final history data when complete
        
    Raises:
        TimeoutError: If execution doesn't complete in time
    """
    start_time = time.time()
    
    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Prompt {prompt_id} did not complete within {timeout}s")
        
        try:
            history = get_history(prompt_id)
            
            if prompt_id in history:
                # Check if execution is complete
                prompt_history = history[prompt_id]
                if "outputs" in prompt_history:
                    return prompt_history
            
            time.sleep(poll_interval)
            
        except Exception as e:
            logger.warning(f"Error checking history: {e}")
            time.sleep(poll_interval)


def generate_image(
    prompt: str,
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    steps: int = 20,
    cfg_scale: float = 8.0,
    sampler_name: str = "euler",
    scheduler: str = "normal",
    seed: int = -1,
    batch_size: int = 1,
    timeout: int = 300
) -> List[bytes]:
    """
    High-level function to generate images using ComfyUI
    
    Args:
        prompt: The positive prompt
        negative_prompt: The negative prompt
        width: Image width
        height: Image height
        steps: Number of sampling steps
        cfg_scale: Classifier-free guidance scale
        sampler_name: Sampler algorithm to use
        scheduler: Scheduler type
        seed: Random seed (-1 for random)
        batch_size: Number of images to generate
        timeout: Maximum time to wait for generation
        
    Returns:
        List of image data as bytes
    """
    # Create workflow
    workflow = create_basic_workflow(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        steps=steps,
        cfg_scale=cfg_scale,
        sampler_name=sampler_name,
        scheduler=scheduler,
        seed=seed,
        batch_size=batch_size
    )
    
    # Queue the prompt
    result = queue_prompt(workflow)
    prompt_id = result.get('prompt_id')
    
    if not prompt_id:
        raise RuntimeError("Failed to get prompt_id from queue response")
    
    logger.info(f"Queued prompt with ID: {prompt_id}")
    
    # Wait for completion
    history = wait_for_completion(prompt_id, timeout=timeout)
    
    # Extract image information
    images = []
    outputs = history.get('outputs', {})
    
    for node_id, node_output in outputs.items():
        if 'images' in node_output:
            for image_info in node_output['images']:
                filename = image_info['filename']
                subfolder = image_info.get('subfolder', '')
                
                # Download the image
                image_data = get_image(filename, subfolder)
                images.append(image_data)
    
    return images


def check_server_status() -> bool:
    """
    Check if ComfyUI server is accessible
    
    Returns:
        True if server is accessible, False otherwise
    """
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except:
        return False
