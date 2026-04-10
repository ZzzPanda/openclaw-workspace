#!/bin/bash
# Usage:
#   ./sdxl-i2v-wan.sh /path/to/image.jpg [positive_prompt] [negative_prompt]
#
# Defaults:
#   Positive: "A girl standing in front of viewer, all her clothes explode magically
#             into many tiny little red roses debris, and then blowed by the wind
#             and fade away quickly. and her naked body, hairless pussy, and
#             large breasts revealed"
#   Negative: Chinese quality prompts
#
# Requires: curl, python3
# Output:   ~/.openclaw/media/outbound/comfy_video.mp4

COMFY_HOST="192.168.30.16"
COMFY_PORT="8000"
COMFY_URL="http://${COMFY_HOST}:${COMFY_PORT}"
OUTBOUND_DIR="$HOME/.openclaw/media/outbound"
mkdir -p "$OUTBOUND_DIR"

INPUT_IMAGE="${1:-}"
POSITIVE="${2:-A girl standing in front of viewer, all her clothes explode magically into many tiny little red roses debris, and then blowed by the wind and fade away quickly. and her naked body, hairless pussy, and large breasts revealed}"
NEGATIVE="${3:-}"
FPS="${FPS:-24}"

if [ -z "$INPUT_IMAGE" ]; then
  echo "Usage: $0 <image_path> [positive_prompt] [negative_prompt]"
  exit 1
fi

if [ ! -f "$INPUT_IMAGE" ]; then
  echo "ERROR: File not found: $INPUT_IMAGE"
  exit 1
fi

echo "=== ComfyUI Wan Image-to-Video ==="
echo "Image: $INPUT_IMAGE"
echo ""

# Step 1: Upload image
echo "Uploading image..."
UPLOAD_RESP=$(curl -s -X POST "${COMFY_URL}/upload/image" \
  -F "image=@${INPUT_IMAGE}" -m 30)

echo "Upload response: $UPLOAD_RESP"

IMAGE_NAME=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('name',''))" 2>/dev/null)

if [ -z "$IMAGE_NAME" ]; then
  echo "ERROR: Failed to upload image"
  exit 1
fi

echo "Uploaded as: $IMAGE_NAME"
echo ""

# Default negative prompt (Chinese quality terms)
if [ -z "$NEGATIVE" ]; then
  NEGATIVE="色彩艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，移动过快，抖动，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，形态畸形的肢体，畸形的性器官，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走"
fi

SEED1=$((RANDOM * 1000 + 100))
SEED2=$((RANDOM * 1000 + 100))
echo "Seeds: $SEED1 / $SEED2"

# Build payload
PAYLOAD=$(cat << PAYLOAD_EOF
{
  "prompt": {
    "6": {"inputs": {"text": "$POSITIVE", "clip": ["69", 0]}, "class_type": "CLIPTextEncode"},
    "7": {"inputs": {"text": "$NEGATIVE", "clip": ["69", 0]}, "class_type": "CLIPTextEncode"},
    "8": {"inputs": {"samples": ["58", 0], "vae": ["39", 0]}, "class_type": "VAEDecode"},
    "39": {"inputs": {"vae_name": "wan_2.1_vae.safetensors"}, "class_type": "VAELoader"},
    "54": {"inputs": {"shift": 8.0, "model": ["67", 0]}, "class_type": "ModelSamplingSD3"},
    "55": {"inputs": {"shift": 8.0, "model": ["68", 0]}, "class_type": "ModelSamplingSD3"},
    "57": {"inputs": {"add_noise": "enable", "noise_seed": $SEED1, "steps": 20, "cfg": 3.5, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 10, "return_with_leftover_noise": "enable", "model": ["54", 0], "positive": ["63", 0], "negative": ["63", 1], "latent_image": ["63", 2]}, "class_type": "KSamplerAdvanced"},
    "58": {"inputs": {"add_noise": "disable", "noise_seed": 0, "steps": 20, "cfg": 3.5, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 10, "end_at_step": 10000, "return_with_leftover_noise": "disable", "model": ["55", 0], "positive": ["63", 0], "negative": ["63", 1], "latent_image": ["57", 0]}, "class_type": "KSamplerAdvanced"},
    "60": {"inputs": {"fps": $FPS, "images": ["8", 0]}, "class_type": "CreateVideo"},
    "61": {"inputs": {"filename_prefix": "video/ComfyUI", "format": "auto", "codec": "auto"}, "class_type": "SaveVideo"},
    "63": {"inputs": {"width": 480, "height": 832, "length": 73, "batch_size": 1, "positive": ["6", 0], "negative": ["7", 0], "vae": ["39", 0], "start_image": ["70", 0]}, "class_type": "WanImageToVideo"},
    "67": {"inputs": {"unet_name": "Wan2.2-I2V-A14B-HighNoise-Q4_K_M.gguf"}, "class_type": "UnetLoaderGGUF"},
    "68": {"inputs": {"unet_name": "Wan2.2-I2V-A14B-LowNoise-Q4_K_M.gguf"}, "class_type": "UnetLoaderGGUF"},
    "69": {"inputs": {"clip_name": "umt5-xxl-encoder-Q8_0.gguf", "type": "wan"}, "class_type": "CLIPLoaderGGUF"},
    "70": {"inputs": {"image": "$IMAGE_NAME"}, "class_type": "LoadImage"}
  },
  "client_id": "openclaw-script"
}
PAYLOAD_EOF
)

echo "Submitting workflow..."
RESPONSE=$(curl -s -X POST "${COMFY_URL}/prompt" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" -m 30)

PROMPT_ID=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('prompt_id',''))" 2>/dev/null)

if [ -z "$PROMPT_ID" ]; then
  echo "ERROR: Failed to submit. Response: $RESPONSE"
  exit 1
fi

echo "Prompt ID: $PROMPT_ID"
echo "Waiting for completion (~2-5 min)..."

MAX_WAIT=600
INTERVAL=15
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))

  STATUS=$(curl -s "${COMFY_URL}/api/history/${PROMPT_ID}" -m 10 | python3 -c "
import json,sys
d=json.load(sys.stdin)
e=d.get('${PROMPT_ID}',{})
print(e.get('status',{}).get('status_str','unknown'))
" 2>/dev/null)

  if [ "$STATUS" = "success" ]; then
    echo "✅ Done! Downloading video..."

    FILENAME=$(curl -s "${COMFY_URL}/api/history/${PROMPT_ID}" -m 10 | python3 -c "
import json,sys
d=json.load(sys.stdin)
e=d.get('${PROMPT_ID}',{})
outputs=e.get('outputs',{})
node61=outputs.get('61',{})
vids=node61.get('videos', node61.get('images',[]))
if vids:
    print(vids[0].get('filename',''))
" 2>/dev/null)

    if [ -n "$FILENAME" ]; then
      curl -s "${COMFY_URL}/api/view?filename=${FILENAME}&subfolder=video" \
        -o "${OUTBOUND_DIR}/comfy_video.mp4" -m 120

      SIZE=$(wc -c < "${OUTBOUND_DIR}/comfy_video.mp4")
      if [ "$SIZE" -gt 10000 ]; then
        echo "✅ Video saved: ${OUTBOUND_DIR}/comfy_video.mp4 (${SIZE} bytes)"
        exit 0
      fi
    fi
  elif [ "$STATUS" = "failed" ]; then
    echo "❌ Workflow failed"
    exit 1
  fi

  echo "  Still running... (${ELAPSED}s)"
done

echo "⚠️ Timeout after ${MAX_WAIT}s"
exit 1
