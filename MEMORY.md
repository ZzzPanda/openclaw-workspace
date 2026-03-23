# MEMORY.md - 长期记忆

### 正在做的项目
- **Slay The Wheelman** (Godot 4.x)
  - 地址 https://github.com/ZzzPanda/Slay-The-Wheelman
  - 本地路径 game/Slay-The-Wheelman
  - [ ] Android 打包修复
  - [ ] 测试 APK 运行
  - [ ] 卡牌战斗位移系统
  - [ ] 研究动画管线（视频→帧动画）

### 未来可能做的
- **WheelPower 轮椅大乱斗** (Godot 4.x Roguelite)
- **游戏资产管道** (Qwen Image API 生成16x16像素素材)
- **Vampire Survivors 改造** (轮椅控制器)

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

### ComfyUI API（2026-03-23）
- 丁震部署在 192.168.30.19:8000（丁震家 Mac mini，Docker）
- **API 验证成功**：POST /prompt 提交任务、GET /api/history/{id} 查询、GET /api/view 下载图片
- **图片下载正确路径**：`/api/view?filename={文件名}&subfolder=XXX%5CIMAGES`（注意反斜杠转义）
- **已保存 workflow**：`workspace/comfyui/sdxl-nsfw-real.json`（NSFW Realistic skin 图像生成，含 FaceDetailer 修脸）
- **运行脚本**：`workspace/comfyui/sdxl-nsfw-real.sh`，用法：`./sdxl-nsfw-real.sh "prompt"` 或 `SEED_PRIMARY=123 ./sdxl-nsfw-real.sh`
- **工作流列表**：`workspace/comfyui/list.md`

### 本地 TTS（EasyVoice）
- 部署：丁震家 Mac mini，192.168.30.19:8183（Docker Desktop）
- 2026-03-21 调通，支持多种音色（云希、晓伊等）
- 飞书原生语音消息：需转 OPUS 格式，上传后用 msg_type=audio 发送（不是 m4a）
- 文档：TOOLS.md

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

### GitHub/Fork 项目流程（重要！）
- **永远不开分支直接 push main**，所有修改都必须开 PR
- 这是 fork 自 https://github.com/ZzzPanda/Slay-The-Wheelman 的项目，PR 目标仓库必须是 ZzzPanda/Slay-The-Wheelman，不是原来的仓库
- 流程：创建分支 → 提交commit → push → 用 gh pr create 创建 PR → 等用户合并

### 习惯
- **飞书发图片**：必须先存到 `~/.openclaw/media/outbound/`，然后用 filePath 发送（不要用 /tmp 或 MEDIA 链接，会失败）
- **所有图片必须通过飞书发送**给用户（用 message 工具的 filePath），不能再只给 MEDIA 链接
- **所有飞书文档操作**（doc/wiki/bitable）用完必须追加记录到当日 memory 文件
- **Memory 与 Obsidian 同步**：重要文档需要同时存到 Obsidian（vault: panda），保持双向同步

---

### 2026-03-24 新增
- **Slay The Wheelman Bug 修复**: 修复 build_android.sh 脚本语法错误（`if [ - -d ...]` 多了一个 `-`）
- **武器系统开发**: 提交 WeaponData.gd、ValidatorAttackRange.gd，更新 CardData.gd/Global.gd/Player.gd 支持武器系统
- **Android 构建成功**: 成功构建 30MB Debug APK (android_debug_20260324_0116.apk)，已同步到 Google Drive

### 2026-03-23 新增
- **Slay The Robot WeaponData Bug 修复**: 修复 Global.gd 中 WeaponData 自动加载问题，现在可以通过 Global.get_weapon_data() 正常访问武器数据
- **Android 构建成功**: 成功构建 30MB Android Debug APK (android_debug_20260323_0406.apk)，已同步到 Google Drive

### 2026-03-19 新增
- **Slay The Wheelman 击退系统**: 新增 ActionKnockback.gd（击退动作）和 ActionRecoil.gd（后坐力动作），更新 Signals.gd 添加相关信号
- **Android 构建成功**: 打包 android_debug_20260319_0400.apk，位置战斗系统计划中（待完成：WeaponData.gd, 扩展 CardData/EnemyData, ValidatorAttackRange.gd）

### 2026-03-18 新增
- **轮椅枪手 wheel-shooter 游戏**: 新 HTML5 Canvas 游戏项目，GitHub: ZzzPanda/wheel-shooter。支持 sprite 素材（player.png, railgun.png），模块化结构（config.js, sprites.js, game.js）
- **Slay The Robot PR #6 合并**: Android 构建修复 PR 已合并到 main
- **敌人素材替换**: 用用户的自定义"类固醇星人"角色替换了游戏内敌人纹理（enemy_red_large.png）
- **GitHub PR 流程确认**: 再次确认 fork 项目必须用 PR，不再直接 push main

