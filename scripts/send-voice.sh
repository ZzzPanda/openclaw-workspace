#!/bin/bash
# TTS → OPUS 语音气泡
# 用法: send-voice.sh "文字内容"
TEXT="$1"
OUTPUT="/tmp/openclaw/voice-opus.m4a"
say "$TEXT" -o "$OUTPUT" 2>/dev/null
echo "$OUTPUT"
