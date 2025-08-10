# gold_factors.py
"""
黄金因子分析模块
基于通胀预期、美元指数、避险需求等因子进行筛选
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class GoldFactorAnalyzer:
    """黄金因子分析器"""
    
    def __init__(self, max_positions=2, min_positions=1):
        """
        初始化黄金因子分析器
        
        Args:
            max_positions: 最大持仓数量，默认2
            min_positions: 最小持仓数量，默认1
        """
        self.max_positions = max_positions
        self.min_positions = min_positions
        self.df = None
        
        # 黄金相关ETF列表
        self.gold_etfs = {
            'GLD': 'SPDR Gold Shares',
            'IAU': 'iShares Gold Trust',
            'SGOL': 'Aberdeen Standard Physical Gold ETF',
            'GLDM': 'SPDR Gold MiniShares Trust',
            'BAR': 'GraniteShares Gold Trust',
            'OUNZ': 'VanEck Merk Gold Trust',
            'UGL': 'ProShares Ultra Gold',
            'DGL': 'Invesco DB Gold Fund'
        }
    
    def fetch_gold_data(self):
        """获取黄金数据"""
        print(f"📊 获取 {len(self.gold_etfs)} 个黄金ETF数据...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # 获取一年数据
        
        gold_data = []
        successful_fetches = 0
        
        for ticker, name in self.gold_etfs.items():
            try:
                # 获取基本信息
                gold = yf.Ticker(ticker)
                info = gold.info
                
                # 获取历史价格数据
                hist_data = gold.history(period="1y")
                
                if not hist_data.empty and len(hist_data) >= 100:
                    # 计算价格变化
                    current_price = hist_data['Close'].iloc[-1]
                    price_1y_ago = hist_data['Close'].iloc[0]
                    price_change_1y = (current_price - price_1y_ago) / price_1y_ago
                    
                    # 计算波动率
                    returns = hist_data['Close'].pct_change().dropna()
                    volatility = returns.std() * np.sqrt(252)
                    
                    # 计算动量（6个月）
                    price_6m_ago = hist_data['Close'].iloc[-126] if len(hist_data) >= 126 else price_1y_ago
                    momentum_6m = (current_price - price_6m_ago) / price_6m_ago
                    
                    # 计算夏普比率
                    risk_free_rate = 0.02
                    sharpe_ratio = (price_change_1y - risk_free_rate) / volatility if volatility > 0 else 0
                    
                    # 计算避险因子（基于波动率）
                    safe_haven_factor = self.calculate_safe_haven_factor(hist_data)
                    
                    # 计算通胀对冲因子（基于长期表现）
                    inflation_hedge_factor = self.calculate_inflation_hedge_factor(hist_data)
                    
                    gold_info = {
                        'ticker': ticker,
                        'name': name,
                        'current_price': current_price,
                        'market_cap': info.get('marketCap', 0),
                        'volume': info.get('volume', 0),
                        'price_change_1y': price_change_1y,
                        'momentum_6m': momentum_6m,
                        'volatility': volatility,
                        'sharpe_ratio': sharpe_ratio,
                        'safe_haven_factor': safe_haven_factor,
                        'inflation_hedge_factor': inflation_hedge_factor,
                        'avg_volume': hist_data['Volume'].mean(),
                        'price_high_52w': hist_data['High'].max(),
                        'price_low_52w': hist_data['Low'].min(),
                        'current_volume': hist_data['Volume'].iloc[-1]
                    }
                    
                    gold_data.append(gold_info)
                    successful_fetches += 1
                else:
                    print(f"⚠️ {ticker} 数据不足")
                    
            except Exception as e:
                print(f"⚠️ {ticker} 数据获取失败：{e}")
        
        print(f"✅ 成功获取 {successful_fetches} 个黄金ETF数据")
        
        if gold_data:
            self.df = pd.DataFrame(gold_data)
            return self.df
        else:
            print("❌ 没有获取到黄金数据")
            return pd.DataFrame()
    
    def calculate_safe_haven_factor(self, hist_data):
        """计算避险因子"""
        try:
            # 简化的避险因子计算：基于价格稳定性
            if len(hist_data) >= 90:
                recent_volatility = hist_data['Close'].iloc[-90:].pct_change().std()
                # 波动率越低，避险因子越高
                safe_haven = 1 - min(recent_volatility * 10, 1)
                return safe_haven
            else:
                return 0.5
        except:
            return 0.5
    
    def calculate_inflation_hedge_factor(self, hist_data):
        """计算通胀对冲因子"""
        try:
            # 简化的通胀对冲因子计算：基于长期价格趋势
            if len(hist_data) >= 252:
                long_term_trend = hist_data['Close'].iloc[-252:].pct_change().mean()
                # 长期趋势为正，通胀对冲因子越高
                inflation_hedge = max(min(long_term_trend * 100, 1), 0)
                return inflation_hedge
            else:
                return 0.5
        except:
            return 0.5
    
    def calculate_gold_factors(self):
        """计算黄金因子"""
        if self.df is None or self.df.empty:
            print("❌ 没有黄金数据")
            return
        
        print("🔍 计算黄金因子...")
        
        # 1. 价格动量因子（越高越好）
        self.df['momentum_factor'] = self.df['price_change_1y'].rank(ascending=False) / len(self.df)
        
        # 2. 波动率因子（越低越好）
        self.df['volatility_factor'] = (1 - self.df['volatility'].rank(ascending=True) / len(self.df))
        
        # 3. 夏普比率因子（越高越好）
        self.df['sharpe_factor'] = self.df['sharpe_ratio'].rank(ascending=False) / len(self.df)
        
        # 4. 避险因子（越高越好）
        self.df['safe_haven_factor_rank'] = self.df['safe_haven_factor'].rank(ascending=False) / len(self.df)
        
        # 5. 通胀对冲因子（越高越好）
        self.df['inflation_hedge_factor_rank'] = self.df['inflation_hedge_factor'].rank(ascending=False) / len(self.df)
        
        # 6. 流动性因子（基于成交量）
        self.df['liquidity_factor'] = self.df['avg_volume'].rank(ascending=False) / len(self.df)
        
        # 7. 价格稳定性因子（基于52周高低点比率）
        self.df['price_stability'] = 1 - ((self.df['price_high_52w'] - self.df['price_low_52w']) / self.df['current_price'])
        self.df['stability_factor'] = self.df['price_stability'].rank(ascending=False) / len(self.df)
        
        # 8. 市值因子（大盘黄金得分更高）
        self.df['market_cap_factor'] = self.df['market_cap'].rank(ascending=False) / len(self.df)
        
        print("✅ 黄金因子计算完成")
    
    def calculate_composite_score(self):
        """计算综合得分"""
        if self.df is None or self.df.empty:
            return
        
        print("🎯 计算综合得分...")
        
        # 权重配置
        weights = {
            'momentum_factor': 0.20,           # 动量权重
            'volatility_factor': 0.15,         # 波动率权重
            'sharpe_factor': 0.15,             # 夏普比率权重
            'safe_haven_factor_rank': 0.20,    # 避险因子权重
            'inflation_hedge_factor_rank': 0.15, # 通胀对冲因子权重
            'liquidity_factor': 0.10,          # 流动性权重
            'stability_factor': 0.05           # 稳定性权重
        }
        
        # 计算综合得分
        self.df['composite_score'] = (
            self.df['momentum_factor'] * weights['momentum_factor'] +
            self.df['volatility_factor'] * weights['volatility_factor'] +
            self.df['sharpe_factor'] * weights['sharpe_factor'] +
            self.df['safe_haven_factor_rank'] * weights['safe_haven_factor_rank'] +
            self.df['inflation_hedge_factor_rank'] * weights['inflation_hedge_factor_rank'] +
            self.df['liquidity_factor'] * weights['liquidity_factor'] +
            self.df['stability_factor'] * weights['stability_factor']
        )
        
        # 按综合得分排序
        self.df = self.df.sort_values('composite_score', ascending=False).reset_index(drop=True)
        
        print("✅ 综合得分计算完成")
    
    def select_top_golds(self):
        """选择顶级黄金"""
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        # 选择前N个黄金
        target_count = min(self.max_positions, len(self.df))
        selected_golds = self.df.head(target_count).copy()
        
        # 添加选择标记
        selected_golds['selected'] = True
        
        return selected_golds
    
    def generate_gold_report(self):
        """生成黄金分析报告"""
        if self.df is None or self.df.empty:
            print("❌ 没有黄金数据")
            return
        
        print("\n" + "="*100)
        print("📊 黄金因子分析报告")
        print("="*100)
        
        print(f"📈 分析黄金ETF数量：{len(self.df)} 个")
        print(f"🎯 目标选择数量：{self.min_positions}-{self.max_positions} 个")
        
        # 显示前10个黄金
        print(f"\n🏆 前10个黄金ETF（按综合得分排序）：")
        print("-" * 130)
        print(f"{'代码':<8} {'名称':<35} {'价格':<10} {'1年变化':<10} {'6月动量':<10} {'避险因子':<10} {'综合得分':<10}")
        print("-" * 130)
        
        for _, row in self.df.head(10).iterrows():
            price = f"${row['current_price']:.2f}"
            change_1y = f"{row['price_change_1y']:.1%}"
            momentum_6m = f"{row['momentum_6m']:.1%}"
            safe_haven = f"{row['safe_haven_factor']:.2f}"
            score = f"{row['composite_score']:.3f}"
            
            print(f"{row['ticker']:<8} {row['name'][:34]:<35} {price:<10} {change_1y:<10} "
                  f"{momentum_6m:<10} {safe_haven:<10} {score:<10}")
        
        print("="*100)
    
    def save_gold_analysis(self, filename=None):
        """保存黄金分析结果"""
        if self.df is None or self.df.empty:
            print("❌ 没有数据可保存")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tickers/gold_factor_analysis_{timestamp}.csv"
        
        # 确保目录存在
        import os
        os.makedirs("tickers", exist_ok=True)
        
        # 保存结果
        self.df.to_csv(filename, index=False)
        print(f"📄 黄金分析结果已保存：{filename}")
        
        return filename

def run_gold_factor_analysis():
    """运行黄金因子分析"""
    print("🚀 开始黄金因子分析...")
    
    analyzer = GoldFactorAnalyzer()
    
    # 获取数据
    df = analyzer.fetch_gold_data()
    if df.empty:
        print("❌ 无法获取黄金数据")
        return None
    
    # 计算因子
    analyzer.calculate_gold_factors()
    
    # 计算综合得分
    analyzer.calculate_composite_score()
    
    # 生成报告
    analyzer.generate_gold_report()
    
    # 选择顶级黄金
    selected_golds = analyzer.select_top_golds()
    
    if not selected_golds.empty:
        print(f"\n🎯 选中的黄金：")
        for _, gold in selected_golds.iterrows():
            print(f"   {gold['ticker']} - {gold['name']} (得分: {gold['composite_score']:.3f})")
        
        # 保存结果
        analyzer.save_gold_analysis()
        
        # 保存选中的黄金列表
        selected_file = "tickers/golds_list.txt"
        with open(selected_file, 'w') as f:
            for _, gold in selected_golds.iterrows():
                f.write(f"{gold['ticker']}\n")
        print(f"📄 选中的黄金列表已保存：{selected_file}")
    
    return analyzer

if __name__ == "__main__":
    run_gold_factor_analysis()
