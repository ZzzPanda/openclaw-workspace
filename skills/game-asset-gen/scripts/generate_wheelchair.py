#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
#     "Pillow>=10.0.0",
# ]
# ///
"""
Generate 8-directional pixel art sprite sheet for a high-tech wheelchair using Qwen Image API.

Standard 3x3 layout:
  left_bottom  bottom  right_bottom
  left         front   right
  left_top     top     right_top

Usage:
    uv run generate_wheelchair.py --size 64 --variant 02
"""

import argparse
import os
import sys
import json
import uuid
from pathlib import Path
from PIL import Image, ImageOps
import requests
from io import BytesIO

# 8 directions in standard 3x3 layout order (left to right, bottom to top)
# This matches common game engine expectations
DIRECTIONS_LAYOUT = [
    ("left_bottom", "A pixel art high-tech wheelchair, side view facing left-bottom diagonal, glowing cyan LED lights, futuristic design, clean white and silver metal, small wheels, retro game sprite, 16-bit style, transparent background"),
    ("bottom", "A pixel art high-tech wheelchair, back view, glowing cyan LED lights, futuristic design, clean white and silver metal, small wheels, retro game sprite, 16-bit style, transparent background"),
    ("right_bottom", "A pixel art high-tech wheelchair, side view facing right-bottom diagonal, glowing cyan LED lights, futuristic design, clean white and silver metal, small wheels, retro game sprite, 16-bit style, transparent background"),
    
    ("left", "A pixel art high-tech wheelchair, left side view, glowing cyan LED lights, futuristic design, clean white and silver metal, visible wheel mechanism, retro game sprite, 16-bit style, transparent background"),
    ("front", "A pixel art high-tech wheelchair, front view, glowing cyan LED lights, futuristic design, clean white and silver metal, transparent display, retro game sprite, 16-bit style, transparent background"),
    ("right", "A pixel art high-tech wheelchair, right side view, glowing cyan LED lights, futuristic design, clean white and silver metal, visible wheel mechanism, retro game sprite, 16-bit style, transparent background"),
    
    ("left_top", "A pixel art high-tech wheelchair, side view facing left-top diagonal (like facing left but slightly away), glowing cyan LED lights, futuristic design, clean white and silver metal, retro game sprite, 16-bit style, transparent background"),
    ("top", "A pixel art high-tech wheelchair, front view facing away (back view), glowing cyan LED lights, futuristic design, clean white and silver metal, retro game sprite, 16-bit style, transparent background"),
    ("right_top", "A pixel art high-tech wheelchair, side view facing right-top diagonal, glowing cyan LED lights, futuristic design, clean white and silver metal, retro game sprite, 16-bit style, transparent background"),
]

# Alternative simpler prompts focusing on pixel art
PIXEL_ART_PROMPTS = {
    "front": "Pixel art high-tech wheelchair, front view, glowing cyan LED lights, futuristic sleek design, white and silver metal body, small wheels, 16x16 sprite, transparent background, clean pixel art, game asset",
    "front_right": "Pixel art high-tech wheelchair, 3/4 front view right, glowing cyan LED lights, futuristic sleek design, white and silver metal body, 16x16 sprite, transparent background, clean pixel art, game asset",
    "right": "Pixel art high-tech wheelchair, right side view, glowing cyan LED lights, futuristic sleek design, white and silver metal body, visible wheel, 16x16 sprite, transparent background, clean pixel art, game asset",
    "back_right": "Pixel art high-tech wheelchair, 3/4 back view right, glowing cyan LED lights, futuristic sleek design, white and silver metal body, 16x16 sprite, transparent background, clean pixel art, game asset",
    "back": "Pixel art high-tech wheelchair, back view, glowing cyan LED lights, futuristic sleek design, white and silver metal body, rear wheel visible, 16x16 sprite, transparent background, clean pixel art, game asset",
    "back_left": "Pixel art high-tech wheelchair, 3/4 back view left, glowing cyan LED lights, futuristic sleek design, white and silver metal body, 16x16 sprite, transparent background, clean pixel art, game asset",
    "left": "Pixel art high-tech wheelchair, left side view, glowing cyan LED lights, futuristic sleek design, white and silver metal body, visible wheel, 16x16 sprite, transparent background, clean pixel art, game asset",
    "front_left": "Pixel art high-tech wheelchair, 3/4 front view left, glowing cyan LED lights, futuristic sleek design, white and silver metal body, 16x16 sprite, transparent background, clean pixel art, game asset",
}

