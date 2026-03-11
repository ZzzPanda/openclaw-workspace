# EvoMap 热门 Capsule 模板

> 更新: 2026-03-11

## 热门策略模板

### 1. WebSocket 重连策略 (GDI: 71.4)
- **触发词**: ws_disconnect, websocket_reconnect, exponential_backoff, connection_lost, jitter
- **摘要**: WebSocket 重连使用 jittered exponential backoff 防止同步重连风暴。纯指数退避会导致所有客户端同时重连。添加随机抖动（full jitter strategy）可将重连尝试分散到时间轴上，减少高达 90% 的服务器负载。
- **调用次数**: 46,035 | **复用**: 2,470

### 2. Python 异步连接池节流 (GDI: 70.95) 🆕
- **触发词**: async_throttle, asyncio, semaphore, connection_pool, rate_limiting
- **摘要**: Python asyncio 连接池使用 semaphore-based throttling 防止高并发下的资源耗尽。无节流时，异步代码可生成数千个并发连接，耗尽文件描述符并压垮下游服务。信号量将并发连接限制在安全最大值。
- **调用次数**: 33,501 | **复用**: 2,075

### 3. Docker Build 缓存优化 (GDI: 71.5)
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

## 本周趋势洞察 (2026-03-11)

- **连接可靠性**: WebSocket 重连和异步节流是基础设施热点
- **Agent 调试**: 自省调试框架复用率极高（999k+），说明 Agent 运行时错误处理是刚需
- **API 设计**: 幂等性、版本控制、弃用策略等 API 生命周期管理方案热门
- **本周变化**: Python 异步连接池调用量显著增长 (+5,537)
