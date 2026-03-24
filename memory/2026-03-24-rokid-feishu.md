# Session: 2026-03-24 15:12:47 UTC

- **Session Key**: agent:main:main
- **Session ID**: b3cb96ba-788f-4172-82cd-c14d46a92cb9
- **Source**: feishu

## Conversation Summary

assistant: ✅ New session started · model: minimax-cn/MiniMax-M2.7
user: System: [2026-03-24 22:49:13 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b531e084b80a0b3bdccd7f6dc2da]

A new session was started via /new or /reset. Run your Session Startup sequence - read the required files before responding to the user. Then greet the user in your configured persona, if one is provided. Be yourself - use your defined voice, mannerisms, and mood. Keep it to 1-3 sentences and ask what they want to do. If the runtime model differs from default_model in the system prompt, mention the default model. Do not mention internal steps, files, tools, or reasoning.
Current time: Tuesday, March 24th, 2026 — 10:49 PM (Asia/Shanghai) / 2026-03-24 14:49 UTC
assistant: Yo Dingzhen 🦐 晚上好！今天想搞点啥？
user: System: [2026-03-24 22:49:31 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b531e096528a4b29f4f0b2a5a013]

Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b531e096528a4b29f4f0b2a5a013",
  "sender_id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "sender": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "timestamp": "Tue 2026-03-24 22:49 GMT+8"
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

你搜索一下 rokid ai眼镜，尤其关注目前它能连接飞书吗
assistant: 搜到了，来了来了 🦐

**好消息：Rokid Glasses 确实可以连接飞书，但需要借助 OpenClaw 作为"桥梁"。**

具体逻辑是这样的：

### 🔗 完整链路
```
Rokid Glasses → OpenClaw → 飞书
```

### 📅 关键时间线
- **2026年2月11日**：Rokid 官宣为 Rokid Glasses 上线「自定义智能体」功能，支持通过 **SSE 接口**接入 OpenClaw 框架
- **OpenClaw 本身支持飞书插件**（官方出了插件包），所以接进来就能操作飞书

### ✨ 接入后能干啥（通过 OpenClaw）
- 语音控制发送飞书消息
- 查询日历、任务
- 搜索文档
- 各种飞书功能的语音控制

### ⚠️ 注意事项
1. **这不是原生直连**，需要你的 OpenClaw 已配置好飞书机器人（就是现在我跑在上面的这个 niko bot）
2. 需要在 Rokid Glasses 的「灵珠平台」上配置 OpenClaw 的 SSE 接口地址
3. GitHub 上已经有人做了 `clawsses` 这个项目专门干这事：`dweddepohl/clawsses`

### 🤔 简单说
**Rokid Glasses + OpenClaw + 飞书插件 = 用语音操控飞书**

你想折腾一下吗？我可以帮你规划步骤，毕竟你的 OpenClaw 已经跑着飞书 bot 了，接入 Rokid 理论上不难。
user: System: [2026-03-24 22:53:19 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b531e1b254ca8b32c805d17cf9e3]

Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b531e1b254ca8b32c805d17cf9e3",
  "sender_id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "sender": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "timestamp": "Tue 2026-03-24 22:53 GMT+8"
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

再给我解释一下这是怎么个链路
assistant: <final>
好，用大白话解释：

**你现在的状态**
```
你（手机/电脑） → OpenClaw（你的bot）→ 飞书
```

我（Niko）跑在 OpenClaw 上，你通过飞书跟我说话，我来帮你执行各种操作。

---

**加上 Rokid Glasses 之后**
```
Rokid Glasses（语音）→ OpenClaw → 飞书
                        ↑
                  你的 OpenClaw（同一套）
```

---

**三个组件各干各的**

| 组件 | 做什么 |
|------|--------|
| **Rokid Glasses** | 负责收音和播放。你说话，它采集语音。 |
| **OpenClaw** | 负责理解和执行。你说"给张三发消息"，OpenClaw 理解这个意图，调用工具完成任务。 |
| **飞书** | 负责消息的展示和送达。OpenClaw 执行完，结果通过飞书发出去。 |

---

**类比一下**

把 OpenClaw 想成一个**老黄牛**：
- Rokid Glasses 是**你的嘴**，负责说话
- 飞书是**收件人**，负责听结果
- OpenClaw 是**老黄牛本身**，听懂你的话然后干活

Rokid 本身不聪明，它只是把语音传给 OpenClaw，OpenClaw 处理完再把结果送回飞书。

---

**所以关键技术点就一个**
Rokid Glasses 通过 **SSE（Server-Sent Events）** 接口连接 OpenClaw Gateway——这个 Gateway 就是你机器上跑着的 OpenClaw 服务。

简单说：**Rokid 是耳朵和嘴，OpenClaw 是大脑，飞书是喉咙**。
</final>
user: System: [2026-03-24 22:54:01 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b531e165ed8a0b2dc6b418a6c384]

Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b531e165ed8a0b2dc6b418a6c384",
  "sender_id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "sender": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "timestamp": "Tue 2026-03-24 22:54 GMT+8"
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

项目的链接发我看看
assistant: <final>
GitHub 项目在这：

**clawsses** — 用 Rokid Glasses 连接 OpenClaw
https://github.com/dweddepohl/clawsses

旁边那个 `clawsses` 是项目名，把 "claws"（OpenClaw 的爪子）+ "glasses" 拼在一起了，挺会起名 😂

里面应该有配置说明，不过我没成功抓取到页面内容，你点进去看看 / 让我帮你截个图也行。
</final>
user: System: [2026-03-24 22:56:14 GMT+8] Feishu[niko] DM | ou_2fa349acf49b639d03a8fb5cae5dd3b3 [msg:om_x100b531e2e1398a4b324673d80f5f82]

Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b531e2e1398a4b324673d80f5f82",
  "sender_id": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "sender": "ou_2fa349acf49b639d03a8fb5cae5dd3b3",
  "timestamp": "Tue 2026-03-24 22:56 GMT+8"
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

感觉很麻烦，算求
assistant: <final>
哈哈合理，毕竟现在用飞书跟我说话已经挺方便了，加个眼镜也没实质性提升 😄

等哪天 Rokid Glasses 出了原生飞书插件再说吧。
</final>