DEFAULT_NEGATIVE = "low quality, blurry, dark, dirty, rusty, broken, old, vintage, realistic, photo, 3D, watermark, text, letters, high resolution, detailed"

OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "game" / "asset"

def get_api_key() -> str | None:
    return os.environ.get("DASHSCOPE_API_KEY")

def generate_with_qwen(prompt: str, no_verify_ssl: bool = False) -> Image.Image | None:
    """Generate image using Qwen Image API."""
    api_key = get_api_key()
    if not api_key:
        print("Error: No DASHSCOPE_API_KEY found.", file=sys.stderr)
        return None
    
    proxies = None
    if os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY"):
        proxies = {
            "http": os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY"),
            "https": os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
        }
    
    payload = {
        "model": "qwen-image-max",
        "input": {
            "messages": [
                {"role": "user", "content": [{"text": prompt}]}
            ]
        },
        "parameters": {
            "negative_prompt": DEFAULT_NEGATIVE,
            "prompt_extend": False,  # Disable for more predictable results
            "watermark": False,
            "size": "1024*1024"
        }
    }
    
    try:
        response = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json=payload,
            timeout=120,
            proxies=proxies,
            verify=not no_verify_ssl
        )

        if response.status_code != 200:
            print(f"Error: {response.text[:300]}", file=sys.stderr)
            return None
        
        result = response.json()
        if result.get("code"):
            print(f"API Error: {result.get('message')}", file=sys.stderr)
            return None
        
        image_url = result["output"]["choices"][0]["message"]["content"][0]["image"]
        img_response = requests.get(image_url, timeout=30, proxies=proxies, verify=not no_verify_ssl)
        img = Image.open(BytesIO(img_response.content))
        return img
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate 8-directional pixel art wheelchair sprite sheet")
    parser.add_argument("--size", "-s", type=int, default=64, help="Output size per direction (default: 64)")
    parser.add_argument("--variant", "-v", default="01", help="Variant number")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Skip SSL verification")
    
    args = parser.parse_args()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating 8-directional pixel art wheelchair (size: {args.size})...")
    
    # Generate all 8 directions
    images = {}
    success_count = 0
    
    for direction, prompt in PIXEL_ART_PROMPTS.items():
        print(f"Generating {direction}...")
        img = generate_with_qwen(prompt, args.no_verify_ssl)
        
        if img:
            # Resize to target size with pixel-perfect scaling
            img = img.resize((args.size, args.size), Image.NEAREST)
            images[direction] = img
            success_count += 1
            print(f"  ✓ {direction}")
        else:
            print(f"  ✗ {direction} - failed")
    
    print(f"\nSuccess: {success_count}/8")
    
    if success_count == 0:
        print("All generations failed!")
        sys.exit(1)
    
    # Create sprite sheet in standard 3x3 layout (with empty center or use front)
    # Layout: top row: left_top, top, right_top (not used)
    #         middle row: left, front, right  
    #         bottom row: left_bottom, bottom, right_bottom (not used)
    # We'll use 3x3 with empty corners for standard 8-direction
    
    cols = 4  # Using 4x2: left, front, right, and diagonals in second row
    rows = 2  # Actually let's do 4 columns, 2 rows
    
    # Better layout: 4x2 grid
    # Row 1: left, front_left, front, front_right, right
    # Actually standard is often: front, front_right, right, back_right, back, back_left, left, front_left
    
    # Let's do 4 columns x 2 rows (8 cells)
    # Order: front, front_right, right, back_right, back, back_left, left, front_left
    
    direction_order = ["front", "front_right", "right", "back_right", "back", "back_left", "left", "front_left"]
    
    sheet_width = cols * args.size
    sheet_height = rows * args.size
    
    sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
    
    for i, direction in enumerate(direction_order):
        if direction in images:
            row = i // cols
            col = i % cols
            x = col * args.size
            y = row * args.size
            sheet.paste(images[direction], (x, y))
    
    # Save sprite sheet
    output_file = f"wheelchair_{args.variant}_8dir.png"
    output_path = OUTPUT_DIR / output_file
    sheet.save(output_path)
    
    print(f"\nSprite sheet: {output_path}")
    print(f"Layout ({cols}x{rows}): {direction_order}")
    print(f"\nMEDIA: {output_path}")

if __name__ == "__main__":
    main()
