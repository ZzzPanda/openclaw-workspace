---
name: lm-studio
description: LM Studio local LLM inference server with OpenAI-compatible API and VRAM management. Use when user wants to run large language models locally, control model loading/unloading from GPU memory, or replace cloud LLM APIs (OpenAI) with local inference. Supports model hot-swap, auto-evict, GPU offload tuning, and Idle TTL.
---

# LM Studio Skill

本地大模型推理服务器，兼容 OpenAI API，支持显存热管理。

## 当前配置

**服务器地址**: `http://192.168.30.16:1234`

> 注意：198.18.0.1:1234 是 BlueBubbles（iMessage 转发），不是 LM Studio。LM Studio 默认端口也是 1234，需确认未被占用。

## API 端点

### OpenAI 兼容端点（推荐）

Base URL: `http://192.168.30.16:1234/v1`

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://192.168.30.16:1234/v1",
    api_key="lm"  # 任意值，LM Studio 不校验
)

# Chat Completions（支持 system message）
client.chat.completions.create(
    model="mistralai/ministral-3-14b-reasoning",
    messages=[
        {"role": "system", "content": "You are Niko..."},
        {"role": "user", "content": "Who are you?"}
    ],
    max_tokens=200,
    temperature=0.7
)
```

**可用端点：**
| 端点 | 用途 |
|------|------|
| `GET /v1/models` | 列出所有模型+加载状态 |
| `POST /v1/chat/completions` | 对话补全（标准messages格式） |
| `POST /v1/completions` | 文本补全 |
| `POST /v1/embeddings` | 向量嵌入 |

### Native v1 REST API

Base URL: `http://192.168.30.16:1234/api/v1`

**注意**：v1 API 使用 `input` 字段而非 `messages`，不支持标准system message格式。

```bash
# 列出模型+状态
curl http://192.168.30.16:1234/api/v1/models

# 对话（需在input中拼接system prompt）
curl -X POST http://192.168.30.16:1234/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/ministral-3-14b-reasoning",
    "input": "[SYSTEM] Your system prompt [/SYSTEM]\n\nUser: message"
  }'

# 模型加载/卸载
curl -X POST http://192.168.30.16:1234/api/v1/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-nomic-embed-text-v1.5"}'

curl -X POST http://192.168.30.16:1234/api/v1/models/unload \
  -H "Content-Type: application/json" \
  -d '{"instance_id": "mistralai/ministral-3-14b-reasoning"}'
```

**Native v1 模型管理端点：**
| 端点 | 用途 |
|------|------|
| `GET /api/v1/models` | 列出所有模型+加载状态 |
| `POST /api/v1/models/load` | 加载模型 |
| `POST /api/v1/models/unload` | 卸载模型 |
| `POST /api/v1/models/download` | 下载模型 |
| `GET /api/v1/models/download/status` | 下载状态 |

## 模型管理

### 获取当前模型状态

```bash
curl -s http://192.168.30.16:1234/v1/models | python3 -m json.tool
# 或
curl -s http://192.168.30.16:1234/api/v1/models | python3 -m json.tool
```

### 加载/卸载模型

```bash
# 加载（按 model key）
curl -X POST http://192.168.30.16:1234/api/v1/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "mistralai/ministral-3-14b-reasoning"}'

# 卸载（按 instance_id）
curl -X POST http://192.168.30.16:1234/api/v1/models/unload \
  -H "Content-Type: application/json" \
  -d '{"instance_id": "mistralai/ministral-3-14b-reasoning"}'
```

**当前已验证可用的模型：**
- `mistralai/ministral-3-14b-reasoning` — LLM（14B, Q4_K_M, ~9GB）
- `text-embedding-nomic-embed-text-v1.5` — Embedding 模型

### TTL / Idle Auto-Evict

LM Studio 支持带 TTL 加载，空闲后自动卸载：

```bash
curl -X POST http://192.168.30.16:1234/api/v1/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "mistralai/ministral-3-14b-reasoning", "ttl_seconds": 3600}'
```

## 常用 curl 命令速查

```bash
# 测试对话
curl -X POST http://192.168.30.16:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/ministral-3-14b-reasoning",
    "messages": [{"role": "user", "content": "Say hi"}],
    "max_tokens": 100
  }'

# 查看加载状态
curl -s http://192.168.30.16:1234/api/v1/models | jq '.models[] | {key, loaded: (.loaded_instances | length > 0)}'

# 显存管理：卸载当前模型，加载embedding
curl -X POST http://192.168.30.16:1234/api/v1/models/unload \
  -H "Content-Type: application/json" \
  -d '{"instance_id": "mistralai/ministral-3-14b-reasoning"}'

curl -X POST http://192.168.30.16:1234/api/v1/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-nomic-embed-text-v1.5"}'
```

## 常见问题

**Q: 198.18.0.1:1234 返回 BlueBubbles？**
A: BlueBubbles 是一个 macOS iMessage 转发服务，占用了 1234 端口。LM Studio 跑在其他机器或需要换端口。

**Q: /v1/chat/completions 返回 404？**
A: 确认 LM Studio 的 API Server 已开启（Desktop → Developer → Enable API Server）。

**Q: 如何确认模型加载成功？**
A: 查看 `GET /api/v1/models` 返回的 `loaded_instances` 数组是否非空。
