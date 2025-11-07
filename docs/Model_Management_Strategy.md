# Model Management Strategy for DriftingMe

## Current Issue: Model Duplication
- Models exist in both `checkpoints/` and `Stable-diffusion/` directories
- Total wasted space: ~12.2GB (duplicated SDXL models)

## Recommended Solution: Symlink Strategy

### 1. Keep Master Copies in `checkpoints/`
```bash
# This should be your single source of truth
models/checkpoints/
├── sd_xl_base_1.0.safetensors (6.5GB)
└── sd_xl_refiner_1.0.safetensors (5.7GB)
```

### 2. Create Symlinks for A1111 Compatibility
```bash
# A1111 expects models in Stable-diffusion/
cd models/Stable-diffusion/
rm sd_xl_*.safetensors  # Remove duplicates
ln -s ../checkpoints/sd_xl_base_1.0.safetensors .
ln -s ../checkpoints/sd_xl_refiner_1.0.safetensors .
```

### 3. Directory Structure After Optimization
```
models/
├── checkpoints/ (ComfyUI primary)
│   ├── sd_xl_base_1.0.safetensors [6.5GB - MASTER COPY]
│   └── sd_xl_refiner_1.0.safetensors [5.7GB - MASTER COPY]
├── Stable-diffusion/ (A1111 compatibility)
│   ├── sd_xl_base_1.0.safetensors -> ../checkpoints/sd_xl_base_1.0.safetensors
│   └── sd_xl_refiner_1.0.safetensors -> ../checkpoints/sd_xl_refiner_1.0.safetensors
└── clip_vision/
    └── clip_vision_g.safetensors [3.5GB]
```

## Benefits of This Approach:
1. **Single Source of Truth**: Models stored only once
2. **Space Efficient**: Saves ~12GB of disk space
3. **Consistency**: Updates to master copy reflect everywhere
4. **Container Agnostic**: Both A1111 and ComfyUI see the same files
5. **Easy Maintenance**: Add new models once, link where needed

## Implementation Commands:
```bash
# 1. Remove duplicates in Stable-diffusion/
rm models/Stable-diffusion/sd_xl_*.safetensors

# 2. Create symlinks
ln -s ../checkpoints/sd_xl_base_1.0.safetensors models/Stable-diffusion/
ln -s ../checkpoints/sd_xl_refiner_1.0.safetensors models/Stable-diffusion/

# 3. Verify symlinks work
ls -la models/Stable-diffusion/
```

## Future Model Management:
- Download new models to `models/checkpoints/`
- Create symlinks as needed for specific container requirements
- Use this pattern for LoRAs, VAEs, etc.