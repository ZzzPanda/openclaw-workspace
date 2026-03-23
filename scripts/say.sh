#!/bin/bash
# 群里艾特我时，默认发语音气泡
# 用法: say.sh "文字内容" [chat_id]
TEXT="$1"
CHAT_ID="${2:-oc_88ef5b4274d312abf28fefd254ef3fec}"  # 日报群默认
OUTPUT="/tmp/openclaw/voice-$$.m4a"
say "$TEXT" -o "$OUTPUT" 2>/dev/null
echo "$OUTPUT"
