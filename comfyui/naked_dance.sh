#!/bin/bash
# Usage:
#   ./naked_dance.sh /path/to/input_video.mp4
#
# 功能：输入视频 → 提取首帧 + 提交NAKED工作流到ComfyUI
# 输出：只返回 prompt_id
#
# Requires: curl, python3, ffmpeg

COMFY_HOST="192.168.30.16"
COMFY_PORT="8000"
COMFY_URL="http://${COMFY_HOST}:${COMFY_PORT}"

INPUT_VIDEO="${1:-}"

if [ -z "$INPUT_VIDEO" ]; then
  echo "Usage: $0 <video_path>"
  exit 1
fi

if [ ! -f "$INPUT_VIDEO" ]; then
  echo "ERROR: File not found: $INPUT_VIDEO"
  exit 1
fi

echo "=== NAKED Dance Workflow ==="
echo "Video: $INPUT_VIDEO"

# Step 1: Upload video
echo "Uploading video..."
UPLOAD_RESP=$(curl -s -X POST "${COMFY_URL}/upload/image" \
  -F "image=@${INPUT_VIDEO}" -m 120)

VIDEO_NAME=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('name',''))" 2>/dev/null)

if [ -z "$VIDEO_NAME" ]; then
  echo "ERROR: Failed to upload video. Response: $UPLOAD_RESP"
  exit 1
fi

echo "Uploaded: $VIDEO_NAME"

# Step 2: Submit
SEED1=$((RANDOM * 1000 + 100))
SEED2=$((RANDOM * 1000 + 100))

