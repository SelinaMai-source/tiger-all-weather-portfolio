# interactive_portfolio_app.py
"""
🐯 Tiger All Weather Portfolio - 完整交互式投资组合系统

集成宏观面、基本面、技术面分析，为用户提供：
1. 基于宏观环境的动态资产配置
2. 基本面筛选的优质资产标的
3. 技术面生成的交易信号
4. 预期收益分析和风险控制
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import sys
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置环境变量
os.environ["ALPHA_VANTAGE_API_KEY"] = "P27YDIBOBM1464SO"
os.environ["YAHOO_FINANCE_ENABLED"] = "true"

# 添加项目路径 - 兼容Streamlit Cloud
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir

# 确保所有必要的路径都在sys.path中
paths_to_add = [
    project_root,
    os.path.join(project_root, 'macro_analysis'),
    os.path.join(project_root, 'fundamental_analysis'),
    os.path.join(project_root, 'technical_analysis'),
    os.path.join(project_root, 'utils'),
    os.path.join(project_root, 'fundamental_analysis', 'equities'),
    os.path.join(project_root, 'technical_analysis', 'equities'),
    os.path.join(project_root, 'technical_analysis', 'bonds'),
    os.path.join(project_root, 'technical_analysis', 'commodities'),
    os.path.join(project_root, 'technical_analysis', 'golds')
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

# 调试信息
st.write(f"🔍 当前工作目录: {os.getcwd()}")
st.write(f"📁 项目根目录: {project_root}")
st.write(f"📂 已添加的路径数量: {len([p for p in paths_to_add if p in sys.path])}")

# 导入各个分析模块
try:
    st.write("🚀 开始导入模块...")
    
    # 导入宏观分析模块
    try:
        from macro_analysis.macro_data import fetch_macro_data
        st.success("✅ 宏观分析模块导入成功")
    except ImportError as e:
        st.warning(f"⚠️ 宏观分析模块导入失败: {e}")
        st.info("💡 宏观分析功能将不可用，但其他功能仍可正常使用")
        fetch_macro_data = None
    
    # 导入资产配置调整模块
    try:
        from macro_analysis.allocation_adjust import adjust_allocation
        st.success("✅ 资产配置调整模块导入成功")
    except ImportError as e:
        st.warning(f"⚠️ 资产配置调整模块导入失败: {e}")
        st.info("💡 资产配置调整功能将不可用")
        adjust_allocation = None
        
    # 导入基本面分析模块
    try:
        from fundamental_analysis.fundamental_manager import FundamentalAnalysisManager
        st.success("✅ 基本面分析模块导入成功")
    except ImportError as e:
        st.warning(f"⚠️ 基本面分析模块导入失败: {e}")
        st.info("💡 基本面分析功能将不可用，但其他功能仍可正常使用")
        FundamentalAnalysisManager = None
        
    # 导入技术分析模块
    try:
        from technical_analysis.technical_signals import TechnicalAnalysisManager
        st.success("✅ 技术分析模块导入成功")
    except ImportError as e:
        st.warning(f"⚠️ 技术分析模块导入失败: {e}")
        st.info("💡 技术分析功能将不可用，但其他功能仍可正常使用")
        TechnicalAnalysisManager = None
        
    st.success("🎯 模块导入完成")
        
except Exception as e:
    st.error(f"❌ 模块导入失败：{e}")
    st.stop()

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
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .analysis-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    .signal-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .signal-card.buy {
        border-left-color: #28a745;
    }
    .signal-card.sell {
        border-left-color: #dc3545;
    }
    .signal-card.hold {
        border-left-color: #ffc107;
    }
</style>
""", unsafe_allow_html=True)

