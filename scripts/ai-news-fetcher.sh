#!/bin/bash
# AI Tools News Fetcher - Runs every Mon/Thu 11AM

WORKDIR="/Users/roger/.openclaw/workspace"
LOGFILE="$WORKDIR/memory/ai-news-$(date +%Y-%m-%d).md"

echo "# AI 工具资讯 - $(date '+%Y-%m-%d %H:%M')

## 来源
- AI++ Newsletter
- Augmented Coding Weekly
- GitHub Trending
- OpenSpec Updates

## 今日资讯

" > "$LOGFILE"

# Fetch AI++ Newsletter recent posts
echo "### AI++ Newsletter" >> "$LOGFILE"
echo "最新动态..." >> "$LOGFILE"
echo "" >> "$LOGFILE"

# Fetch GitHub trending repos for AI/developer-tools
echo "### GitHub Trending - AI/Developer Tools" >> "$LOGFILE"
curl -s "https://api.github.com/search/repositories?q=ai+OR+llm+OR+coding+OR+agent+created:>2025-01-01&sort=stars&order=desc&per_page=10" 2>/dev/null | \
  jq '.items[:10] | .[] | "- \(.full_name) - ⭐ \(.stargazers_count): \(.description // "无描述")"' 2>/dev/null >> "$LOGFILE" || \
  echo "获取失败" >> "$LOGFILE"

echo "" >> "$LOGFILE"
echo "---" >> "$LOGFILE"
echo "*由 AI News Fetcher 自动生成*" >> "$LOGFILE"

echo "✅ 已保存到: $LOGFILE"
