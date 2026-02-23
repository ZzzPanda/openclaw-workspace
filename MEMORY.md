# MEMORY.md - 长期记忆

### WheelPower 轮椅大乱斗
- 类型：俯视角科幻 Roguelite 射击游戏
- 引擎：Godot 4.x
- 位置：`~/openclaw/workspace/game/wheelpower/`
- 状态：立项，MVP 规划中
- **战斗设计参考**：见 `memory/pve-combat-design.md`（来自 IKAROS 的 PVE 战斗设计笔记）
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

### EvoMap 协作演化市场
- 热门策略模板：`~/openclaw/workspace/evomap-assets/trending-capsules.md`
- **触发规则：** 当问题不能快速解决时，查看 EvoMap skill 和本地缓存的热门 Capsule
- 常用信号：TimeoutError、FeishuFormatError、session_amnesia、OOMKilled 等

### 已完成
- 2026-02-17: 从豆包切换到 qwen-image，告别浏览器自动化！
- 2026-02-18: 帮主人把泰国行程（4段航班）同步到日历「飞行计划」
- 2026-02-18: 搭建知识中枢 - 飞书文档→Obsidian 同步框架
- 2026-02-18: 语音入口调研完成，报告已输出
- 2026-02-18: 安装 rclone (游戏素材 Google Drive 同步用)
- 2026-02-18: 用 qwen-image API 批量生成像素素材（轮椅、武器、敌人）
- 2026-02-20: 搜索并整理游戏开发/关卡设计书籍推荐，存入 `game/level-design-books.md`
- 2026-02-20: 安装 EvoMap skill，热门策略已存到本地

### 小红书发布
- 账号: 鸡肉和巴豆（已扫码登录）
- Skill: `write-xiaohongshu`，MCP: `rednote-mcp`
- **当前方案**：不自动发，改为帮他生成文案+图片，他手动发
- **爆款格式 (2025)**:
  - 标题: [人群]+[痛点]+[解决方案]+[好奇钩子]，≤18字
  - 图片: 要加文字说明（如"LOOK1：职场风"），每300字配1张
  - 正文: 每段≤3行，用 emoji 分隔（✅ 💡 🔥），重点加粗/红色
  - 标签: 带话题标签，关键词密度够

### 飞书群聊
- 日报群 ID: oc_816ba7e2a49043650d23cb5011b8defb

### 习惯
- **飞书发图片**：必须先存到 `~/.openclaw/media/outbound/`，然后用 filePath 发送（不要用 /tmp 或 MEDIA 链接，会失败）
- **所有图片必须通过飞书发送**给用户（用 message 工具的 filePath），不能再只给 MEDIA 链接
- **所有飞书文档操作**（doc/wiki/bitable）用完必须追加记录到当日 memory 文件
- **Memory 与 Obsidian 同步**：重要文档需要同时存到 Obsidian（vault: panda），保持双向同步

---

*最后更新：2026-02-22*

### 2026-02-22 新增
- **类固醇星球 Steroidia**：新游戏项目，背景设定：星球上的人只练上半身不练腿，脑袋尖尖的。九龙（9种类固醇）作为圣物：群勃龙、康力龙、氧雄龙、康复龙、美替诺龙、葵酸诺龙、苯丙酸诺龙、氧氧龙、氟甲睾酮。设定文档：`game/steroidia设定.md`
- **游戏设计艺术**：用户分享《游戏设计艺术》读书笔记，核心是游戏设计是为玩家创造体验，有100+透镜工具，四元素模型（机制/故事/美学/技术）。已保存到 `game/game-design-books.md`
