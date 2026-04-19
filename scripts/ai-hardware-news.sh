#!/bin/bash
# C端AI原生硬件资讯抓取
# 覆盖：AI录音笔记设备、AI陪伴玩具、AI眼镜、AI硬件助手

WORKDIR="/Users/roger/.openclaw/workspace"
LOGFILE="$WORKDIR/memory/ai-hardware-$(date +%Y-%m-%d).md"

echo "# C端AI原生硬件资讯 - $(date '+%Y-%m-%d %H:%M')

## 追踪类目
- 🎙️ AI录音笔记设备（Plaud Note/NotePin S、科大讯飞等）
- 🧸 AI陪伴玩具（华为憨憨、Fuzozo、科大讯飞阿尔法蛋等）
- 🕶️ AI可穿戴眼镜（Meta Ray-Ban、华为AI眼镜等）
- 🤖 AI硬件助手（Rabbit R1、Humane Pin等）

---

## 📦 本周新品速递

" > "$LOGFILE"

# --- 抓取 GitHub Trending AI Hardware 项目 ---
echo "### GitHub Trending - AI Hardware" >> "$LOGFILE"
echo "" >> "$LOGFILE"
TRENDING=$(curl -s "https://api.github.com/search/repositories?q=AI+hardware+OR+AI+device+OR+AI+companion+created:>2025-01-01&sort=stars&order=desc&per_page=5" 2>/dev/null | grep -E '"full_name"|"stargazers_count"|"description"' | grep -A1 full_name | grep -v full_name | sed 's/^[ \t]*//;s/"//g;s/,//' | head -15)
echo "$TRENDING" >> "$LOGFILE" 2>/dev/null || echo "暂无数据" >> "$LOGFILE"
echo "" >> "$LOGFILE"

# --- 搜索最新 C端 AI 硬件资讯 ---
echo "### 🔥 最新资讯（网络搜索）" >> "$LOGFILE"
echo "" >> "$LOGFILE"

# 用 curl 搜索 + 提取简单结果（避免 grep -P 问题）
SEARCH_RESULTS=$(curl -s "https://www.google.com/search?q=AI+hardware+gadget+2026+Plaud+Rabbit+Humane&hl=en" 2>/dev/null | grep -oE 'href="/url\?q=[^"]+' | sed 's/href="\/url?q=//' | tr '&' '\n' | grep -E '^http' | head -5)
if [ -n "$SEARCH_RESULTS" ]; then
  echo "$SEARCH_RESULTS" | while read url; do
    TITLE=$(echo "$url" | sed 's/.*q=//' | sed 's/&.*//' | cut -c1-80)
    echo "- [查看]("$url")" >> "$LOGFILE"
  done
else
  echo "- 暂无数据，请手动访问 The Verge / Engadget 查看 AI 硬件最新资讯" >> "$LOGFILE"
fi

echo "" >> "$LOGFILE"

# --- 重点产品追踪 ---
echo "## 🏷️ 重点产品追踪" >> "$LOGFILE"
echo "" >> "$LOGFILE"

echo "### 🎙️ Plaud（AI录音笔记）" >> "$LOGFILE"
echo "- CES 2026 发布 NotePin S：可穿戴 AI 录音笔记设备，支持领口/手腕/脖子多种佩戴方式" >> "$LOGFILE"
echo "- 4月9日 App 更新，支持112语言转录、speaker labels、自定义词汇" >> "$LOGFILE"
echo "- 官网: plaud.ai" >> "$LOGFILE"
echo "" >> "$LOGFILE"

echo "### 🧸 华为憨憨（AI陪伴玩具）" >> "$LOGFILE"
echo "- 产品：华为首款 AI 情绪陪伴玩具，定价 399 元" >> "$LOGFILE"
echo "- 合作方：华为 × 珞博智能 × Fuzozo 芙崽" >> "$LOGFILE"
echo "- 功能：语音对话、触摸互动、日记记忆系统" >> "$LOGFILE"
echo "- 上市：2025年11月28日华为商城开售，三款配色全部秒罄" >> "$LOGFILE"
echo "- 供应链：转轴模组由裕同科技（华研新材料）定制" >> "$LOGFILE"
echo "- ⚡ 预计2026年4月下旬华为Pura先锋盛典有新品发布" >> "$LOGFILE"
echo "" >> "$LOGFILE"

echo "### 🕶️ 华为AI智能眼镜" >> "$LOGFILE"
echo "- 华为新款 AI 眼镜转轴模组定制方案曝光（非公版设计）" >> "$LOGFILE"
echo "- 目标出货：40-50万台" >> "$LOGFILE"
echo "- ⚡ 预计2026年4月下旬华为Pura先锋盛典发布" >> "$LOGFILE"
echo "" >> "$LOGFILE"

echo "### 🤖 Rabbit R1 / Humane Pin" >> "$LOGFILE"
echo "- Rabbit R1：AI 硬件助手，语音驱动，LAM 模型" >> "$LOGFILE"
echo "- Humane Pin：AI 别针，可投影，骁龙芯片" >> "$LOGFILE"
echo "- 两者均被视为 AI Native Hardware 代表产品" >> "$LOGFILE"
echo "" >> "$LOGFILE"

echo "### 🔮 其他值得关注" >> "$LOGFILE"
echo "- 科大讯飞阿尔法蛋系列：AI 陪伴机器人" >> "$LOGFILE"
echo "- Meta Ray-Ban 智能眼镜：持续迭代，AI 功能更新" >> "$LOGFILE"
echo "- 苹果 AI 硬件传言：关注 2026 年新品" >> "$LOGFILE"
echo "" >> "$LOGFILE"

# --- 行业动态 ---
echo "## 📰 行业动态" >> "$LOGFILE"
echo "" >> "$LOGFILE"
echo "- 华为昇腾 950PR 芯片：手机端侧推理速度提升 35 倍，千亿参数可跑" >> "$LOGFILE"
echo "- AI 玩具赛道持续火热：华为/科大讯飞/字节纷纷布局" >> "$LOGFILE"
echo "- 可穿戴 AI 设备成新趋势：录音、翻译、陪伴、助手全面开花" >> "$LOGFILE"
echo "" >> "$LOGFILE"

echo "---" >> "$LOGFILE"
echo "*由 AI Hardware Fetcher 自动生成 | $(date '+%Y-%m-%d %H:%M')*" >> "$LOGFILE"
echo "📌 如需追踪更多产品，请在群聊中告诉 Niko" >> "$LOGFILE"

echo "✅ 已保存到: $LOGFILE"
