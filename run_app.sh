#!/bin/bash

# 🐯 Tiger All Weather Portfolio - 启动脚本

echo "🚀 启动 Tiger All Weather Portfolio 交互式应用..."

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "✅ 激活虚拟环境..."
    source venv/bin/activate
else
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
pip install -r requirements_streamlit.txt

# 启动应用
echo "🌐 启动 Streamlit 应用..."
echo "📱 应用将在浏览器中打开: http://localhost:8501"
echo "🔄 按 Ctrl+C 停止应用"

streamlit run interactive_portfolio_app.py --server.port 8501 --server.address 0.0.0.0
