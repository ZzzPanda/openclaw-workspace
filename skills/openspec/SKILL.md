# OpenSpec Skill

**规范驱动开发 (Spec-Driven Development) 框架**，用于 AI 编码助手。

## 安装

```bash
npm install -g @fission-ai/openspec
```

## 初始化项目

```bash
# 在项目目录中初始化
openspec init . --tools claude

# 支持的工具: claude, cursor, copilot, windsurf, roocode 等
```

## 核心命令

| 命令 | 说明 |
|------|------|
| `openspec init` | 初始化 OpenSpec |
| `openspec new change <name>` | 创建新变更提案 |
| `openspec view` | 查看交互式仪表板 |
| `openspec status` | 显示变更状态 |
| `openspec validate` | 验证规范 |

## Claude Code 集成

初始化后会自动创建：
- `.claude/commands/opsx/` - 4 个命令
- `.claude/skills/` - 4 个 skill

### 常用命令

```
/opsx:propose   - 提出新需求变更
/opsx:explore   - 探索/查看现有规格
/opsx:apply      - 应用变更到代码
/opsx:archive   - 归档完成的变更
```

## 工作流 (4阶段)

1. **Specify** - 定义"做什么"和"为什么"，关注用户体验
2. **Plan** - 确定技术栈、架构、约束
3. **Tasks** - 拆分成可独立实现的小任务
4. **Implement** - 逐步实现，人工审核

## 使用场景

当用户想要：
- 用规范驱动的方式开发项目
- 让 AI 生成详细的规格文档后再写代码
- 将大任务拆分成可管理的小任务
- 替代"vibe coding"（模糊提示）方式

## 触发关键词

- "openspec"
- "规范驱动开发"
- "spec-driven"
- "用规范来开发"
