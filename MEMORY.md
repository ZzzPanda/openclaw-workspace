# MEMORY.md - 长期记忆

## 项目

### 游戏资产管道 (Game Asset Pipeline)
- 目标：为2D游戏生成16x16像素武器艺术
- 工具：**Qwen Image API** (通义万相) - 无需浏览器！
- 位置：`~/openclaw/workspace/game/asset/`
- Skill: `~/openclaw/workspace/skills/game-asset-gen/`
- 使用方式：
  ```bash
  uv run ~/openclaw/workspace/skills/game-asset-gen/scripts/generate_asset.py --weapon plasma --variant 01
  ```
- 支持武器：pistol, rifle, sniper, rocket, plasma, shotgun, smg, laser, grenade, medkit

### 已完成
- 2026-02-17: 从豆包切换到 qwen-image，告别浏览器自动化！
- 2026-02-18: 帮主人把泰国行程（4段航班）同步到日历「飞行计划」

---

*最后更新：2026-02-17*
