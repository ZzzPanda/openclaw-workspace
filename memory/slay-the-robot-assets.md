# Slay The Robot 素材替换清单

> 项目地址: https://github.com/ZzzPanda/Slay-The-Robot

## 📁 素材目录结构

```
Slay-The-Robot/
├── external/sprites/          # 外部素材（占位符为主）
│   ├── artifacts/             # 神器图标 (7个)
│   ├── cards/                 # 卡牌背景 (4个)
│   ├── characters/            # 角色立绘 (4角色×3=12个)
│   ├── enemies/               # 敌人精灵 (18个)
│   ├── events/                # 事件图片 (1个)
│   └── icon.svg              # 正式素材 - 项目图标
├── sprites/                   # 项目内置素材
│   ├── icon.png               # 占位符 - 应用图标
│   └── health_bar_frame.PNG  # 占位符 - 血条框架
├── scenes/                     # 场景文件 (.tscn)
├── themes/                     # 主题文件 (.tres)
└── addons/                     # 插件素材
```

---

## 🔴 占位符素材清单 (需要替换)

### 1. 敌人精灵 (enemies/) - 18个文件

| 文件名 | 尺寸 | 颜色 | 状态 |
|--------|------|------|------|
| enemy_red_small.png | 64×64 | 红色 | 🔴 占位符 |
| enemy_red_medium.png | 96×96 | 红色 | 🔴 占位符 |
| enemy_red_large.png | 128×128 | 红色 | 🔴 占位符 |
| enemy_blue_small.png | 64×64 | 蓝色 | 🔴 占位符 |
| enemy_blue_medium.png | 96×96 | 蓝色 | 🔴 占位符 |
| enemy_blue_large.png | 128×128 | 蓝色 | 🔴 占位符 |
| enemy_green_small.png | 64×64 | 绿色 | 🔴 占位符 |
| enemy_green_medium.png | 96×96 | 绿色 | 🔴 占位符 |
| enemy_green_large.png | 128×128 | 绿色 | 🔴 占位符 |
| enemy_yellow_small.png | 64×64 | 黄色 | 🔴 占位符 |
| enemy_yellow_medium.png | 96×96 | 黄色 | 🔴 占位符 |
| enemy_yellow_large.png | 128×128 | 黄色 | 🔴 占位符 |
| enemy_purple_small.png | 64×64 | 紫色 | 🔴 占位符 |
| enemy_purple_medium.png | 96×96 | 紫色 | 🔴 占位符 |
| enemy_purple_large.png | 128×128 | 紫色 | 🔴 占位符 |

**建议**: 替换为真正的敌人插画，建议三种尺寸对应 small/medium/large 三种敌人类型

---

### 2. 神器图标 (artifacts/) - 7个文件

| 文件名 | 尺寸 | 颜色 | 状态 |
|--------|------|------|------|
| artifact_red.png | 64×64 | 红色 | 🔴 占位符 |
| artifact_blue.png | 64×64 | 蓝色 | 🔴 占位符 |
| artifact_green.png | 64×64 | 绿色 | 🔴 占位符 |
| artifact_yellow.png | 64×64 | 黄色 | 🔴 占位符 |
| artifact_purple.png | 64×64 | 紫色 | 🔴 占位符 |
| artifact_orange.png | 64×64 | 橙色 | 🔴 占位符 |
| artifact_white.png | 64×64 | 白色 | 🔴 占位符 |

**建议**: 替换为独特的神器图标，每个神器应该有独立的美术设计

---

### 3. 卡牌背景 (cards/) - 4个文件

| 文件名 | 尺寸 | 颜色 | 状态 |
|--------|------|------|------|
| card_red.png | 96×96 | 红色 | 🔴 占位符 |
| card_blue.png | 96×96 | 蓝色 | 🔴 占位符 |
| card_green.png | 96×96 | 绿色 | 🔴 占位符 |
| card_orange.png | 96×96 | 橙色 | 🔴 占位符 |

**建议**: 替换为完整的卡牌模板背景，包含卡牌边框、费用孔、卡图区域等

---

### 4. 角色立绘 (characters/) - 12个文件

每个角色包含 3 个文件 (共4个角色):

| 角色 | 文件 | 尺寸 | 状态 |
|------|------|------|------|
| Red | character_red.png | 96×96 | 🔴 占位符 |
| Red | character_red_icon.png | 64×64 | 🔴 占位符 |
| Red | character_red_text_energy.png | 16×16 | 🔴 占位符 |
| Blue | character_blue.png | 96×96 | 🔴 占位符 |
| Blue | character_blue_icon.png | 64×64 | 🔴 占位符 |
| Blue | character_blue_text_energy.png | 16×16 | 🔴 占位符 |
| Green | character_green.png | 96×96 | 🔴 占位符 |
| Green | character_green_icon.png | 64×64 | 🔴 占位符 |
| Green | character_green_text_energy.png | 16×16 | 🔴 占位符 |
| Orange | character_orange.png | 96×96 | 🔴 占位符 |
| Orange | character_orange_icon.png | 64×64 | 🔴 占位符 |
| Orange | character_orange_text_energy.png | 16×16 | 🔴 占位符 |

**建议**: 
- 96×96: 角色全身立绘
- 64×64: 角色头像/图标
- 16×16: 能量图标（可能需要重新设计）

---

### 5. 事件图片 (events/) - 1个文件

| 文件名 | 尺寸 | 状态 |
|--------|------|------|
| event_pick_something.png | - | 🔴 占位符 |

---

### 6. UI 占位符

| 文件名 | 路径 | 状态 |
|--------|------|------|
| icon.png | sprites/ | 🔴 占位符 |
| health_bar_frame.PNG | sprites/ | 🔴 占位符 |

---

## 🟢 正式素材 (已确认)

| 文件名 | 路径 | 说明 |
|--------|------|------|
| icon.svg | external/sprites/ | 项目 Logo |

---

## 📋 替换优先级建议

### 高优先级 (游戏核心体验)
1. **卡牌背景** - 玩家最常看到
2. **角色立绘** - 职业选择和战斗展示
3. **敌人精灵** - 战斗核心视觉

### 中等优先级
4. **神器图标** - 被动能力展示
5. **UI 元素** - 血条框架、应用图标

### 低优先级
6. **事件图片** - 出现频率较低

---

## 🎨 素材规格参考

| 类型 | 建议尺寸 | 格式 |
|------|----------|------|
| 敌人 Small | 64×64 | PNG |
| 敌人 Medium | 96×96 | PNG |
| 敌人 Large | 128×128 | PNG |
| 神器图标 | 64×64 | PNG |
| 卡牌背景 | 256×384 (标准卡牌比例) | PNG |
| 角色立绘 | 128×128 | PNG |
| 角色头像 | 64×64 | PNG |

---

*文档创建时间: 2026-03-12*
