# Wan22.com NSFW 工作流调研报告

> 调研时间：2026-03-22
> 注意：`wan22.com` 域名本身无法访问（DNS 解析到 benchmark IP 198.18.2.113），本报告聚焦于 **Wan 2.2 生态**中的 NSFW 工作流能力。

---

## 一、wan22.com 域名状态

| 项目 | 结果 |
|------|------|
| 域名 | wan22.com |
| DNS 解析 | 198.18.2.113（基准测试 IP，非真实公网服务） |
| 网页访问 | 无法连接 |
| 搜索索引 | 零结果 |

**结论**：`wan22.com` 可能不存在、仅供内网使用，或域名已失效。用户可能指的是以下相关域名之一：
- `wan22.ai` / `wan22.net` / `wan22.studio` / `wan22.io`

---

## 二、Wan 2.2 核心技术概述

Wan 2.2 是**阿里巴巴通义万相实验室（Tongyi Lab）**开发的开源视频生成模型系列。

| 特性 | 说明 |
|------|------|
| 架构 | **MoE（Mixture-of-Experts）**，首个开源 MoE 视频扩散模型 |
| 参数量 | Wan2.2-T2V-A14B（约 14B 参数），另有 1.3B 轻量版 |
| 分辨率 | 480P / 720P，24fps |
| 视频长度 | 通常 5 秒 |
| 许可证 | Apache 2.0（可商用） |
| 发布日期 | 2025 年 7 月 28 日 |
| GitHub | github.com/Wan-Video/Wan2.2 |
| HuggingFace | hf.co/Wan-AI/Wan2.2-I2V-A14B 等 |

---

## 三、NSFW 相关功能详解

### 1. 脱衣 / 换装（Undress / Clothing Removal）

| 维度 | 详情 |
|------|------|
| **实现方式** | 通过 NSFW LoRA 模型实现，叠加在 Wan 2.2 基础模型之上 |
| **典型 LoRA** | `change_clothes_to_nothing`（HuggingFace: rahul7star/wan2.2Lora）、`WAN22-action-missionian-pov-i2v-low`、各色 undress LoRA |
| **社区工作流** | ComfyUI 工作流：`Remove Clothes NSFW Wan22 Animate`（OpenArt） |
| **运行方式** | 本地 ComfyUI + Wan2.2 I2V 模型 + NSFW LoRA |
| **注意事项** | 公开平台（wan22.ai 等）有内容审核；无审核需本地运行 |
| **推荐配置** | RTX 3090/4090 + 24GB VRAM，FP8 量化可降低显存需求 |

### 2. 换脸（Face Swap）

| 维度 | 详情 |
|------|------|
| **官方方案** | Wan 2.2 **VACE（Visual Animation Condition）** 扩展，支持视频角色替换 |
| **相关模型** | `Wan-AI/Wan2.1-VACE-14B`、`ali-vilab/VACE-Wan2.1-1.3B-Preview` |
| **VACE 工作流** | 上传参考图像（角色 A）+ 目标视频 → 视频中角色 B 被替换为角色 A |
| **社区工作流** | Civitai: `Wan22 Fun VACE Video Face Swap With High Fidelity` |
| **第三方工具** | Reactor（开源最佳）、InsightFace inswapper 系列 |
| **效果** | 可保留原视频的动作、表情、环境；面部保真度高 |

### 3. 舞蹈动作迁移（Dance / Motion Transfer）

| 维度 | 详情 |
|------|------|
| **核心模型** | **Wan2.2 Animate**（专精动作迁移的分支） |
| **功能模式** | **Animation 模式**：输入静态人物图 + 动作参考视频 → 人物按视频动作跳舞 |
| **技术原理** | 骨骼信号控制身体动作 + 人脸隐式特征驱动表情 |
| **适用场景** | TikTok 舞蹈复刻、武术动作、影视表演迁移 |
| **效果评价** | 手指细节、表情、动作连贯性均较好，社区反馈"几乎无鬼畜" |
| **资源** | HuggingFace Space: `Wan-AI/Wan2.2-Animate`（可免费在线体验） |

### 4. 动作迁移（Pose / Action Transfer）

