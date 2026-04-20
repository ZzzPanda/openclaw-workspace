#!/usr/bin/env python3
"""
C端AI硬件资讯抓取 v2
- Reddit: 抓取 AI硬件相关subreddit的热门帖
- YouTube: 搜索最新AI硬件视频
- Brave Search: 实时新闻搜索
输出: markdown 格式日志
"""

import urllib.request
import urllib.parse
import json
import sys
from datetime import datetime, timedelta

WORKDIR = "/Users/roger/.openclaw/workspace"
LOGFILE = f"{WORKDIR}/memory/ai-hardware-{datetime.now().strftime('%Y-%m-%d')}.md"

BRAVE_API_KEY = None  # 从环境变量读取

def get_brave_search_results(query, count=5):
    """用 Brave Search API 搜新闻"""
    try:
        import os
        api_key = os.environ.get("BRAVE_SEARCH_API_KEY") or os.environ.get("BRAVE_API_KEY")
        if not api_key:
            return None
        url = f"https://api.search.brave.com/res/v1/news/search?q={urllib.parse.quote(query)}&count={count}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "X-Subscription-Token": api_key
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            results = []
            for item in data.get("results", [])[:count]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "description": item.get("description", "")[:150]
                })
            return results
    except Exception as e:
        return None

def get_reddit_ai_hardware():
    """从 Reddit 抓 AI硬件相关热门"""
    subreddits = [
        "gadgets",
        "ArtificialHuman", 
        "smartglasses",
        "rabor",
        "AI_Technology",
    ]
    results = []
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=5"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                posts = data.get("data", {}).get("children", [])
                for post in posts[:3]:
                    p = post.get("data", {})
                    title = p.get("title", "")
                    # 过滤AI硬件相关
                    keywords = ["AI", "hardware", "robot", "glass", "wearable", "Rabbit", "Humane", "Plaud", "Pin", "Pin", "眼镜", "硬件", "机器人"]
                    if any(k.lower() in title.lower() for k in keywords):
                        results.append({
                            "title": title,
                            "url": f"https://reddit.com{p.get('permalink', '')}",
                            "score": p.get("score", 0),
                            "sub": sub,
                            "comments": p.get("num_comments", 0)
                        })
        except Exception:
            pass
    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:8]

def get_youtube_ai_hardware():
    """从 YouTube 搜 AI硬件最新视频"""
    try:
        import os
        api_key = os.environ.get("YOUTUBE_API_KEY")
        if not api_key:
            return None
        query = "AI hardware gadget 2026"
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={urllib.parse.quote(query)}&type=video&order=date&maxResults=5&publishedAfter={(datetime.now()-timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')}&key={api_key}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            results = []
            for item in data.get("items", []):
                vid = item.get("id", {}).get("videoId", "")
                snippet = item.get("snippet", {})
                results.append({
                    "title": snippet.get("title", ""),
                    "channel": snippet.get("channelTitle", ""),
                    "url": f"https://youtube.com/watch?v={vid}",
                    "published": snippet.get("publishedAt", "")[:10]
                })
            return results
    except Exception:
        return None

def main():
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    md = f"""# C端AI原生硬件资讯 - {today}

> 实时抓取 Reddit / YouTube / 新闻

---

## 🔥 Reddit 热门讨论

"""

    reddit_results = get_reddit_ai_hardware()
    if reddit_results:
        for r in reddit_results:
            md += f"- [{r['title']}]({r['url']}) `(r/{r['sub']} | ▲{r['score']} 💬{r['comments']})`\n"
    else:
        md += "- 暂无数据（Reddit 公开接口可能受限）\n"

    md += "\n## 📺 YouTube 最新视频\n\n"
    
    yt_results = get_youtube_ai_hardware()
    if yt_results:
        for y in yt_results:
            md += f"- [{y['title']}]({y['url']}) (`{y['channel']}` | {y['published']})\n"
    else:
        md += "- 无 YouTube API Key 或搜索失败\n"
        md += "- 建议: 访问 [YouTube AI Hardware 搜索](https://www.youtube.com/results?search_query=AI+hardware+gadget+2026)\n"

    md += "\n## 📰 实时新闻搜索\n\n"
    
    # Brave News Search
    brave_news = get_brave_search_results("AI hardware gadget wearable 2026", 5)
    if brave_news:
        for n in brave_news:
            md += f"- [{n['title']}]({n['url']})\n  > {n['description']}...\n"
    else:
        md += "- 无 Brave Search API Key 或搜索失败\n"
        md += "- 建议配置 BRAVE_SEARCH_API_KEY 环境变量\n"

    md += f"""
---

*由 AI Hardware Fetcher v2 自动生成 | {today}*
"""

    # 保存文件
    with open(LOGFILE, "w", encoding="utf-8") as f:
        f.write(md)
    
    # 输出到 stdout（供 cron 捕获）
    print(md)
    print(f"\n✅ 已保存到: {LOGFILE}")

if __name__ == "__main__":
    main()
