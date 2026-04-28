#!/bin/bash
# 直接调用 Brave Search API，绕过 OpenClaw 工具层
# 用法: ./brave_search.sh "搜索query"

API_KEY="BSA9UKYQCK550pNploYJcHnhL7aaP7l"
QUERY="$1"

if [ -z "$QUERY" ]; then
  echo "Usage: $0 <search-query>"
  exit 1
fi

curl -s -G "https://api.search.brave.com/res/v1/web/search" \
  --data-urlencode "q=${QUERY}" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${API_KEY}" \
  2>/dev/null | python3 -c "
import json, sys, re

data = json.load(sys.stdin)

def strip_html(t):
    return re.sub(r'<[^>]+>', '', t)

results = data.get('web', {}).get('results', [])
for r in results[:10]:
    title = strip_html(r.get('title', ''))
    desc = strip_html(r.get('description', ''))
    url = r.get('url', '')
    print(f'### {title}')
    print(f'{desc}')
    print(f'🔗 {url}')
    print()
" 2>/dev/null