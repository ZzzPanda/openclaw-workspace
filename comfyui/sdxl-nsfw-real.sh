#!/bin/bash
# Usage:
#   ./comfy_run.sh                         - run with default prompt
#   ./comfy_run.sh "your positive prompt" - run with custom prompt
#   ./comfy_run.sh "pos" "neg"           - custom positive + negative
#
# The script sends a workflow to ComfyUI at 192.168.30.16:8000,
# waits for completion, downloads the output image, and copies it to:
#   ~/.openclaw/media/outbound/comfy_output.png
#
# Requires: curl, python3

COMFY_HOST="192.168.30.16"
COMFY_PORT="8000"
COMFY_URL="http://${COMFY_HOST}:${COMFY_PORT}"

OUTBOUND_DIR="$HOME/.openclaw/media/outbound"
mkdir -p "$OUTBOUND_DIR"

# Default prompts
POSITIVE="${1:-score_9, score_8_up, score_7_up, BREAK, woman, blonde hair, hot, top view, head looks back, chest down, ass up, all fours, male pov, male hands, spreading pussy, ass focus, skin pores, on the floor, in front of big glass ceiling to floor window, night city, sun tan, sweat, neon light, lens flare, highly detailed, detailed skin, depth of field, film grain, sexy, interior}"
NEGATIVE="${2:-score_6, score_5, score_4, tan line, muscular, censored, furry, child, kid, teen, chibi, watermark, text, verybadimagenegative_v1.3, boring composition, boring perspective, simple background, source_pony, bad_hands, bad_feet, deformed, malformed, missing_limbs, extra_limbs, missing_digits, missing_fingers, bad_fingers, simple background, white background, realistic, 2d, birthmarks, spots, moles, 2girls, multiple girls}"

SEED_PRIMARY=${SEED_PRIMARY:-$((RANDOM * 1000 + 100))}
SEED_FACEDETAILER=${SEED_FACEDETAILER:-$((RANDOM * 1000 + 100))}
SEED_SECONDARY=${SEED_SECONDARY:-$((RANDOM * 1000 + 100))}

echo "=== ComfyUI Workflow Runner ==="
echo "Host: $COMFY_URL"
echo "Positive: ${POSITIVE:0:80}..."
echo "Seeds: primary=$SEED_PRIMARY facedetailer=$SEED_FACEDETAILER secondary=$SEED_SECONDARY"
echo ""

