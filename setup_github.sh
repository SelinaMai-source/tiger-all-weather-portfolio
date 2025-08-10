#!/bin/bash

# 🚀 Tiger All Weather Portfolio - GitHub 仓库设置脚本

echo "🐯 设置 GitHub 仓库连接..."

# 检查是否已配置远程仓库
if git remote get-url origin > /dev/null 2>&1; then
    echo "✅ 已配置远程仓库："
    git remote -v
    echo ""
    echo "如果这是正确的仓库，请直接执行："
    echo "git push -u origin main"
    exit 0
fi

echo "❌ 未配置远程仓库"
echo ""
echo "请按以下步骤操作："
echo ""
echo "1. 访问 https://github.com"
echo "2. 创建新仓库：tiger-all-weather-portfolio"
echo "3. 设置为 Public"
echo "4. 不要初始化任何文件"
echo "5. 复制仓库URL"
echo ""
echo "然后执行以下命令（替换YOUR_USERNAME为您的GitHub用户名）："
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/tiger-all-weather-portfolio.git"
echo "git push -u origin main"
echo ""
echo "推送完成后，Streamlit Cloud 就能看到所有文件了！"
