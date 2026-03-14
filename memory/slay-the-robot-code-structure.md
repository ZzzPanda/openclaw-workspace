# Slay The Robot 代码结构分析

> 项目地址: https://github.com/ZzzPanda/Slay-The-Robot
> 游戏引擎: Godot 4.4 (GDScript)
> 类型: 类杀戮尖塔( slay the spire)卡牌构建框架

---

## 📂 整体目录结构

```
Slay-The-Robot/
├── autoload/              # 全局单例 (游戏核心系统)
├── scripts/               # 核心逻辑脚本
│   ├── actions/           # 动作系统
│   ├── combatants/        # 战斗单位 (玩家/敌人)
│   ├── ui/                # UI 界面
│   ├── artifacts/         # 神器系统
│   ├── status_effects/    # 状态效果
│   ├── validators/       # 条件验证器
│   └── ...
├── scenes/                # 场景文件 (.tscn)
├── data/                  # 数据定义
│   ├── prototype/         # 原型数据 (卡牌/敌人/神器等)
│   ├── readonly/         # 静态数据
│   └── mutable/          # 玩家存档数据
├── external/sprites/      # 美术素材
├── addons/                # 插件
└── project.godot          # Godot 项目配置
```

---

## 🔧 核心系统详解

### 1. 动作系统 (actions/)

**概述**: 驱动游戏中所有行为的系统，从攻击到抽卡，从商店购买到世界生成，都通过动作系统完成。

#### 基础动作
| 文件 | 功能 |
|------|------|
| `BaseAction.gd` | 所有动作的基类，定义 execute() 方法 |
| `BaseAsyncAction.gd` | 异步动作基类，支持延时动作 |

#### 战斗动作
| 文件 | 功能 |
|------|------|
| `ActionAttack.gd` | 造成伤害 |
| `ActionBlock.gd` | 获得格挡 |
| `ActionDirectDamage.gd` | 直接伤害 |
| `ActionAddEnergy.gd` | 增加能量 |
| `ActionDraw.gd` | 抽卡 |
| `ActionEndTurn.gd` | 结束回合 |

#### 卡牌动作 (cardset_actions/)
| 文件 | 功能 |
|------|------|
| `ActionAddCardsToHand.gd` | 抽牌到手上 |
| `ActionPlayCards.gd` | 出牌 |
| `ActionDiscardCards.gd` | 丢弃卡牌 |
| `ActionExhaustCards.gd` | 耗尽卡牌 |
| `ActionUpgradeCards.gd` | 升级卡牌 |
| `ActionTransformCards.gd` | 转换卡牌 |
| `ActionBanishCards.gd` | 抹除卡牌 |

#### 玩家动作 (player_actions/)
| 文件 | 功能 |
|------|------|
| `ActionAddArtifact.gd` | 获得神器 |
| `ActionAddMoney.gd` | 增加金币 |
| `ActionAddConsumable.gd` | 添加消耗品 |

#### 世界生成动作 (world_generation_actions/)
| 文件 | 功能 |
|------|------|
| `ActionGenerateAct.gd` | 生成地图/关卡 |
| `ActionStartCombat.gd` | 开始战斗 |

---

### 2. 战斗单位系统 (combatants/)

**概述**: 玩家和敌人的基类实现

| 文件 | 功能 |
|------|------|
| `BaseCombatant.gd` | 战斗单位基类，包含生命值、格挡、状态效果管理等 |
| `Player.gd` | 玩家特殊逻辑 |
| `Enemy.gd` | 敌人 AI 和意图系统 |
| `HealthLayer.gd` | 多层血条系统 |
| `LayeredHealthBar.gd` | 血条 UI |

**关键机制**:
- 血量分层 (多层血条)
- 状态效果堆叠
- 意图系统 (敌人下回合行动计划)

---

### 3. 状态效果系统 (status_effects/)

**概述**: 游戏中各种增益/减益效果

