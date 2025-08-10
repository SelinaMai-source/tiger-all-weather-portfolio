# 🐯 Tiger All Weather Portfolio - 智能全天候资产配置系统

## 🌟 项目简介
这是一个基于人工智能的全天候资产配置系统，集成了宏观分析、基本面分析和技术分析，为用户提供智能化的投资组合建议。系统能够根据不同的市场环境自动调整资产配置策略，实现"全天候"投资目标。

## 🚀 快速部署

### 方式1：Streamlit Cloud（推荐）
1. Fork 或 Clone 此仓库
2. 在 [Streamlit Cloud](https://share.streamlit.io/) 部署
3. 配置环境变量（API密钥）
4. 享受免费托管！

### 方式2：本地运行
```bash
# 克隆仓库
git clone https://github.com/你的用户名/tiger-all-weather-portfolio.git
cd tiger-all-weather_portfolio

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run interactive_portfolio_app.py
```

## 📱 主要功能

### 🎯 宏观环境分析
- 经济指标监控
- 市场情绪分析
- 政策影响评估
- 资产配置建议

### 📊 基本面筛选
- 股票价值评估
- 债券信用分析
- 商品供需分析
- 黄金投资机会

### 📈 技术面信号
- 趋势分析
- 动量指标
- 支撑阻力位
- 交易时机判断

### 💰 智能资产配置
- 动态权重调整
- 风险控制
- 收益优化
- 组合再平衡

## 🏗️ 系统架构

```
tiger_all_weather_portfolio/
├── macro_analysis/          # 宏观分析模块
├── fundamental_analysis/     # 基本面分析模块
├── technical_analysis/       # 技术分析模块
├── utils/                    # 工具函数
├── interactive_portfolio_app.py  # 主应用
└── requirements.txt          # 依赖包
```

## 🔧 技术栈
- **前端**: Streamlit
- **数据处理**: Pandas, NumPy
- **可视化**: Plotly, Matplotlib
- **数据源**: Yahoo Finance, FRED API
- **机器学习**: Scikit-learn
- **技术指标**: TA-Lib

## 📊 数据来源
- **股票数据**: Yahoo Finance
- **经济数据**: FRED (Federal Reserve Economic Data)
- **商品数据**: Yahoo Finance
- **债券数据**: Yahoo Finance
- **汇率数据**: Yahoo Finance

## ⚙️ 配置要求
- Python 3.8+
- 内存: 2GB+
- 存储: 1GB+
- 网络: 稳定的互联网连接

## 🔑 API密钥配置
在 `.streamlit/secrets.toml` 中配置：
```toml
FRED_API_KEY = "your_fred_api_key"
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_key"
```

## 📈 使用示例
1. 选择投资金额和期限
2. 设置风险偏好
3. 系统自动分析市场环境
4. 生成个性化投资组合
5. 查看详细分析和建议

## 🤝 贡献指南
欢迎提交Issue和Pull Request！
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证
MIT License

## 📞 联系方式
- 项目地址: [GitHub](https://github.com/你的用户名/tiger-all-weather-portfolio)
- 在线演示: [Streamlit App](https://your-app-name.streamlit.app/)

## 🙏 致谢
感谢所有开源项目的贡献者！

---
⭐ 如果这个项目对您有帮助，请给我们一个Star！
