#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
#     "Pillow>=10.0.0",
# ]
# ///
"""
Generate 16x16 pixel game asset sprites using Qwen Image API.

Usage:
    uv run generate_asset.py --weapon pistol --variant 01
"""

import argparse
import os
import sys
import json
import uuid
from pathlib import Path
from PIL import Image
import requests

# Weapon prompt templates
WEAPON_PROMPTS = {
    "pistol": "A simple pixel art handgun, side view, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges, weapon pointing right",
    "rifle": "A simple pixel art assault rifle, side view, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges, weapon pointing right",
    "sniper": "A simple pixel art sniper rifle, side view, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges, long barrel, weapon pointing right",
    "rocket": "A simple pixel art rocket launcher, side view, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges, weapon pointing right",
    "plasma": "A simple pixel art plasma rifle, side view, glowing cyan energy elements, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges, sci-fi weapon pointing right",
    "shotgun": "A simple pixel art shotgun, side view, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges, weapon pointing right",
    "smg": "A simple pixel art submachine gun, side view, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges, weapon pointing right",
    "laser": "A simple pixel art laser sword, side view, glowing cyan blade, black handle on transparent background, 16x16 pixels, retro game sprite, clean edges",
    "grenade": "A simple pixel art hand grenade, oval shape with pin, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges",
    "medkit": "A simple pixel art medical kit, white box with red cross, black silhouette on transparent background, 16x16 pixels, retro game sprite, clean edges",
}

DEFAULT_NEGATIVE = "color, colored, realistic, photorealistic, 3D, high detail, noise, blur, watermark, text, letters, background"

OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "game" / "asset"

def get_api_key() -> str | None:
    """Get API key from environment."""
    return os.environ.get("DASHSCOPE_API_KEY")

def generate_with_qwen(prompt: str, output_path: str, no_verify_ssl: bool = False) -> str | None:
    """Generate image using Qwen Image API."""
    api_key = get_api_key()
    if not api_key:
        print("Error: No DASHSCOPE_API_KEY found.", file=sys.stderr)
        return None
    
    # Use proxy if available
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
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ]
        },
        "parameters": {
            "negative_prompt": DEFAULT_NEGATIVE,
            "prompt_extend": True,
            "watermark": False,
            "size": "1024*1024"
        }
    }
    
    print(f"Generating image with Qwen Image API...")
    
    try:
        # Make API request
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

        print(f"Response status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response text: {response.text[:1000]}", file=sys.stderr)
            response.raise_for_status()
        
        result = response.json()
        
        if result.get("code"):
            print(f"API Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
            print(f"Full response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
            return None
        
        choices = result.get("output", {}).get("choices", [])
        if not choices:
            print("Error: No image in response", file=sys.stderr)
            return None
        
        image_url = choices[0]["message"]["content"][0]["image"]
        
        # Download image
        img_response = requests.get(image_url, timeout=30, proxies=proxies, verify=not no_verify_ssl)
        img_response.raise_for_status()
        
        # Save temp file
        temp_path = f"/tmp/qwen_temp_{uuid.uuid4().hex}.png"
        with open(temp_path, "wb") as f:
            f.write(img_response.content)
        
        # Resize to 16x16 using PIL
        print("Resizing to 16x16...")
        img = Image.open(temp_path)
        img = img.resize((16, 16), Image.NEAREST)  # Use NEAREST for pixel art
        img.save(output_path)
        
        # Clean up temp
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return output_path
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        try:
            error_detail = response.json()
            print(f"Error details: {json.dumps(error_detail, indent=2, ensure_ascii=False)}", file=sys.stderr)
        except:
            print(f"Response text: {response.text[:500]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate 16x16 pixel game assets")
    parser.add_argument("--weapon", "-w", required=True, help="Weapon type (pistol, rifle, etc.)")
    parser.add_argument("--variant", "-v", default="01", help="Variant number (01, 02, etc.)")
    parser.add_argument("--prompt", "-p", help="Custom prompt (overrides weapon default)")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Skip SSL verification")
    
    args = parser.parse_args()
    
    weapon = args.weapon.lower()
    
    # Get prompt
    if args.prompt:
        prompt = args.prompt
    elif weapon in WEAPON_PROMPTS:
        prompt = WEAPON_PROMPTS[weapon]
    else:
        print(f"Unknown weapon: {weapon}", file=sys.stderr)
        print(f"Available: {', '.join(WEAPON_PROMPTS.keys())}", file=sys.stderr)
        sys.exit(1)
    
    # Output path
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = f"{weapon}_{args.variant}.png"
    output_path = OUTPUT_DIR / output_file
    
    print(f"Generating {weapon} variant {args.variant}...")
    print(f"Prompt: {prompt}")
    
    result = generate_with_qwen(prompt, str(output_path), args.no_verify_ssl)
    
    if result:
        print(f"\nGenerated: {output_path}")
        print(f"MEDIA: {output_path}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
