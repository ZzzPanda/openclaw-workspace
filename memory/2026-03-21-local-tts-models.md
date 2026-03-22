# Session: 2026-03-21 05:18:33 UTC

- **Session Key**: agent:main:main
- **Session ID**: e913c69e-8be8-47d6-89a7-009779794064
- **Source**: feishu

## Conversation Summary

user: Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.
When reading HEARTBEAT.md, use workspace file /Users/roger/.openclaw/workspace/HEARTBEAT.md (exact case). Do not read docs/heartbeat.md.
Current time: Saturday, March 21st, 2026 — 4:36 AM (Asia/Shanghai) / 2026-03-20 20:36 UTC
assistant: HEARTBEAT_OK
user: System: [2026-03-21 09:06:20 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b54eabe76b0acc2d215e3f2c946f]

Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b54eabe76b0acc2d215e3f2c946f",
  "sender_id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "sender": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "timestamp": "Sat 2026-03-21 09:06 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "name": "ou_2fa349acf49b639d03a8fb5cae5dd3b3"
}
```

调研一下有什么部署在本地的那种文字转语音的模型
assistant: 根据搜索结果，2026 年主流的本地部署开源 TTS 模型有这些选择：

## 🏆 推荐本地部署的 TTS 模型

### 1. **CosyVoice2-0.5B** ⭐ 最推荐
- **大小**: 0.5B 参数 (~1GB)
- **特点**: 阿里开源，支持中文、多语言，音质好，推理快
- **部署**: 消费级 GPU 即可运行

### 2. **Fish Speech V1.5**
- **大小**: ~3B 参数
- **特点**: 中文效果极佳，支持多语言，延迟低
- **部署**: 需要 6GB+ VRAM

### 3. **XTTS-v2**
- **大小**: ~1B 参数  
- **特点**: 支持 17 种语言，语音克隆能力强
- **部署**: 4GB VRAM 可运行

### 4. **Bark**
- **大小**: ~1B 参数
- **特点**: 生成自然语音，可加背景音乐/笑声
- **部署**: 需要 8GB+ VRAM

### 5. **Mozilla TTS**
- **大小**: 小型模型
- **特点**: 完全开源可商用，CPU 可跑
- **部署**: CPU 友好，延迟较高

---

## 🚀 快速部署方式

| 方式 | 命令 |
|------|------|
| **Ollama** | `ollama run` (部分模型) |
| **xtts-api-server** | Docker 一键部署 |
| **Coqui TTS** | `pip install coqui-tts` |
| **Fish Audio** | Docker 部署 |

---

## 💡 建议

- **中文为主**: 用 **CosyVoice2** 或 **Fish Speech**
- **CPU 优先**: **Coqui TTS** 或 **Mozilla TTS**
- **最快方案**: 用已封装好的 Docker 镜像（如 `ghcr.io/remsky/xtts-api-server`）

需要我帮你搭建其中一个吗？
user: System: [2026-03-21 13:12:56 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b54d6c34ceca0b3fa7e8643c5855]

Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b54d6c34ceca0b3fa7e8643c5855",
  "sender_id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "sender": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "timestamp": "Sat 2026-03-21 13:12 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "name": "ou_2fa349acf49b639d03a8fb5cae5dd3b3"
}
```

第一个方案 你先帮我看看部署流程
assistant: 找到两种部署方式：

## 🚀 方案一：Docker 一键部署（推荐）

最简单的方式，用这个现成镜像（带 Web UI + API + 语音克隆）：

```bash
docker run -d \
  --name cosyvoice \
  --gpus '"device=0"' \
  -p 8188:8188 \
  -v cosyvoice-data:/data/voices \
  neosun/cosyvoice:latest
```

**访问**: 浏览器打开 `http://localhost:8188`

---

## 🔧 方案二：官方 Docker（需要自己配置）

```bash
# 1. 克隆仓库
git clone https://github.com/FunAudioLLM/CosyVoice.git
cd CosyVoice

# 2. 构建 Docker 镜像
cd runtime/python
docker build -t cosyvoice:v1.0 .

# 3. 启动 gRPC 服务
docker run -d --runtime=nvidia -p 50000:50000 cosyvoice:v1.0 \
  /bin/bash -c "cd /opt/CosyVoice/CosyVoice/runtime/python/grpc && \
  python3 server.py --port 50000 --max_conc 4 --model_dir iic/CosyVoice-300M && sleep infinity"
```