# Build JSON payload
PAYLOAD=$(cat << PAYLOAD_EOF
{
  "prompt": {
    "210": {"inputs": {"ckpt_name": "cyberillustrious_v50.safetensors"}, "class_type": "CheckpointLoaderSimple"},
    "211": {"inputs": {"width": 1024, "aspect_ratio": "3:2", "direction": "Vertical", "info": "Example widths: 512, 768, 1024, 1280, 1920"}, "class_type": "AspectRatioImageSize"},
    "214": {"inputs": {"text": "$POSITIVE", "clip": ["245", 1]}, "class_type": "CLIPTextEncode"},
    "215": {"inputs": {"text": "$NEGATIVE", "clip": ["245", 1]}, "class_type": "CLIPTextEncode"},
    "216": {"inputs": {"seed": $SEED_PRIMARY, "steps": 35, "cfg": 6.0, "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0, "model": ["245", 0], "positive": ["214", 0], "negative": ["215", 0], "latent_image": ["217", 0]}, "class_type": "KSampler"},
    "217": {"inputs": {"width": ["211", 0], "height": ["211", 1], "batch_size": 1}, "class_type": "EmptyLatentImage"},
    "219": {"inputs": {"samples": ["216", 0], "vae": ["210", 2]}, "class_type": "VAEDecode"},
    "245": {"inputs": {"lora_1": {"on": true, "lora": "add-detail-xl.safetensors", "strength": 1.3}, "lora_2": {"on": true, "lora": "ThiccPonyXL_V1.safetensors", "strength": 0.28}, "lora_3": {"on": true, "lora": "Civit\\\\amateur_style_v1_pony.safetensors", "strength": 1.25}, "lora_4": {"on": true, "lora": "Civit\\\\RealSkin_xxXL_v1.safetensors", "strength": 1.6}, "lora_5": {"on": true, "lora": "Civit\\\\Pony Realism Slider.safetensors", "strength": 1.6}, "lora_6": {"on": true, "lora": "Sarah SDXL\\\\Sarah SDXL\\\\Sarah_Lady2_epoch_9.safetensors", "strength": 1}, "model": ["210", 0], "clip": ["246", 0]}, "class_type": "Power Lora Loader (rgthree)"},
    "246": {"inputs": {"stop_at_clip_layer": -2, "clip": ["210", 1]}, "class_type": "CLIPSetLastLayer"},
    "247": {"inputs": {"samples": ["253", 0], "vae": ["210", 2]}, "class_type": "VAEDecode"},
    "249": {"inputs": {"model_name": "sam_vit_b_01ec64.pth", "device_mode": "AUTO"}, "class_type": "SAMLoader"},
    "250": {"inputs": {"model_name": "bbox/face_yolov8m.pt"}, "class_type": "UltralyticsDetectorProvider"},
    "251": {"inputs": {"filename_prefix": "XXX/IMAGES/0", "images": ["254", 0]}, "class_type": "SaveImage"},
    "253": {"inputs": {"seed": $SEED_SECONDARY, "steps": 20, "cfg": 7.0, "sampler_name": "dpmpp_sde", "scheduler": "karras", "denoise": 0.45, "model": ["256", 0], "positive": ["214", 0], "negative": ["215", 0], "latent_image": ["259", 0]}, "class_type": "KSampler"},
    "254": {"inputs": {"guide_size": 1152.0, "guide_size_for": true, "max_size": 1152.0, "seed": $SEED_FACEDETAILER, "steps": 31, "cfg": 7.0, "sampler_name": "dpmpp_sde", "scheduler": "karras", "denoise": 0.44, "feather": 4, "noise_mask": true, "force_inpaint": false, "bbox_threshold": 0.5, "bbox_dilation": 8, "bbox_crop_factor": 1.5, "sam_detection_hint": "center-1", "sam_dilation": 0, "sam_threshold": 0.93, "sam_bbox_expansion": 0, "sam_mask_hint_threshold": 0.7, "sam_mask_hint_use_negative": "False", "drop_size": 10, "wildcard": "", "cycle": 1, "inpaint_model": false, "noise_mask_feather": 2, "tiled_encode": false, "tiled_decode": false, "image": ["247", 0], "model": ["256", 0], "clip": ["256", 1], "vae": ["256", 2], "positive": ["214", 0], "negative": ["215", 0], "bbox_detector": ["250", 0], "sam_model_opt": ["249", 0]}, "class_type": "FaceDetailer"},
    "256": {"inputs": {"ckpt_name": "fucktastic25DCheckpointPony_10.safetensors"}, "class_type": "CheckpointLoaderSimple"},
    "259": {"inputs": {"pixels": ["260", 0], "vae": ["256", 2]}, "class_type": "VAEEncode"},
    "260": {"inputs": {"width": 1500, "height": 1500, "upscale_method": "nearest-exact", "keep_proportion": "resize", "pad_color": "0, 0, 0", "crop_position": "center", "divisible_by": 2, "device": "cpu", "image": ["219", 0]}, "class_type": "ImageResizeKJv2"}
  },
  "client_id": "openclaw-script"
}
PAYLOAD_EOF
)

# Submit workflow
echo "Submitting workflow..."
RESPONSE=$(curl -s -X POST "${COMFY_URL}/prompt" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  -m 30)

echo "Raw response: $RESPONSE"

PROMPT_ID=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('prompt_id',''))" 2>/dev/null)

if [ -z "$PROMPT_ID" ]; then
  echo "ERROR: Failed to submit workflow. Check response above."
  exit 1
fi

echo "Prompt ID: $PROMPT_ID"
echo "Waiting for completion (this takes ~30-60s)..."

# Poll for completion
MAX_WAIT=180
INTERVAL=10
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))

  STATUS=$(curl -s "${COMFY_URL}/api/history/${PROMPT_ID}" -m 10 | python3 -c "import json,sys; d=json.load(sys.stdin); e=d.get('${PROMPT_ID}',{}); print(e.get('status',{}).get('status_str','unknown'))" 2>/dev/null)

  if [ "$STATUS" = "success" ]; then
    echo "✅ Done! Downloading output..."

    # Get output filename
    FILENAME=$(curl -s "${COMFY_URL}/api/history/${PROMPT_ID}" -m 10 | python3 -c "
import json,sys
d=json.load(sys.stdin)
e=d.get('${PROMPT_ID}',{})
outputs=e.get('outputs',{})
node251=outputs.get('251',{})
images=node251.get('images',[])
if images:
    print(images[0].get('filename',''))
" 2>/dev/null)

    if [ -n "$FILENAME" ]; then
      # Handle both forward slash and backslash in subfolder path
      SUBFOLDER_ESCAPED="XXX%5CIMAGES"
      curl -s "${COMFY_URL}/api/view?filename=${FILENAME}&subfolder=${SUBFOLDER_ESCAPED}" \
        -o "${OUTBOUND_DIR}/comfy_output.png" -m 60

      SIZE=$(wc -c < "${OUTBOUND_DIR}/comfy_output.png")
      if [ "$SIZE" -gt 1000 ]; then
        echo "✅ Image saved: ${OUTBOUND_DIR}/comfy_output.png (${SIZE} bytes)"
        echo ""
        echo "Next step: use message tool to send this file to Feishu:"
        echo "  filePath: ${OUTBOUND_DIR}/comfy_output.png"
        exit 0
      else
        echo "⚠️ Downloaded file too small (${SIZE} bytes), may have failed"
        exit 1
      fi
    fi
  elif [ "$STATUS" = "failed" ]; then
    echo "❌ Workflow failed"
    exit 1
  fi

  echo "  Still running... (${ELAPSED}s elapsed, status=$STATUS)"
done

echo "⚠️ Timeout after ${MAX_WAIT}s"
exit 1
