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

#### 发送原生语音消息到飞书（推荐）
1. **转 OPUS 格式**：`ffmpeg -y -i 源文件.mp3 -acodec libopus -ac 1 -ar 16000 输出.opus`
2. **上传获取 file_key**：调用 `POST https://open.feishu.cn/open-apis/im/v1/files`
   - header: `Authorization: Bearer {token}`
   - form: `file_type=opus`, `file_name=xxx.opus`, `file=@文件路径`
3. **发送语音消息**：调用 `POST https://open.feishu.cn/open-apis/im/v1/messages`
   - `msg_type: audio`
   - `content: {"file_key": "上一步返回的key"}`
4. 体积最小（约为 MP3 的 70%），飞书显示为原生语音气泡

**临时方案（走 message 工具）**：转 m4a 后直接发文件（不是语音气泡，但能播放）

---

Add whatever helps you do your job. This is your cheat sheet.
