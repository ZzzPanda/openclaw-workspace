#!/usr/bin/env python3
"""
B站梗指南追更工具
功能：
1. 视频内容摘要
2. 弹幕/评论热词提取
3. 梗指南账号追更
"""

import json
import subprocess
import sys
import re
import urllib.request
import urllib.parse
from datetime import datetime, timedelta


def get_video_info(bvid: str) -> dict:
    """获取视频基本信息"""
    url = f"https://www.bilibili.com/video/{bvid}"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # 提取标题
        title_match = re.search(r'<title>([^<]+)</title>', html)
        title = title_match.group(1) if title_match else "未知标题"
        title = title.replace('_哔哩哔哩_bilibili', '').strip()
        
        # 提取简介
        desc_match = re.search(r'"desc":"([^"]+)"', html)
        description = desc_match.group(1) if desc_match else ""
        description = description.replace('\\n', '\n')
        
        return {"bvid": bvid, "title": title, "description": description}
    except Exception as e:
        return {"error": str(e)}


def search_new_videos(keyword: str = "梗指南", days: int = 7) -> list:
    """搜索最近N天的新视频"""
    results = []
    try:
        query = urllib.parse.quote(keyword)
        url = f"https://search.bilibili.com/article?keyword={query}&search_type=article"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # 提取视频标题和链接
        title_pattern = r'title="([^"]+)"[^>]*href="//www\.bilibili\.com/video/([^"]+)'
        matches = re.findall(title_pattern, html)
        
        for match in matches[:10]:
            results.append({
                "bvid": match[1][:12],  # BV号
                "title": match[0][:60]
            })
    except Exception as e:
        results.append({"error": str(e)})
    
    return results


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python bilibili_meme.py info <BV号>      # 获取视频信息")
        print("  python bilibili_meme.py track             # 追更梗指南")
        print("  python bilibili_meme.py search <关键词>   # 搜索梗")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "info" and len(sys.argv) >= 3:
        bvid = sys.argv[2]
        info = get_video_info(bvid)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        
    elif command == "track":
        videos = search_new_videos()
        print(json.dumps(videos, ensure_ascii=False, indent=2))
        
    elif command == "search" and len(sys.argv) >= 3:
        keyword = sys.argv[2]
        videos = search_new_videos(keyword)
        print(json.dumps(videos, ensure_ascii=False, indent=2))
        
    else:
        print("未知命令")


if __name__ == "__main__":
    main()
