# simple_app.py
"""
🐯 Tiger All Weather Portfolio - 简化版应用
确保基本功能能够正常运行
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
import os
import sys
warnings.filterwarnings('ignore')

# 🔑 配置API密钥
os.environ["FRED_API_KEY"] = "550d6a640ad3000f9170f28e7157af72"
os.environ["ALPHA_VANTAGE_API_KEY"] = "P27YDIBOBM1464SO"
os.environ["YAHOO_FINANCE_ENABLED"] = "true"

# 设置页面配置
st.set_page_config(
    page_title="🐯 Tiger All Weather Portfolio",
    page_icon="🐯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_mock_macro_data():
    """生成模拟宏观数据"""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    
    indicators = {
        "CPIAUCSL": "通胀 - CPI：用于判断通胀压力，通胀上升利好黄金、商品，利空债券",
        "GS10": "10年期美债收益率：长期利率代表",
        "UNRATE": "失业率：经济衰退信号，失业率高 → 债券上涨、股票下跌",
        "VIXCLS": "VIX恐慌指数：高VIX代表市场避险情绪浓厚，利空股票、利好债券"
    }
    
    macro_data = {}
    for fred_code, description in indicators.items():
        # 生成模拟时间序列数据
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        if "CPI" in fred_code:
            base_value = 300
            trend = np.linspace(0, 5, len(date_range))
            noise = np.random.normal(0, 0.5, len(date_range))
            values = base_value + trend + noise
        elif "GS" in fred_code:
            base_value = 4.0
            trend = np.sin(np.linspace(0, 4*np.pi, len(date_range))) * 0.5
            noise = np.random.normal(0, 0.1, len(date_range))
            values = base_value + trend + noise
        elif "UNRATE" in fred_code:
            base_value = 4.5
            trend = np.linspace(0, -1, len(date_range))
            noise = np.random.normal(0, 0.2, len(date_range))
            values = base_value + trend + noise
        elif "VIX" in fred_code:
            base_value = 20
            trend = np.random.exponential(5, len(date_range))
            noise = np.random.normal(0, 2, len(date_range))
            values = base_value + trend + noise
        else:
            base_value = 100
            trend = np.linspace(0, 10, len(date_range))
            noise = np.random.normal(0, 5, len(date_range))
            values = base_value + trend + noise
        
        df = pd.DataFrame(values, index=date_range, columns=["value"])
        df.index.name = "date"
        
        macro_data[fred_code] = {
            "description": description,
            "data": df
        }
    
    return macro_data

def display_macro_analysis():
    """显示宏观分析"""
    st.header("📊 宏观环境分析")
    
    with st.spinner("正在分析宏观环境..."):
        macro_data = generate_mock_macro_data()
        
        # 显示宏观指标
        for code, content in macro_data.items():
            with st.expander(f"📈 {code} - {content['description']}"):
                st.write(content['description'])
                
                # 创建图表
                fig = px.line(content['data'], y='value', title=f"{code} 趋势")
                st.plotly_chart(fig, use_container_width=True)
                
                # 显示最新数据
                st.write("最新数据：")
                st.dataframe(content['data'].tail(5))

def generate_portfolio_recommendation(investment_amount, investment_horizon, risk_profile):
    """生成投资组合建议"""
    st.header("💰 智能资产配置建议")
    
    # 基础配置
    base_allocation = {
        "股票": 0.40,
        "债券": 0.30,
        "黄金": 0.15,
        "商品": 0.10,
        "现金": 0.05
    }
    
    # 根据投资期限调整
    if investment_horizon == "短期 (1-3年)":
        base_allocation["现金"] += 0.10
        base_allocation["股票"] -= 0.10
    elif investment_horizon == "长期 (10年以上)":
        base_allocation["股票"] += 0.10
        base_allocation["债券"] -= 0.10
    
    # 根据风险偏好调整
    if risk_profile == "保守":
        base_allocation["债券"] += 0.15
        base_allocation["股票"] -= 0.15
    elif risk_profile == "激进":
        base_allocation["股票"] += 0.15
        base_allocation["债券"] -= 0.15
    
    # 显示配置
    st.subheader("📊 建议资产配置")
    
    # 创建饼图
    fig = go.Figure(data=[go.Pie(labels=list(base_allocation.keys()), 
                               values=list(base_allocation.values()),
                               hole=0.3)])
    fig.update_layout(title="资产配置比例")
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示详细配置
    st.subheader("📋 详细配置")
    for asset, allocation in base_allocation.items():
        amount = investment_amount * allocation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.metric(asset, f"${amount:,.2f}", f"{allocation*100:.1f}%")
    
    # 投资建议
    st.subheader("💡 投资建议")
    if risk_profile == "保守":
        st.info("保守型配置：注重资本保值和稳定收益，适合风险承受能力较低的投资者。")
    elif risk_profile == "平衡":
        st.success("平衡型配置：在风险和收益之间取得平衡，适合大多数投资者。")
    else:
        st.warning("激进型配置：追求高收益，但风险也较高，适合风险承受能力强的投资者。")

def main():
    st.title("🐯 Tiger All Weather Portfolio")
    st.markdown("### 智能全天候资产配置系统")
    
    # 侧边栏配置
    st.sidebar.header("⚙️ 投资配置")
    
    investment_amount = st.sidebar.number_input(
        "投资金额 ($)", 
        min_value=1000, 
        max_value=1000000, 
        value=100000,
        step=1000
    )
    
    investment_horizon = st.sidebar.selectbox(
        "投资期限",
        ["短期 (1-3年)", "中期 (3-10年)", "长期 (10年以上)"]
    )
    
    risk_profile = st.sidebar.selectbox(
        "风险偏好",
        ["保守", "平衡", "激进"]
    )
    
    # 主界面
    tab1, tab2, tab3 = st.tabs(["📊 宏观分析", "💰 资产配置", "📈 技术分析"])
    
    with tab1:
        display_macro_analysis()
    
    with tab2:
        if st.button("🚀 生成投资组合建议"):
            generate_portfolio_recommendation(investment_amount, investment_horizon, risk_profile)
    
    with tab3:
        st.header("📈 技术分析")
        st.info("技术分析模块正在开发中，敬请期待！")
        
        # 显示一些技术指标示例
        st.subheader("🔍 技术指标示例")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("RSI", "65.2", "中性")
            st.metric("MACD", "0.15", "↑ 看涨")
        
        with col2:
            st.metric("布林带", "中轨", "正常")
            st.metric("成交量", "1.2M", "↑ 放大")

if __name__ == "__main__":
    main()