---

## ⚠️ 前提条件

| 要求 | 说明 |
|------|------|
| **NVIDIA GPU** | 必须有 GPU + CUDA |
| **Docker** | 已安装 |
| **nvidia-docker** | 已配置 |

---

## 💡 建议

**方案一最简单**，一行命令搞定。要我帮你运行吗？需要确认：
1. Mac 上有 NVIDIA GPU 吗？（如果没有需要用 CPU 版或用远程服务器）
2. Docker 和 nvidia-docker 已安装？
user: System: [2026-03-21 13:16:28 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b54d6d40d24a8b2d177dd73696db]

Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b54d6d40d24a8b2d177dd73696db",
  "sender_id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "sender": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "timestamp": "Sat 2026-03-21 13:16 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "name": "ou_2fa349acf49b639d03a8fb5cae5dd3b3"
}
```

我有一台windows上有显卡和cuda ，本地局域网里要怎么搞
assistant: Windows 部署方案来了！

## 🪟 Windows 本地部署 CosyVoice

### 方式一：Docker Desktop（推荐）

1. **安装 Docker Desktop**
   - 下载: https://www.docker.com/products/docker-desktop
   - 记得勾选 "Use WSL 2" 或 "Use Hyper-V"

2. **安装 NVIDIA GPU 支持**
   - Docker Desktop → Settings → GPU
   - 或者用 nvidia-docker2（需要 WSL2）

3. **运行容器**
   ```powershell
   docker run -d --name cosyvoice --gpus all -p 8188:8188 -v cosyvoice-data:C:\data\voices neosun/cosyvoice:latest
   ```

4. **局域网访问**
   - 查 Windows IP: `ipconfig`
   - 其他设备访问: `http://你的IP:8188`

---

### 方式二：Windows 原生运行（不需要 Docker）

```powershell
# 1. 安装 CUDA 12.x + cuDNN（已安装略过）

# 2. 安装 Anaconda
# 下载: https://www.anaconda.com/download

# 3. 创建环境
conda create -n cosyvoice python=3.10
conda activate cosyvoice

# 4. 克隆项目
git clone https://github.com/FunAudioLLM/CosyVoice.git
cd CosyVoice

# 5. 安装依赖（可能需要手动处理 deepspeed）
pip install -r requirements.txt

# 6. 下载模型
# 首次运行会自动下载，或手动:
# git lfs install
# git clone https://www.modelscope.cn/iic/CosyVoice-300M.git pretrained_models/

# 7. 启动 WebUI
python webui.py --port 8188 --model_dir pretrained_models/CosyVoice-300M
```

---

### 🌐 局域网调用 API

启动后可以用 API：

```bash
# TTS 请求示例
curl -X POST http://192.168.x.x:8188/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好世界", "voice": "中文女声"}'
```

---

### 💡 建议

- **Docker 方式**更简单，依赖隔离更好
- **Windows 原生**调试方便但环境复杂

你想用哪种方式？我可以帮你一步步配置。
user: System: [2026-03-21 13:17:42 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b54d6d1a8eca8b3d63d819e5960b]

Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b54d6d1a8eca8b3d63d819e5960b",
  "sender_id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "sender": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "timestamp": "Sat 2026-03-21 13:17 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "name": "ou_2fa349acf49b639d03a8fb5cae5dd3b3"
}
```

1 方案 不用你搞 生成个plan给我
assistant: 已生成部署计划 → `memory/cosyvoice-deploy-plan.md`

## 快速概览

| 步骤 | 操作 |
|------|------|
| 1 | 安装 Docker Desktop |
| 2 | 启用 GPU 支持 |
| 3 | 运行: `docker run -d --name cosyvoice --gpus all -p 8188:8188 -v cosyvoice-data:C:\data\voices neosun/cosyvoice:latest` |
| 4 | 访问 `http://localhost:8188` |
| 5 | 查 IP `ipconfig`，局域网访问 |

有问题随时问 🦐
