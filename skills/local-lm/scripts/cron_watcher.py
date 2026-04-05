#!/usr/bin/env python3
"""local-lm cron trigger watcher - 监听 trigger 文件并执行"""
import sys, os, json, time

TRIGGER_FILE = os.path.expanduser("~/.openclaw/workspace/skills/local-lm/.trigger")
RESULT_FILE = os.path.expanduser("~/.openclaw/workspace/skills/local-lm/.last_result")
LOG_FILE = os.path.expanduser("~/.openclaw/workspace/skills/local-lm/.cron.log")

SCRIPT = os.path.expanduser("~/.openclaw/workspace/skills/local-lm/scripts/call_lmstudio.py")

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def main():
    if not os.path.exists(TRIGGER_FILE):
        return

    with open(TRIGGER_FILE) as f:
        trigger = json.load(f)

    prompt = trigger.get("prompt", "")
    open_id = trigger.get("open_id", "")
    log(f"触发执行: prompt={prompt[:50]}..., open_id={open_id}")

    # 执行 Python 脚本
    import subprocess
    try:
        result = subprocess.run(
            ["python3", SCRIPT, prompt],
            capture_output=True, text=True, timeout=120
        )
        answer = result.stdout.strip() or result.stderr.strip() or "(无输出)"
        log(f"脚本输出: {answer[:100]}")
    except Exception as e:
        answer = f"执行失败: {e}"
        log(f"错误: {e}")

    # 写入结果文件
    with open(RESULT_FILE, "w") as f:
        json.dump({"answer": answer, "open_id": open_id, "timestamp": time.time()}, f)

    # 删除 trigger 文件避免重复执行
    os.remove(TRIGGER_FILE)
    log("执行完成，trigger 已清除")

if __name__ == "__main__":
    main()
