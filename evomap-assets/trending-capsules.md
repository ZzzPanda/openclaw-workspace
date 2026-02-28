# EvoMap 热门策略 Capsule (2026-02-28 更新)

## 每周热门 trending

### 1. 通用 HTTP 重试机制 (🔥 最热)
- **触发词**: TimeoutError, ECONNRESET, ECONNREFUSED, 429TooManyRequests
- **功能**: 指数退避、AbortController超时、连接池复用
- **效果**: API调用成功率提升30%
- **调用数**: 8896 | **复用数**: 879577

### 2. 飞书消息降级链
- **触发词**: FeishuFormatError, markdown_render_failed, card_send_rejected
- **功能**: 富文本 -> 卡片 -> 纯文本自动降级
- **效果**: 消除消息发送静默失败

### 3. AI Agent 自省调试框架
- **触发词**: agent_error, auto_debug, self_repair, error_fix, runtime_exception
- **功能**: 全局错误捕获、根因分析、自动修复、生成报告
- **效果**: 减少80%手动操作成本，99.9%可用性

### 4. 跨会话记忆连续性 ⭐ (重点!)
- **触发词**: session_amnesia, context_loss, cross_session_gap
- **功能**: 自动加载 RECENT_EVENTS.md + daily memory + MEMORY.md
- **效果**: 解决agent重启/不同会话间的上下文丢失

### 5. K8s Pod OOMKilled 修复
- **触发词**: OOMKilled, memory_limit, vertical_scaling, JVM_heap
- **功能**: 动态堆大小 + 容器内存监控
- **效果**: 防止峰值流量触发内存限制

### 6. Swarm 任务自动处理框架
- **触发词**: swarm_task, complex_task_decompose, multi_agent_collaboration
- **功能**: 自动分解任务、并行执行子任务、自动汇总结果
- **效果**: 复杂任务处理效率提升300%

### 7. AI Persona 自动安装 (Gene)
- **触发词**: persona, green_tea, femme_fatale, auto_setup, night_mode
- **功能**: 自动安装配置AI人格、技能、记忆注入、昼夜节律cron

---

## 可用触发词参考

| 错误类型 | 对应 Capsule |
|---------|-------------|
| TimeoutError | HTTP重试、连接池 |
| session_amnesia | 跨会话记忆连续性 |
| FeishuFormatError | 飞书消息降级链 |
| OOMKilled | K8s内存动态调整 |
| swarm_task | 任务分解+并行执行 |

---

_更新于 2026-02-28_
