# commodity_factors.py
"""
大宗商品因子分析模块
基于供需基本面、库存、季节性等因子进行筛选
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class CommodityFactorAnalyzer:
    """大宗商品因子分析器"""
    
    def __init__(self, max_positions=3, min_positions=2):
        """
        初始化大宗商品因子分析器
        
        Args:
            max_positions: 最大持仓数量，默认3
            min_positions: 最小持仓数量，默认2
        """
        self.max_positions = max_positions
        self.min_positions = min_positions
        self.df = None
        
        # 大宗商品ETF列表
        self.commodity_etfs = {
            'USO': 'United States Oil Fund',
            'UNG': 'United States Natural Gas Fund',
            'GLD': 'SPDR Gold Shares',
            'SLV': 'iShares Silver Trust',
            'DBC': 'Invesco DB Commodity Index Tracking Fund',
            'GSG': 'iShares S&P GSCI Commodity-Indexed Trust',
            'COMT': 'iShares Commodity Select Strategy ETF',
            'PDBC': 'Invesco Optimum Yield Diversified Commodity Strategy No K-1 ETF',
            'WEAT': 'Teucrium Wheat Fund',
            'CORN': 'Teucrium Corn Fund',
            'SOYB': 'Teucrium Soybean Fund',
            'CPER': 'United States Copper Index Fund'
        }
    
    def fetch_commodity_data(self):
        """获取大宗商品数据"""
        print(f"📊 获取 {len(self.commodity_etfs)} 个大宗商品ETF数据...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # 获取一年数据
        
        commodity_data = []
        successful_fetches = 0
        
        for ticker, name in self.commodity_etfs.items():
            try:
                # 获取基本信息
                commodity = yf.Ticker(ticker)
                info = commodity.info
                
                # 获取历史价格数据
                hist_data = commodity.history(period="1y")
                
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
                    
                    # 计算季节性因子（基于历史表现）
                    seasonal_factor = self.calculate_seasonal_factor(hist_data)
                    
                    commodity_info = {
                        'ticker': ticker,
                        'name': name,
                        'current_price': current_price,
                        'market_cap': info.get('marketCap', 0),
                        'volume': info.get('volume', 0),
                        'price_change_1y': price_change_1y,
                        'momentum_6m': momentum_6m,
                        'volatility': volatility,
                        'sharpe_ratio': sharpe_ratio,
                        'seasonal_factor': seasonal_factor,
                        'avg_volume': hist_data['Volume'].mean(),
                        'price_high_52w': hist_data['High'].max(),
                        'price_low_52w': hist_data['Low'].min(),
                        'current_volume': hist_data['Volume'].iloc[-1]
                    }
                    
                    commodity_data.append(commodity_info)
                    successful_fetches += 1
                else:
                    print(f"⚠️ {ticker} 数据不足")
                    
            except Exception as e:
                print(f"⚠️ {ticker} 数据获取失败：{e}")
        
        print(f"✅ 成功获取 {successful_fetches} 个大宗商品ETF数据")
        
        if commodity_data:
            self.df = pd.DataFrame(commodity_data)
            return self.df
        else:
            print("❌ 没有获取到大宗商品数据")
            return pd.DataFrame()
    
    def calculate_seasonal_factor(self, hist_data):
        """计算季节性因子"""
        try:
            # 简化的季节性计算：基于最近3个月的表现
            if len(hist_data) >= 90:
                recent_3m = hist_data['Close'].iloc[-90:].pct_change().mean()
                return recent_3m
            else:
                return 0
        except:
            return 0
    
    def calculate_commodity_factors(self):
        """计算大宗商品因子"""
        if self.df is None or self.df.empty:
            print("❌ 没有大宗商品数据")
            return
        
        print("🔍 计算大宗商品因子...")
        
        # 1. 价格动量因子（越高越好）
        self.df['momentum_factor'] = self.df['price_change_1y'].rank(ascending=False) / len(self.df)
        
        # 2. 波动率因子（越低越好）
        self.df['volatility_factor'] = (1 - self.df['volatility'].rank(ascending=True) / len(self.df))
        
        # 3. 夏普比率因子（越高越好）
        self.df['sharpe_factor'] = self.df['sharpe_ratio'].rank(ascending=False) / len(self.df)
        
        # 4. 季节性因子（越高越好）
        self.df['seasonal_factor_rank'] = self.df['seasonal_factor'].rank(ascending=False) / len(self.df)
        
        # 5. 流动性因子（基于成交量）
        self.df['liquidity_factor'] = self.df['avg_volume'].rank(ascending=False) / len(self.df)
        
        # 6. 价格稳定性因子（基于52周高低点比率）
        self.df['price_stability'] = 1 - ((self.df['price_high_52w'] - self.df['price_low_52w']) / self.df['current_price'])
        self.df['stability_factor'] = self.df['price_stability'].rank(ascending=False) / len(self.df)
        
        # 7. 市值因子（大盘商品得分更高）
        self.df['market_cap_factor'] = self.df['market_cap'].rank(ascending=False) / len(self.df)
        
        print("✅ 大宗商品因子计算完成")
    
    def calculate_composite_score(self):
        """计算综合得分"""
        if self.df is None or self.df.empty:
            return
        
        print("🎯 计算综合得分...")
        
        # 权重配置
        weights = {
            'momentum_factor': 0.25,      # 动量权重
            'volatility_factor': 0.15,    # 波动率权重
            'sharpe_factor': 0.20,        # 夏普比率权重
            'seasonal_factor_rank': 0.15, # 季节性权重
            'liquidity_factor': 0.10,     # 流动性权重
            'stability_factor': 0.10,     # 稳定性权重
            'market_cap_factor': 0.05     # 市值权重
        }
        
        # 计算综合得分
        self.df['composite_score'] = (
            self.df['momentum_factor'] * weights['momentum_factor'] +
            self.df['volatility_factor'] * weights['volatility_factor'] +
            self.df['sharpe_factor'] * weights['sharpe_factor'] +
            self.df['seasonal_factor_rank'] * weights['seasonal_factor_rank'] +
            self.df['liquidity_factor'] * weights['liquidity_factor'] +
            self.df['stability_factor'] * weights['stability_factor'] +
            self.df['market_cap_factor'] * weights['market_cap_factor']
        )
        
        # 按综合得分排序
        self.df = self.df.sort_values('composite_score', ascending=False).reset_index(drop=True)
        
        print("✅ 综合得分计算完成")
    
    def select_top_commodities(self):
        """选择顶级大宗商品"""
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        # 选择前N个大宗商品
        target_count = min(self.max_positions, len(self.df))
        selected_commodities = self.df.head(target_count).copy()
        
        # 添加选择标记
        selected_commodities['selected'] = True
        
        return selected_commodities
    
    def generate_commodity_report(self):
        """生成大宗商品分析报告"""
        if self.df is None or self.df.empty:
            print("❌ 没有大宗商品数据")
            return
        
        print("\n" + "="*100)
        print("📊 大宗商品因子分析报告")
        print("="*100)
        
        print(f"📈 分析大宗商品数量：{len(self.df)} 个")
        print(f"🎯 目标选择数量：{self.min_positions}-{self.max_positions} 个")
        
        # 显示前10个大宗商品
        print(f"\n🏆 前10个大宗商品（按综合得分排序）：")
        print("-" * 130)
        print(f"{'代码':<8} {'名称':<35} {'价格':<10} {'1年变化':<10} {'6月动量':<10} {'波动率':<10} {'综合得分':<10}")
        print("-" * 130)
        
        for _, row in self.df.head(10).iterrows():
            price = f"${row['current_price']:.2f}"
            change_1y = f"{row['price_change_1y']:.1%}"
            momentum_6m = f"{row['momentum_6m']:.1%}"
            volatility = f"{row['volatility']:.1%}"
            score = f"{row['composite_score']:.3f}"
            
            print(f"{row['ticker']:<8} {row['name'][:34]:<35} {price:<10} {change_1y:<10} "
                  f"{momentum_6m:<10} {volatility:<10} {score:<10}")
        
        print("="*100)
    
    def save_commodity_analysis(self, filename=None):
        """保存大宗商品分析结果"""
        if self.df is None or self.df.empty:
            print("❌ 没有数据可保存")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tickers/commodity_factor_analysis_{timestamp}.csv"
        
        # 确保目录存在
        import os
        os.makedirs("tickers", exist_ok=True)
        
        # 保存结果
        self.df.to_csv(filename, index=False)
        print(f"📄 大宗商品分析结果已保存：{filename}")
        
        return filename

def run_commodity_factor_analysis():
    """运行大宗商品因子分析"""
    print("🚀 开始大宗商品因子分析...")
    
    analyzer = CommodityFactorAnalyzer()
    
    # 获取数据
    df = analyzer.fetch_commodity_data()
    if df.empty:
        print("❌ 无法获取大宗商品数据")
        return None
    
    # 计算因子
    analyzer.calculate_commodity_factors()
    
    # 计算综合得分
    analyzer.calculate_composite_score()
    
    # 生成报告
    analyzer.generate_commodity_report()
    
    # 选择顶级大宗商品
    selected_commodities = analyzer.select_top_commodities()
    
    if not selected_commodities.empty:
        print(f"\n🎯 选中的大宗商品：")
        for _, commodity in selected_commodities.iterrows():
            print(f"   {commodity['ticker']} - {commodity['name']} (得分: {commodity['composite_score']:.3f})")
        
        # 保存结果
        analyzer.save_commodity_analysis()
        
        # 保存选中的大宗商品列表
        selected_file = "tickers/commodities_list.txt"
        with open(selected_file, 'w') as f:
            for _, commodity in selected_commodities.iterrows():
                f.write(f"{commodity['ticker']}\n")
        print(f"📄 选中的大宗商品列表已保存：{selected_file}")
    
    return analyzer

if __name__ == "__main__":
    run_commodity_factor_analysis()
