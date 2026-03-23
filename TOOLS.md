# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### 飞书语音（正确流程）
**关键：必须用 EasyVoice 生成 + 转 OPUS 格式 + message 工具 asVoice=true**

**完整流程（实测可发出语音气泡）：**
1. 调用 EasyVoice API 生成 MP3（见下方 EasyVoice 节）
2. 转 OPUS：`ffmpeg -y -i 源.mp3 -acodec libopus -ac 1 -ar 16000 输出.opus`
3. 用 message 工具发送：`filePath=输出.opus`, `asVoice: true`

**注意：**
- 内置 `tts` 工具（channel=feishu）发的不是飞书语音气泡，**不要用**
- OPUS 格式是必须的，m4a/mp3 发出去是文件不是语音气泡
- **发送规则**：闲聊/简单回复 → 语音气泡；复杂内容（代码/列表/技术说明）→ 文字

### 日历 (Mac)

- 工具: `icalBuddy`
- 安装: `brew install ical-buddy`
- 权限: 系统设置 → 隐私与安全性 → 隐私 → 日历 → 添加 Terminal/icalBuddy
- 命令:
  - `icalBuddy eventsToday+7` - 未来7天事件
  - `icalBuddy -sc eventsToday+7` - 按日历分组
  - `icalBuddy -ic "工作" eventsToday+7` - 查看特定日历

---

### itch.io 游戏发布流程

**账号**: 0rangePandaman  
**密码**: 19941010orangepanda  
**两步验证邮箱**: niko@dignew.com

#### 发布步骤（网页手动）
1. 打开 https://itch.io/game/new
2. 填写游戏信息：
   - Title: 游戏标题
   - Project URL: wheel-shooter (英文+连字符)
   - Kind: HTML
3. 点击 Upload files 上传 wheel-shooter.zip
4. 点 Save & view page
5. 如需更新：Edit game → 删除旧文件 → 上传新文件 → Save

#### Butler CLI 自动发布（推荐！）
```bash
# 首次设置（只需一次）
export BUTLER_API_KEY="你的API密钥"
curl -L "https://broth.itch.zone/butler/darwin-amd64/LATEST/archive/default" -o /tmp/butler.zip
unzip -o /tmp/butler.zip -d /tmp
mv /tmp/butler /usr/local/bin/butler
chmod +x /usr/local/bin/butler

# 上传游戏（每次更新）
cd ~/.openclaw/workspace/game/wheel-shooter
butler push . 0rangepandaman/wheel-shooter:html
```

#### 游戏链接格式
- 页面: https://0rangepandaman.itch.io/{project-url}
- Secret 链接: https://0rangepandaman.itch.io/{project-url}?secret=xxx

---

---

### 🎤 EasyVoice TTS（本地语音合成）

**部署机器**: `192.168.30.19`
**端口**: `8183`
**Docker 启动**: `python ./webui.py --port 50000`（Docker Desktop 端口映射到 8183）

#### API 地址
```
http://192.168.30.19:8183/api/v1/tts
```

#### 获取可用音色
```bash
curl http://192.168.30.19:8183/api/v1/tts/voiceList
```

#### 生成语音（POST）
```bash
curl -X POST http://192.168.30.19:8183/api/v1/tts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "要转换的文本",
    "voice": "zh-CN-YunxiNeural",
    "rate": "+0%",
    "pitch": "+0Hz",
    "volume": "+0%"
  }'
```

**返回示例**:
```json
{
  "code": 200,
  "success": true,
  "data": {
    "audio": "/zh-CN-YunxiNeural-你好-1234567890.mp3",
    "srt": "/zh-CN-YunxiNeural-你好-1234567890.srt",
    "file": "zh-CN-YunxiNeural-你好-1234567890.mp3"
  }
}
```

**下载音频**: `http://192.168.30.19:8183{audio路径}`

#### 常用音色推荐
| 音色 | 风格 |
|------|------|
| `zh-CN-YunxiNeural` | 男声，阳光开朗，默认 |
| `zh-CN-XiaoyiNeural` | 女声，活泼可爱 |
| `zh-CN-YunjianNeural` | 男声，运动激情 |
| `zh-CN-XiaoxiaoNeural` | 女声，温暖流畅 |
| `zh-CN-YunxiaNeural` | 男声，可爱卡通 |

#### 发送原生语音消息到飞书
**正确方式（message 工具 + OPUS）：**
1. `ffmpeg -y -i 源文件.mp3 -acodec libopus -ac 1 -ar 16000 输出.opus`
2. `message 工具 filePath=输出.opus asVoice=true`

**完整 API 方式（备选）：**
1. 上传文件：`POST https://open.feishu.cn/open-apis/im/v1/files`
   - header: `Authorization: Bearer {token}`
   - form: `file_type=opus`, `file_name=xxx.opus`, `file=@文件路径`
2. 发语音：`POST https://open.feishu.cn/open-apis/im/v1/messages`
   - `msg_type: audio`
   - `content: {"file_key": "上一步返回的key"}`

> 注意：message 工具方式已经可以发出正确的语音气泡，无需用完整 API。

---

### 📷 飞书发图片（正确流程）

**优先使用脚本：**
```bash
./scripts/send_image.sh <本地图片路径> [收件人open_id/chat_id]
```

脚本会自动：
1. 复制图片到 `~/.openclaw/media/outbound/`
2. 返回规范化的 filePath

然后用 `message 工具` + `filePath` 发送。

**Fallback（之前的方式）：** 直接复制图片到 `~/.openclaw/media/outbound/`，然后用 message 工具的 `filePath` 参数发送。

**规则：**
- 所有图片都必须先存到 `~/.openclaw/media/outbound/`，不要直接用 `/tmp` 或绝对路径
- 发送用 `message 工具 filePath=路径`，不要用 `media` 参数

---

Add whatever helps you do your job. This is your cheat sheet.
