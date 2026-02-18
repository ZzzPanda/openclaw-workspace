# 语音入口调研报告

## 1. Mac 语音唤醒/语音输入方案

### 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Mac 原生 Dictation（听写）** | 系统自带，无需安装；使用 Siri 语音识别；支持连续语音输入 | 需要联网（云端识别）；唤醒需要按 Fn 键或自定义快捷键 | 日常文字输入 |
| **Whisper (OpenAI)** | 开源免费；支持本地离线运行；多语言支持；高精度 | 需要较高配置（建议 8GB+ RAM）；首次加载较慢 | 离线语音转文字、隐私敏感场景 |
| **Whisper.cpp** | macOS 原生加速（Apple Silicon）；完全离线；低延迟 | 需要编译或使用 Homebrew 安装；对硬件有一定要求 | 实时语音转文字、开发者集成 |
| **CapsWriter-Offline** | 一键语音输入；支持热词；可结合 LLM 处理 | 主要是 Windows 方案 | Windows 用户 |
| **MacWhisper (第三方 App)** | 界面友好；支持多种模型大小；支持 Apple Silicon 加速 | 付费版功能更全；免费版有功能限制 | 非技术用户快速上手 |
| **Hey Siri 唤醒** | 语音唤醒便捷 | Mac 端支持有限；需要保持麦克风开启 | 简单语音命令控制 |

### 推荐：ASR 方案

**首选：Whisper.cpp（本地离线） + macOS 原生 Dictation（云端备用）**

- 使用 Homebrew 一键安装：`brew install whisper.cpp`
- 支持 Apple Silicon (M1/M2/M3) 原生加速
- 可通过 `whisper-cli` 命令行快速调用

---

## 2. TTS 方案

### 现有工具对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **say 命令** | macOS 原生自带；无需网络；无成本 | 机械感强；音质单一 | 简单系统提示 |
| **ElevenLabs** | 语音自然；多语言支持；语音克隆 | 需要 API Key；有费用 | 高质量语音输出 |
| **OpenAI TTS** | 自然度高；支持语气/情感控制 | 需要 API Key；仅英文效果最佳 | 开发者集成 |
| **MiniMax Speech 02** | 零样本语音克隆；多语言支持 | 主要是 API 服务 | 高质量语音合成 |
| **Kokoro** | 开源；本地可运行；支持多种音色 | 需要自行部署 | 离线场景 |

### 推荐：TTS 方案

**第一阶段：使用 `say` 命令**（零成本、快速集成）
```bash
say "Hello, this is a test"
```

**第二阶段：集成 ElevenLabs 或 OpenAI TTS**（高质量输出）
- ElevenLabs API 费用：约 $1/万字符
- OpenAI TTS：约 $0.015/千字符

---

## 3. 自动化方案

### 定时任务

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **cron** | 简单易用；Linux/Unix 标准 | macOS 已废弃；需额外配置权限 | 简单定时任务 |
| **launchd** | macOS 原生推荐；支持系统睡眠恢复 | 配置较复杂（XML plist） | 长期后台服务 |
| **launchctl** | 命令行管理 launchd 任务 | 学习曲线较陡 | 开发者 |
| **macOS Scheduled Tasks (GUI)** | 无需命令行 | 功能有限 | 简单定时提醒 |

### 推送通知

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **osascript (AppleScript)** | 系统原生；无需安装 | 功能有限 | 本地通知 |
| **terminal-notifier** | 功能丰富；支持图片/链接 | 需要安装 | 格式化通知 |
| **Pushover** | 跨设备推送（iPhone/Android） | 需要注册付费 | 重要任务提醒 |
| **Telegram Bot API** | 免费；支持多媒体 | 需要网络 | 手机即时通知 |
| **飞书/Discord Webhook** | 免费；支持群组推送 | 需要配置 | 团队通知 |

### 推荐：自动化方案

**定时任务：launchd**
```xml
<!-- ~/Library/LaunchAgents/com.example.task.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.task</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/your-script.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

**推送通知：osascript（本地）或飞书 Webhook（远程）**
```bash
# 本地通知
osascript -e 'display notification "任务完成" with title "语音助手"'

# 飞书 Webhook（需要配置）
curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{"msg_type": "text", "content": {"text": "任务完成"}}'
```

---

## 4. 推荐方案总结

### 第一阶段：快速原型
- **ASR**：使用 macOS 原生 Dictation（Fn 键唤醒）
- **TTS**：使用 `say` 命令
- **自动化**：使用 `cron` 或简单的 `sleep &&` 循环
- **推送**：使用 `osascript` 本地通知

### 第二阶段：生产级
- **ASR**：Whisper.cpp 本地离线识别
- **TTS**：ElevenLabs API 或 OpenAI TTS
- **自动化**：launchd 定时任务
- **推送**：飞书/Telegram Webhook 推送至手机

---

## 5. 待解决的问题

1. **语音唤醒方式**：如何在不按任何键的情况下实现语音唤醒？（可能需要后台持续运行的麦克风监听服务）
2. **Whisper 实时性**：Whisper.cpp 的实时转写延迟能否接受？（测试基准：<500ms）
3. **飞书集成**：调研飞书机器人的 API 推送方案
4. **隐私考量**：本地离线 vs 云端识别的权衡
5. **唤醒词训练**：是否有开源的自定义唤醒词方案？（如 "Hey Snips" 替代方案）

---

*调研完成时间：2026-02-18*
