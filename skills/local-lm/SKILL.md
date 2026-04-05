---
name: lm-local
description: 直接调用本地 LM Studio 大模型，不经过云端模型。触发方式：1) 文本命令 `!lm-local <提示词>`；2) 自然语言如"用 lm-local 回答：..."、"调用本地 LM Studio"、"用本地模型回答"。功能：将提示词通过 Python 脚本发送给本地 LM Studio API（POST /v1/chat/completions，stream=False），等待完整响应后原样输出，**raw dump 不经过任何云端模型解读**。适用场景：用户想要完全离线的大模型对话体验。
---

## ⚠️ 输出处理规则

**执行后直接 raw dump 输出，不送回模型解读。** 即：脚本返回什么就展示什么，不做任何理解和转述。

# Local LM Studio Skill

完全本地的大模型推理管道。**不消耗任何云端 token。**

## 触发方式

- **文本命令**: `!local-lm <提示词>` → 直接执行脚本
- **自然语言**: "用 local-lm 回答：..." → 同样执行脚本

## 两种模式

### 单次对话
```
!local-lm 你好
```
- 每次独立调用，不记忆上下文
- 默认 system prompt: "You are a helpful assistant. Keep responses concise."

### 多轮对话（保持上下文）
```
!local-lm --session <会话ID> <用户消息>
```

示例：
```
!local-lm --session buddy 你好吗
!local-lm --session buddy 你刚才说什么？
```

**多轮模式细节：**
- 同一 session_id 的对话自动累积历史（最多支持约 20 轮，视模型 context window 而定）
- session 文件保存在 `~/.openclaw/workspace/skills/local-lm/sessions/<session_id>.json`
- 不同 session_id 相互独立

## 执行脚本

```bash
# 单次
python3 ~/.openclaw/workspace/skills/local-lm/scripts/call_lmstudio.py "<提示词>" [system_prompt]

# 多轮（session_id 在前，提示词在后）
python3 ~/.openclaw/workspace/skills/local-lm/scripts/call_lmstudio.py --session <会话ID> "<提示词>" [system_prompt]
```

## VRAM 空闲释放机制

idle 检测 + 手动卸载结合：
- 每次调用记录时间戳
- 超过 3 分钟空闲再次调用 → 先 unload 再重新 load
- 模型保持在内存直到 idle evict 或手动 unload

**手动卸载（立即释放 VRAM）：**
```bash
python3 ~/.openclaw/workspace/skills/local-lm/scripts/call_lmstudio.py --unload
```

## 自定义 System Prompt

默认 system prompt 存储在 `system_prompt.txt`，直接编辑该文件即可自定义默认行为。

如需在对话时临时指定 system prompt，单次对话时作为第二个参数传入：

```
!local-lm 你现在的角色是一个物理学家，用中文回答
```

## 配置

- **地址**: `http://192.168.30.16:1234`
- **模型**: `mistralai/ministral-3-14b-reasoning`（14B Q4_K_M）
- **System prompt**: `system_prompt.txt`（可编辑）
- **Timeout**: 120s
- **Max tokens**: 2048
- **Temperature**: 0.7
- **Idle 检测**: 180s（3分钟空闲触发 unload + 重新 load）

## 示例对话

```
用户: !local-lm --session tech 解释一下量子计算
用户: !local-lm --session tech 它和传统计算的区别是什么
用户: !local-lm --session tech 能给我一个代码例子吗
用户: !local-lm --unload  # 手动释放 VRAM
```

## 错误处理

- 连接失败 → 打印错误信息，提示检查 LM Studio 是否运行
- API 超时 → 打印超时错误
