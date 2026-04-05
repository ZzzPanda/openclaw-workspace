#!/usr/bin/env python3
"""
调用 LM Studio 本地大模型（直接转发，不经过云端模型）

功能：
- 单次对话 / 多轮对话（session 维系上下文）
- Idle TTL：超过 idle_timeout 秒未调用，自动释放 VRAM
- System prompt 可自定义
"""

import sys
import os
import json
import time
import urllib.request
import urllib.error

# ============ 配置 ============
BASE_URL = "http://192.168.30.16:1234"
DEFAULT_MODEL = "mistralai/ministral-3-14b-reasoning"
SKILL_DIR = os.path.expanduser("~/.openclaw/workspace/skills/local-lm")
SYSTEM_PROMPT_FILE = os.path.join(SKILL_DIR, "system_prompt.txt")
IDLE_TIMEOUT = 180  # 3 分钟（秒）
SESSION_DIR = os.path.join(SKILL_DIR, "sessions")
STATE_FILE = os.path.join(SKILL_DIR, ".last_call")

def get_default_system_prompt() -> str:
    """从文件读取默认 system prompt"""
    if os.path.exists(SYSTEM_PROMPT_FILE):
        with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "You are a helpful assistant."

DEFAULT_SYSTEM = get_default_system_prompt()
# ==============================


def get_last_call_time() -> float:
    """读取上次调用时间戳"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return float(f.read().strip())
    return 0

def set_last_call_time():
    """更新上次调用时间戳"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(time.time()))

def get_loaded_model_instance() -> str | None:
    """查询当前已加载模型的 instance_id"""
    req = urllib.request.Request(
        f"{BASE_URL}/api/v1/models",
        headers={"Authorization": "Bearer lm"},
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            loaded = data.get("models", [])
            for model in loaded:
                instances = model.get("loaded_instances", [])
                if instances:
                    return instances[0].get("instance_id")
    except Exception:
        pass
    return None

def unload_model():
    """卸载当前模型，释放 VRAM"""
    instance_id = get_loaded_model_instance()
    if not instance_id:
        print("[local-lm] 模型未加载，无需卸载", file=sys.stderr)
        return

    payload = json.dumps({"instance_id": instance_id}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/v1/models/unload",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": "Bearer lm"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(f"[local-lm] 已卸载模型: {result}", file=sys.stderr)
    except Exception as e:
        print(f"[local-lm] 卸载失败: {e}", file=sys.stderr)

def load_model(model: str) -> bool:
    """加载模型（直接调 chat completions 会自动加载，这里不做预加载）"""
    return True

def call_lmstudio(prompt: str, system_prompt: str = DEFAULT_SYSTEM, messages: list = None) -> tuple:
    """调用 Chat Completions，返回 (回答, 更新后的messages)"""
    
    # 更新最后调用时间
    set_last_call_time()

    # 构建消息
    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    if messages:
        full_messages.extend(messages)
    full_messages.append({"role": "user", "content": prompt})

    payload = {
        "model": DEFAULT_MODEL,
        "messages": full_messages,
        "max_tokens": 2048,
        "temperature": 0.7,
        "stream": False
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/v1/chat/completions",
        data=data,
        headers={"Content-Type": "application/json", "Authorization": "Bearer lm"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            msg = result["choices"][0]["message"]
            # 推理模型(如ministral-3-14b-reasoning)把内容放在 reasoning_content 里
            assistant_message = msg.get("content") or msg.get("reasoning_content") or ""
            updated_messages = full_messages + [{"role": "assistant", "content": assistant_message}]
            return assistant_message, updated_messages
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"连接失败: {e.reason}")


def load_session(session_id: str) -> list:
    """加载会话历史"""
    path = os.path.join(SESSION_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_session(session_id: str, messages: list):
    """保存会话历史"""
    os.makedirs(SESSION_DIR, exist_ok=True)
    path = os.path.join(SESSION_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)

    # 手动卸载
    if sys.argv[1] == "--unload":
        unload_model()
        sys.exit(0)

    # 多轮对话
    if sys.argv[1] == "--session":
        if len(sys.argv) < 4:
            print("用法: python3 call_lmstudio.py --session <session_id> \"<prompt>\" [system_prompt]", file=sys.stderr)
            sys.exit(1)
        session_id = sys.argv[2]
        prompt = sys.argv[3]
        system_prompt = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_SYSTEM

        messages = load_session(session_id)
        answer, updated = call_lmstudio(prompt, system_prompt, messages if messages else None)
        save_session(session_id, updated)
        print(answer)
    else:
        # 单次对话
        prompt = sys.argv[1]
        system_prompt = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_SYSTEM
        answer, _ = call_lmstudio(prompt, system_prompt)
        print(answer)
