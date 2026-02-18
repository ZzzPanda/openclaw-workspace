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

Add whatever helps you do your job. This is your cheat sheet.
