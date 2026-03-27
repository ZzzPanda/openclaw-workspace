---
name: lm-studio
description: LM Studio local LLM inference server with OpenAI-compatible API and VRAM management. Use when user wants to run large language models locally, control model loading/unloading from GPU memory, or replace cloud LLM APIs (OpenAI) with local inference. Supports model hot-swap, auto-evict, GPU offload tuning, and Idle TTL.
---

# LM Studio

本地大模型推理服务器，兼容 OpenAI API，支持显存热管理。

## 启动 Server

```bash
lms server start
# 默认端口: http://localhost:1234
# Headless 后台运行，开机自启
```

## OpenAI 兼容端点

只需把 base_url 指向 LM Studio，现有 OpenAI SDK 代码无缝切换：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm"  # 任意值，LM Studio 不校验
)

# Chat Completions（支持 text + 图片）
client.chat.completions.create(
    model="model-id",  # 模型 ID（不是文件名）
    messages=[{"role": "user", "content": "hello"}]
)

# Text Completions
client.completions.create(
    model="model-id",
    prompt="The capital of France is"
)

# Embeddings
client.embeddings.create(
    model="model-id",
    input="text to embed"
)
```

| 端点 | 用途 |
|------|------|
| `GET /v1/models` | 列出已加载模型 |
| `POST /v1/chat/completions` | 对话补全 |
| `POST /v1/completions` | 文本补全 |
| `POST /v1/embeddings` | 向量嵌入 |
| `POST /v1/responses` | Responses API |

## Native REST API

```bash
# 列出已加载模型
curl http://localhost:1234/api/v0/models \
  -H "Authorization: Bearer $LM_API_TOKEN"

# 文本补全
curl -X POST http://localhost:1234/api/v0/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-oss-20b", "prompt": "hello"}'

# 向量嵌入
curl -X POST http://localhost:1234/api/v0/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-oss-20b", "input": "text"}'
```

## 模型加载/卸载（VRAM 热管理）

### CLI

```bash
# 加载模型（全部 GPU 卸载）
lms load <model_id> --gpu-offload 100

# 部分 GPU 卸载（减少 VRAM 占用）
lms load <model_id> --gpu-offload 35

# 卸载模型
lms unload <model_id>

# 查看状态
lms status
```

### REST API

```bash
# 卸载指定模型
curl -X POST http://localhost:1234/api/v1/models/unload \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"instance_id": "openai/gpt-oss-20b"}'
```

### Python SDK

```python
from lmstudio import LLMWrapper

model = LLMWrapper("gpt-oss-20b")
model.load(gpu_offload=1.0)   # 1.0=全 VRAM，0.0=全 CPU

# 用完卸载
model.unload()
```

## Idle TTL / Auto-Evict

自动弹出空闲模型，释放 VRAM：

```bash
# 带 TTL 加载（空闲60秒后自动卸载）
curl -X POST http://localhost:1234/api/v0/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-oss-20b", "ttl": 60}'
```

- TTL 单位为秒，空闲计时器在每次请求时重置
- **Auto-Evict**：新模型加载时自动卸载旧模型（仅一份占用 VRAM）
- 配置路径：Desktop → Developer → Server Settings

## GPU Offload 原理

| 值 | 行为 |
|----|------|
| `0.0` | 全 CPU 推理 |
| `0.5` | 半量层卸载到 GPU |
| `1.0` | 全量卸载到 VRAM（推荐 RTX 系列） |

Qwen/Qwen2 系列推荐 `0.7~0.9`（部分层 CPU），7B 模型 8GB VRAM 够用。

## SDK 安装

```bash
pip install lmstudio
```

Python SDK 文档：https://lmstudio.ai/docs/python/basic-usage
