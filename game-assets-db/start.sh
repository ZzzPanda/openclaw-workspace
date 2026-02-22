#!/bin/bash
# 启动素材库 Web UI

cd "$(dirname "$0")"

echo "🎮 启动游戏素材库..."
uv run --with fastapi --with uvicorn --with jinja2 --with python-multipart python app.py
