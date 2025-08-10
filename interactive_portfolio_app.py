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

# 静默导入各个分析模块
try:
    # 导入宏观分析模块
    from macro_analysis.macro_data import fetch_macro_data
    fetch_macro_data_available = True
except ImportError:
    fetch_macro_data_available = False
    fetch_macro_data = None
    
# 导入资产配置调整模块
try:
    from macro_analysis.allocation_adjust import adjust_allocation
    adjust_allocation_available = True
except ImportError:
    adjust_allocation_available = False
    adjust_allocation = None
    
# 导入基本面分析模块
try:
    from fundamental_analysis.fundamental_manager import FundamentalAnalysisManager
    fundamental_analysis_available = True
except ImportError:
    fundamental_analysis_available = False
    FundamentalAnalysisManager = None
    
# 导入技术分析模块
try:
    from technical_analysis.technical_signals import TechnicalAnalysisManager
    technical_analysis_available = True
except ImportError:
    technical_analysis_available = False
    TechnicalAnalysisManager = None

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
                if not fundamental_analysis_available:
                    st.error("❌ 基本面分析模块未正确导入")
                    return False
                
                # 创建基本面分析管理器实例
                fundamental_manager = FundamentalAnalysisManager()
                
                # 运行所有资产类别的分析
                st.info("🔄 正在分析各个资产类别...")
                
                # 股票分析
                equity_success = fundamental_manager.run_equity_analysis()
                if equity_success:
                    equity_assets = fundamental_manager.all_selected_assets.get('equities')
                    if equity_assets is not None and not equity_assets.empty:
                        # 复制完整的资产信息
                        self.equity_candidates = equity_assets.copy()
                        # 添加筛选日期
                        self.equity_candidates['selected_date'] = datetime.now().strftime('%Y-%m-%d')
                        st.success(f"✅ 股票筛选完成，选出 {len(self.equity_candidates)} 只股票")
                    else:
                        st.warning("⚠️ 股票筛选未返回结果")
                        self.equity_candidates = pd.DataFrame()
                else:
                    st.warning("⚠️ 股票分析失败")
                    self.equity_candidates = pd.DataFrame()
                
                # 债券分析
                bond_success = fundamental_manager.run_bond_analysis()
                if bond_success:
                    bond_assets = fundamental_manager.all_selected_assets.get('bonds')
                    if bond_assets is not None and not bond_assets.empty:
                        # 复制完整的资产信息
                        self.bond_candidates = bond_assets.copy()
                        # 添加筛选日期
                        self.bond_candidates['selected_date'] = datetime.now().strftime('%Y-%m-%d')
                        st.success(f"✅ 债券筛选完成，选出 {len(self.bond_candidates)} 只债券")
                    else:
                        st.warning("⚠️ 债券筛选未返回结果")
                        self.bond_candidates = pd.DataFrame()
                else:
                    st.warning("⚠️ 债券分析失败")
                    self.bond_candidates = pd.DataFrame()
                
                # 商品分析
                commodity_success = fundamental_manager.run_commodity_analysis()
                if commodity_success:
                    commodity_assets = fundamental_manager.all_selected_assets.get('commodities')
                    if commodity_assets is not None and not commodity_assets.empty:
                        # 复制完整的资产信息
                        self.commodity_candidates = commodity_assets.copy()
                        # 添加筛选日期
                        self.commodity_candidates['selected_date'] = datetime.now().strftime('%Y-%m-%d')
                        st.success(f"✅ 商品筛选完成，选出 {len(commodity_assets)} 只商品")
                    else:
                        st.warning("⚠️ 商品筛选未返回结果")
                        self.commodity_candidates = pd.DataFrame()
                else:
                    st.warning("⚠️ 商品分析失败")
                    self.commodity_candidates = pd.DataFrame()
                
                # 黄金分析
                gold_success = fundamental_manager.run_gold_analysis()
                if gold_success:
                    gold_assets = fundamental_manager.all_selected_assets.get('golds')
                    if gold_assets is not None and not gold_assets.empty:
                        # 复制完整的资产信息
                        self.gold_candidates = gold_assets.copy()
                        # 添加筛选日期
                        self.gold_candidates['selected_date'] = datetime.now().strftime('%Y-%m-%d')
                        st.success(f"✅ 黄金筛选完成，选出 {len(gold_assets)} 只黄金")
                    else:
                        st.warning("⚠️ 黄金筛选未返回结果")
                        self.gold_candidates = pd.DataFrame()
                else:
                    st.warning("⚠️ 黄金分析失败")
                    self.gold_candidates = pd.DataFrame()
                
                # 检查是否有任何资产类别成功
                total_candidates = (
                    len(self.equity_candidates) if hasattr(self, 'equity_candidates') and not self.equity_candidates.empty else 0 +
                    len(self.bond_candidates) if hasattr(self, 'bond_candidates') and not self.bond_candidates.empty else 0 +
                    len(self.commodity_candidates) if hasattr(self, 'commodity_candidates') and not self.commodity_candidates.empty else 0 +
                    len(self.gold_candidates) if hasattr(self, 'gold_candidates') and not self.gold_candidates.empty else 0
                )
                
                if total_candidates > 0:
                    st.success(f"🎉 基本面分析完成！总共筛选出 {total_candidates} 个标的")
                    return True
                else:
                    st.warning("⚠️ 基本面分析未返回任何结果")
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
        # 检查资产配置
        if not self.asset_allocation:
            st.error("❌ 缺少宏观分析数据，请先运行宏观分析")
            return None
        
        # 检查基本面分析结果
        if not hasattr(self, 'equity_candidates') or self.equity_candidates is None or self.equity_candidates.empty:
            st.error("❌ 缺少基本面分析数据，请先运行基本面分析")
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
        
        # 整合技术分析建议
        if hasattr(self, 'technical_manager') and self.technical_manager:
            portfolio['technical_signals'] = self._integrate_technical_signals()
        
        return portfolio
    
    def _integrate_technical_signals(self):
        """整合技术分析信号到投资组合"""
        technical_recommendations = {}
        
        if hasattr(self.technical_manager, 'all_signals'):
            for asset_class, signals in self.technical_manager.all_signals.items():
                if signals:
                    recommendations = []
                    for ticker, signal in list(signals.items())[:5]:  # 取前5个信号
                        recommendations.append({
                            'ticker': ticker,
                            'signal': signal.get('signal', 'WATCH'),
                            'strategy': signal.get('strategy', 'technical'),
                            'confidence': signal.get('confidence', 0.3),
                            'recommendation': signal.get('recommendation', '建议观望，一周内买入'),
                            'price': signal.get('price', 0),
                            'stop_loss': signal.get('stop_loss', 0),
                            'target': signal.get('target', 0)
                        })
                    technical_recommendations[asset_class] = recommendations
        
        return technical_recommendations
    
    def _select_equity_stocks(self, total_amount):
        """选择股票标的"""
        if self.equity_candidates is None or self.equity_candidates.empty:
            # 如果没有基本面分析结果，使用技术分析结果
            if hasattr(self, 'technical_manager') and self.technical_manager and 'equities' in self.technical_manager.all_signals:
                signals = self.technical_manager.all_signals['equities']
                selected = list(signals.keys())[:8]  # 取前8个
                per_stock_amount = total_amount / len(selected)
                
                stocks = []
                for ticker in selected:
                    signal = signals[ticker]
                    stocks.append({
                        'ticker': ticker,
                        'name': f'{ticker} Stock',
                        'amount': per_stock_amount,
                        'weight': per_stock_amount / total_amount * 100,
                        'sector': 'N/A',
                        'market_cap': 'N/A',
                        'technical_signal': signal.get('signal', 'WATCH'),
                        'recommendation': signal.get('recommendation', '建议观望，一周内买入')
                    })
                return stocks
            else:
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
                'market_cap': stock.get('market_cap', 'N/A'),
                'technical_signal': 'N/A',
                'recommendation': '基于基本面分析选择'
            })
        
        return stocks
    
    def _select_bond_etfs(self, total_amount, allocation):
        """选择债券ETF"""
        bonds = []
        
        # 检查是否有技术分析建议
        bond_signals = []
        if hasattr(self, 'technical_manager') and self.technical_manager and 'bonds' in self.technical_manager.all_signals:
            bond_signals = list(self.technical_manager.all_signals['bonds'].keys())
        
        # 中期债券
        if allocation['bonds_mid'] > 0:
            mid_amount = total_amount * allocation['bonds_mid'] / (allocation['bonds_mid'] + allocation['bonds_long'])
            ticker = bond_signals[0] if bond_signals else 'BND'
            bonds.append({
                'ticker': ticker,
                'name': 'Vanguard Total Bond Market ETF',
                'amount': mid_amount,
                'weight': mid_amount / total_amount * 100,
                'duration': '中期',
                'type': '国债+信用债',
                'technical_signal': 'WATCH',
                'recommendation': '建议观望，一周内买入'
            })
        
        # 长期债券
        if allocation['bonds_long'] > 0:
            long_amount = total_amount * allocation['bonds_long'] / (allocation['bonds_mid'] + allocation['bonds_long'])
            ticker = bond_signals[1] if len(bond_signals) > 1 else 'TLT'
            bonds.append({
                'ticker': ticker,
                'name': 'iShares 20+ Year Treasury Bond ETF',
                'amount': long_amount,
                'weight': long_amount / total_amount * 100,
                'duration': '长期',
                'type': '长期国债',
                'technical_signal': 'WATCH',
                'recommendation': '建议观望，一周内买入'
            })
        
        return bonds
    
    def _select_gold_assets(self, total_amount):
        """选择黄金资产"""
        # 检查是否有技术分析建议
        gold_ticker = 'GLD'
        if hasattr(self, 'technical_manager') and self.technical_manager and 'golds' in self.technical_manager.all_signals:
            gold_signals = list(self.technical_manager.all_signals['golds'].keys())
            if gold_signals:
                gold_ticker = gold_signals[0]
        
        return [{
            'ticker': gold_ticker,
            'name': 'SPDR Gold Shares',
            'amount': total_amount,
            'weight': 100,
            'type': '黄金ETF',
            'technical_signal': 'WATCH',
            'recommendation': '建议观望，一周内买入'
        }]
    
    def _select_commodity_assets(self, total_amount):
        """选择商品资产"""
        # 检查是否有技术分析建议
        commodity_ticker = 'DJP'
        if hasattr(self, 'technical_manager') and self.technical_manager and 'commodities' in self.technical_manager.all_signals:
            commodity_signals = list(self.technical_manager.all_signals['commodities'].keys())
            if commodity_signals:
                commodity_ticker = commodity_signals[0]
        
        return [{
            'ticker': commodity_ticker,
            'name': 'iPath Bloomberg Commodity Index ETN',
            'amount': total_amount,
            'weight': 100,
            'type': '商品指数',
            'technical_signal': 'WATCH',
            'recommendation': '建议观望，一周内买入'
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

def display_fundamental_results(system):
    """显示基本面分析结果"""
    st.subheader("📊 基本面分析结果")
    
    asset_class_names = {
        'equities': '股票',
        'bonds': '债券',
        'commodities': '大宗商品',
        'golds': '黄金'
    }
    
    # 显示各资产类别的筛选结果
    for asset_class, name in asset_class_names.items():
        candidates_attr = f"{asset_class}_candidates"
        if hasattr(system, candidates_attr) and not getattr(system, candidates_attr).empty:
            candidates = getattr(system, candidates_attr)
            st.write(f"**{name} 筛选结果 ({len(candidates)} 个标的)**")
            
            # 创建结果表格
            result_data = []
            for _, row in candidates.iterrows():
                result_data.append({
                    '代码': row['ticker'],
                    '名称': row.get('name', 'N/A'),
                    '得分': f"{row.get('score', 0):.1f}" if 'score' in row else 'N/A',
                    '筛选日期': row.get('selected_date', 'N/A'),
                    '状态': '✅ 已筛选'
                })
            
            if result_data:
                df = pd.DataFrame(result_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info(f"⚠️ {name} 暂无筛选结果")
        else:
            # 如果没有筛选结果，尝试从投资组合中获取建议的标的
            if hasattr(system, 'portfolio') and system.portfolio and 'assets' in system.portfolio:
                portfolio_assets = system.portfolio['assets'].get(asset_class, [])
                if portfolio_assets:
                    st.write(f"**{name} 投资组合建议 ({len(portfolio_assets)} 个标的)**")
                    
                    # 从投资组合中提取标的信息
                    result_data = []
                    for asset in portfolio_assets:
                        result_data.append({
                            '代码': asset.get('ticker', 'N/A'),
                            '名称': asset.get('name', asset.get('ticker', 'N/A')),
                            '权重': f"{asset.get('weight', 0):.1f}%" if 'weight' in asset else 'N/A',
                            '金额': f"${asset.get('amount', 0):,.2f}" if 'amount' in asset else 'N/A',
                            '状态': '💼 投资组合推荐'
                        })
                    
                    if result_data:
                        df = pd.DataFrame(result_data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info(f"💡 {name} 暂无投资组合建议")
                else:
                    st.write(f"**{name} 筛选结果**")
                    st.info(f"💡 {name} 暂无筛选结果，建议先运行基本面分析")
            else:
                st.write(f"**{name} 筛选结果**")
                st.info(f"💡 {name} 暂无筛选结果，建议先运行基本面分析")
        
        st.divider()
    
    # 添加筛选说明
    st.info("💡 基本面分析基于财务指标、行业地位、成长性等多维度指标进行筛选，结果将定期更新")

def display_technical_signals(technical_manager):
    """显示技术分析信号"""
    st.subheader("📈 技术分析信号")
    
    if not technical_manager:
        st.warning("⚠️ 技术分析数据不可用")
        return
    
    # 获取信号汇总
    try:
        summary = technical_manager.get_trading_summary()
        
        # 显示信号统计
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总信号数", summary.get('total_signals', 0))
        with col2:
            st.metric("买入信号", summary.get('buy_signals', 0), delta=f"+{summary.get('buy_signals', 0)}")
        with col3:
            st.metric("卖出信号", summary.get('sell_signals', 0), delta=f"-{summary.get('sell_signals', 0)}")
        with col4:
            st.metric("观望信号", summary.get('watch_signals', 0))
    except Exception as e:
        st.warning(f"⚠️ 无法获取信号汇总：{e}")
        summary = {'total_signals': 0, 'buy_signals': 0, 'sell_signals': 0, 'watch_signals': 0}
    
    # 显示每个资产类别的所有标的和技术分析结果
    st.subheader("🎯 各资产类别技术分析结果")
    
    asset_class_names = {
        'equities': '股票',
        'bonds': '债券',
        'commodities': '大宗商品',
        'golds': '黄金'
    }
    
    # 获取所有资产类别的标的列表（确保唯一性）
    all_tickers = {
        'equities': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'JPM', 'JNJ', 'V', 'PG', 'UNH', 'HD', 'MA'],
        'bonds': ['TLT', 'IEF', 'SHY', 'AGG', 'BND', 'VCIT', 'VCSH', 'LQD', 'HYG', 'JNK', 'BNDX', 'VWOB', 'EMB', 'PCY', 'LEMB'],
        'commodities': ['DIA', 'SPY', 'QQQ', 'IWM', 'GLD', 'SLV', 'USO', 'UNG', 'DBA', 'DBC', 'XLE', 'XLF', 'XLK', 'XLV', 'XLI'],
        'golds': ['GLD', 'IAU', 'SGOL', 'GLDM', 'BAR', 'OUNZ', 'GLTR', 'AAAU', 'GLDE', 'BGLD', 'XAUUSD=X', 'GC=F']
    }
    
    for asset_class, tickers in all_tickers.items():
        asset_name = asset_class_names.get(asset_class, asset_class)
        st.write(f"**{asset_name} 技术分析结果**")
        
        # 获取该资产类别的技术分析信号
        signals = technical_manager.all_signals.get(asset_class, {})
        
        # 为每个标的创建技术分析结果（确保唯一性）
        analysis_results = []
        processed_tickers = set()  # 用于跟踪已处理的标的
        
        for ticker in tickers:
            if ticker in processed_tickers:
                continue  # 跳过已处理的标的
                
            if ticker in signals:
                # 有明确信号的情况
                signal = signals[ticker]
                analysis_results.append({
                    '代码': ticker,
                    '策略': signal.get('strategy', '综合技术指标'),
                    '信号': signal.get('signal', 'WATCH'),
                    '置信度': f"{signal.get('confidence', 0):.1%}",
                    '建议': signal.get('recommendation', '建议观望，一周内买入'),
                    '价格': f"${signal.get('price', 0):.2f}" if signal.get('price', 0) > 0 else 'N/A',
                    '状态': '🟢 有信号'
                })
            else:
                # 没有明确信号的情况，显示观望状态
                analysis_results.append({
                    '代码': ticker,
                    '策略': '综合技术指标',
                    '信号': 'WATCH',
                    '置信度': '50.0%',
                    '建议': '当前无明显交易信号，建议观望',
                    '价格': 'N/A',
                    '状态': '🟡 观望中'
                })
            
            processed_tickers.add(ticker)  # 标记为已处理
        
        if analysis_results:
            df = pd.DataFrame(analysis_results)
            st.dataframe(df, use_container_width=True)
            
            # 添加实时更新提示
            st.info(f"💡 {asset_name} 技术分析结果将实时更新，建议定期刷新页面获取最新信号")
        else:
            st.info(f"⚠️ {asset_name} 暂无技术分析数据")
        
        st.divider()
    
    # 显示最强信号
    try:
        if summary.get('strongest_signals'):
            st.subheader("🔥 最强交易信号")
            strongest_df = pd.DataFrame(summary['strongest_signals'])
            st.dataframe(strongest_df, use_container_width=True)
    except Exception as e:
        st.info("暂无最强信号数据")
    
    # 显示技术分析状态
    if hasattr(technical_manager, 'analysis_status'):
        st.subheader("📊 技术分析状态")
        status_data = []
        for asset_class, status in technical_manager.analysis_status.items():
            status_text = {
                'success': '✅ 成功',
                'error': '❌ 失败',
                'watch_signals': '👀 观望信号',
                'no_signals': '⚠️ 无信号'
            }.get(status, status)
            
            status_data.append({
                '资产类别': asset_class_names.get(asset_class, asset_class),
                '状态': status_text,
                '信号数量': len(technical_manager.all_signals.get(asset_class, {}))
            })
        
        if status_data:
            status_df = pd.DataFrame(status_data)
            st.dataframe(status_df, use_container_width=True)
    
    # 添加自动刷新说明
    st.info("🔄 技术分析结果将根据市场数据自动更新，建议每15-30分钟刷新一次页面")

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
                if run_macro and fetch_macro_data_available:
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
                if run_fundamental and fundamental_analysis_available:
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
                if run_technical and technical_analysis_available:
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
        
        # 显示所有资产类别的筛选结果
        if (hasattr(system, 'equity_candidates') and system.equity_candidates is not None and not system.equity_candidates.empty) or \
           (hasattr(system, 'bond_candidates') and system.bond_candidates is not None and not system.bond_candidates.empty) or \
           (hasattr(system, 'commodity_candidates') and system.commodity_candidates is not None and not system.commodity_candidates.empty) or \
           (hasattr(system, 'gold_candidates') and system.gold_candidates is not None and not system.gold_candidates.empty):
            
            # 调用基本面结果显示函数
            display_fundamental_results(system)
            
            # 显示股票候选池的额外信息（如果有的话）
            if system.equity_candidates is not None and not system.equity_candidates.empty:
                st.subheader("📋 股票候选池详情")
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
        else:
            st.info("💡 点击上方按钮运行基本面分析")
    
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
                    asset_class_name = {
                        'equities': '股票',
                        'bonds': '债券',
                        'gold': '黄金',
                        'commodities': '大宗商品'
                    }.get(asset_class, asset_class)
                    
                    st.write(f"**{asset_class_name}：**")
                    asset_df = pd.DataFrame(assets)
                    
                    # 格式化金额显示
                    if 'amount' in asset_df.columns:
                        asset_df['金额'] = asset_df['amount'].apply(lambda x: f"${x:,.2f}")
                        asset_df['权重'] = asset_df['weight'].apply(lambda x: f"{x:.1f}%")
                    
                    # 显示资产表格
                    st.dataframe(asset_df, use_container_width=True)
                    
                    # 显示技术分析建议
                    if 'technical_signals' in portfolio and asset_class in portfolio['technical_signals']:
                        st.write(f"**{asset_class_name}技术分析建议：**")
                        tech_signals = portfolio['technical_signals'][asset_class]
                        if tech_signals:
                            tech_df = pd.DataFrame(tech_signals)
                            # 格式化显示
                            if 'price' in tech_df.columns:
                                tech_df['价格'] = tech_df['price'].apply(lambda x: f"${x:.2f}" if x > 0 else 'N/A')
                            if 'confidence' in tech_df.columns:
                                tech_df['置信度'] = tech_df['confidence'].apply(lambda x: f"{x:.1%}")
                            
                            st.dataframe(tech_df[['ticker', 'signal', 'strategy', 'confidence', 'recommendation']], 
                                        use_container_width=True)
                        else:
                            st.info(f"⚠️ {asset_class_name} 暂无技术分析建议")
                    
                    st.divider()
            
            # 技术分析建议汇总
            if 'technical_signals' in portfolio:
                st.subheader("📈 技术分析建议汇总")
                
                all_recommendations = []
                for asset_class, signals in portfolio['technical_signals'].items():
                    for signal in signals:
                        asset_class_name = {
                            'equities': '股票',
                            'bonds': '债券',
                            'gold': '黄金',
                            'commodities': '大宗商品',
                            'golds': '黄金'
                        }.get(asset_class, asset_class)
                        
                        all_recommendations.append({
                            '资产类别': asset_class_name,
                            '代码': signal['ticker'],
                            '信号': signal['signal'],
                            '策略': signal['strategy'],
                            '置信度': f"{signal['confidence']:.1%}",
                            '建议': signal['recommendation']
                        })
                
                if all_recommendations:
                    rec_df = pd.DataFrame(all_recommendations)
                    st.dataframe(rec_df, use_container_width=True)
                    
                    # 统计信号类型
                    signal_counts = rec_df['信号'].value_counts()
                    st.write("**信号统计：**")
                    for signal, count in signal_counts.items():
                        signal_icon = {
                            'BUY': '🟢',
                            'SELL': '🔴',
                            'WATCH': '🟡'
                        }.get(signal, '⚪')
                        st.write(f"{signal_icon} {signal}: {count} 个")
                else:
                    st.info("暂无技术分析建议")
            
            # 投资建议总结
            st.subheader("💡 投资建议总结")
            
            # 根据技术分析生成建议
            if 'technical_signals' in portfolio:
                buy_signals = 0
                watch_signals = 0
                
                for asset_class, signals in portfolio['technical_signals'].items():
                    for signal in signals:
                        if signal['signal'] == 'BUY':
                            buy_signals += 1
                        elif signal['signal'] == 'WATCH':
                            watch_signals += 1
                
                if buy_signals > 0:
                    st.success(f"🎯 建议买入 {buy_signals} 个标的，把握当前投资机会")
                
                if watch_signals > 0:
                    st.info(f"👀 建议观望 {watch_signals} 个标的，等待更好的入场时机")
                
                st.info("""
                **投资策略建议：**
                - 📈 对于买入信号的标的，建议一周内分批建仓
                - 👀 对于观望信号的标的，建议持续关注，等待技术指标改善
                - ⚖️ 建议采用定投策略，分散投资风险
                - 📊 定期回顾投资组合，根据市场变化调整配置
                """)
            else:
                st.info("💡 建议采用均衡配置策略，定期再平衡投资组合")

if __name__ == "__main__":
    main()
