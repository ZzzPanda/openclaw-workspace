# MEMORY.md - 长期记忆

### WheelPower 轮椅大乱斗
- 类型：俯视角科幻 Roguelite 射击游戏
- 引擎：Godot 4.x
- 位置：`~/openclaw/workspace/game/wheelpower/`
- 状态：立项，MVP 规划中
- **核心机制：**
  - 主角有枪，准心跟随鼠标射击
  - 可以选择不同的轮椅载具
  - 轮椅上有机械臂，操作武器自动射击
  -手中的枪可以和轮椅上的枪切换
  - 枪械后坐力会使轮椅产生反方向移动

### Vampire Survivors 改造
- 位置：`~/openclaw/workspace/game/VampireSurvivors/`
- PR 已合并：feat/wheelchair-controller
- 添加：轮椅控制器、准星、手动射击、单元测试

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
- 2026-02-18: 搭建知识中枢 - 飞书文档→Obsidian 同步框架
- 2026-02-18: 语音入口调研完成，报告已输出
- 2026-02-18: 安装 rclone (游戏素材 Google Drive 同步用)
- 2026-02-18: 用 qwen-image API 批量生成像素素材（轮椅、武器、敌人）

---

*最后更新：2026-02-19*
