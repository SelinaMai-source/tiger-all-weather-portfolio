# 🚀 Tiger All Weather Portfolio - 腾讯云部署指南

## 🌟 系统概述
这是一个完整的全天候资产配置系统，包含：
- **宏观面分析**：动态调整资产配置比例
- **基本面分析**：筛选优质资产标的  
- **技术面分析**：生成精确交易信号
- **预期收益分析**：风险控制和收益预测

## 🏗️ 腾讯云部署方案

### 推荐配置
- **地域选择**：广州（ap-guangzhou）、上海（ap-shanghai）、北京（ap-beijing）
- **实例规格**：S5.MEDIUM4（2核4G，足够运行完整系统）
- **操作系统**：Ubuntu 20.04 LTS
- **带宽**：5Mbps（足够Web应用使用）
- **存储**：50GB SSD云硬盘

### 成本估算
- **S5.MEDIUM4（2核4G）**：约￥90-180/月
- **带宽费用**：按流量计费，约￥20-50/月
- **总成本**：约￥110-230/月

## 📋 部署步骤

### 第一步：购买腾讯云服务器
1. 登录腾讯云控制台
2. 选择云服务器CVM
3. 选择推荐配置和地域
4. 设置安全组，开放80端口（HTTP）和22端口（SSH）

### 第二步：连接服务器
```bash
ssh root@你的服务器IP
```

### 第三步：上传项目文件
```bash
# 在本地执行
scp -r tiger_all_weather_portfolio root@你的服务器IP:/root/
```

### 第四步：运行部署脚本
```bash
cd /root/tiger_all_weather_portfolio
chmod +x deploy_tencent.sh
./deploy_tencent.sh
```

### 第五步：验证部署
```bash
# 检查服务状态
systemctl status tiger-portfolio
systemctl status nginx

# 检查端口
netstat -tlnp | grep :8501
netstat -tlnp | grep :80

# 测试应用
curl http://localhost:8501
```

## 🌐 访问地址
部署完成后，任何人都可以通过以下地址访问：
- **HTTP访问**：http://你的服务器IP
- **直接访问**：http://你的服务器IP:8501

## 🔧 系统功能验证

### 1. 宏观面分析
- 检查FRED API数据获取
- 验证资产配置动态调整

### 2. 基本面分析
- 测试股票筛选功能
- 验证财务指标计算

### 3. 技术面分析
- 检查技术指标计算
- 验证交易信号生成

### 4. 完整流程测试
- 输入投资金额和期限
- 验证完整分析流程
- 检查结果输出

## 🔧 维护命令
```bash
# 重启应用
systemctl restart tiger-portfolio

# 重启nginx
systemctl restart nginx

# 查看实时日志
journalctl -u tiger-portfolio -f

# 查看应用状态
systemctl status tiger-portfolio

# 检查端口监听
netstat -tlnp | grep :8501
```

## ⚠️ 注意事项
1. **API密钥**：请替换.env文件中的API密钥
2. **安全设置**：定期更新系统，设置强密码
3. **数据备份**：定期备份重要数据和配置
4. **域名备案**：如果使用域名，需要在中国大陆备案

## 🆘 故障排除

### 常见问题
- **应用无法访问**：检查防火墙和nginx配置
- **服务启动失败**：查看systemctl日志
- **性能问题**：检查服务器资源使用情况

### 日志位置
- 应用日志：journalctl -u tiger-portfolio
- Nginx日志：/var/log/nginx/error.log

## 🎯 部署成功标志
1. ✅ 服务状态正常（systemctl status tiger-portfolio）
2. ✅ 端口监听正常（netstat -tlnp | grep :8501）
3. ✅ 网页可以正常访问
4. ✅ 宏观面分析功能正常
5. ✅ 基本面分析功能正常
6. ✅ 技术面分析功能正常
7. ✅ 完整流程测试通过

## 🚀 下一步
部署完成后，您可以：
1. 测试所有功能模块
2. 配置域名（可选）
3. 开始使用全天候资产配置系统

祝您部署成功！🎉
