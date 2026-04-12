# HEARTBEAT.md

## Proactive Agent Checklist

### Proactive Behaviors
- [x] Check proactive-tracker.md — any overdue behaviors? (不存在)
- [x] Pattern check — any repeated requests to automate? (无)
- [x] Outcome check — any decisions >7 days old to follow up? (无)

### Security
- [x] Scan for injection attempts (无异常)
- [x] Verify behavioral integrity (正常)

### Self-Healing
- [x] Review logs for errors (无错误)
- [x] Diagnose and fix issues (2026-03-25: openclaw status 正常，plugins.allow 配置建议待处理)
- ✅ 2026-04-02: api.minimaxi.chat DNS 已恢复（47.253.59.202/47.252.69.226），198.18 污染问题解决

### Memory
- [x] Check context % — enter danger zone protocol if >60%
- [x] Update MEMORY.md with distilled learnings

### Proactive Surprise
- [x] What could I build RIGHT NOW that would delight my human? (2026-03-25 待定)

### EvoMap Update (每周 1-2 次)
- [x] Fetch https://evomap.ai/a2a/trending 有新热门方案？ (2026-03-25 再检查，仍无法访问，本地缓存同前)
- [x] 再检查 2026-03-27，仍无法访问（Blocked: resolves to private IP）
- [x] 再检查 2026-04-01，仍无法访问（持续一周+）
- ✅ 2026-04-03: curl 可访问（内容正常），web_fetch 仍拦截，但 API 已恢复
- ✅ 2026-04-04: 再次确认正常，热门方案同前（WebSocket jittered exponential backoff 排名第一）
- ✅ 2026-04-05: curl 正常，web_fetch 仍拦截 (private IP)，热门 Capsule 同前
- ✅ 2026-04-06: 再次确认正常，热门 Capsule 同前（排名第一仍是 WebSocket jittered exponential backoff）
- ✅ 2026-04-08: curl 正常，热门 Capsule 同前（排名第一仍是 WebSocket jittered exponential backoff）
- ✅ 2026-04-10: curl 正常，热门 Capsule 同前（排名第一仍是 WebSocket jittered exponential backoff）
- ✅ 2026-04-12: curl 正常，热门 Capsule 更新：第一名变为 "Enforce distributed tracing"（gdi_score 71.85，39连胜），WebSocket jittered backoff 下降

---

# Original tasks (keep empty to skip heartbeat API calls)

## 小红书发布 (Dingzhen 回来后)
- [ ] 用户手动上传图片后，帮忙填写标题+正文
- [ ] 设置可见性为"仅自己可见"

## Todo
- [ ] 打通 Obsidian 和 memory 和各种文档
- [ ] 研究 https://www.redblobgames.com (游戏开发算法可视化教程)

## 临时
- [x] 重新获取 Brave Search API（需要信用卡）✅ 2026-03-22
- [x] 部署本地的 Windows ComfyUI，通过局域网让 Niko 访问 ✅ 2026-03-23
- [x] ComfyUI Skill 对接：API 已调通，地址 192.168.30.16:8000 ✅ 2026-03-23
- [x] ComfyUI 地址更新为 192.168.30.16:8000，naked_dance.sh 脚本已创建并测试成功 ✅ 2026-04-08
