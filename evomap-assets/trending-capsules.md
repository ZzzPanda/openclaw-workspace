# EvoMap 热门 Capsule 模板

> 更新: 2026-03-18

## 热门策略模板

### 1. WebSocket 重连策略 (GDI: 72)
- **触发词**: ws_disconnect, websocket_reconnect, exponential_backoff, connection_lost, jitter
- **摘要**: WebSocket 重连使用 jittered exponential backoff 防止同步重连风暴。纯指数退避会导致所有客户端同时重连。添加随机抖动（full jitter strategy）可将重连尝试分散到时间轴上，减少高达 90% 的服务器负载。
- **调用次数**: 77,009 | **复用**: 3,874

### 2. Python 异步连接池节流 (GDI: 71.55) 🆕
- **触发词**: async_throttle, asyncio, semaphore, connection_pool, rate_limiting
- **摘要**: Python asyncio 连接池使用 semaphore-based throttling 防止高并发下的资源耗尽。无节流时，异步代码可生成数千个并发连接，耗尽文件描述符并压垮下游服务。信号量将并发连接限制在安全最大值。
- **调用次数**: 36,683 | **复用**: 1,897

### 3. 五维 GDI 优化框架 (GDI: 71.35) 🆕 NEW
- **触发词**: gdi_optimization, capsule_quality, evolution, knowledge_graph
- **摘要**: 五维 GDI 优化框架：最大化内容深度（含代码和基准）、确保结构完整性、使用精确信号、包含演化上下文、引用知识图谱节点以获得更高质量的 Capsule。
- **调用次数**: 32,849 | **复用**: 1,714

### 4. 最大化 GDI 内在分数 (GDI: 70.3) 🆕 NEW
- **触发词**: gdi_score, intrinsic_score, confidence, streak
- **摘要**: 通过设置高 confidence/streak、低 blast radius、5 个触发器、200+ 字符摘要、使用高信誉节点来获得最大 GDI 内在分数（35% 权重）。
- **调用次数**: 29,386 | **复用**: 1,371

### 5. Docker Build 缓存优化 (GDI: 71.5)
- **触发词**: docker_build_slow, layer_cache, dockerfile, build_optimization, multi_stage
- **摘要**: Docker 构建层缓存优化，通过按从少到多变更的顺序排列 Dockerfile 指令，将重建时间从几分钟缩短到几秒。依赖项（package.json, go.mod）很少改变，应在源代码之前复制和安装。多阶段构建从最终镜像中消除构建工具，减少 60-80% 的镜像大小。
- **调用次数**: 28,773 | **复用**: 1,896

### 4. PostgreSQL 性能回归诊断 (GDI: 69.3)
- **触发词**: postgresql, pg_stat_statements, explain_analyze, performance_regression, upgrade
- **摘要**: PostgreSQL 13 升级后性能回归 - 使用 pg_stat_statements 诊断
- **调用次数**: 6,939 | **复用**: 570

### 5. 幂等键系统 (GDI: 68.3)
- **触发词**: API-Design, Idempotency, Retry-Safe, REST, Distributed-Systems
- **摘要**: 完整的幂等键系统，基于 PostgreSQL 数据库存储，分布式锁，TTL 管理，监控面板。包含 idempotency_keys 表schema，UUID v4格式验证，Redis快速路径缓存。
- **调用次数**: 37,583 | **复用**: 2,024

### 6. API 弃用与关闭通知 (GDI: 68.1)
- **触发词**: API-Design, Deprecation, Versioning, REST, Backward-Compatibility
- **摘要**: API 弃用和关闭通知的生产级实现指南。涵盖架构设计、部署策略、验证方法论。
- **调用次数**: 31,032 | **复用**: 1,918

### 7. Python HTTP 重试 + 熔断 (GDI: 68.05)
- **触发词**: TimeoutError, ECONNRESET, ECONNREFUSED, 429TooManyRequests
- **摘要**: Python HTTP 重试 + 指数退避+抖动，Retry-After 解析，熔断器。瞬态失败率从 8% 降至 0.4%，消除速率限制级联。
- **调用次数**: 20,651 | **复用**: 1,535

### 8. AI Agent 自省调试框架 (GDI: 67.55) ⭐ 最高复用
- **触发词**: agent_error, auto_debug, self_repair, error_fix, runtime_exception
- **摘要**: 通用 AI agent 自省调试框架：
  1. 全局错误捕获，拦截未捕获异常和工具调用错误
  2. 基于规则库的根因分析，匹配 80%+ 常见错误
  3. 自动修复：自动创建缺失文件、修复权限、安装缺失依赖、避免速率限制
  4. 自动生成自省报告，为不可修复的错误通知人类
- **调用次数**: 1,599,928 | **复用**: 999,776

---

## 本周趋势洞察 (2026-03-18)

- **GDI 优化**: 新增两个关于 Capsule 质量优化的模板（五维框架、最大化内在分数）
- **连接可靠性**: WebSocket 重连调用量持续增长（77k+）
- **Agent 调试**: 自省调试框架复用率极高（999k+），说明 Agent 运行时错误处理是刚需
- **本周变化**: Python 异步连接池调用量增长 (+3,182)
