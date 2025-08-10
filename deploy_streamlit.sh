#!/bin/bash

# 🚀 Tiger All Weather Portfolio - Streamlit Cloud 部署脚本

echo "🐯 开始部署 Tiger All Weather Portfolio 到 Streamlit Cloud..."

# 检查Git状态
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 工作目录干净，准备部署..."
else
    echo "⚠️  检测到未提交的更改，正在提交..."
    git add .
    git commit -m "Update: 准备部署到Streamlit Cloud"
fi

# 检查远程仓库
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ 未配置远程仓库，请先配置GitHub仓库："
    echo "git remote add origin https://github.com/你的用户名/tiger-all-weather-portfolio.git"
    exit 1
fi

# 推送到GitHub
echo "📤 推送到GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码推送成功！"
    echo ""
    echo "🚀 接下来请按以下步骤完成部署："
    echo ""
    echo "1. 访问 https://share.streamlit.io/"
    echo "2. 使用GitHub账号登录"
    echo "3. 点击 'New app'"
    echo "4. 选择仓库: $(git remote get-url origin | sed 's/.*github\.com\///' | sed 's/\.git//')"
    echo "5. 设置 Main file path: interactive_portfolio_app.py"
    echo "6. 点击 'Deploy!'"
    echo ""
    echo "⏱️  部署完成后，您将获得一个类似这样的URL："
    echo "https://your-app-name.streamlit.app/"
    echo ""
    echo "🔧 记得在Streamlit Cloud中配置环境变量（API密钥）"
    echo ""
    echo "🎉 部署完成后，您的全天候资产配置系统就可以在线访问了！"
else
    echo "❌ 代码推送失败，请检查GitHub仓库配置"
    exit 1
fi