class CompletePortfolioSystem:
    """完整的投资组合系统"""
    
    def __init__(self):
        self.macro_data = None
        self.asset_allocation = None
        self.equity_candidates = None
        self.technical_signals = None
        self.portfolio_recommendation = None
        self.technical_manager = TechnicalAnalysisManager()
        
    def run_macro_analysis(self):
        """运行宏观分析模块"""
        with st.spinner("🔍 正在分析宏观环境..."):
            try:
                self.macro_data = fetch_macro_data()
                if self.macro_data:
                    self.asset_allocation = adjust_allocation(self.macro_data)
                    st.success(f"✅ 宏观分析完成，获取 {len(self.macro_data)} 个指标")
                    return True
                else:
                    st.error("❌ 宏观数据获取失败")
                    return False
            except Exception as e:
                st.error(f"❌ 宏观分析失败：{e}")
                return False
    
    def run_fundamental_analysis(self):
        """运行基本面分析模块"""
        with st.spinner("📊 正在筛选优质资产..."):
            try:
                # 检查函数是否可用
                if FundamentalAnalysisManager is None:
                    st.error("❌ 基本面分析模块未正确导入")
                    return False
                
                # 创建基本面分析管理器实例
                fundamental_manager = FundamentalAnalysisManager()
                success = fundamental_manager.run_equity_analysis()
                
                if success:
                    # 获取选中的股票
                    selected_equities = fundamental_manager.get_selected_tickers('equities')
                    if selected_equities:
                        # 创建DataFrame
                        self.equity_candidates = pd.DataFrame({
                            'ticker': selected_equities,
                            'selected_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        st.success(f"✅ 基本面分析完成，筛选出 {len(self.equity_candidates)} 只股票")
                        return True
                    else:
                        st.warning("⚠️ 基本面分析未返回股票结果")
                        return False
                else:
                    st.error("❌ 基本面分析执行失败")
                    return False
            except Exception as e:
                st.error(f"❌ 基本面分析失败：{e}")
                return False
    
    def run_technical_analysis(self):
        """运行技术面分析模块"""
        with st.spinner("📈 正在生成技术信号..."):
            try:
                # 检查技术分析管理器是否可用
                if self.technical_manager is None:
                    st.error("❌ 技术分析模块未正确导入")
                    return False
                
                results = self.technical_manager.run_all_analysis()
                success_count = sum(results.values())
                if success_count > 0:
                    st.success(f"✅ 技术分析完成，{success_count}/4 个资产类别成功")
                    return True
                else:
                    st.warning("⚠️ 技术分析未生成有效信号")
                    return False
            except Exception as e:
                st.error(f"❌ 技术分析失败：{e}")
                return False
    
    def generate_portfolio_recommendation(self, investment_amount, investment_horizon, risk_profile):
        """生成投资组合建议"""
        if not self.asset_allocation or not self.equity_candidates:
            st.error("❌ 缺少必要数据，无法生成投资组合建议")
            return None
        
        # 根据投资期限调整配置
        horizon_adj = self._adjust_for_horizon(investment_horizon)
        
        # 根据风险偏好调整配置
        risk_adj = self._adjust_for_risk(risk_profile)
        
        # 应用调整
        final_allocation = self._apply_adjustments(horizon_adj, risk_adj)
        
        # 创建详细投资组合
        portfolio = self._create_detailed_portfolio(final_allocation, investment_amount)
        
        return portfolio
    
    def _adjust_for_horizon(self, horizon):
        """根据投资期限调整配置"""
        if horizon == "短期 (1-3年)":
            return {"equities": -5, "bonds_mid": 5, "bonds_long": 0, "gold": 0, "commodities": 0}
        elif horizon == "中期 (3-7年)":
            return {"equities": 0, "bonds_mid": 0, "bonds_long": 0, "gold": 0, "commodities": 0}
        elif horizon == "长期 (7年以上)":
            return {"equities": 5, "bonds_mid": -2, "bonds_long": -3, "gold": 0, "commodities": 0}
        return {"equities": 0, "bonds_mid": 0, "bonds_long": 0, "gold": 0, "commodities": 0}
    
    def _adjust_for_risk(self, risk_profile):
        """根据风险偏好调整配置"""
        if risk_profile == "保守":
            return {"equities": -10, "bonds_mid": 5, "bonds_long": 5, "gold": 0, "commodities": 0}
        elif risk_profile == "平衡":
            return {"equities": 0, "bonds_mid": 0, "bonds_long": 0, "gold": 0, "commodities": 0}
        elif risk_profile == "积极":
            return {"equities": 10, "bonds_mid": -3, "bonds_long": -5, "gold": -2, "commodities": 0}
        return {"equities": 0, "bonds_mid": 0, "bonds_long": 0, "gold": 0, "commodities": 0}
    
    def _apply_adjustments(self, horizon_adj, risk_adj):
        """应用调整到基准配置"""
        adjusted = self.asset_allocation.copy()
        
        for asset in adjusted:
            adjusted[asset] += horizon_adj.get(asset, 0) + risk_adj.get(asset, 0)
            adjusted[asset] = max(0, min(100, adjusted[asset]))  # 确保在0-100%范围内
        
        # 重新标准化到100%
        total = sum(adjusted.values())
        if total > 0:
            for asset in adjusted:
                adjusted[asset] = round(adjusted[asset] / total * 100, 1)
        
        return adjusted
    
    def _create_detailed_portfolio(self, allocation, investment_amount):
        """创建详细的投资组合"""
        portfolio = {
            'allocation': allocation,
            'total_amount': investment_amount,
            'assets': {}
        }
        
        # 股票配置
        equity_amount = investment_amount * allocation['equities'] / 100
        portfolio['assets']['equities'] = self._select_equity_stocks(equity_amount)
        
        # 债券配置
        bond_amount = investment_amount * (allocation['bonds_mid'] + allocation['bonds_long']) / 100
        portfolio['assets']['bonds'] = self._select_bond_etfs(bond_amount, allocation)
        
        # 黄金配置
        gold_amount = investment_amount * allocation['gold'] / 100
        portfolio['assets']['gold'] = self._select_gold_assets(gold_amount)
        
        # 商品配置
        commodity_amount = investment_amount * allocation['commodities'] / 100
        portfolio['assets']['commodities'] = self._select_commodity_assets(commodity_amount)
        
        return portfolio
    
    def _select_equity_stocks(self, total_amount):
        """选择股票标的"""
        if self.equity_candidates is None or self.equity_candidates.empty:
            return []
        
        # 选择前8只股票
        selected = self.equity_candidates.head(8)
        per_stock_amount = total_amount / len(selected)
        
        stocks = []
        for _, stock in selected.iterrows():
            stocks.append({
                'ticker': stock.get('ticker', 'N/A'),
                'name': stock.get('name', 'N/A'),
                'amount': per_stock_amount,
                'weight': per_stock_amount / total_amount * 100,
                'sector': stock.get('sector', 'N/A'),
                'market_cap': stock.get('market_cap', 'N/A')
            })
        
        return stocks
    
    def _select_bond_etfs(self, total_amount, allocation):
        """选择债券ETF"""
        bonds = []
        
        # 中期债券
        if allocation['bonds_mid'] > 0:
            mid_amount = total_amount * allocation['bonds_mid'] / (allocation['bonds_mid'] + allocation['bonds_long'])
            bonds.append({
                'ticker': 'BND',
                'name': 'Vanguard Total Bond Market ETF',
                'amount': mid_amount,
                'weight': mid_amount / total_amount * 100,
                'duration': '中期',
                'type': '国债+信用债'
            })
        
        # 长期债券
        if allocation['bonds_long'] > 0:
            long_amount = total_amount * allocation['bonds_long'] / (allocation['bonds_mid'] + allocation['bonds_long'])
            bonds.append({
                'ticker': 'TLT',
                'name': 'iShares 20+ Year Treasury Bond ETF',
                'amount': long_amount,
                'weight': long_amount / total_amount * 100,
                'duration': '长期',
                'type': '长期国债'
            })
        
        return bonds
    
    def _select_gold_assets(self, total_amount):
        """选择黄金资产"""
        return [{
            'ticker': 'GLD',
            'name': 'SPDR Gold Shares',
            'amount': total_amount,
            'weight': 100,
            'type': '黄金ETF'
        }]
    
    def _select_commodity_assets(self, total_amount):
        """选择商品资产"""
        return [{
            'ticker': 'DJP',
            'name': 'iPath Bloomberg Commodity Index ETN',
            'amount': total_amount,
            'weight': 100,
            'type': '商品指数'
        }]

def calculate_portfolio_metrics(portfolio, investment_amount):
    """计算投资组合指标"""
    metrics = {
        'expected_return': 0,
        'volatility': 0,
        'sharpe_ratio': 0,
        'max_drawdown': 0,
        'correlation_matrix': None
    }
    
    # 简化的预期收益计算（基于历史数据）
    asset_returns = {
        'equities': 0.08,      # 8% 年化收益
        'bonds_mid': 0.04,     # 4% 年化收益
        'bonds_long': 0.05,    # 5% 年化收益
        'gold': 0.06,          # 6% 年化收益
        'commodities': 0.03    # 3% 年化收益
    }
    
    # 计算加权预期收益
    total_return = 0
    for asset_class, allocation in portfolio['allocation'].items():
        if asset_class in asset_returns:
            total_return += asset_returns[asset_class] * allocation / 100
    
    metrics['expected_return'] = total_return
    
    # 简化的波动率计算
    asset_volatilities = {
        'equities': 0.18,
        'bonds_mid': 0.08,
        'bonds_long': 0.12,
        'gold': 0.20,
        'commodities': 0.25
    }
    
    # 计算加权波动率
    total_volatility = 0
    for asset_class, allocation in portfolio['allocation'].items():
        if asset_class in asset_volatilities:
            total_volatility += (asset_volatilities[asset_class] * allocation / 100) ** 2
    
    metrics['volatility'] = total_volatility ** 0.5
    
    # 计算夏普比率（假设无风险利率为2%）
    risk_free_rate = 0.02
    if metrics['volatility'] > 0:
        metrics['sharpe_ratio'] = (metrics['expected_return'] - risk_free_rate) / metrics['volatility']
    
    return metrics

def generate_portfolio_charts(portfolio, metrics):
    """生成投资组合图表"""
    charts = {}
    
    # 资产配置饼图
    allocation_data = portfolio['allocation']
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(allocation_data.keys()),
        values=list(allocation_data.values()),
        hole=0.3,
        marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    )])
    fig_pie.update_layout(
        title="资产配置分布",
        height=400,
        showlegend=True
    )
    charts['allocation'] = fig_pie
    
    # 预期收益vs风险散点图
    asset_returns = {
        'equities': 0.08,
        'bonds_mid': 0.04,
        'bonds_long': 0.05,
        'gold': 0.06,
        'commodities': 0.03
    }
    
    asset_volatilities = {
        'equities': 0.18,
        'bonds_mid': 0.08,
        'bonds_long': 0.12,
        'gold': 0.20,
        'commodities': 0.25
    }
    
    fig_scatter = go.Figure()
    for asset_class in allocation_data.keys():
        if asset_class in asset_returns:
            fig_scatter.add_trace(go.Scatter(
                x=[asset_volatilities[asset_class]],
                y=[asset_returns[asset_class]],
                mode='markers+text',
                name=asset_class,
                text=[asset_class],
                textposition="top center",
                marker=dict(size=20)
            ))
    
    fig_scatter.update_layout(
        title="风险-收益特征",
        xaxis_title="波动率",
        yaxis_title="预期年化收益",
        height=400
    )
    charts['risk_return'] = fig_scatter
    
    return charts

