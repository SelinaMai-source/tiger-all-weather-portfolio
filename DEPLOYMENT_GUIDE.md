# 🚀 全天候资产配置系统部署指南

## 🌟 项目概述
这是一个基于Streamlit的全天候资产配置系统，集成了宏观分析、基本面分析和技术分析，为用户提供智能化的投资组合建议。

## 📋 部署方式选择

### 方式1：Streamlit Cloud（推荐）
- ✅ 完全免费
- ✅ 自动部署
- ✅ 全球CDN加速
- ✅ 无需服务器维护

### 方式2：腾讯云服务器
- ✅ 完全控制
- ✅ 自定义域名
- ✅ 高性能
- ❌ 需要付费和维护

## 🚀 Streamlit Cloud 部署步骤

### 第一步：创建GitHub仓库
1. 访问 [GitHub](https://github.com)
2. 点击 "New repository"
3. 仓库名称：`tiger-all-weather-portfolio`
4. 描述：`🐯 Tiger All Weather Portfolio - 智能全天候资产配置系统`
5. 设置为 **Public**（必须）
6. 不要初始化README、.gitignore或license
7. 点击 "Create repository"

### 第二步：上传代码到GitHub
```bash
# 在本地项目目录执行
git remote add origin https://github.com/你的用户名/tiger-all-weather-portfolio.git
git push -u origin main
```

### 第三步：Streamlit Cloud部署
1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用GitHub账号登录
3. 点击 "New app"
4. 配置部署：
   - **Repository**: `你的用户名/tiger-all-weather-portfolio`
   - **Branch**: `main`
   - **Main file path**: `interactive_portfolio_app.py`
   - **App URL**: 自定义（可选）
5. 点击 "Deploy!"

### 第四步：配置环境变量
在Streamlit Cloud中设置secrets：
1. 进入应用设置
2. 点击 "Secrets"
3. 添加以下配置：
```toml
FRED_API_KEY = "your_fred_api_key"
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_key"
YAHOO_FINANCE_ENABLED = "true"
```

## 🌐 访问地址
部署成功后，您将获得：
- **Streamlit Cloud URL**: `https://your-app-name.streamlit.app/`
- **GitHub仓库**: `https://github.com/你的用户名/tiger-all-weather-portfolio`

## 🔧 本地测试
在部署前，建议先在本地测试：
```bash
# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run interactive_portfolio_app.py
```

## 📱 功能特性
- 🎯 宏观环境分析
- 📊 基本面筛选
- 📈 技术面信号
- 💰 智能资产配置
- 📊 可视化图表
- 🔄 实时数据更新

## ⚠️ 注意事项
1. **API密钥**: 确保在Streamlit Cloud中正确设置
2. **仓库公开**: GitHub仓库必须是公开的
3. **依赖兼容**: requirements.txt中的版本要兼容
4. **文件路径**: 确保main file path正确

## 🆘 常见问题解决
- **部署失败**: 检查requirements.txt和代码语法
- **API调用失败**: 检查secrets配置
- **页面无法访问**: 等待部署完成或检查配置
- **模块导入错误**: 确保所有依赖都已安装

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

## 📞 技术支持
如果遇到问题，请检查：
1. GitHub仓库设置
2. Streamlit Cloud配置
3. 环境变量设置
4. 代码语法和依赖

祝您部署成功！🎉
