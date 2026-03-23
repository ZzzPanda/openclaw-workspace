#!/bin/bash
# TTS → OPUS 语音气泡 发送脚本
# 用法: tts-opus.sh "要说的内容"

TEXT="$1"
TMP_DIR="/tmp/openclaw/tts-opus"
OUTPUT="$TMP_DIR/voice-$(date +%s).opus"
CHAT_ID="${2:-oc_348222757eed69203faf73d7111371eb}"

mkdir -p "$TMP_DIR"

# 1. 生成 MP3 (用 say 命令，Mac 原生)
TMP_MP3="$TMP_DIR/temp-$$.mp3"
say -o "$TMP_MP3" "$TEXT" 2>/dev/null

# 2. 转 OPUS
ffmpeg -i "$TMP_MP3" -c:a libopus -b:a 128k "$OUTPUT" -y 2>/dev/null
rm -f "$TMP_MP3"

# 3. 发送到飞书
openclaw message send \
  --channel feishu \
  --target "chat:$CHAT_ID" \
  --voice "$OUTPUT"

echo "Sent: $TEXT"
rm -f "$OUTPUT"
