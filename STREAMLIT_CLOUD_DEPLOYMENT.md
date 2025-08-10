# 🚀 Streamlit Cloud 部署指南

## 🌟 部署目标
使用 GitHub + Streamlit Cloud 免费部署全天候资产配置系统

## 📋 部署步骤

### 第一步：准备GitHub仓库
1. 在GitHub上创建新仓库
2. 仓库名称：`tiger-all-weather-portfolio`
3. 设置为公开仓库（Public）

### 第二步：上传代码到GitHub
```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit: Tiger All Weather Portfolio"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/tiger-all-weather-portfolio.git

# 推送到GitHub
git push -u origin main
```

### 第三步：Streamlit Cloud部署
1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择你的GitHub仓库
5. 设置部署配置：
   - **Repository**: tiger-all-weather-portfolio
   - **Branch**: main
   - **Main file path**: interactive_portfolio_app.py
6. 点击 "Deploy!"

### 第四步：配置环境变量
在Streamlit Cloud中设置secrets：
1. 进入应用设置
2. 点击 "Secrets"
3. 添加API密钥：
```toml
FRED_API_KEY = "your_fred_api_key"
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_key"
```

### 第五步：等待部署完成
- 部署时间：约2-5分钟
- 部署成功后，您会获得一个类似这样的URL：
  `https://your-app-name.streamlit.app/`

## 🌐 访问地址
部署完成后，任何人都可以通过以下地址访问：
- **Streamlit Cloud URL**: https://your-app-name.streamlit.app/
- **GitHub仓库**: https://github.com/你的用户名/tiger-all-weather-portfolio

## 🔧 维护和更新
```bash
# 本地修改代码后
git add .
git commit -m "Update: 描述你的更新"
git push origin main

# Streamlit Cloud会自动重新部署
```

## ⚠️ 注意事项
1. **API密钥**：在Streamlit Cloud中安全设置
2. **仓库公开**：确保GitHub仓库是公开的
3. **文件路径**：确保main file path正确
4. **依赖版本**：requirements.txt中的版本要兼容

## 🆘 常见问题
- **部署失败**：检查requirements.txt和代码语法
- **API调用失败**：检查secrets配置
- **页面无法访问**：等待部署完成或检查配置

## 🎯 部署成功标志
1. ✅ GitHub仓库代码上传成功
2. ✅ Streamlit Cloud连接成功
3. ✅ 应用部署完成
4. ✅ 页面可以正常访问
5. ✅ 所有功能模块正常工作

## 🚀 下一步
部署完成后，您可以：
1. 分享链接给用户
2. 测试所有功能
3. 根据用户反馈优化
4. 定期更新和维护

祝您部署成功！🎉
