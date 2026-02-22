#!/bin/bash
# 本地测试运行脚本

set -e

echo "🎮 游戏素材库 - 测试套件"
echo "=========================="

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 安装依赖
echo -e "${YELLOW}安装依赖...${NC}"
uv pip install pytest pytest-cov playwright httpx -q

# 安装 Playwright 浏览器
echo -e "${YELLOW}安装 Playwright 浏览器...${NC}"
playwright install chromium --with-deps 2>/dev/null || true

# 启动服务器
echo -e "${YELLOW}启动服务器...${NC}"
pkill -f "uvicorn app:app" 2>/dev/null || true
uvicorn app:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 3

# 清理函数
cleanup() {
    echo -e "${YELLOW}清理...${NC}"
    kill $SERVER_PID 2>/dev/null || true
}
trap cleanup EXIT

# 运行测试
echo ""
echo -e "${GREEN}=== 单元测试 ===${NC}"
pytest tests/unit/ -v --cov=. --cov-report=term-missing

echo ""
echo -e "${GREEN}=== 集成测试 ===${NC}"
pytest tests/integration/ -v

echo ""
echo -e "${GREEN}=== E2E 测试 ===${NC}"
pytest tests/e2e/ -v --headed=false

echo ""
echo -e "${GREEN}✅ 所有测试完成!${NC}"
