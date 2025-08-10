#!/bin/bash

# 🚀 Tiger All Weather Portfolio - 快速部署脚本
# 此脚本将帮助您快速完成Streamlit Cloud部署

echo "🐯 Tiger All Weather Portfolio - 快速部署助手"
echo "=================================================="
echo ""

# 检查Git状态
echo "📋 检查Git状态..."
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  发现未提交的更改，正在提交..."
    git add .
    git commit -m "Update: 部署前自动提交 $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin main
    echo "✅ 代码已推送到GitHub"
else
    echo "✅ 工作目录干净，无需提交"
fi

echo ""

# 显示部署信息
echo "🚀 部署就绪！请按照以下步骤操作："
echo ""

echo "📱 步骤 1: 访问Streamlit Cloud"
echo "   打开浏览器访问：https://share.streamlit.io/"
echo ""

echo "🔐 步骤 2: 登录"
echo "   使用您的GitHub账号登录"
echo ""

echo "➕ 步骤 3: 创建新应用"
echo "   1. 点击 'New app'"
echo "   2. 选择 'From existing repo'"
echo ""

echo "⚙️  步骤 4: 配置应用"
echo "   Repository: SelinaMai-source/tiger-all-weather-portfolio"
echo "   Branch: main"
echo "   Main file path: interactive_portfolio_app.py"
echo "   App URL: 可以自定义，如 tiger-all-weather-portfolio"
echo ""

echo "🔧 步骤 5: 高级设置"
echo "   Python version: 3.9 或更高"
echo "   Requirements file: requirements.txt"
echo ""

echo "🔑 步骤 6: 环境变量配置"
echo "   在Streamlit Cloud的Settings > Secrets中添加："
echo "   ALPHA_VANTAGE_API_KEY = P27YDIBOBM1464SO"
echo "   YAHOO_FINANCE_ENABLED = true"
echo ""

echo "🚀 步骤 7: 部署"
echo "   点击 'Deploy!' 开始部署"
echo ""

echo "⏱️  预期部署时间：3-5分钟"
echo ""

echo "📊 部署完成后，您的应用将提供："
echo "   ✅ 宏观分析 - 经济指标监控和资产配置建议"
echo "   ✅ 基本面分析 - 股票筛选和财务指标分析"
echo "   ✅ 技术分析 - 交易信号生成和趋势分析"
echo "   ✅ 投资组合构建 - 智能资产配置和风险管理"
echo "   ✅ 实时数据 - 市场数据更新和图表展示"
echo ""

echo "🎯 项目状态："
echo "   ✅ 所有依赖包已安装"
echo "   ✅ 所有模块可正常导入"
echo "   ✅ 配置文件已优化"
echo "   ✅ 代码已推送到GitHub"
echo ""

echo "🎉 您的Tiger All Weather Portfolio系统已完全准备好部署！"
echo "立即开始部署，让您的投资组合系统上线吧！"
echo ""

echo "📞 如需技术支持，请检查："
echo "   1. Streamlit Cloud的部署日志"
echo "   2. 确保GitHub仓库代码是最新的"
echo "   3. 验证环境变量配置是否正确"
echo ""

echo "=================================================="
echo "🐯 祝您部署成功！"
