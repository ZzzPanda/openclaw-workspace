# ComfyUI Workflows

All saved workflows for `192.168.30.19:8000`.

---

## sdxl-nsfw-real

**File:** `sdxl-nsfw-real.json`
**Script:** `sdxl-nsfw-real.sh`
**Type:** Image Generation (SDXL + FaceDetailer)

**Models:**
- Checkpoint: `cyberillustrious_v50.safetensors` (main)
- Checkpoint: `fucktastic25DCheckpointPony_10.safetensors` (FaceDetailer)
- LoRAs: `add-detail-xl`, `ThiccPonyXL_V1`, `amateur_style_v1_pony`, `RealSkin_xxXL_v1`, `Pony Realism Slider`, `Sarah_Lady2_epoch_9`
- SAM: `sam_vit_b_01ec64.pth`
- Face detection: `bbox/face_yolov8m.pt`

**Run:**
```bash
# Default prompt
./sdxl-nsfw-real.sh

# Custom prompt
./sdxl-nsfw-real.sh "your positive prompt text"

# Custom pos + neg
./sdxl-nsfw-real.sh "pos text" "neg text"

# Fixed seed
SEED_PRIMARY=1234 ./sdxl-nsfw-real.sh
```

**Output:** `~/.openclaw/media/outbound/comfy_output.png`
**Approx time:** 30-60s

---

## sdxl-i2v-wan

**File:** `sdxl-i2v-wan.json`
**Script:** `sdxl-i2v-wan.sh`
**Type:** Image-to-Video (Wan 2.2 I2V)

**Models:**
- Unet: `Wan2.2-I2V-A14B-HighNoise-Q4_K_M.gguf` + `Wan2.2-I2V-A14B-LowNoise-Q4_K_M.gguf`
- VAE: `wan_2.1_vae.safetensors`
- CLIP: `umt5-xxl-encoder-Q8_0.gguf`

**Run:**
```bash
# Upload image + generate video
./sdxl-i2v-wan.sh /path/to/image.jpg

# Custom prompts
./sdxl-i2v-wan.sh /path/to/image.jpg "your positive" "your negative"

# Change FPS (default 24)
FPS=30 ./sdxl-i2v-wan.sh /path/to/image.jpg
```

**Output:** `~/.openclaw/media/outbound/comfy_video.mp4`
**Approx time:** 2-5 min

---
