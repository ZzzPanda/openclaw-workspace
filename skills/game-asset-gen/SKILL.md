---
name: game-asset-gen
description: Generate 16x16 pixel game assets (weapons, items) using Qwen Image API. No browser required.
homepage: https://dashscope.aliyuncs.com/
metadata: {"openclaw":{"emoji":"⚔️","requires":{"bins":["uv"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Game Asset Generator

Generate 16x16 pixel weapon/item sprites for 2D games using Qwen Image API. No browser automation required!

## Usage

生成武器精灵图：
```
生成一个 16x16 像素武器: pistol
```

支持的武器类型：
- `pistol` - 手枪
- `rifle` - 步枪
- `sniper` - 狙击枪
- `rocket` - 火箭筒
- `plasma` - 等离子步枪
- `shotgun` - 霰弹枪
- `smg` - 冲锋枪
- `laser` - 激光剑
- `grenade` - 手雷
- `medkit` - 医疗包

## 命令

```bash
# 生成武器
uv run ~/openclaw/workspace/skills/game-asset-gen/scripts/generate_asset.py --weapon pistol

# 指定变体 (01, 02, 03...)
uv run ~/openclaw/workspace/skills/game-asset-gen/scripts/generate_asset.py --weapon rifle --variant 02

# 自定义提示词
uv run ~/openclaw/workspace/skills/game-asset-gen/scripts/generate_asset.py --weapon custom --prompt "your custom prompt"
```

## 工作流

1. 使用 qwen-image API 生成 1024x1024 图像
2. 用 PIL 缩小到 16x16（使用 NEAREST 插值保持像素风格）
3. 保存到 `~/openclaw/workspace/game/asset/[weapon]_[variant].png`

## 输出位置

所有生成的资产保存在：`~/openclaw/workspace/game/asset/`

示例文件名：
- `pistol_01.png`
- `plasma_02.png`
- `sniper_01.png`
