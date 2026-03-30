#!/bin/bash
set -e

echo "========================================"
echo "  云上泰和 · OpenClaw 安装脚本"
echo "========================================"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js >= 18"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 版本过低，需要 >= 18，当前版本: $(node -v)"
    exit 1
fi
echo "✅ Node.js 版本检查通过: $(node -v)"

# Check npm or pnpm
if command -v pnpm &> /dev/null; then
    PKG_MGR="pnpm"
elif command -v npm &> /dev/null; then
    PKG_MGR="npm"
else
    echo "❌ npm 或 pnpm 未安装"
    exit 1
fi
echo "✅ 包管理器: $PKG_MGR"

# Install OpenClaw CLI
echo "📦 安装 OpenClaw CLI..."
npm install -g openclaw@latest 2>/dev/null || pnpm add -g openclaw@latest 2>/dev/null || npx openclaw --version

# Create workspace directories
OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspaces/yunshang-taihe"

echo "📁 创建工作区目录..."
mkdir -p "$WORKSPACE_DIR"

# Copy configs
echo "📋 复制配置文件..."
cp -r configs/* "$OPENCLAW_DIR/" 2>/dev/null || true

# Copy skills
echo "🛠️ 复制 Skills..."
mkdir -p "$OPENCLAW_DIR/workspaces/yunshang-taihe/skills"
cp -r skills/* "$OPENCLAW_DIR/workspaces/yunshang-taihe/skills/" 2>/dev/null || true

# Copy scripts
mkdir -p "$OPENCLAW_DIR/scripts"
cp -r scripts/* "$OPENCLAW_DIR/scripts/" 2>/dev/null || true

# Make scripts executable
chmod +x "$OPENCLAW_DIR/scripts/"*.py 2>/dev/null || true

echo ""
echo "========================================"
echo "  安装完成！"
echo "========================================"
echo ""
echo "下一步："
echo "1. 编辑配置文件，替换 YOUR_KEY_HERE"
echo "   nano ~/.openclaw/configs/openclaw.json"
echo ""
echo "2. 启动 Gateway"
echo "   openclaw gateway start"
echo ""
echo "3. 访问管理界面"
echo "   http://localhost:10039"
echo ""
echo "详细文档: docs/QUICKSTART.md"