| 文件 | 功能 |
|------|------|
| `BaseStatusEffect.gd` | 状态效果基类 |
| `StatusEffectBomb.gd` | 炸弹效果 |
| `StatusEffectDuplicateCardPlays.gd` | 复制出牌 |
| `StatusEffectAttachedCard.gd` | attached 卡牌 |

---

### 4. 拦截器系统 (action_interceptors/)

**概述**: 在动作执行前修改行为的系统，实现复杂的卡牌交互

| 文件 | 功能 |
|------|------|
| `BaseActionInterceptor.gd` | 拦截器基类 |
| `InterceptorDamageIncrease.gd` | 伤害增加 |
| `InterceptorDuplicateAttacks.gd` | 攻击复制 |
| `InterceptorDuplicateCardPlays.gd` | 出牌复制 |
| `InterceptorNegateDebuff.gd` | 免疫debuff |
| `InterceptorPreserveBlock.gd` | 保留格挡 |

---

### 5. 验证器系统 (validators/)

**概述**: 条件判断系统，用于卡牌是否可用、UI 显示等

| 分类 | 文件 | 功能 |
|------|------|------|
| 卡牌 | `ValidatorCardColor.gd` | 卡牌颜色验证 |
| 卡牌 | `ValidatorCardRarity.gd` | 卡牌稀有度验证 |
| 卡牌 | `ValidatorCardType.gd` | 卡牌类型验证 |
| 卡牌 | `ValidatorCardEnergyCost.gd` | 能量费用验证 |
| 卡牌 | `ValidatorCardTag.gd` | 卡牌标签验证 |
| 出牌 | `ValidatorCardPlayEnergyInput.gd` | 出牌能量验证 |
| 战斗 | `ValidatorInCombat.gd` | 是否在战斗中 |
| 战斗 | `ValidatorEnemyAttacking.gd` | 敌人是否在攻击 |
| 玩家 | `ValidatorPlayerHealth.gd` | 玩家生命值验证 |

---

### 6. UI 系统 (ui/)

#### 核心 UI
| 文件 | 功能 |
|------|------|
| `Combat.gd` | 战斗场景主控制器 |
| `Hand.gd` | 手牌管理 |
| `Card.gd` | 卡牌 UI 组件 |
| `Map.gd` | 地图系统 |

#### 菜单 UI (menus/)
| 文件 | 功能 |
|------|------|
| `TitleScreen.gd` | 标题画面 |
| `MainMenu.gd` | 主菜单 |
| `NewRunMenu.gd` | 新游戏菜单 |
| `CodexMenu.gd` | 百科菜单 |

#### 战斗 UI (general/)
| 文件 | 功能 |
|------|------|
| `DialogueOverlay.gd` | 对话系统 |
| `KeywordTooltip.gd` | 关键词提示 |

---

### 7. 神器系统 (artifacts/)

**概述**: 被动效果系统

| 文件 | 功能 |
|------|------|
| `BaseArtifact.gd` | 神器基类 |
| `ArtifactBlockOnAttacks.gd` | 攻击时获得格挡 |
| `ArtifactDrawOnKill.gd` | 击杀时抽牌 |
| `ArtifactRetainHand.gd` | 保留手牌 |

---

### 8. 数据系统 (data/)

#### 原型数据 (prototype/)
| 文件 | 功能 |
|------|------|
| `CardData.gd` | 卡牌数据定义 |
| `EnemyData.gd` | 敌人数据定义 |
| `ArtifactData.gd` | 神器数据定义 |
| `PlayerData.gd` | 玩家数据定义 |

#### 存档数据 (mutable/)
| 文件 | 功能 |
|------|------|
| `CombatStatsData.gd` | 战斗统计数据 |
| `ProfileData.gd` | 玩家档案 |
| `ShopData.gd` | 商店数据 |
| `LocationData.gd` | 位置数据 |