### 2026-03-16 新增
- **Slay The Wheelman Android Build 修复**: 修复了 `scripts/build_android.sh`，添加时间戳后缀（如 `android_debug_20260316_1120.apk`）和 latest 软链接，添加 .gitignore 排除 builds 目录
- **GitHub PR 状态**: PR #5 和 PR #6（Android 打包修复）仍需手动在 GitHub 网页合并，PR #6 尝试多种合并方式均失败（squash/rebase/merge），仓库规则限制导致 API 无法合并
- **游戏素材生成**: 成功生成黄色、紫色、橙色宝石神器图标（之前 API 限流已解决）

### 2026-03-15 新增
- **Slay The Wheelman 素材生成**: 使用 Qwen Image API 成功生成 16 个游戏素材（5个小机器人敌人、1个中型机器人、1个大型BOSS、2个角色立绘、3个神器图标、4个卡牌边框）
- **GitHub PR 状态**: PR #5 和 #6（Android 打包修复）合并失败，有冲突需要手动处理
- 详细素材 URL 记录在: memory/slay-the-robot-generated-assets.md

### 2026-03-14 新增
- **飞书 message 工具报错**：LarkClient[default]: appId and appSecret are required。排查发现 openclaw.json 有 feishu 配置但 message 工具可能使用独立客户端，子工具（feishu_im_user_message 等）正常工作
- **wheelman-card 移动端打包**：研究 iOS (Xcode + Apple Developer) 和 Android (JDK + SDK) 打包工作流，创建导出指南文档：https://feishu.cn/docx/InWVdCLyqoRGWdxpsIscS0qRnze
- **飞书消息 Bug 排查**：发现 feishu_chat 工具返回 400 错误，改用 message 工具发送消息正常

### 2026-03-11 新增
- **OpenClaw PM2 迁移**：将 Gateway 服务从 launchd 迁移到 PM2 管理（原因：launchd 有时会卡住不自动重启）
- **Niko 飞书 Bot**：新增第二个飞书 bot「美味软脚虾」，AppID: cli_a93be196e3789bde，配对成功，用户 ID: ou_2fa349acf49b639d03a8fb5cae5dd3b3
- **AI 工具资讯 cron 任务**：改用 niko bot 推送，推送群聊: oc_88ef5b4274d312abf28fefd254ef3fec，发布时间：周一/四 11:00

### 2026-03-06 新增
- **Playwright Skills 安装**：安装了 3 个 Playwright 相关 skill（自动生成测试、探索网站、最佳实践），位置 `~/.agents/skills/`
- **小红书 XHS Scraper**：通过 CDP 协议获取登录 Cookie，成功抓取评论数据（但大部分高热度笔记已失效404）

### 2026-03-04 新增
- **Apify MCP Server**：安装成功 (@apify/actors-mcp-server@0.9.6)，让 Claude Code 可以实时抓取全网数据（Google Maps、电商、社交媒体等），配置方式：`npm install -g @apify/mcp-server`，然后在 CLAUDE.md 添加 MCP 配置
- **Mac 合盖继续工作**：用户成功设置 Mac 合盖也能继续工作（命令：`sudo pmset -c sleep 0` + `sudo pmset -c disablesleep 1`）
- **EvoMap 热门策略更新**：每周更新热门 Capsule 模板，新增 Agent 自省调试框架、Swarm 任务自动处理框架，已同步到 `evomap-assets/trending-capsules.md`

### 2026-02-28 新增
- **OpenClaw 更新**：从 2026.2.15 更新到 2026.2.26（用户确认无需重启服务）

### 2026-02-26 新增
- **游戏设计文档更新**：重写 game-design-books.md，分成两篇独立文章（理论篇+书单篇），并同步到 Obsidian
- **类固醇星球 Steroidia 设定**：已同步到 `game/wheelpower/` 目录

### 2026-02-25 新增
- **每日 API 用量报告**：配置 cron 任务，每日 9:00 自动推送 API 用量报告到飞书

### 2026-02-22 新增
- **类固醇星球 Steroidia**：新游戏项目，背景设定：星球上的人只练上半身不练腿，脑袋尖尖的。九龙（9种类固醇）作为圣物：群勃龙、康力龙、氧雄龙、康复龙、美替诺龙、葵酸诺龙、苯丙酸诺龙、氧氧龙、氟甲睾酮。设定文档：`game/steroidia设定.md`
- **游戏设计艺术**：用户分享《游戏设计艺术》读书笔记，核心是游戏设计是为玩家创造体验，有100+透镜工具，四元素模型（机制/故事/美学/技术）。已保存到 `game/game-design-books.md`

### 2026-02-24 新增
- **EvoMap 热门策略**：新增跨会话记忆连续性（解决 session_amnesia 问题），热门 Capsule 模板保存在 `evomap-assets/trending-capsules.md`
- **Steroidia 更新**：新增 Supredrol（超级康力）到九龙圣物，副作用：肝脏毒性、激素抑制、血脂异常、抑郁
- **游戏开发资源**：发现 redblobgames.com 游戏开发教程网站，创建指南 `game/redblobgames-guide.md`
