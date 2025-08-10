# bond_factors.py
"""
债券因子分析模块
基于收益率、信用评级、久期等因子进行筛选
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class BondFactorAnalyzer:
    """债券因子分析器"""
    
    def __init__(self, max_positions=3, min_positions=2):
        """
        初始化债券因子分析器
        
        Args:
            max_positions: 最大持仓数量，默认3
            min_positions: 最小持仓数量，默认2
        """
        self.max_positions = max_positions
        self.min_positions = min_positions
        self.df = None
        
        # 债券ETF列表
        self.bond_etfs = {
            'TLT': '20+ Year Treasury Bond ETF',
            'IEF': '7-10 Year Treasury Bond ETF', 
            'SHY': '1-3 Year Treasury Bond ETF',
            'LQD': 'Investment Grade Corporate Bond ETF',
            'HYG': 'High Yield Corporate Bond ETF',
            'TIP': 'TIPS Bond ETF',
            'BND': 'Total Bond Market ETF',
            'AGG': 'Core U.S. Aggregate Bond ETF',
            'VCIT': 'Vanguard Intermediate-Term Corporate Bond ETF',
            'VCSH': 'Vanguard Short-Term Corporate Bond ETF'
        }
    
    def fetch_bond_data(self):
        """获取债券数据"""
        print(f"📊 获取 {len(self.bond_etfs)} 个债券ETF数据...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # 获取一年数据
        
        bond_data = []
        successful_fetches = 0
        
        for ticker, name in self.bond_etfs.items():
            try:
                # 获取基本信息
                bond = yf.Ticker(ticker)
                info = bond.info
                
                # 获取历史价格数据
                hist_data = bond.history(period="1y")
                
                if not hist_data.empty and len(hist_data) >= 100:
                    # 计算收益率（简化版，使用价格变化）
                    current_price = hist_data['Close'].iloc[-1]
                    price_1y_ago = hist_data['Close'].iloc[0]
                    yield_change = (current_price - price_1y_ago) / price_1y_ago
                    
                    # 计算波动率
                    returns = hist_data['Close'].pct_change().dropna()
                    volatility = returns.std() * np.sqrt(252)
                    
                    # 计算夏普比率（简化版）
                    risk_free_rate = 0.02  # 假设无风险利率2%
                    sharpe_ratio = (yield_change - risk_free_rate) / volatility if volatility > 0 else 0
                    
                    bond_info = {
                        'ticker': ticker,
                        'name': name,
                        'current_price': current_price,
                        'market_cap': info.get('marketCap', 0),
                        'volume': info.get('volume', 0),
                        'yield_change_1y': yield_change,
                        'volatility': volatility,
                        'sharpe_ratio': sharpe_ratio,
                        'avg_volume': hist_data['Volume'].mean(),
                        'price_high_52w': hist_data['High'].max(),
                        'price_low_52w': hist_data['Low'].min(),
                        'current_volume': hist_data['Volume'].iloc[-1]
                    }
                    
                    bond_data.append(bond_info)
                    successful_fetches += 1
                else:
                    print(f"⚠️ {ticker} 数据不足")
                    
            except Exception as e:
                print(f"⚠️ {ticker} 数据获取失败：{e}")
        
        print(f"✅ 成功获取 {successful_fetches} 个债券ETF数据")
        
        if bond_data:
            self.df = pd.DataFrame(bond_data)
            return self.df
        else:
            print("❌ 没有获取到债券数据")
            return pd.DataFrame()
    
    def calculate_bond_factors(self):
        """计算债券因子"""
        if self.df is None or self.df.empty:
            print("❌ 没有债券数据")
            return
        
        print("🔍 计算债券因子...")
        
        # 1. 收益率因子（越高越好）
        self.df['yield_factor'] = self.df['yield_change_1y'].rank(ascending=False) / len(self.df)
        
        # 2. 波动率因子（越低越好）
        self.df['volatility_factor'] = (1 - self.df['volatility'].rank(ascending=True) / len(self.df))
        
        # 3. 夏普比率因子（越高越好）
        self.df['sharpe_factor'] = self.df['sharpe_ratio'].rank(ascending=False) / len(self.df)
        
        # 4. 流动性因子（基于成交量）
        self.df['liquidity_factor'] = self.df['avg_volume'].rank(ascending=False) / len(self.df)
        
        # 5. 价格稳定性因子（基于52周高低点比率）
        self.df['price_stability'] = 1 - ((self.df['price_high_52w'] - self.df['price_low_52w']) / self.df['current_price'])
        self.df['stability_factor'] = self.df['price_stability'].rank(ascending=False) / len(self.df)
        
        # 6. 市值因子（大盘债券得分更高）
        self.df['market_cap_factor'] = self.df['market_cap'].rank(ascending=False) / len(self.df)
        
        print("✅ 债券因子计算完成")
    
    def calculate_composite_score(self):
        """计算综合得分"""
        if self.df is None or self.df.empty:
            return
        
        print("🎯 计算综合得分...")
        
        # 权重配置
        weights = {
            'yield_factor': 0.25,      # 收益率权重
            'volatility_factor': 0.20,  # 波动率权重
            'sharpe_factor': 0.20,      # 夏普比率权重
            'liquidity_factor': 0.15,   # 流动性权重
            'stability_factor': 0.15,   # 稳定性权重
            'market_cap_factor': 0.05   # 市值权重
        }
        
        # 计算综合得分
        self.df['composite_score'] = (
            self.df['yield_factor'] * weights['yield_factor'] +
            self.df['volatility_factor'] * weights['volatility_factor'] +
            self.df['sharpe_factor'] * weights['sharpe_factor'] +
            self.df['liquidity_factor'] * weights['liquidity_factor'] +
            self.df['stability_factor'] * weights['stability_factor'] +
            self.df['market_cap_factor'] * weights['market_cap_factor']
        )
        
        # 按综合得分排序
        self.df = self.df.sort_values('composite_score', ascending=False).reset_index(drop=True)
        
        print("✅ 综合得分计算完成")
    
    def select_top_bonds(self):
        """选择顶级债券"""
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        # 选择前N只债券
        target_count = min(self.max_positions, len(self.df))
        selected_bonds = self.df.head(target_count).copy()
        
        # 添加选择标记
        selected_bonds['selected'] = True
        
        return selected_bonds
    
    def generate_bond_report(self):
        """生成债券分析报告"""
        if self.df is None or self.df.empty:
            print("❌ 没有债券数据")
            return
        
        print("\n" + "="*100)
        print("📊 债券因子分析报告")
        print("="*100)
        
        print(f"📈 分析债券数量：{len(self.df)} 个")
        print(f"🎯 目标选择数量：{self.min_positions}-{self.max_positions} 个")
        
        # 显示前10只债券
        print(f"\n🏆 前10只债券（按综合得分排序）：")
        print("-" * 120)
        print(f"{'代码':<8} {'名称':<35} {'价格':<10} {'收益率':<10} {'波动率':<10} {'夏普比率':<10} {'综合得分':<10}")
        print("-" * 120)
        
        for _, row in self.df.head(10).iterrows():
            price = f"${row['current_price']:.2f}"
            yield_change = f"{row['yield_change_1y']:.1%}"
            volatility = f"{row['volatility']:.1%}"
            sharpe = f"{row['sharpe_ratio']:.2f}"
            score = f"{row['composite_score']:.3f}"
            
            print(f"{row['ticker']:<8} {row['name'][:34]:<35} {price:<10} {yield_change:<10} "
                  f"{volatility:<10} {sharpe:<10} {score:<10}")
        
        print("="*100)
    
    def save_bond_analysis(self, filename=None):
        """保存债券分析结果"""
        if self.df is None or self.df.empty:
            print("❌ 没有数据可保存")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tickers/bond_factor_analysis_{timestamp}.csv"
        
        # 确保目录存在
        import os
        os.makedirs("tickers", exist_ok=True)
        
        # 保存结果
        self.df.to_csv(filename, index=False)
        print(f"📄 债券分析结果已保存：{filename}")
        
        return filename

def run_bond_factor_analysis():
    """运行债券因子分析"""
    print("🚀 开始债券因子分析...")
    
    analyzer = BondFactorAnalyzer()
    
    # 获取数据
    df = analyzer.fetch_bond_data()
    if df.empty:
        print("❌ 无法获取债券数据")
        return None
    
    # 计算因子
    analyzer.calculate_bond_factors()
    
    # 计算综合得分
    analyzer.calculate_composite_score()
    
    # 生成报告
    analyzer.generate_bond_report()
    
    # 选择顶级债券
    selected_bonds = analyzer.select_top_bonds()
    
    if not selected_bonds.empty:
        print(f"\n🎯 选中的债券：")
        for _, bond in selected_bonds.iterrows():
            print(f"   {bond['ticker']} - {bond['name']} (得分: {bond['composite_score']:.3f})")
        
        # 保存结果
        analyzer.save_bond_analysis()
        
        # 保存选中的债券列表
        selected_file = "tickers/bonds_list.txt"
        with open(selected_file, 'w') as f:
            for _, bond in selected_bonds.iterrows():
                f.write(f"{bond['ticker']}\n")
        print(f"📄 选中的债券列表已保存：{selected_file}")
    
    return analyzer

if __name__ == "__main__":
    run_bond_factor_analysis()
