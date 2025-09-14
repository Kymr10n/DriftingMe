# Noir Preset Configuration

These are the optimized settings for creating film noir style images with the DriftingMe setup. Apply these settings manually in the Automatic1111 WebUI for the best noir aesthetic.

## Manual Setup

1. **Open the WebUI** at http://localhost:7860
2. **Apply these settings** from the noir_preset.json:

### Generation Settings
- **Prompt**: `film noir, high-contrast chiaroscuro lighting, dramatic shadows, rain-soaked city at night, 35mm cinematic, deep blacks, hard rim light, subtle grain, inked outlines, consistent character: 35yo man, short messy dark hair, light stubble, tired eyes, clean composition, storytelling panel, evocative mood`
- **Negative Prompt**: `blurry, low-res, extra fingers, deformed hands, watermark, signature, oversaturated colors, cartoonish, low contrast, flat lighting, text artifacts`
- **Sampling Method**: `DPM++ 2M Karras`
- **Sampling Steps**: `30`
- **CFG Scale**: `7.0`

### Model Recommendation
- Place an SDXL noir/comic-style checkpoint in the `models/Stable-diffusion/` directory
- The current SDXL base model will work, but a specialized noir/comic model will give better results

## Using with Extensions

If you have the **Preset Manager** extension installed:
1. Go to the Extensions tab in WebUI
2. Import the settings from the noir_preset.json file
3. Apply the preset before generating images

## Save as Style

You can save these settings as a style in the WebUI:
1. Enter the prompts and settings above
2. Go to the "Styles" section below the prompt boxes
3. Click "Save Style" and name it "Noir"
4. The style will be available for future use

## Character Consistency Tips

For consistent character generation across multiple images:
- Use the same seed for similar poses
- Consider using ControlNet for pose consistency
- Use img2img for variations of the same character