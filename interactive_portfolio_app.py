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
                    
                    # 保存筛选结果到session state，确保数据持久化
                    st.session_state.fundamental_results = {
                        'equity_candidates': self.equity_candidates,
                        'bond_candidates': self.bond_candidates,
                        'commodity_candidates': self.commodity_candidates,
                        'gold_candidates': self.gold_candidates,
                        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
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
        
        # 验证配置一致性
        if not self._validate_allocation_consistency(final_allocation):
            st.warning("⚠️ 资产配置与宏观分析建议存在差异，已进行一致性调整")
            st.info(f"📊 调整后配置：{final_allocation}")
        
        # 创建详细投资组合
        portfolio = self._create_detailed_portfolio(final_allocation, investment_amount)
        
        # 保存最终配置到session state，确保一致性
        st.session_state.final_allocation = final_allocation
        st.session_state.portfolio = portfolio
        
        return portfolio
    
    def _validate_allocation_consistency(self, adjusted_allocation):
        """验证调整后的配置与宏观分析建议的一致性"""
        if not hasattr(self, 'asset_allocation') or not self.asset_allocation:
            return True
        
        # 计算配置差异
        differences = {}
        total_diff = 0
        
        for asset in adjusted_allocation:
            if asset in self.asset_allocation:
                diff = abs(adjusted_allocation[asset] - self.asset_allocation[asset])
                differences[asset] = diff
                total_diff += diff
        
        # 如果总差异超过2%，认为不一致（降低阈值以提高一致性）
        if total_diff > 2:
            # 进行一致性调整
            self._reconcile_allocation(adjusted_allocation)
            return False
        
        return True
    
    def _reconcile_allocation(self, adjusted_allocation):
        """协调配置差异，确保与宏观分析建议一致"""
        if not hasattr(self, 'asset_allocation') or not self.asset_allocation:
            return
        
        # 计算调整权重
        total_adjusted = sum(adjusted_allocation.values())
        total_macro = sum(self.asset_allocation.values())
        
        if total_adjusted > 0 and total_macro > 0:
            # 按比例调整到宏观分析建议，但保留一定的个性化调整
            for asset in adjusted_allocation:
                if asset in self.asset_allocation:
                    # 使用加权平均，宏观分析占90%，个性化调整占10%（提高宏观分析权重）
                    macro_weight = 0.9
                    personal_weight = 0.1
                    adjusted_allocation[asset] = (
                        self.asset_allocation[asset] * macro_weight + 
                        adjusted_allocation[asset] * personal_weight
                    )
            
            # 重新标准化到100%
            total = sum(adjusted_allocation.values())
            if total > 0:
                for asset in adjusted_allocation:
                    adjusted_allocation[asset] = round(adjusted_allocation[asset] / total * 100, 1)
    
    def _adjust_for_horizon(self, horizon):
        """根据投资期限调整配置（减少调整幅度以保持一致性）"""
        if horizon == "短期 (1-3年)":
            return {"equities": -2, "bonds_mid": 2, "bonds_long": 0, "gold": 0, "commodities": 0}
        elif horizon == "中期 (3-7年)":
            return {"equities": 0, "bonds_mid": 0, "bonds_long": 0, "gold": 0, "commodities": 0}
        elif horizon == "长期 (7年以上)":
            return {"equities": 2, "bonds_mid": -1, "bonds_long": -1, "gold": 0, "commodities": 0}
        return {"equities": 0, "bonds_mid": 0, "bonds_long": 0, "gold": 0, "commodities": 0}
    
    def _adjust_for_risk(self, risk_profile):
        """根据风险偏好调整配置"""
        if risk_profile == "保守":
            return {"equities": -5, "bonds_mid": 3, "bonds_long": 2, "gold": 0, "commodities": 0}
        elif risk_profile == "平衡":
            return {"equities": 0, "bonds_mid": 0, "bonds_long": 0, "gold": 0, "commodities": 0}
        elif risk_profile == "积极":
            return {"equities": 5, "bonds_mid": -2, "bonds_long": -2, "gold": -1, "commodities": 0}
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
        
        # 中期债券配置 - 保持与宏观分析一致
        bonds_mid_amount = investment_amount * allocation['bonds_mid'] / 100
        portfolio['assets']['bonds_mid'] = self._select_bond_etfs(bonds_mid_amount, {'bonds_mid': allocation['bonds_mid'], 'bonds_long': 0})
        
        # 长期债券配置 - 保持与宏观分析一致
        bonds_long_amount = investment_amount * allocation['bonds_long'] / 100
        portfolio['assets']['bonds_long'] = self._select_bond_etfs(bonds_long_amount, {'bonds_mid': 0, 'bonds_long': allocation['bonds_long']})
        
        # 黄金配置
        gold_amount = investment_amount * allocation['gold'] / 100
        portfolio['assets']['gold'] = self._select_gold_assets(gold_amount)
        
        # 商品配置
        commodity_amount = investment_amount * allocation['commodities'] / 100
        portfolio['assets']['commodities'] = self._select_commodity_assets(commodity_amount)
        
        # 验证总投资金额
        total_invested = sum([
            sum(asset['amount'] for asset in portfolio['assets']['equities']),
            sum(asset['amount'] for asset in portfolio['assets']['bonds_mid']),
            sum(asset['amount'] for asset in portfolio['assets']['bonds_long']),
            sum(asset['amount'] for asset in portfolio['assets']['gold']),
            sum(asset['amount'] for asset in portfolio['assets']['commodities'])
        ])
        
        # 如果金额不匹配，进行微调
        if abs(total_invested - investment_amount) > 0.01:
            adjustment_factor = investment_amount / total_invested
            for asset_class in portfolio['assets']:
                for asset in portfolio['assets'][asset_class]:
                    asset['amount'] = round(asset['amount'] * adjustment_factor, 2)
                    asset['weight'] = round(asset['weight'] * adjustment_factor, 2)
        
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
        if self.equity_candidates is not None and not self.equity_candidates.empty:
            # 使用基本面分析筛选出的股票
            selected_stocks = self.equity_candidates.head(8)  # 取前8只
            per_stock_amount = total_amount / len(selected_stocks)
            
            stocks = []
            for _, row in selected_stocks.iterrows():
                stocks.append({
                    'ticker': row['ticker'],
                    'name': row.get('name', row['ticker']),
                    'amount': per_stock_amount,
                    'weight': per_stock_amount / total_amount * 100,
                    'sector': row.get('sector', 'N/A'),
                    'market_cap': row.get('market_cap', 'N/A'),
                    'score': row.get('score', 'N/A'),
                    'fundamental_rating': '✅ 基本面筛选'
                })
            return stocks
        else:
            # 如果没有基本面分析结果，返回空列表
            st.warning("⚠️ 股票基本面分析结果不可用")
            return []
    
    def _select_bond_etfs(self, total_amount, allocation):
        """选择债券标的"""
        # 确定债券类型
        bond_type = None
        if allocation.get('bonds_mid', 0) > 0:
            bond_type = 'bonds_mid'
        elif allocation.get('bonds_long', 0) > 0:
            bond_type = 'bonds_long'
        
        if bond_type == 'bonds_mid':
            # 选择中期债券
            if hasattr(self, 'bond_candidates') and self.bond_candidates is not None and not self.bond_candidates.empty:
                # 使用基本面分析筛选出的债券
                selected_bonds = self.bond_candidates.head(5)  # 取前5只
                per_bond_amount = total_amount / len(selected_bonds)
                
                bonds = []
                for _, row in selected_bonds.iterrows():
                    bonds.append({
                        'ticker': row['ticker'],
                        'name': row.get('name', row['ticker']),
                        'amount': per_bond_amount,
                        'weight': per_bond_amount / total_amount * 100,
                        'duration': '中期 (2-5年)',
                        'score': row.get('score', 'N/A'),
                        'fundamental_rating': '✅ 基本面筛选'
                    })
                return bonds
            else:
                st.warning("⚠️ 债券基本面分析结果不可用")
                return []
        
        elif bond_type == 'bonds_long':
            # 选择长期债券
            if hasattr(self, 'bond_candidates') and self.bond_candidates is not None and not self.bond_candidates.empty:
                # 使用基本面分析筛选出的债券
                selected_bonds = self.bond_candidates.head(5)  # 取前5只
                per_bond_amount = total_amount / len(selected_bonds)
                
                bonds = []
                for _, row in selected_bonds.iterrows():
                    bonds.append({
                        'ticker': row['ticker'],
                        'name': row.get('name', row['ticker']),
                        'amount': per_bond_amount,
                        'weight': per_bond_amount / total_amount * 100,
                        'duration': '长期 (10年以上)',
                        'score': row.get('score', 'N/A'),
                        'fundamental_rating': '✅ 基本面筛选'
                    })
                return bonds
            else:
                st.warning("⚠️ 债券基本面分析结果不可用")
                return []
        
        return []
    
    def _select_gold_assets(self, total_amount):
        """选择黄金标的"""
        if hasattr(self, 'gold_candidates') and self.gold_candidates is not None and not self.gold_candidates.empty:
            # 使用基本面分析筛选出的黄金标的
            selected_golds = self.gold_candidates.head(3)  # 取前3只
            per_gold_amount = total_amount / len(selected_golds)
            
            golds = []
            for _, row in selected_golds.iterrows():
                golds.append({
                    'ticker': row['ticker'],
                    'name': row.get('name', row['ticker']),
                    'amount': per_gold_amount,
                    'weight': per_gold_amount / total_amount * 100,
                    'type': '贵金属',
                    'score': row.get('score', 'N/A'),
                    'fundamental_rating': '✅ 基本面筛选'
                })
            return golds
        else:
            st.warning("⚠️ 黄金基本面分析结果不可用")
            return []
    
    def _select_commodity_assets(self, total_amount):
        """选择商品标的"""
        if hasattr(self, 'commodity_candidates') and self.commodity_candidates is not None and not self.commodity_candidates.empty:
            # 使用基本面分析筛选出的商品标的
            selected_commodities = self.commodity_candidates.head(3)  # 取前3只
            per_commodity_amount = total_amount / len(selected_commodities)
            
            commodities = []
            for _, row in selected_commodities.iterrows():
                commodities.append({
                    'ticker': row['ticker'],
                    'name': row.get('name', row['ticker']),
                    'amount': per_commodity_amount,
                    'weight': per_commodity_amount / total_amount * 100,
                    'type': '大宗商品',
                    'score': row.get('score', 'N/A'),
                    'fundamental_rating': '✅ 基本面筛选'
                })
            return commodities
        else:
            st.warning("⚠️ 商品基本面分析结果不可用")
            return []

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

def display_fundamental_results(system, portfolio_assets=None):
    """显示基本面分析结果"""
    st.subheader("🔍 基本面分析结果")
    
    # 首先尝试从session state恢复数据
    if 'fundamental_results' in st.session_state:
        fundamental_results = st.session_state.fundamental_results
        system.equity_candidates = fundamental_results.get('equity_candidates', pd.DataFrame())
        system.bond_candidates = fundamental_results.get('bond_candidates', pd.DataFrame())
        system.commodity_candidates = fundamental_results.get('commodity_candidates', pd.DataFrame())
        system.gold_candidates = fundamental_results.get('gold_candidates', pd.DataFrame())
        
        # 显示分析时间
        analysis_date = fundamental_results.get('analysis_date', 'N/A')
        st.info(f"📅 分析时间: {analysis_date}")
    
    asset_class_names = {
        'equities': '股票',
        'bonds': '债券',
        'commodities': '大宗商品',
        'golds': '黄金'
    }
    
    # 检查基本面分析是否有结果
    has_fundamental_results = False
    for asset_class in asset_class_names.keys():
        candidates_attr = f"{asset_class}_candidates"
        if hasattr(system, candidates_attr) and not getattr(system, candidates_attr).empty:
            has_fundamental_results = True
            break
    
    if not has_fundamental_results:
        st.warning("⚠️ 基本面分析尚未运行或未返回结果")
        st.info("💡 请先运行基本面分析模块")
        return
    
    # 如果有投资组合数据，优先显示投资组合中的标的
    if portfolio_assets:
        st.info("🎯 显示投资组合中的标的的基本面分析结果")
        
        for asset_class, name in asset_class_names.items():
            if asset_class in portfolio_assets and portfolio_assets[asset_class]:
                st.write(f"**{name} 投资组合标的 ({len(portfolio_assets[asset_class])} 个)**")
                
                # 获取投资组合中的标的代码
                portfolio_tickers = [asset.get('ticker', '') for asset in portfolio_assets[asset_class]]
                
                # 从基本面分析结果中筛选出投资组合中的标的
                candidates_attr = f"{asset_class}_candidates"
                if hasattr(system, candidates_attr) and not getattr(system, candidates_attr).empty:
                    candidates = getattr(system, candidates_attr)
                    # 筛选投资组合中的标的
                    portfolio_candidates = candidates[candidates['ticker'].isin(portfolio_tickers)]
                    
                    if not portfolio_candidates.empty:
                        # 创建结果表格，优化数值显示
                        result_data = []
                        for _, row in portfolio_candidates.iterrows():
                            # 格式化得分显示
                            score = row.get('score', 0)
                            if isinstance(score, (int, float)):
                                if score >= 80:
                                    score_display = f"🟢 {score:.1f}"
                                elif score >= 60:
                                    score_display = f"🟡 {score:.1f}"
                                else:
                                    score_display = f"🔴 {score:.1f}"
                            else:
                                score_display = 'N/A'
                            
                            # 格式化其他数值字段
                            market_cap = row.get('market_cap', 0)
                            if isinstance(market_cap, (int, float)) and market_cap > 0:
                                if market_cap >= 1e12:
                                    market_cap_display = f"${market_cap/1e12:.1f}T"
                                elif market_cap >= 1e9:
                                    market_cap_display = f"${market_cap/1e9:.1f}B"
                                elif market_cap >= 1e6:
                                    market_cap_display = f"${market_cap/1e6:.1f}M"
                                else:
                                    market_cap_display = f"${market_cap:,.0f}"
                            else:
                                market_cap_display = 'N/A'
                            
                            result_data.append({
                                '代码': row['ticker'],
                                '名称': row.get('name', 'N/A'),
                                '得分': score_display,
                                '市值': market_cap_display,
                                '筛选日期': row.get('selected_date', 'N/A'),
                                '状态': '✅ 已入选投资组合'
                            })
                        
                        if result_data:
                            df = pd.DataFrame(result_data)
                            st.dataframe(df, use_container_width=True)
                            
                            # 添加得分分布图表
                            if 'score' in portfolio_candidates.columns:
                                score_values = portfolio_candidates['score'].dropna()
                                if len(score_values) > 0:
                                    fig = px.histogram(
                                        x=score_values,
                                        title=f"{name} 投资组合标的得分分布",
                                        labels={'x': '筛选得分', 'y': '标的数量'},
                                        nbins=10
                                    )
                                    fig.update_layout(showlegend=False)
                                    st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f"⚠️ 投资组合中的 {name} 标的在基本面分析中未找到")
                else:
                    st.warning(f"⚠️ {name} 暂无基本面分析结果")
                
                st.divider()
    else:
        # 如果没有投资组合数据，显示所有筛选结果（但限制数量）
        st.info("💡 显示基本面分析筛选结果（建议生成投资组合以查看最终标的）")
        
        for asset_class, name in asset_class_names.items():
            candidates_attr = f"{asset_class}_candidates"
            if hasattr(system, candidates_attr) and not getattr(system, candidates_attr).empty:
                candidates = getattr(system, candidates_attr)
                st.write(f"**{name} 筛选结果 ({len(candidates)} 个标的)**")
                
                # 只显示前10个结果，避免信息过载
                if len(candidates) > 10:
                    st.info(f"💡 显示前10个筛选结果（共{len(candidates)}个）")
                    display_candidates = candidates.head(10)
                else:
                    display_candidates = candidates
                
                # 创建结果表格，优化数值显示
                result_data = []
                for _, row in display_candidates.iterrows():
                    # 格式化得分显示
                    score = row.get('score', 0)
                    if isinstance(score, (int, float)):
                        if score >= 80:
                            score_display = f"🟢 {score:.1f}"
                        elif score >= 60:
                            score_display = f"🟡 {score:.1f}"
                        else:
                            score_display = f"🔴 {score:.1f}"
                    else:
                        score_display = 'N/A'
                    
                    # 格式化其他数值字段
                    market_cap = row.get('market_cap', 0)
                    if isinstance(market_cap, (int, float)) and market_cap > 0:
                        if market_cap >= 1e12:
                            market_cap_display = f"${market_cap/1e12:.1f}T"
                        elif market_cap >= 1e9:
                            market_cap_display = f"${market_cap/1e9:.1f}B"
                        elif market_cap >= 1e6:
                            market_cap_display = f"${market_cap/1e6:.1f}M"
                        else:
                            market_cap_display = f"${market_cap:,.0f}"
                    else:
                        market_cap_display = 'N/A'
                    
                    result_data.append({
                        '代码': row['ticker'],
                        '名称': row.get('name', 'N/A'),
                        '得分': score_display,
                        '市值': market_cap_display,
                        '筛选日期': row.get('selected_date', 'N/A'),
                        '状态': '🔍 已筛选'
                    })
                
                if result_data:
                    df = pd.DataFrame(result_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # 添加得分分布图表
                    if 'score' in candidates.columns:
                        score_values = candidates['score'].dropna()
                        if len(score_values) > 0:
                            fig = px.histogram(
                                x=score_values,
                                title=f"{name} 筛选得分分布",
                                labels={'x': '筛选得分', 'y': '标的数量'},
                                nbins=10
                            )
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(f"⚠️ {name} 筛选结果为空")
                
                st.divider()
    
    # 添加一致性检查
    if portfolio_assets:
        st.subheader("🔍 基本面分析与投资组合一致性检查")
        
        consistency_data = []
        for asset_class, name in asset_class_names.items():
            if asset_class in portfolio_assets and portfolio_assets[asset_class]:
                portfolio_tickers = [asset.get('ticker', '') for asset in portfolio_assets[asset_class]]
                candidates_attr = f"{asset_class}_candidates"
                
                if hasattr(system, candidates_attr) and not getattr(system, candidates_attr).empty:
                    candidates = getattr(system, candidates_attr)
                    fundamental_tickers = candidates['ticker'].tolist()
                    
                    # 计算重叠度
                    overlap = len(set(portfolio_tickers) & set(fundamental_tickers))
                    consistency = overlap / len(portfolio_tickers) * 100 if portfolio_tickers else 0
                    
                    consistency_data.append({
                        '资产类别': name,
                        '投资组合标的数': len(portfolio_tickers),
                        '基本面筛选数': len(fundamental_tickers),
                        '重叠数': overlap,
                        '一致性': f"{consistency:.1f}%"
                    })
        
        if consistency_data:
            consistency_df = pd.DataFrame(consistency_data)
            st.dataframe(consistency_df, use_container_width=True)
            
            # 计算总体一致性
            total_consistency = sum([row['重叠数'] for row in consistency_data]) / sum([row['投资组合标的数'] for row in consistency_data]) * 100
            
            if total_consistency >= 90:
                st.success(f"🎯 总体一致性: {total_consistency:.1f}% - 优秀")
            elif total_consistency >= 80:
                st.success(f"🎯 总体一致性: {total_consistency:.1f}% - 良好")
            elif total_consistency >= 70:
                st.warning(f"🎯 总体一致性: {total_consistency:.1f}% - 一般")
            else:
                st.error(f"🎯 总体一致性: {total_consistency:.1f}% - 需改进")

def display_technical_signals(technical_manager, portfolio_assets=None):
    """显示技术分析信号"""
    st.subheader("📈 技术分析信号")
    
    if not technical_manager:
        st.warning("⚠️ 技术分析数据不可用")
        return
    
    # 获取信号汇总
    try:
        summary = technical_manager.get_trading_summary()
        
        # 显示信号统计，使用更好的布局
        st.subheader("📊 信号统计概览")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总信号数", summary.get('total_signals', 0))
        with col2:
            buy_count = summary.get('buy_signals', 0)
            st.metric("买入信号", buy_count, delta=f"+{buy_count}", delta_color="normal")
        with col3:
            sell_count = summary.get('sell_signals', 0)
            st.metric("卖出信号", sell_count, delta=f"-{sell_count}", delta_color="inverse")
        with col4:
            watch_count = summary.get('watch_signals', 0)
            st.metric("观望信号", watch_count)
        
        # 添加信号分布饼图
        if summary.get('total_signals', 0) > 0:
            signal_data = {
                '买入': buy_count,
                '卖出': sell_count,
                '观望': watch_count
            }
            
            # 过滤掉值为0的信号类型
            signal_data = {k: v for k, v in signal_data.items() if v > 0}
            
            if signal_data:
                fig = px.pie(
                    values=list(signal_data.values()),
                    names=list(signal_data.keys()),
                    title="信号类型分布",
                    color_discrete_map={
                        '买入': '#00ff00',
                        '卖出': '#ff0000',
                        '观望': '#ffff00'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ 无法获取信号汇总：{e}")
        summary = {'total_signals': 0, 'buy_signals': 0, 'sell_signals': 0, 'watch_signals': 0}
    
    # 显示每个资产类别的技术分析结果
    st.subheader("🎯 各资产类别技术分析结果")
    
    asset_class_names = {
        'equities': '股票',
        'bonds': '债券',
        'commodities': '大宗商品',
        'golds': '黄金'
    }
    
    # 获取技术分析信号
    all_signals = technical_manager.all_signals if hasattr(technical_manager, 'all_signals') else {}
    
    # 统计各资产类别的信号分布
    asset_class_signals = {}
    
    for asset_class, name in asset_class_names.items():
        asset_name = asset_class_names.get(asset_class, asset_class)
        st.write(f"**{asset_name} 技术分析结果**")
        
        # 获取该资产类别的技术分析信号
        signals = all_signals.get(asset_class, {})
        
        if not signals:
            st.info(f"💡 {name} 暂无技术分析信号")
            st.divider()
            continue
        
        # 如果有投资组合数据，优先显示投资组合中的标的
        if portfolio_assets and asset_class in portfolio_assets:
            portfolio_tickers = [asset.get('ticker', '') for asset in portfolio_assets[asset_class]]
            filtered_signals = {ticker: signal for ticker, signal in signals.items() if ticker in portfolio_tickers}
            
            if filtered_signals:
                st.info(f"🎯 显示投资组合中的 {len(filtered_signals)} 个标的的技术分析")
                signals = filtered_signals
            else:
                st.warning(f"⚠️ 投资组合中的 {name} 标的暂无技术分析信号")
                st.divider()
                continue
        else:
            # 如果没有投资组合数据，只显示前3个信号，避免信息过载
            if len(signals) > 3:
                st.info(f"💡 显示前3个技术分析信号（共{len(signals)}个，建议生成投资组合以查看相关标的）")
                # 只取前3个信号
                signals = dict(list(signals.items())[:3])
            else:
                st.info(f"💡 显示所有 {len(signals)} 个标的的技术分析")
        
        # 为每个有信号的标的创建技术分析结果
        analysis_results = []
        
        buy_count = 0
        sell_count = 0
        watch_count = 0
        
        for ticker, signal in signals.items():
            # 统计信号数量
            signal_type = signal.get('signal', 'WATCH')
            if signal_type == 'BUY':
                buy_count += 1
            elif signal_type == 'SELL':
                sell_count += 1
            else:
                watch_count += 1
            
            # 格式化置信度显示
            confidence = signal.get('confidence', 0)
            if isinstance(confidence, (int, float)):
                if confidence >= 80:
                    confidence_display = f"🟢 {confidence:.1%}"
                elif confidence >= 60:
                    confidence_display = f"🟡 {confidence:.1%}"
                else:
                    confidence_display = f"🔴 {confidence:.1%}"
            else:
                confidence_display = 'N/A'
            
            # 格式化价格显示
            price = signal.get('price', 0)
            if isinstance(price, (int, float)) and price > 0:
                price_display = f"${price:.2f}"
            else:
                price_display = 'N/A'
            
            # 添加状态标识
            if portfolio_assets and asset_class in portfolio_assets:
                portfolio_tickers = [asset.get('ticker', '') for asset in portfolio_assets[asset_class]]
                if ticker in portfolio_tickers:
                    status = '✅ 投资组合标的'
                else:
                    status = '🔍 筛选标的'
            else:
                status = '🔍 筛选标的'
            
            analysis_results.append({
                '代码': ticker,
                '策略': signal.get('strategy', '综合技术指标'),
                '信号': signal_type,
                '置信度': confidence_display,
                '建议': signal.get('recommendation', '建议观望，一周内买入'),
                '价格': price_display,
                '状态': status
            })
        
        # 记录该资产类别的信号统计
        asset_class_signals[asset_class] = {
            'buy': buy_count,
            'sell': sell_count,
            'watch': watch_count,
            'total': len(signals)
        }
        
        if analysis_results:
            # 创建技术分析结果表格
            df = pd.DataFrame(analysis_results)
            st.dataframe(df, use_container_width=True)
            
            # 添加信号分布图表
            if buy_count > 0 or sell_count > 0 or watch_count > 0:
                signal_distribution = {
                    '买入': buy_count,
                    '卖出': sell_count,
                    '观望': watch_count
                }
                # 过滤掉值为0的信号类型
                signal_distribution = {k: v for k, v in signal_distribution.items() if v > 0}
                
                if signal_distribution:
                    fig = px.pie(
                        values=list(signal_distribution.values()),
                        names=list(signal_distribution.keys()),
                        title=f"{name} 信号分布",
                        color_discrete_map={
                            '买入': '#00ff00',
                            '卖出': '#ff0000',
                            '观望': '#ffff00'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"⚠️ {name} 暂无有效的技术分析结果")
        
        st.divider()
    
    # 添加一致性检查
    if portfolio_assets:
        st.subheader("🔍 技术分析与投资组合一致性检查")
        
        consistency_data = []
        for asset_class, name in asset_class_names.items():
            if asset_class in portfolio_assets and portfolio_assets[asset_class]:
                portfolio_tickers = [asset.get('ticker', '') for asset in portfolio_assets[asset_class]]
                
                if asset_class in all_signals:
                    technical_tickers = list(all_signals[asset_class].keys())
                    overlap = len(set(portfolio_tickers) & set(technical_tickers))
                    consistency = overlap / len(portfolio_tickers) * 100 if portfolio_tickers else 0
                    
                    consistency_data.append({
                        '资产类别': name,
                        '投资组合标的数': len(portfolio_tickers),
                        '技术分析标的数': len(technical_tickers),
                        '重叠数': overlap,
                        '一致性': f"{consistency:.1f}%"
                    })
        
        if consistency_data:
            consistency_df = pd.DataFrame(consistency_data)
            st.dataframe(consistency_df, use_container_width=True)
            
            # 计算总体一致性
            total_consistency = sum([row['重叠数'] for row in consistency_data]) / sum([row['投资组合标的数'] for row in consistency_data]) * 100
            
            if total_consistency >= 90:
                st.success(f"🎯 总体一致性: {total_consistency:.1f}% - 优秀")
            elif total_consistency >= 80:
                st.success(f"🎯 总体一致性: {total_consistency:.1f}% - 良好")
            elif total_consistency >= 70:
                st.warning(f"🎯 总体一致性: {total_consistency:.1f}% - 一般")
            else:
                st.error(f"🎯 总体一致性: {total_consistency:.1f}% - 需改进")

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
        
        # 系统状态概览
        st.subheader("📊 系统状态概览")
        
        # 检查各模块状态
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if fetch_macro_data_available:
                st.success("✅ 宏观分析模块")
            else:
                st.error("❌ 宏观分析模块")
        
        with col2:
            if fundamental_analysis_available:
                st.success("✅ 基本面分析模块")
            else:
                st.error("❌ 基本面分析模块")
        
        with col3:
            if technical_analysis_available:
                st.success("✅ 技术分析模块")
            else:
                st.error("❌ 技术分析模块")
        
        with col4:
            if hasattr(system, 'portfolio') and system.portfolio:
                st.success("✅ 投资组合已生成")
            else:
                st.info("💡 投资组合待生成")
        
        # 添加整体信息一致性检查
        if 'portfolio' in st.session_state and hasattr(system, 'asset_allocation') and system.asset_allocation:
            st.subheader("🔍 整体信息一致性检查")
            
            portfolio = st.session_state.portfolio
            portfolio_allocation = portfolio.get('allocation', {})
            
            # 检查宏观配置与投资组合配置的一致性
            macro_portfolio_consistency = []
            for asset, macro_weight in system.asset_allocation.items():
                portfolio_weight = portfolio_allocation.get(asset, 0)
                diff = abs(portfolio_weight - macro_weight)
                macro_portfolio_consistency.append(diff)
            
            avg_macro_diff = sum(macro_portfolio_consistency) / len(macro_portfolio_consistency) if macro_portfolio_consistency else 0
            
            # 检查基本面分析结果与投资组合的一致性
            fundamental_consistency = []
            if hasattr(system, 'equity_candidates') and not system.equity_candidates.empty:
                portfolio_equity_tickers = [asset.get('ticker', '') for asset in portfolio.get('assets', {}).get('equities', [])]
                fundamental_equity_tickers = system.equity_candidates['ticker'].tolist()
                equity_overlap = len(set(portfolio_equity_tickers) & set(fundamental_equity_tickers))
                equity_consistency = equity_overlap / len(portfolio_equity_tickers) * 100 if portfolio_equity_tickers else 0
                fundamental_consistency.append(equity_consistency)
            
            # 检查技术分析结果与投资组合的一致性
            technical_consistency = []
            if hasattr(system, 'technical_manager') and hasattr(system.technical_manager, 'all_signals'):
                for asset_class in ['equities', 'bonds', 'commodities', 'golds']:
                    if asset_class in portfolio.get('assets', {}) and asset_class in system.technical_manager.all_signals:
                        portfolio_tickers = [asset.get('ticker', '') for asset in portfolio['assets'][asset_class]]
                        technical_tickers = list(system.technical_manager.all_signals[asset_class].keys())
                        overlap = len(set(portfolio_tickers) & set(technical_tickers))
                        consistency = overlap / len(portfolio_tickers) * 100 if portfolio_tickers else 0
                        technical_consistency.append(consistency)
            
            avg_fundamental_consistency = sum(fundamental_consistency) / len(fundamental_consistency) if fundamental_consistency else 0
            avg_technical_consistency = sum(technical_consistency) / len(technical_consistency) if technical_consistency else 0
            
            # 显示一致性报告
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if avg_macro_diff <= 1:
                    st.success(f"📊 宏观配置一致性: {avg_macro_diff:.1f}%")
                elif avg_macro_diff <= 3:
                    st.warning(f"📊 宏观配置一致性: {avg_macro_diff:.1f}%")
                else:
                    st.error(f"📊 宏观配置一致性: {avg_macro_diff:.1f}%")
            
            with col2:
                if avg_fundamental_consistency >= 80:
                    st.success(f"🔍 基本面一致性: {avg_fundamental_consistency:.1f}%")
                elif avg_fundamental_consistency >= 60:
                    st.warning(f"🔍 基本面一致性: {avg_fundamental_consistency:.1f}%")
                else:
                    st.error(f"🔍 基本面一致性: {avg_fundamental_consistency:.1f}%")
            
            with col3:
                if avg_technical_consistency >= 80:
                    st.success(f"📈 技术面一致性: {avg_technical_consistency:.1f}%")
                elif avg_technical_consistency >= 60:
                    st.warning(f"📈 技术面一致性: {avg_technical_consistency:.1f}%")
                else:
                    st.error(f"📈 技术面一致性: {avg_technical_consistency:.1f}%")
            
            # 总体一致性评估
            overall_consistency = (avg_macro_diff + (100 - avg_fundamental_consistency) + (100 - avg_technical_consistency)) / 3
            overall_score = 100 - overall_consistency
            
            if overall_score >= 90:
                st.success(f"🎯 整体信息一致性评分: {overall_score:.1f}/100 - 优秀")
            elif overall_score >= 80:
                st.success(f"🎯 整体信息一致性评分: {overall_score:.1f}/100 - 良好")
            elif overall_score >= 70:
                st.warning(f"🎯 整体信息一致性评分: {overall_score:.1f}/100 - 一般")
            else:
                st.error(f"🎯 整体信息一致性评分: {overall_score:.1f}/100 - 需改进")
            
            st.info("💡 信息一致性检查确保各模块传达的信息保持一致，提高投资决策的准确性")
        
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
                
                # 使用更好的布局显示结果
                for analysis_type, result in analysis_results.items():
                    analysis_name = {
                        'macro': '📊 宏观分析',
                        'fundamental': '🔍 基本面分析',
                        'technical': '📈 技术分析'
                    }.get(analysis_type, analysis_type)
                    
                    if "✅" in result:
                        st.success(f"{analysis_name}: {result}")
                    elif "❌" in result:
                        st.error(f"{analysis_name}: {result}")
                    elif "⚠️" in result:
                        st.warning(f"{analysis_name}: {result}")
                    else:
                        st.info(f"{analysis_name}: {result}")
                
                # 总体状态和改进的统计
                success_count = sum(1 for result in analysis_results.values() if "✅" in result)
                total_count = len([r for r in analysis_results.values() if "⏭️" not in r])
                
                if success_count > 0:
                    st.success(f"🎉 快速分析完成！{success_count}/{total_count} 个模块成功")
                    
                    # 显示成功模块的详细信息
                    if success_count == total_count:
                        st.balloons()
                        st.success("🎊 所有模块分析成功！系统已准备就绪")
                    elif success_count >= total_count * 0.7:
                        st.info("👍 大部分模块分析成功，系统基本可用")
                    else:
                        st.warning("⚠️ 部分模块分析成功，建议检查失败模块")
                else:
                    st.warning("⚠️ 快速分析完成，但没有模块成功")
                
                # 添加后续操作建议
                if success_count > 0:
                    st.subheader("💡 后续操作建议")
                    
                    if "✅" in analysis_results.get('macro', ''):
                        st.info("📊 宏观分析已完成，可以查看资产配置建议")
                    
                    if "✅" in analysis_results.get('fundamental', ''):
                        st.info("🔍 基本面分析已完成，可以查看筛选结果")
                    
                    if "✅" in analysis_results.get('technical', ''):
                        st.info("📈 技术分析已完成，可以查看交易信号")
                    
                    if success_count >= 2:
                        st.success("🎯 建议生成投资组合，查看完整的投资建议")
        
        # 系统使用说明
        st.subheader("📖 系统使用说明")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **🔧 使用步骤：**
            1. 设置投资参数（金额、期限、风险偏好）
            2. 运行快速分析或单独运行各模块
            3. 查看分析结果和投资建议
            4. 生成投资组合
            5. 根据技术分析信号调整策略
            """)
        
        with col2:
            st.info("""
            **⚡ 快速开始：**
            - 点击"运行快速分析"按钮
            - 系统将自动运行所有可用模块
            - 完成后可查看各标签页的详细结果
            - 建议定期刷新数据保持最新状态
            """)
        
        # 添加系统信息
        st.subheader("ℹ️ 系统信息")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 当前时间", datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        with col2:
            st.metric("🔄 数据更新", "实时", help="数据将根据市场情况实时更新")
        
        with col3:
            st.metric("📊 分析频率", "15-30分钟", help="建议刷新频率")
    
    # 宏观分析标签页
    with tab2:
        st.subheader("📊 宏观环境分析")
        
        if not hasattr(system, 'macro_data') or not system.macro_data:
            st.info("💡 请先运行宏观分析")
            if st.button("🔍 运行宏观分析", type="primary"):
                with st.spinner("正在分析宏观环境..."):
                    if system.run_macro_analysis():
                        st.success("✅ 宏观分析完成")
                        st.rerun()
                    else:
                        st.error("❌ 宏观分析失败")
        else:
            # 显示宏观数据
            st.success("✅ 宏观分析已完成")
            
            # 显示关键指标
            st.subheader("🔑 关键宏观指标")
            
            # 创建指标展示
            macro_indicators = []
            for indicator, data in system.macro_data.items():
                if data and 'data' in data and not data['data'].empty:
                    latest_value = data['data']['value'].iloc[-1]
                    latest_date = data['data'].index[-1]
                    
                    # 格式化数值显示
                    if isinstance(latest_value, (int, float)):
                        if abs(latest_value) >= 1e12:
                            value_display = f"{latest_value/1e12:.2f}T"
                        elif abs(latest_value) >= 1e9:
                            value_display = f"{latest_value/1e9:.2f}B"
                        elif abs(latest_value) >= 1e6:
                            value_display = f"{latest_value/1e6:.2f}M"
                        elif abs(latest_value) >= 1e3:
                            value_display = f"{latest_value/1e3:.2f}K"
                        else:
                            value_display = f"{latest_value:.2f}"
                    else:
                        value_display = str(latest_value)
                    
                    macro_indicators.append({
                        '指标': indicator,
                        '最新值': value_display,
                        '最新日期': latest_date.strftime('%Y-%m-%d'),
                        '状态': '✅ 正常'
                    })
            
            if macro_indicators:
                df = pd.DataFrame(macro_indicators)
                st.dataframe(df, use_container_width=True)
            
            # 显示资产配置建议
            if hasattr(system, 'asset_allocation') and system.asset_allocation:
                st.subheader("📈 基于宏观环境的资产配置建议")
                
                # 创建资产配置展示
                allocation_data = []
                for asset, weight in system.asset_allocation.items():
                    asset_names = {
                        'equities': '股票',
                        'bonds_mid': '中期债券',
                        'bonds_long': '长期债券',
                        'gold': '黄金',
                        'commodities': '大宗商品'
                    }
                    
                    allocation_data.append({
                        '资产类别': asset_names.get(asset, asset),
                        '建议配置': f"{weight:.1f}%",
                        '状态': '✅ 已配置' if weight > 0 else '⏭️ 暂不配置'
                    })
                
                if allocation_data:
                    df = pd.DataFrame(allocation_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # 添加配置图表
                    fig = px.pie(
                        values=list(system.asset_allocation.values()),
                        names=[asset_names.get(asset, asset) for asset in system.asset_allocation.keys()],
                        title="宏观环境资产配置建议",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # 检查与投资组合配置的一致性
                if 'portfolio' in st.session_state:
                    st.subheader("🔍 宏观配置与投资组合配置一致性检查")
                    
                    portfolio = st.session_state.portfolio
                    portfolio_allocation = portfolio.get('allocation', {})
                    
                    consistency_data = []
                    total_diff = 0
                    
                    for asset, macro_weight in system.asset_allocation.items():
                        portfolio_weight = portfolio_allocation.get(asset, 0)
                        diff = abs(portfolio_weight - macro_weight)
                        total_diff += diff
                        
                        asset_names = {
                            'equities': '股票',
                            'bonds_mid': '中期债券',
                            'bonds_long': '长期债券',
                            'gold': '黄金',
                            'commodities': '大宗商品'
                        }
                        
                        consistency_data.append({
                            '资产类别': asset_names.get(asset, asset),
                            '宏观建议': f"{macro_weight:.1f}%",
                            '投资组合': f"{portfolio_weight:.1f}%",
                            '差异': f"{diff:.1f}%",
                            '状态': '✅ 一致' if diff <= 1 else '⚠️ 轻微差异' if diff <= 3 else '❌ 显著差异'
                        })
                    
                    if consistency_data:
                        consistency_df = pd.DataFrame(consistency_data)
                        st.dataframe(consistency_df, use_container_width=True)
                        
                        # 计算总体一致性
                        avg_diff = total_diff / len(system.asset_allocation) if system.asset_allocation else 0
                        consistency_score = max(0, 100 - avg_diff * 10)  # 差异越大，分数越低
                        
                        if consistency_score >= 90:
                            st.success(f"🎯 配置一致性评分: {consistency_score:.1f}/100 - 优秀")
                        elif consistency_score >= 80:
                            st.success(f"🎯 配置一致性评分: {consistency_score:.1f}/100 - 良好")
                        elif consistency_score >= 70:
                            st.warning(f"🎯 配置一致性评分: {consistency_score:.1f}/100 - 一般")
                        else:
                            st.error(f"🎯 配置一致性评分: {consistency_score:.1f}/100 - 需改进")
                        
                        st.info("💡 宏观配置与投资组合配置应保持一致，差异过大时建议重新生成投资组合")
                else:
                    st.info("💡 生成投资组合后可查看配置一致性")
            else:
                st.warning("⚠️ 资产配置数据不可用")
    
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
            
            # 获取投资组合数据（如果已生成）
            portfolio_assets = None
            if 'portfolio' in st.session_state:
                portfolio_assets = st.session_state.portfolio.get('assets', {})
            
            # 调用基本面结果显示函数，传递投资组合数据
            display_fundamental_results(system, portfolio_assets)
            
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
            # 获取投资组合数据（如果已生成）
            portfolio_assets = None
            if 'portfolio' in st.session_state:
                portfolio_assets = st.session_state.portfolio.get('assets', {})
            
            # 调用技术分析显示函数，传递投资组合数据
            display_technical_signals(system.technical_manager, portfolio_assets)
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
            
            # 资产配置 - 使用更好的布局和颜色
            col1, col2 = st.columns(2)
            with col1:
                st.write("**🎯 资产配置权重**")
                
                # 创建资产配置的进度条显示
                if 'equities' in portfolio['allocation']:
                    equity_weight = portfolio['allocation']['equities']
                    st.progress(equity_weight / 100)
                    st.metric("📈 股票", f"{equity_weight:.1f}%", 
                             help="包括成长股、价值股和防御性股票")
                
                # 显示债券配置（分别显示中期和长期）
                if 'bonds_mid' in portfolio['allocation'] and portfolio['allocation']['bonds_mid'] > 0:
                    st.progress(portfolio['allocation']['bonds_mid'] / 100)
                    st.metric("🏦 中期债券", f"{portfolio['allocation']['bonds_mid']:.1f}%",
                             help="2-5年期债券，提供稳定收益")
                
                if 'bonds_long' in portfolio['allocation'] and portfolio['allocation']['bonds_long'] > 0:
                    st.progress(portfolio['allocation']['bonds_long'] / 100)
                    st.metric("🏦 长期债券", f"{portfolio['allocation']['bonds_long']:.1f}%",
                             help="10年期及以上债券，提供长期收益")
                
                # 显示黄金配置
                if 'gold' in portfolio['allocation']:
                    gold_weight = portfolio['allocation']['gold']
                    st.progress(gold_weight / 100)
                    st.metric("🥇 黄金", f"{gold_weight:.1f}%",
                             help="贵金属避险资产")
                
                # 显示商品配置
                if 'commodities' in portfolio['allocation']:
                    commodity_weight = portfolio['allocation']['commodities']
                    st.progress(commodity_weight / 100)
                    st.metric("🛢️ 大宗商品", f"{commodity_weight:.1f}%",
                             help="能源、农产品等商品资产")
                
                # 验证总配置是否为100%
                total_weight = sum(portfolio['allocation'].values())
                if abs(total_weight - 100) > 0.1:
                    st.warning(f"⚠️ 配置总权重: {total_weight:.1f}% (应为100%)")
                else:
                    st.success(f"✅ 配置总权重: {total_weight:.1f}%")
            
            with col2:
                st.write("**💰 投资金额分配**")
                st.metric("💵 总投资", f"${investment_amount:,.0f}",
                         help=f"基于{investment_horizon}期限和{risk_profile}风险偏好的配置")
                
                # 计算并显示各资产类别的投资金额，使用更好的格式
                if 'equities' in portfolio['allocation']:
                    equity_amount = investment_amount * portfolio['allocation']['equities'] / 100
                    st.metric("📈 股票投资", f"${equity_amount:,.0f}",
                             delta=f"{portfolio['allocation']['equities']:.1f}%",
                             delta_color="normal")
                
                if 'bonds_mid' in portfolio['allocation'] and portfolio['allocation']['bonds_mid'] > 0:
                    bonds_mid_amount = investment_amount * portfolio['allocation']['bonds_mid'] / 100
                    st.metric("🏦 中期债券投资", f"${bonds_mid_amount:,.0f}",
                             delta=f"{portfolio['allocation']['bonds_mid']:.1f}%",
                             delta_color="normal")
                
                if 'bonds_long' in portfolio['allocation'] and portfolio['allocation']['bonds_long'] > 0:
                    bonds_long_amount = investment_amount * portfolio['allocation']['bonds_long'] / 100
                    st.metric("🏦 长期债券投资", f"${bonds_long_amount:,.0f}",
                             delta=f"{portfolio['allocation']['bonds_long']:.1f}%",
                             delta_color="normal")
                
                if 'gold' in portfolio['allocation']:
                    gold_amount = investment_amount * portfolio['allocation']['gold'] / 100
                    st.metric("🥇 黄金投资", f"${gold_amount:,.0f}",
                             delta=f"{portfolio['allocation']['gold']:.1f}%",
                             delta_color="normal")
                
                if 'commodities' in portfolio['allocation']:
                    commodity_amount = investment_amount * portfolio['allocation']['commodities'] / 100
                    st.metric("🛢️ 商品投资", f"${commodity_amount:,.0f}",
                             delta=f"{portfolio['allocation']['commodities']:.1f}%",
                             delta_color="normal")
                
                # 验证总投资金额
                calculated_total = sum([
                    investment_amount * portfolio['allocation'].get('equities', 0) / 100,
                    investment_amount * portfolio['allocation'].get('bonds_mid', 0) / 100,
                    investment_amount * portfolio['allocation'].get('bonds_long', 0) / 100,
                    investment_amount * portfolio['allocation'].get('gold', 0) / 100,
                    investment_amount * portfolio['allocation'].get('commodities', 0) / 100
                ])
                
                if abs(calculated_total - investment_amount) > 0.01:
                    st.warning(f"⚠️ 计算总投资: ${calculated_total:,.0f} (应为${investment_amount:,.0f})")
                else:
                    st.success(f"✅ 投资金额验证通过: ${calculated_total:,.0f}")
            
            # 生成图表
            metrics = calculate_portfolio_metrics(portfolio, investment_amount)
            charts = generate_portfolio_charts(portfolio, metrics)
            
            # 显示图表 - 使用更好的布局
            st.subheader("📊 投资组合可视化")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(charts['allocation'], use_container_width=True)
            
            with col2:
                st.plotly_chart(charts['risk_return'], use_container_width=True)
            
            # 投资组合指标 - 使用更好的颜色和布局
            st.subheader("📈 投资组合关键指标")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                expected_return = metrics['expected_return']
                if expected_return >= 0.08:
                    color = "normal"
                elif expected_return >= 0.05:
                    color = "off"
                else:
                    color = "inverse"
                st.metric("🎯 预期年化收益", f"{expected_return:.1%}", delta_color=color)
            
            with col2:
                volatility = metrics['volatility']
                if volatility <= 0.15:
                    color = "normal"
                elif volatility <= 0.25:
                    color = "off"
                else:
                    color = "inverse"
                st.metric("📊 年化波动率", f"{volatility:.1%}", delta_color=color)
            
            with col3:
                sharpe_ratio = metrics['sharpe_ratio']
                if sharpe_ratio >= 1.0:
                    color = "normal"
                elif sharpe_ratio >= 0.5:
                    color = "off"
                else:
                    color = "inverse"
                st.metric("⚖️ 夏普比率", f"{sharpe_ratio:.2f}", delta_color=color)
            
            with col4:
                max_drawdown = metrics['max_drawdown']
                if max_drawdown <= 0.15:
                    color = "normal"
                elif max_drawdown <= 0.25:
                    color = "off"
                else:
                    color = "inverse"
                st.metric("📉 最大回撤", f"{max_drawdown:.1%}", delta_color=color)
            
            # 详细资产列表 - 改进显示格式
            st.subheader("📋 详细资产配置")
            for asset_class, assets in portfolio['assets'].items():
                if assets:
                    asset_class_name = {
                        'equities': '📈 股票',
                        'bonds_mid': '🏦 中期债券',
                        'bonds_long': '🏦 长期债券',
                        'gold': '🥇 黄金',
                        'commodities': '🛢️ 大宗商品'
                    }.get(asset_class, asset_class)
                    
                    st.write(f"**{asset_class_name}：**")
                    asset_df = pd.DataFrame(assets)
                    
                    # 格式化金额显示
                    if 'amount' in asset_df.columns:
                        asset_df['💰 投资金额'] = asset_df['amount'].apply(
                            lambda x: f"${x:,.2f}" if isinstance(x, (int, float)) else 'N/A'
                        )
                        asset_df['⚖️ 权重'] = asset_df['weight'].apply(
                            lambda x: f"{x:.1f}%" if isinstance(x, (int, float)) else 'N/A'
                        )
                    
                    # 显示资产表格
                    st.dataframe(asset_df, use_container_width=True)
                    
                    # 显示技术分析建议
                    if 'technical_signals' in portfolio and asset_class in portfolio['technical_signals']:
                        st.write(f"**🔍 {asset_class_name}技术分析建议：**")
                        tech_signals = portfolio['technical_signals'][asset_class]
                        if tech_signals:
                            tech_df = pd.DataFrame(tech_signals)
                            # 格式化显示
                            if 'price' in tech_df.columns:
                                tech_df['💵 价格'] = tech_df['price'].apply(
                                    lambda x: f"${x:.2f}" if isinstance(x, (int, float)) and x > 0 else 'N/A'
                                )
                            if 'confidence' in tech_df.columns:
                                tech_df['🎯 置信度'] = tech_df['confidence'].apply(
                                    lambda x: f"{x:.1%}" if isinstance(x, (int, float)) else 'N/A'
                                )
                            
                            # 只显示关键列
                            display_cols = ['ticker', 'signal', 'strategy', 'confidence', 'recommendation']
                            available_cols = [col for col in display_cols if col in tech_df.columns]
                            
                            if available_cols:
                                st.dataframe(tech_df[available_cols], use_container_width=True)
                        else:
                            st.info(f"⚠️ {asset_class_name} 暂无技术分析建议")
                    
                    st.divider()
            
            # 技术分析建议汇总 - 改进显示
            if 'technical_signals' in portfolio:
                st.subheader("📈 技术分析建议汇总")
                
                all_recommendations = []
                for asset_class, signals in portfolio['technical_signals'].items():
                    for signal in signals:
                        asset_class_name = {
                            'equities': '📈 股票',
                            'bonds_mid': '🏦 中期债券',
                            'bonds_long': '🏦 长期债券',
                            'gold': '🥇 黄金',
                            'commodities': '🛢️ 大宗商品',
                            'golds': '🥇 黄金'
                        }.get(asset_class, asset_class)
                        
                        # 格式化信号显示
                        signal_icon = {
                            'BUY': '🟢',
                            'SELL': '🔴',
                            'WATCH': '🟡'
                        }.get(signal['signal'], '⚪')
                        
                        all_recommendations.append({
                            '资产类别': asset_class_name,
                            '代码': signal['ticker'],
                            '信号': f"{signal_icon} {signal['signal']}",
                            '策略': signal['strategy'],
                            '置信度': f"{signal['confidence']:.1%}",
                            '建议': signal['recommendation']
                        })
                
                if all_recommendations:
                    rec_df = pd.DataFrame(all_recommendations)
                    st.dataframe(rec_df, use_container_width=True)
                    
                    # 统计信号类型
                    signal_counts = {}
                    for rec in all_recommendations:
                        signal = rec['信号'].split(' ')[1] if ' ' in rec['信号'] else rec['信号']
                        signal_counts[signal] = signal_counts.get(signal, 0) + 1
                    
                    st.write("**📊 信号统计：**")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        buy_count = signal_counts.get('BUY', 0)
                        st.metric("🟢 买入信号", buy_count)
                    
                    with col2:
                        sell_count = signal_counts.get('SELL', 0)
                        st.metric("🔴 卖出信号", sell_count)
                    
                    with col3:
                        watch_count = signal_counts.get('WATCH', 0)
                        st.metric("🟡 观望信号", watch_count)
                else:
                    st.info("暂无技术分析建议")
            
            # 投资建议总结 - 改进显示
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
                
                col1, col2 = st.columns(2)
                with col1:
                    if buy_signals > 0:
                        st.success(f"🎯 建议买入 {buy_signals} 个标的，把握当前投资机会")
                    else:
                        st.info("💡 当前暂无强烈买入信号")
                
                with col2:
                    if watch_signals > 0:
                        st.info(f"👀 建议观望 {watch_signals} 个标的，等待更好的入场时机")
                    else:
                        st.info("💡 当前暂无观望信号")
                
                st.info("""
                **📋 投资策略建议：**
                - 📈 对于买入信号的标的，建议一周内分批建仓
                - 👀 对于观望信号的标的，建议持续关注，等待技术指标改善
                - ⚖️ 建议采用定投策略，分散投资风险
                - 📊 定期回顾投资组合，根据市场变化调整配置
                - 🎯 关注宏观环境变化，适时调整资产配置比例
                """)
            else:
                st.info("💡 建议采用均衡配置策略，定期再平衡投资组合")

if __name__ == "__main__":
    main()