def display_technical_signals(technical_manager):
    """显示技术分析信号"""
    st.subheader("📈 技术分析信号")
    
    # 获取信号汇总
    summary = technical_manager.get_trading_summary()
    
    # 显示信号统计
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总信号数", summary['total_signals'])
    with col2:
        st.metric("买入信号", summary['buy_signals'], delta=f"+{summary['buy_signals']}")
    with col3:
        st.metric("卖出信号", summary['sell_signals'], delta=f"-{summary['sell_signals']}")
    with col4:
        st.metric("持有信号", summary['hold_signals'])
    
    # 显示最强信号
    if summary['strongest_signals']:
        st.subheader("🔥 最强交易信号")
        for signal in summary['strongest_signals']:
            signal_class = signal['signal'].lower()
            st.markdown(f"""
            <div class="signal-card {signal_class}">
                <strong>{signal['ticker']}</strong> ({signal['asset_class']}) - {signal['signal']}<br>
                信号强度: {signal['strength']:.2f}
            </div>
            """, unsafe_allow_html=True)
    
    # 按资产类别显示信号
    for asset_class in ['equities', 'bonds', 'commodities', 'golds']:
        signals = technical_manager.get_asset_class_signals(asset_class)
        if not signals.empty:
            st.subheader(f"📊 {asset_class.title()} 技术信号")
            st.dataframe(signals[['ticker', 'signal', 'strength', 'timestamp']].head(10))