| 维度 | 详情 |
|------|------|
| **与舞蹈迁移的关系** | 舞蹈迁移是动作迁移的子集，动作迁移涵盖所有人体动作 |
| **技术方案** | Wan2.2 Animate 的 **骨骼信号（skeleton signal）** + **空间对齐融合** |
| **Replacement 模式** | 同时替换角色 + 保留原视频动作；Animation 模式则仅迁移动作 |
| **辅助技术** | 辅助"重光照 LoRA"用于角色替换后与环境融合 |

---

## 四、其他有趣的 NSFW / 创作功能

| 功能 | 说明 |
|------|------|
| **全身替换** | 将视频中原角色替换为任意角色（包括体型、姿态、表情全部迁移） |
| **换装视频** | 在视频中替换衣物纹理，同时保持光影、遮挡关系自然 |
| **NSFW Image-to-Video** | 将静态裸体/半裸图像转换为动态视频 |
| **LoRA 生态** | Civitai/TensorArt 上有大量 NSFW 专用 LoRA（姿势、场景、动作等） |
| **ComfyUI 整合包** | 一键整合包（含模型+LoRA+工作流），降低使用门槛 |

---

## 五、API 与自动化调用

### 官方 / 第三方 API

| 提供方 | 说明 |
|--------|------|
| **wan22.ai** | 付费订阅制，Creator Plan $19.9/月，约 20 个视频额度 |
| **wan22.net** | 集成 Wan 2.2/2.5、Flux、VEO3，支持 API |
| **Atlas Cloud** | Wan2.2 Media Models API，透明定价 |
| **Kie.ai** | Wan 2.6 API，多镜头 1080p，支持 T2V/I2V/Reference-to-Video |
| **Alibaba DashScope** | 官方基准 API（最低价），但有内容审核 |
| **HuggingFace Inference API** | 部分模型支持 |

### 本地自动化

- **ComfyUI** 是最流行的本地自动化方式
- GitHub 有 Wan2.2 完整推理代码，支持多 GPU（`torchrun`）
- LoRA 热插拔，无需重新训练基础模型

---

## 六、开源替代品

| 模型 / 工具 | 特点 | NSFW 支持 |
|------------|------|-----------|
| **Wan 2.2 / 2.1** | 阿里巴巴开源，MoE 架构，720P 视频 | 本地运行无限制 |
| **Animate Anyone**（阿里） | 人物动画专用，动作迁移效果优秀 | 需自行找 NSFW LoRA |
| **MuseTalk** | 数字人口型同步 | 否 |
| **EchoMimic** | 音频驱动数字人 | 否 |
| **LoRA（NSFW 专用）** | TensorArt、Civitai 大量 NSFW LoRA | 支持（本地） |

**综合评价**：Wan 2.2 是目前**开源生态最完善**的视频生成 + 动作迁移模型，NSFW 能力通过 LoRA 扩展实现。

---

## 七、价格 / 付费模式

| 平台 | 模式 | 价格参考 |
|------|------|---------|
| wan22.ai | 订阅制 | Creator Plan $19.9/月（约 20 个视频） |
| 本地运行 | 一次性硬件成本 | RTX 4090（约 ¥15000） |
| API（DashScope） | 按量计费 | 最低基准价，有审核 |
| Kie.ai / Atlas Cloud | 按量计费 | 竞争性定价 |
| HuggingFace Space | 免费额度 | Wan2.2 Animate 可免费在线用 |

---

## 八、总结

`wan22.com` 域名本身**无法访问**，可能是一个不存在或内网化的地址。用户实际想了解的应是 **Wan 2.2 视频生成生态**。

**核心结论**：
1. **Wan 2.2 Animate** 是动作迁移 / 舞蹈复刻的最佳开源方案
2. **VACE** 模型支持高质量视频换脸
3. **NSFW LoRA**（undress、clothing removal）在 Civitai/TensorArt 有大量社区资源，需本地 ComfyUI 运行以绕过审核
4. **完全免费 + 无限制** 的方案是本地部署（ComfyUI + Wan 2.2 + NSFW LoRA），硬件门槛约 RTX 3090/4090
5. 在线平台均有不同程度的内容审查

---

*调研基于 2026-03-22 的公开信息，部分细节可能随版本更新变化。*
