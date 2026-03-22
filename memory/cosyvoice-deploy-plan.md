# CosyVoice 部署计划

> 生成日期: 2026-03-21

## 目标
在 Windows PC 上部署 CosyVoice TTS 服务，实现局域网内可访问

---

## 硬件环境
- OS: Windows
- GPU: NVIDIA 显卡（支持 CUDA）
- 网络: 局域网

---

## 部署步骤

### 步骤 1: 安装 Docker Desktop
1. 下载: https://www.docker.com/products/docker-desktop
2. 安装并启动
3. 验证: `docker --version`

### 步骤 2: 启用 GPU 支持
Docker Desktop → Settings → GPU → 勾选 GPU

或确认 WSL2 已安装:
```powershell
wsl --status
```

### 步骤 3: 拉取并运行 CosyVoice 镜像
```powershell
docker run -d --name cosyvoice --gpus all -p 8188:8188 -v cosyvoice-data:C:\data\voices neosun/cosyvoice:latest
```

### 步骤 4: 验证部署
1. 浏览器访问: `http://localhost:8188`
2. 确认 Web UI 正常加载

### 步骤 5: 局域网访问
1. 查询本机 IP:
   ```powershell
   ipconfig
   ```
   找到 IPv4 地址，如 `192.168.1.100`

2. 其他设备访问: `http://192.168.1.100:8188`

---

## API 调用示例

### TTS 生成
```bash
curl -X POST http://192.168.1.100:8188/tts ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"你好世界\", \"voice\": \"中文女声\"}"
```

### 语音克隆（需要提供音频参考）
```bash
curl -X POST http://192.168.1.100:8188/clone ^
  -F "audio=@参考音频.wav" ^
  -F "text=要转语音的文本"
```

---

## 常用命令

| 操作 | 命令 |
|------|------|
| 停止服务 | `docker stop cosyvoice` |
| 启动服务 | `docker start cosyvoice` |
| 查看日志 | `docker logs -f cosyvoice` |
| 重启 | `docker restart cosyvoice` |
| 删除容器 | `docker rm -f cosyvoice` |

---

## 注意事项

1. 首次启动需要下载模型（约 2-3GB），耐心等待
2. 确保防火墙允许 8188 端口
3. GPU 显存建议 6GB 以上
4. 模型文件会持久化在命名卷 `cosyvoice-data` 中

---

## Niko (Mac) 调用方式

部署完成后，Niko 可以通过 HTTP API 调用:

```python
import requests

def tts(text):
    resp = requests.post(
        "http://192.168.x.x:8188/tts",
        json={"text": text, "voice": "中文女声"}
    )
    return resp.content  # 音频数据
```
