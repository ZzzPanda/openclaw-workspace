---
name: doubao-gen
description: Use Doubao (豆包) AI to generate images for game assets. Activated when user wants to generate pixel art, game sprites, or AI images via Doubao. Workflow: open Doubao → enter image generation → input prompt → download result.
---

# Doubao Image Generation

Generate images using Doubao's AI image generation feature.

## Workflow

1. **Open Doubao**
   ```python
   browser(action="open", profile="chrome", targetUrl="https://www.doubao.com")
   ```

2. **Navigate to Image Generation**
   - Click "图像生成" button in the sidebar
   - Or navigate directly to: `https://www.doubao.com/chat/create-image`

3. **Enter Prompt**
   - Use the textbox to enter your prompt
   - For pixel art: include "像素画", "16x16", "游戏素材", "透明背景" etc.

4. **Generate**
   - Click the generate button (right arrow icon)

5. **Download Image**
   - Click on the generated image to open preview
   - Extract image URL via JavaScript:
     ```javascript
     document.querySelector('img[alt="preview"]')?.src
     ```
   - Download using curl:
     ```bash
     curl -L -o <output_path> "<image_url>"
     ```

## Pixel Art Tips

- Include "像素画" or "pixel art" in prompt
- Specify resolution: "16x16", "32x32", "64x64"
- Add "游戏素材", "sprite", "透明背景" for game use
- For style: "精灵风格", "8-bit", "复古"

## Default Asset Directory

```
/Users/roger/.openclaw/workspace/game/asset/
```

## Quick Download Command

```bash
curl -L -o /Users/roger/.openclaw/workspace/game/asset/<filename> "<url>"
```
