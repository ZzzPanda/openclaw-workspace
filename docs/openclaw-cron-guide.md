# OpenClaw 定时任务实战指南

> 如何让 AI 自主在深夜帮你干活

---

## 🎯 什么是定时任务

OpenClaw 的 cron 功能可以让你定时触发 AI 任务：
- 指定时间自动执行
- 独立会话，不干扰主对话
- 执行完自动发消息汇报结果

---

## 📝 配置示例：夜间自由任务

这是一个典型的夜间任务配置，每天凌晨 1 点和 4 点让 AI 自主干活：

```json
{
  "name": "夜间自由任务",
  "schedule": {
    "kind": "cron",
    "expr": "0 1 * * *",      // 每天凌晨1点
    "tz": "Asia/Shanghai"    // 时区
  },
  "sessionTarget": "isolated", // 独立会话
  "payload": {
    "kind": "agentTurn",
    "message": "基于今天的记忆发挥你的主动性，专注 Slay-The-Robot 项目。任务优先级：1）修复当天遇到的 bug 2）推进游戏开发 3）优化代码。不要管其他项目！完成后汇报你做了什么。",
    "timeoutSeconds": 7200    // 超时2小时
  },
  "delivery": {
    "mode": "announce",
    "channel": "last"          // 发回当前会话
  }
}
```

---

## 🛠️ 创建命令

```bash
# 创建定时任务
openclaw cron add \
  --name "夜间自由任务" \
  --cron "0 1 * * *" \
  --session isolated \
  --message "基于今天的记忆发挥你的主动性，专注项目..."
```

---

## ⏰ Cron 表达式速查

| 表达式 | 含义 |
|--------|------|
| `0 1 * * *` | 每天凌晨 1:00 |
| `0 4 * * *` | 每天凌晨 4:00 |
| `0 9 * * *` | 每天早上 9:00 |
| `0 23 * * *` | 每天晚上 23:00 |
| `0 11 * * 1,4` | 周一和周四 11:00 |
| `0 9 * * 5` | 每周五 9:00 |

格式：`分 时 日 月 周`

---

## 📤 消息推送配置

### 发到飞书群
```json
"delivery": {
  "mode": "announce",
  "channel": "feishu",
  "to": "chat:oc_xxx"  // 群ID
}
```

### 发给用户
```json
"delivery": {
  "mode": "announce",
  "channel": "feishu",
  "to": "ou_xxx"  // 用户ID
}
```

### 发回当前会话
```json
"delivery": {
  "mode": "announce",
  "channel": "last"
}
```

---

## ⚙️ 进阶选项

### 关闭失败告警
```bash
openclaw cron edit <job-id> --no-failure-alert
```

### 手动触发任务
```bash
openclaw cron run <job-id> --force
```

### 查看任务状态
```bash
openclaw cron list
openclaw cron logs <job-id>
```

---

## 💡 最佳实践

1. **用 isolated 会话** - 不干扰主对话
2. **设置超时** - 防止任务卡死
3. **任务指令要具体** - 明确让 AI 做什么
4. **关闭失败告警** - 偶发网络错误不必打扰

---

## 📂 文件位置

- 任务配置：`~/.openclaw/cron/jobs.json`
- 执行日志：`~/.openclaw/cron/runs/`

---

> 傻 bot 也能学会的定时任务教程 ✓