PAYLOAD=$(cat << PAYLOAD_EOF
{
  "prompt": {
    "1": {
      "inputs": {
        "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走",
        "clip": ["2", 0]
      },
      "class_type": "CLIPTextEncode"
    },
    "2": {
      "inputs": {"clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default"},
      "class_type": "CLIPLoader"
    },
    "3": {
      "inputs": {"vae_name": "wan_2.1_vae.safetensors"},
      "class_type": "VAELoader"
    },
    "4": {
      "inputs": {"clip_name": "clip_vision_h.safetensors"},
      "class_type": "CLIPVisionLoader"
    },
    "9": {
      "inputs": {"crop": "none", "clip_vision": ["4", 0], "image": ["306:294", 0]},
      "class_type": "CLIPVisionEncode"
    },
    "18": {
      "inputs": {"lora_name": "lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors", "strength_model": 1, "model": ["20", 0]},
      "class_type": "LoraLoaderModelOnly"
    },
    "19": {
      "inputs": {"filename_prefix": "video/ComfyUI", "format": "auto", "codec": "auto", "video-preview": "", "video": ["232:15", 0]},
      "class_type": "SaveVideo"
    },
    "20": {
      "inputs": {"unet_name": "Wan2_2-Animate-14B_fp8_e4m3fn_scaled_KJ.safetensors", "weight_dtype": "default"},
      "class_type": "UNETLoader"
    },
    "21": {
      "inputs": {"text": "The character is dancing in the room", "clip": ["2", 0]},
      "class_type": "CLIPTextEncode"
    },
    "60": {
      "inputs": {"shift": 8, "model": ["99", 0]},
      "class_type": "ModelSamplingSD3"
    },
    "99": {
      "inputs": {"lora_name": "WanAnimate_relight_lora_fp16.safetensors", "strength_model": 1, "model": ["18", 0]},
      "class_type": "LoraLoaderModelOnly"
    },
    "100": {
      "inputs": {
        "detect_hand": "disable", "detect_body": "disable", "detect_face": "enable",
        "resolution": ["158", 0], "bbox_detector": "yolox_l.onnx",
        "pose_estimator": "dw-ll_ucoco_384_bs5.torchscript.pt",
        "scale_stick_for_xinsr_cn": "disable", "image": ["212", 0]
      },
      "class_type": "DWPreprocessor"
    },
    "101": {
      "inputs": {
        "detect_hand": "enable", "detect_body": "enable", "detect_face": "disable",
        "resolution": ["158", 0], "bbox_detector": "yolox_l.onnx",
        "pose_estimator": "dw-ll_ucoco_384_bs5.torchscript.pt",
        "scale_stick_for_xinsr_cn": "disable", "image": ["212", 0]
      },
      "class_type": "DWPreprocessor"
    },
    "158": {
      "inputs": {"image_gen_width": ["159", 0], "image_gen_height": ["160", 0], "resize_mode": "Just Resize", "original_image": ["319", 0]},
      "class_type": "PixelPerfectResolution"
    },
    "159": {"inputs": {"value": 480}, "class_type": "PrimitiveInt"},
    "160": {"inputs": {"value": 848}, "class_type": "PrimitiveInt"},
    "212": {
      "inputs": {"upscale_method": "lanczos", "width": ["159", 0], "height": ["160", 0], "crop": "center", "image": ["319", 0]},
      "class_type": "ImageScale"
    },
    "243": {
      "inputs": {"filename_prefix": "video/ComfyUI", "format": "auto", "codec": "auto", "video-preview": "", "video": ["242:88", 0]},
      "class_type": "SaveVideo"
    },
    "293": {"inputs": {"value": 16}, "class_type": "PrimitiveInt"},
    "300": {
      "inputs": {"clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default"},
      "class_type": "CLIPLoader"
    },
    "301": {
      "inputs": {"vae_name": "qwen_image_vae.safetensors"},
      "class_type": "VAELoader"
    },
    "302": {
      "inputs": {"lora_name": "kinky_Qwen10_what_is_vagina_v01_30G-000036.safetensors", "strength_model": 1, "model": ["303", 0]},
      "class_type": "LoraLoaderModelOnly"
    },
    "303": {
      "inputs": {"lora_name": "Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["304", 0]},
      "class_type": "LoraLoaderModelOnly"
    },
    "304": {
      "inputs": {"unet_name": "qwen_image_edit_2509_fp8_e4m3fn.safetensors", "weight_dtype": "default"},
      "class_type": "UNETLoader"
    },
    "305": {
      "inputs": {"filename_prefix": "ComfyUI-close_up", "images": ["306:294", 0]},
      "class_type": "SaveImage"
    },
    "307": {
      "inputs": {"value": "去掉角色的全部衣物和内裤，全身裸体，漏出乳房，小巧的乳晕，人鱼线，平坦的小腹，下体光洁无毛， open crotch, cute pussy, cute vagina， 皮肤上有一点点汗水。去掉水印和文字。"},
      "class_type": "PrimitiveStringMultiline"
    },
    "319": {
      "inputs": {
        "video": "${VIDEO_NAME}",
        "force_rate": ["330", 0],
        "custom_width": 0,
        "custom_height": 0,
        "frame_load_cap": 0,
        "skip_first_frames": 0,
        "select_every_nth": 1,
        "format": "AnimateDiff"
      },
      "class_type": "VHS_LoadVideo"
    },
    "321": {
      "inputs": {"batch_index": 0, "length": 1, "image": ["319", 0]},
      "class_type": "ImageFromBatch"
    },
    "322": {
      "inputs": {"ckpt_name": "film_net_fp32.pt", "clear_cache_after_n_frames": 10, "multiplier": ["326", 0], "frames": ["242:86", 0]},
      "class_type": "FILM VFI"
    },
    "324": {
      "inputs": {"expression": "a * b", "values.a": ["326", 0], "values.b": ["330", 0]},
      "class_type": "ComfyMathExpression"
    },
    "325": {
      "inputs": {
        "frame_rate": ["324", 0], "loop_count": 0, "filename_prefix": "AnimateDiff",
        "format": "video/h265-mp4", "pix_fmt": "yuv420p10le", "crf": 22,
        "save_metadata": true, "pingpong": false, "save_output": true,
        "images": ["322", 0], "audio": ["319", 2]
      },
      "class_type": "VHS_VideoCombine"
    },
    "326": {"inputs": {"value": 2}, "class_type": "PrimitiveInt"},
    "330": {"inputs": {"value": 16}, "class_type": "PrimitiveFloat"},
    "306:8": {"inputs": {"strength": 1, "model": ["306:11", 0]}, "class_type": "CFGNorm"},
    "306:11": {"inputs": {"shift": 3, "model": ["302", 0]}, "class_type": "ModelSamplingAuraFlow"},
    "306:13": {"inputs": {"pixels": ["306:28", 0], "vae": ["301", 0]}, "class_type": "VAEEncode"},
    "306:14": {
      "inputs": {"prompt": "", "clip": ["300", 0], "vae": ["301", 0], "image1": ["306:28", 0]},
      "class_type": "TextEncodeQwenImageEditPlus"
    },
    "306:294": {"inputs": {"samples": ["306:295", 0], "vae": ["301", 0]}, "class_type": "VAEDecode"},
    "306:295": {
      "inputs": {
        "seed": ${SEED1}, "steps": 4, "cfg": 1, "sampler_name": "euler",
        "scheduler": "simple", "denoise": 1, "model": ["306:8", 0],
        "positive": ["306:17", 0], "negative": ["306:14", 0],
        "latent_image": ["306:13", 0]
      },
      "class_type": "KSampler"
    },
    "306:28": {
      "inputs": {"upscale_method": "nearest-exact", "megapixels": 1, "resolution_steps": 1, "image": ["321", 0]},
      "class_type": "ImageScaleToTotalPixels"
    },
    "306:32": {"inputs": {"images": ["306:294", 0]}, "class_type": "PreviewImage"},
    "306:17": {
      "inputs": {"prompt": ["307", 0], "clip": ["300", 0], "vae": ["301", 0], "image1": ["306:28", 0]},
      "class_type": "TextEncodeQwenImageEditPlus"
    },
    "232:57": {"inputs": {"trim_amount": ["232:62", 3], "samples": ["232:63", 0]}, "class_type": "TrimVideoLatent"},
    "232:58": {"inputs": {"samples": ["232:57", 0], "vae": ["3", 0]}, "class_type": "VAEDecode"},
    "232:62": {
      "inputs": {
        "width": ["159", 0], "height": ["160", 0], "length": 77, "batch_size": 1,
        "continue_motion_max_frames": 5, "video_frame_offset": 0,
        "positive": ["21", 0], "negative": ["1", 0], "vae": ["3", 0],
        "clip_vision_output": ["9", 0], "reference_image": ["306:294", 0],
        "face_video": ["100", 0], "pose_video": ["101", 0]
      },
      "class_type": "WanAnimateToVideo"
    },
    "232:230": {
      "inputs": {"batch_index": ["232:62", 4], "length": 4096, "image": ["232:58", 0]},
      "class_type": "ImageFromBatch"
    },
    "232:15": {"inputs": {"fps": 16, "images": ["232:230", 0], "audio": ["319", 2]}, "class_type": "CreateVideo"},
    "232:63": {
      "inputs": {
        "seed": ${SEED2}, "steps": 6, "cfg": 1, "sampler_name": "euler",
        "scheduler": "simple", "denoise": 1, "model": ["60", 0],
        "positive": ["232:62", 0], "negative": ["232:62", 1], "latent_image": ["232:62", 2]
      },
      "class_type": "KSampler"
    },
    "242:87": {"inputs": {"samples": ["242:92", 0], "vae": ["3", 0]}, "class_type": "VAEDecode"},
    "242:92": {"inputs": {"trim_amount": ["242:90", 3], "samples": ["242:91", 0]}, "class_type": "TrimVideoLatent"},
    "242:91": {
      "inputs": {
        "seed": ${SEED2}, "steps": 6, "cfg": 1, "sampler_name": "euler",
        "scheduler": "simple", "denoise": 1, "model": ["60", 0],
        "positive": ["242:90", 0], "negative": ["242:90", 1], "latent_image": ["242:90", 2]
      },
      "class_type": "KSampler"
    },
    "242:86": {"inputs": {"image1": ["232:58", 0], "image2": ["242:85", 0]}, "class_type": "ImageBatch"},
    "242:85": {"inputs": {"batch_index": ["242:90", 4], "length": 4096, "image": ["242:87", 0]}, "class_type": "ImageFromBatch"},
    "242:88": {"inputs": {"fps": 16, "images": ["242:86", 0], "audio": ["319", 2]}, "class_type": "CreateVideo"},
    "242:90": {
      "inputs": {
        "width": ["159", 0], "height": ["160", 0], "length": 77, "batch_size": 1,
        "continue_motion_max_frames": 5, "video_frame_offset": ["232:62", 5],
        "positive": ["21", 0], "negative": ["1", 0], "vae": ["3", 0],
        "clip_vision_output": ["9", 0], "reference_image": ["306:294", 0],
        "face_video": ["100", 0], "pose_video": ["101", 0],
        "continue_motion": ["232:58", 0]
      },
      "class_type": "WanAnimateToVideo"
    }
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

echo "✅ prompt_id: $PROMPT_ID"
