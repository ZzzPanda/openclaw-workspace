#!/usr/bin/env python3
"""TTS → OPUS 语音气泡，发送到飞书"""
import subprocess
import os
import sys
import json
import uuid
import urllib.request
import urllib.error

TEXT = sys.argv[1] if len(sys.argv) > 1 else "测试消息"
CHAT_ID = sys.argv[2] if len(sys.argv) > 2 else "oc_348222757eed69203faf73d7111371eb"

TMP_DIR = f"/tmp/openclaw/tts-opus"
os.makedirs(TMP_DIR, exist_ok=True)

mp3_path = f"{TMP_DIR}/temp-{os.getpid()}.mp3"
opus_path = f"{TMP_DIR}/voice-{os.getpid()}.opus"

# 1. 用 say 生成 MP3
subprocess.run(["say", "-o", mp3_path, TEXT], check=True, capture_output=True)

# 2. 转 OPUS
subprocess.run([
    "ffmpeg", "-i", mp3_path,
    "-c:a", "libopus", "-b:a", "128k",
    opus_path, "-y"
], capture_output=True)

os.remove(mp3_path)

# 3. 读取 OPUS 文件为 base64
with open(opus_path, "rb") as f:
    opus_data = base64.b64encode(f.read()).decode()

os.remove(opus_path)

# 4. 发送到飞书（调用 OpenClaw MCP HTTP endpoint）
# 先获取 gateway port
gateway_port = os.environ.get("OPENCLAW_GATEWAY_PORT", "18790")

payload = json.dumps({
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
        "channel": "feishu",
        "target": f"chat:{CHAT_ID}",
        "asVoice": True,
        "buffer": f"data:audio/opus;base64,{opus_data}"
    },
    "id": str(uuid.uuid4())
}).encode()

req = urllib.request.Request(
    f"http://127.0.0.1:{gateway_port}/rpc",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("OK:", resp.read().decode())
except Exception as e:
    print(f"发送失败: {e}", file=sys.stderr)