#### 静态数据 (readonly/)
| 文件 | 功能 |
|------|------|
| `ActData.gd` | 关卡数据 |
| `EventData.gd` | 事件数据 |
| `StatusEffectData.gd` | 状态效果数据 |
| `CharacterData.gd` | 角色数据 |

---

### 9. 全局单例 (autoload/)

| 文件 | 功能 |
|------|------|
| `Global.gd` | 全局状态和游戏主循环 (181KB，核心文件) |
| `ActionHandler.gd` | 动作处理器，执行动作队列 |
| `ActionGenerator.gd` | 动作生成器 |
| `Random.gd` | 确定性随机数生成器 (重要！) |
| `FileLoader.gd` | 文件加载器 |
| `Scenes.gd` | 场景管理 |
| `Scripts.gd` | 脚本管理 |
| `Signals.gd` | 信号系统 |
| `DebugLogger.gd` | 调试日志 |

---

## 🔄 系统关系图

```
┌─────────────────────────────────────────────────────────────┐
│                      Global.gd                              │
│              (全局状态、游戏循环、信号)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ ActionHandler │ │ Random.gd    │ │ FileLoader   │
│   动作系统     │ │  确定性随机   │ │   文件加载    │
└──────┬───────┘ └──────────────┘ └──────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                     Actions (动作层)                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  │ 攻击    │ │ 抽卡    │ │ 获得能量 │ │ 状态效果 │            │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘            │
│       │           │           │           │                  │
│       └───────────┴───────────┴───────────┘                  │
│                       │                                       │
│                       ▼                                       │
│            ┌─────────────────────┐                            │
│            │ ActionInterceptors  │  (拦截器，可修改动作)       │
│            └─────────────────────┘                            │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                 Combatants (战斗单位层)                        │
│  ┌────────────────┐              ┌────────────────┐          │
│  │    Player     │              │     Enemy      │          │
│  │ - 生命值       │ ◄──────────► │ - 意图系统     │          │
│  │ - 格挡         │    战斗      │ - AI 行为      │          │
│  │ - 状态效果     │              │ - 状态效果     │          │
│  └────────────────┘              └────────────────┘          │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                      UI Layer                                 │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │
│  │ Hand   │ │ Card   │ │ Combat │ │ Map    │ │ Shop   │     │
│  │ 手牌   │ │ 卡牌   │ │ 战斗   │ │ 地图   │ │ 商店   │     │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘     │
│                                                              │
│  使用 Validators 验证是否可交互                                │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                   Data Layer                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ CardData    │ │ EnemyData   │ │PlayerData   │            │
│  │ 卡牌定义    │ │ 敌人定义    │ │ 玩家存档    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│                                                              │
│  自动保存到 JSON (SerializableData)                          │
└──────────────────────────────────────────────────────────────┘
```

---

## 📌 核心设计模式

### 1. 数据驱动 (Data-Driven)
- 卡牌、敌人、神器都通过 JSON/GD 脚本定义
- 很少需要硬编码新内容

### 2. 动作队列 (Action Queue)
- 所有行为都封装为 Action 对象
- ActionHandler 顺序执行，支持异步

### 3. 确定性随机 (Deterministic RNG)
- Random.gd 确保相同种子产生相同结果
- 防止存档刷钱

### 4. 信号系统 (Signals)
- 使用 Godot Signal 进行解耦通信
- Signals.gd 集中管理全局信号

### 5. 自动保存 (Auto-Save)
- SerializableData 自动序列化到 JSON
- 无需手动处理存档

---

## 🎯 扩展点

如果你想 mod 这个框架，可以:

1. **添加新卡牌** → 在 `data/prototype/` 添加 CardData
2. **添加新敌人** → 在 `data/prototype/` 添加 EnemyData
3. **添加新神器** → 在 `scripts/artifacts/` 添加 Artifact
4. **添加新动作** → 在 `scripts/actions/` 添加 Action
5. **添加新验证条件** → 在 `scripts/validators/` 添加 Validator

---

*文档创建时间: 2026-03-12*
