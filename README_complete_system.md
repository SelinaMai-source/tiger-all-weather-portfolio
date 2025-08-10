# 🐯 Tiger All Weather Portfolio - 完整交互式投资组合系统

## 🌟 系统概述

这是一个完整的全天候投资组合系统，集成了宏观面、基本面、技术面分析，为用户提供个性化的投资建议和交易信号。

## 🎯 核心功能

### 1. 宏观面分析 (Macro Analysis)
- **经济指标监控**: CPI、PCE、GDP、就业数据、利率等
- **动态资产配置**: 基于宏观环境自动调整大类资产权重
- **风险预警**: 识别经济周期变化和风险信号

### 2. 基本面分析 (Fundamental Analysis)
- **股票筛选**: 价值因子 + 动量因子双重筛选
- **财务健康度**: ROE、毛利率、现金流、负债率等指标
- **行业分散**: 确保投资组合的行业多样性

### 3. 技术面分析 (Technical Analysis)
- **技术指标**: RSI、MACD、布林带、移动平均线等
- **交易信号**: 生成买入/卖出信号和入场时机
- **风险控制**: 止损位和目标价位设定

### 4. 投资组合优化
- **个性化配置**: 根据用户风险偏好和投资期限调整
- **资产配置**: 股票、债券、黄金、大宗商品的动态配比
- **预期收益分析**: 风险调整后收益和最大回撤预测

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 虚拟环境 (推荐)

### 安装步骤

1. **克隆项目**
```bash
git clone <repository_url>
cd tiger_all_weather_portfolio
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements_streamlit.txt
```

4. **启动应用**
```bash
./run_app.sh
# 或
streamlit run interactive_portfolio_app.py
```

## 📱 使用指南

### 1. 设置投资参数
- **可支配资金**: 输入计划投资的金额
- **风险偏好**: 选择保守型、平衡型或激进型
- **投资期限**: 选择短期(1-3年)、中期(3-7年)或长期(7年以上)

### 2. 运行分析
点击"开始分析"按钮，系统将自动运行：
- 宏观环境分析
- 基本面股票筛选
- 技术面信号生成

### 3. 查看结果
系统将显示：
- 投资组合概览和关键指标
- 资产配置分布图表
- 详细配置建议表格
- 宏观环境分析结果
- 技术分析信号摘要
- 个性化投资建议

## 🏗️ 系统架构

```
tiger_all_weather_portfolio/
├── macro_analysis/           # 宏观分析模块
│   ├── macro_data.py        # 宏观数据获取
│   └── allocation_adjust.py # 资产配置调整
├── fundamental_analysis/     # 基本面分析模块
│   └── equities/            # 股票分析
├── technical_analysis/      # 技术面分析模块
│   ├── technical_indicators.py # 技术指标计算
│   ├── technical_signals.py    # 信号生成
│   ├── equities/            # 股票技术策略
│   ├── bonds/               # 债券技术策略
│   ├── commodities/         # 大宗商品技术策略
│   └── golds/               # 黄金技术策略
├── interactive_portfolio_app.py # 主应用界面
├── run_app.sh               # 启动脚本
└── requirements_streamlit.txt # 依赖文件
```

## 📊 输出示例

### 投资组合概览
- 预期年化收益率: 8.5%
- 投资组合波动率: 15.2%
- 夏普比率: 0.43
- 最大回撤: 30.4%

### 资产配置
- 股票类资产: 35.0%
- 长期债券: 40.0%
- 中期债券: 15.0%
- 黄金: 5.0%
- 大宗商品: 5.0%

### 技术分析信号
- 总信号数: 12
- 高置信度信号: 8
- 买入信号: 9
- 卖出信号: 3

## 🔧 自定义配置

### 调整风险参数
在 `interactive_portfolio_app.py` 中修改：
```python
def _adjust_for_risk(self, risk_profile):
    if risk_profile == "保守型":
        return {"equities": -0.15, "bonds_long": 0.15, ...}
```

### 修改技术指标
在 `technical_indicators.py` 中调整指标参数：
```python
def calculate_rsi(data: pd.Series, window: int = 14) -> pd.Series:
    # 修改RSI计算窗口
```

### 添加新的资产类别
在相应的策略文件中添加新的资产类型和筛选逻辑。

## 📈 性能优化

### 数据缓存
- 使用本地缓存减少API调用
- 实现增量数据更新

### 并行处理
- 多线程运行不同资产类别的分析
- 异步处理数据获取

### 内存管理
- 及时释放大型数据对象
- 使用生成器处理大量数据

## 🚨 风险提示

1. **投资风险**: 本系统提供的建议仅供参考，不构成投资建议
2. **数据准确性**: 依赖第三方数据源，可能存在延迟或错误
3. **市场变化**: 市场环境快速变化，建议定期更新分析
4. **专业咨询**: 实际投资前请咨询专业投资顾问

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进系统：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📞 联系方式

- 项目维护者: Tiger Group
- 邮箱: [your-email@example.com]
- 项目地址: [repository-url]

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**免责声明**: 本系统仅供学习和研究使用，不构成投资建议。投资有风险，入市需谨慎。
