#!/bin/bash
# 🐯 Tiger All Weather Portfolio - 腾讯云部署脚本

echo "🚀 开始部署全天候资产配置系统..."

# 更新系统
apt update && apt upgrade -y

# 安装软件
apt install -y python3 python3-pip python3-venv nginx git curl

# 创建项目目录
mkdir -p /root/tiger_all_weather_portfolio
cd /root/tiger_all_weather_portfolio

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements_streamlit.txt

# 配置服务
cp tiger-portfolio.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable tiger-portfolio

# 配置nginx
cp nginx-tiger-portfolio.conf /etc/nginx/sites-available/tiger-portfolio
ln -sf /etc/nginx/sites-available/tiger-portfolio /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 启动服务
systemctl start tiger-portfolio
systemctl restart nginx

# 配置防火墙
ufw allow 80/tcp
ufw allow 22/tcp
ufw --force enable

echo "✅ 部署完成！"
echo "🌐 访问地址: http://$(curl -s ifconfig.me)"