def main():
    """主函数"""
    st.markdown('<h1 class="main-header">🐯 Tiger All Weather Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">基于宏观环境、基本面筛选和技术分析的智能资产配置系统</p>', unsafe_allow_html=True)
    
    # 侧边栏配置
    st.sidebar.title("⚙️ 系统配置")
    
    # 投资参数
    st.sidebar.subheader("💰 投资参数")
    investment_amount = st.sidebar.number_input(
        "投资金额 (USD)", 
        min_value=10000, 
        max_value=10000000, 
        value=100000, 
        step=10000
    )
    
    investment_horizon = st.sidebar.selectbox(
        "投资期限",
        ["短期 (1-3年)", "中期 (3-7年)", "长期 (7年以上)"]
    )
    
    risk_profile = st.sidebar.selectbox(
        "风险偏好",
        ["保守", "平衡", "积极"]
    )
    
    # 分析选项
    st.sidebar.subheader("🔍 分析选项")
    run_macro = st.sidebar.checkbox("宏观分析", value=True)
    run_fundamental = st.sidebar.checkbox("基本面分析", value=True)
    run_technical = st.sidebar.checkbox("技术分析", value=True)
    
    # 主界面
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 概览", "📊 宏观分析", "🔍 基本面分析", "📈 技术分析", "💼 投资组合"])
    
    # 初始化系统
    if 'portfolio_system' not in st.session_state:
        st.session_state.portfolio_system = CompletePortfolioSystem()
    
    system = st.session_state.portfolio_system
    
    # 概览标签页
    with tab1:
        st.subheader("🎯 系统概览")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **全天候策略特点：**
            - 🎯 基于宏观环境的动态资产配置
            - 📊 多因子基本面筛选
            - 📈 技术分析信号生成
            - ⚖️ 风险分散和收益优化
            """)
        
        with col2:
            st.info("""
            **适用场景：**
            - 💼 长期投资组合管理
            - 🛡️ 风险控制需求
            - 📈 追求稳定收益
            - 🌍 应对不同经济环境
            """)
        
        # 快速分析按钮
        if st.button("🚀 运行快速分析", type="primary"):
            with st.spinner("正在运行分析..."):
                analysis_results = {}
                
                # 运行宏观分析
                if run_macro and fetch_macro_data is not None:
                    try:
                        macro_success = system.run_macro_analysis()
                        if macro_success:
                            analysis_results['macro'] = "✅ 宏观分析完成"
                        else:
                            analysis_results['macro'] = "❌ 宏观分析失败"
                    except Exception as e:
                        analysis_results['macro'] = f"❌ 宏观分析异常: {str(e)[:50]}"
                elif run_macro:
                    analysis_results['macro'] = "⚠️ 宏观分析模块不可用"
                else:
                    analysis_results['macro'] = "⏭️ 跳过宏观分析"
                
                # 运行基本面分析
                if run_fundamental and FundamentalAnalysisManager is not None:
                    try:
                        fundamental_success = system.run_fundamental_analysis()
                        if fundamental_success:
                            analysis_results['fundamental'] = "✅ 基本面分析完成"
                        else:
                            analysis_results['fundamental'] = "❌ 基本面分析失败"
                    except Exception as e:
                        analysis_results['fundamental'] = f"❌ 基本面分析异常: {str(e)[:50]}"
                elif run_fundamental:
                    analysis_results['fundamental'] = "⚠️ 基本面分析模块不可用"
                else:
                    analysis_results['fundamental'] = "⏭️ 跳过基本面分析"
                
                # 运行技术分析
                if run_technical and TechnicalAnalysisManager is not None:
                    try:
                        technical_success = system.run_technical_analysis()
                        if technical_success:
                            analysis_results['technical'] = "✅ 技术分析完成"
                        else:
                            analysis_results['technical'] = "⚠️ 技术分析未生成有效信号"
                    except Exception as e:
                        analysis_results['fundamental'] = f"❌ 技术分析异常: {str(e)[:50]}"
                elif run_technical:
                    analysis_results['technical'] = "⚠️ 技术分析模块不可用"
                else:
                    analysis_results['technical'] = "⏭️ 跳过技术分析"
                
                # 显示分析结果
                st.subheader("📊 分析结果")
                for analysis_type, result in analysis_results.items():
                    if "✅" in result:
                        st.success(result)
                    elif "❌" in result:
                        st.error(result)
                    elif "⚠️" in result:
                        st.warning(result)
                    else:
                        st.info(result)
                
                # 总体状态
                success_count = sum(1 for result in analysis_results.values() if "✅" in result)
                total_count = len([r for r in analysis_results.values() if "⏭️" not in r])
                
                if success_count > 0:
                    st.success(f"🎉 快速分析完成！{success_count}/{total_count} 个模块成功")
                else:
                    st.warning("⚠️ 快速分析完成，但没有模块成功执行")
    
    # 宏观分析标签页
    with tab2:
        st.subheader("📊 宏观环境分析")
        
        if st.button("🔍 更新宏观数据", type="primary"):
            if system.run_macro_analysis():
                st.success("✅ 宏观数据更新成功")
        
        if system.macro_data:
            st.success("✅ 宏观数据已加载")
            
            # 显示宏观指标
            for indicator, data in system.macro_data.items():
                with st.expander(f"📈 {indicator} - {data['description']}"):
                    st.dataframe(data['data'].tail(10))
        
        if system.asset_allocation:
            st.subheader("🎯 资产配置建议")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**调整后配置：**")
                for asset, weight in system.asset_allocation.items():
                    st.metric(asset.replace('_', ' ').title(), f"{weight}%")
            
            with col2:
                # 配置调整原因
                st.write("**配置调整原因：**")
                st.info("""
                - 📊 基于最新宏观指标
                - 🎯 遵循全天候策略原则
                - ⚖️ 平衡风险与收益
                """)
    
    # 基本面分析标签页
    with tab3:
        st.subheader("🔍 基本面分析")
        
        if st.button("📊 更新基本面数据", type="primary"):
            if system.run_fundamental_analysis():
                st.success("✅ 基本面分析完成")
        
        if system.equity_candidates is not None and not system.equity_candidates.empty:
            st.success(f"✅ 已筛选 {len(system.equity_candidates)} 只股票")
            
            # 显示股票候选池
            st.subheader("📋 股票候选池")
            st.dataframe(system.equity_candidates.head(20))
            
            # 股票分布统计
            if 'sector' in system.equity_candidates.columns:
                sector_counts = system.equity_candidates['sector'].value_counts()
                fig_sector = px.bar(
                    x=sector_counts.index, 
                    y=sector_counts.values,
                    title="行业分布"
                )
                st.plotly_chart(fig_sector, use_container_width=True)
    
    # 技术分析标签页
    with tab4:
        st.subheader("📈 技术分析")
        
        if st.button("📈 运行技术分析", type="primary"):
            if system.run_technical_analysis():
                st.success("✅ 技术分析完成")
        
        if hasattr(system.technical_manager, 'all_signals') and system.technical_manager.all_signals:
            display_technical_signals(system.technical_manager)
        else:
            st.info("💡 点击上方按钮运行技术分析")
    
    # 投资组合标签页
    with tab5:
        st.subheader("💼 投资组合构建")
        
        if st.button("🎯 生成投资组合", type="primary"):
            if system.asset_allocation and system.equity_candidates is not None:
                portfolio = system.generate_portfolio_recommendation(
                    investment_amount, investment_horizon, risk_profile
                )
                
                if portfolio:
                    st.session_state.portfolio = portfolio
                    st.success("✅ 投资组合生成成功")
                else:
                    st.error("❌ 投资组合生成失败")
            else:
                st.warning("⚠️ 请先完成宏观分析和基本面分析")
        
        if 'portfolio' in st.session_state:
            portfolio = st.session_state.portfolio
            
            # 显示投资组合
            st.subheader("📊 投资组合详情")
            
            # 资产配置
            col1, col2 = st.columns(2)
            with col1:
                st.write("**资产配置：**")
                for asset, weight in portfolio['allocation'].items():
                    st.metric(asset.replace('_', ' ').title(), f"{weight}%")
            
            with col2:
                st.write("**投资金额：**")
                st.metric("总投资", f"${investment_amount:,.0f}")
                for asset, weight in portfolio['allocation'].items():
                    amount = investment_amount * weight / 100
                    st.metric(asset.replace('_', ' ').title(), f"${amount:,.0f}")
            
            # 生成图表
            metrics = calculate_portfolio_metrics(portfolio, investment_amount)
            charts = generate_portfolio_charts(portfolio, metrics)
            
            # 显示图表
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(charts['allocation'], use_container_width=True)
            
            with col2:
                st.plotly_chart(charts['risk_return'], use_container_width=True)
            
            # 投资组合指标
            st.subheader("📈 投资组合指标")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("预期年化收益", f"{metrics['expected_return']:.1%}")
            with col2:
                st.metric("年化波动率", f"{metrics['volatility']:.1%}")
            with col3:
                st.metric("夏普比率", f"{metrics['sharpe_ratio']:.2f}")
            with col4:
                st.metric("最大回撤", f"{metrics['max_drawdown']:.1%}")
            
            # 详细资产列表
            st.subheader("📋 详细资产配置")
            for asset_class, assets in portfolio['assets'].items():
                if assets:
                    st.write(f"**{asset_class.title()}：**")
                    asset_df = pd.DataFrame(assets)
                    st.dataframe(asset_df, use_container_width=True)

if __name__ == "__main__":
    main()
