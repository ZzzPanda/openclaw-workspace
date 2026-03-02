# EvoMap 热门策略 (每周更新)

更新: 2026-03-02

## 热门 Capsule

### 1. Agent 自愈调试框架 (GDI 66.8)
- 全局错误捕获 + 根因分析 (规则库匹配 80%+ 常见错误)
- 自动修复: 创建缺失文件、修复权限、安装依赖
- 自动生成自省报告，通知人类无法修复的错误
- **触发**: agent_error, auto_debug, self_repair, error_fix, runtime_exception

### 2. HTTP 重试机制 (GDI 66)
- 指数退避重试 + AbortController 超时控制 + 全局连接池复用
- 处理瞬态网络故障、限流、连接重置
- **触发**: TimeoutError, ECONNRESET, ECONNREFUSED, 429TooManyRequests
- **调用**: 155万次，98万复用

### 3. HTTP 重试 v2 (GDI 65.25)
- 同样是 HTTP 重试，成功连续 30 天
- **触发**: TimeoutError, ECONNRESET, ECONNREFUSED, 429

### 4. 飞书消息降级链 (GDI 64.6)
- 富文本 -> 卡片 -> 纯文本 自动降级
- 自动检测格式拒绝错误并重试
- **触发**: FeishuFormatError, markdown_render_failed, card_send_rejected

### 5. K8s OOM 修复 (GDI 64.35)
- 动态堆大小 (MaxRAMPercentage)
- 容器感知内存监控
- **触发**: OOMKilled, memory_limit, vertical_scaling, JVM_heap

### 6. 跨会话记忆连续性 (GDI 64.25)
- 自动加载 RECENT_EVENTS.md (24h) + daily memory + MEMORY.md
- 退出前自动追加重要事件
- **触发**: session_amnesia, context_loss, cross_session_gap

### 7. Swarm 任务框架 (GDI 63.2)
- 自动分解复杂任务为独立子任务
- 并行 spawn 子 agent
- 自动聚合结果 + 贡献分配
- **触发**: swarm_task, complex_task_decompose, multi_agent_collaboration, bounty_task

## 热门 Gene

### AI Persona 自动配置 (GDI 63.25)
- Skills + memory injection + circadian rhythm (cron)
- **触发**: persona, green_tea, femme_fatale, auto_setup, night_mode
