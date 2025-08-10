# advanced_equity_factors.py
"""
高级股票因子分析模块
实现Fama-French五因子模型和Carhart四因子模型
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AdvancedEquityFactorAnalyzer:
    """高级股票因子分析器"""
    
    def __init__(self, df=None):
        """
        初始化高级因子分析器
        
        Args:
            df: 包含股票数据的DataFrame，如果为None则从文件加载
        """
        self.df = df
        if df is None:
            self.load_equity_data()
        
        # 因子权重配置
        self.factor_weights = {
            # Fama-French三因子
            'market_factor': 0.25,      # 市场因子
            'size_factor': 0.15,        # 规模因子
            'value_factor': 0.20,       # 价值因子
            
            # Carhart四因子（包含动量）
            'momentum_factor': 0.15,    # 动量因子
            
            # Fama-French五因子（新增）
            'profitability_factor': 0.15,  # 盈利能力因子
            'investment_factor': 0.10,     # 投资因子
        }
    
    def load_equity_data(self, file_path="tickers/equities_list_labeled.csv"):
        """从文件加载股票数据"""
        try:
            self.df = pd.read_csv(file_path)
            print(f"✅ 成功加载 {len(self.df)} 只股票数据")
        except FileNotFoundError:
            print(f"❌ 文件 {file_path} 不存在，请先运行股票筛选")
            self.df = pd.DataFrame()
    
    def calculate_market_factor(self):
        """计算市场因子（相对于市场基准的表现）"""
        print("🔍 计算市场因子...")
        
        # 使用SPY作为市场基准
        try:
            spy = yf.Ticker("SPY")
            spy_hist = spy.history(period="1y")
            market_return = (spy_hist['Close'].iloc[-1] - spy_hist['Close'].iloc[0]) / spy_hist['Close'].iloc[0]
            
            # 计算每只股票相对于市场的超额收益
            self.df['market_factor'] = self.df['momentum_6m'].apply(
                lambda x: (x - market_return) if x is not None else 0
            )
            
            # 标准化市场因子
            self.df['market_factor_normalized'] = (
                self.df['market_factor'] - self.df['market_factor'].mean()
            ) / self.df['market_factor'].std()
            
        except Exception as e:
            print(f"⚠️ 市场因子计算失败：{e}")
            self.df['market_factor_normalized'] = 0
    
    def calculate_size_factor(self):
        """计算规模因子（小盘股溢价）"""
        print("🔍 计算规模因子...")
        
        # 基于市值计算规模因子（小盘股得分更高）
        self.df['size_factor'] = self.df['marketCap'].apply(
            lambda x: 1 if x < 10e9 else (0.5 if x < 50e9 else 0)
        )
        
        # 标准化规模因子
        self.df['size_factor_normalized'] = (
            self.df['size_factor'] - self.df['size_factor'].mean()
        ) / self.df['size_factor'].std()
    
    def calculate_value_factor(self):
        """计算价值因子（基于PE和PB）"""
        print("🔍 计算价值因子...")
        
        # 计算价值因子（PE和PB越低越好）
        self.df['pe_factor'] = self.df['trailingPE'].apply(
            lambda x: 1 if x < 15 else (0.5 if x < 25 else 0)
        )
        
        self.df['pb_factor'] = self.df['priceToBook'].apply(
            lambda x: 1 if x < 1.5 else (0.5 if x < 3 else 0)
        )
        
        # 综合价值因子
        self.df['value_factor'] = (self.df['pe_factor'] + self.df['pb_factor']) / 2
        
        # 标准化价值因子
        self.df['value_factor_normalized'] = (
            self.df['value_factor'] - self.df['value_factor'].mean()
        ) / self.df['value_factor'].std()
    
    def calculate_momentum_factor(self):
        """计算动量因子（价格动量）"""
        print("🔍 计算动量因子...")
        
        # 基于6个月动量计算动量因子
        self.df['momentum_factor'] = self.df['momentum_6m'].apply(
            lambda x: max(0, min(1, (x + 0.3) / 0.9)) if x is not None else 0
        )
        
        # 标准化动量因子
        self.df['momentum_factor_normalized'] = (
            self.df['momentum_factor'] - self.df['momentum_factor'].mean()
        ) / self.df['momentum_factor'].std()
    
    def calculate_profitability_factor(self):
        """计算盈利能力因子（ROE、毛利率等）"""
        print("🔍 计算盈利能力因子...")
        
        # ROE因子
        self.df['roe_factor'] = self.df['returnOnEquity'].apply(
            lambda x: 1 if x is not None and x > 0.15 else (0.5 if x is not None and x > 0.08 else 0)
        )
        
        # 毛利率因子
        self.df['gross_margin_factor'] = self.df['grossMargins'].apply(
            lambda x: 1 if x is not None and x > 0.3 else (0.5 if x is not None and x > 0.15 else 0)
        )
        
        # 综合盈利能力因子
        self.df['profitability_factor'] = (self.df['roe_factor'] + self.df['gross_margin_factor']) / 2
        
        # 标准化盈利能力因子
        self.df['profitability_factor_normalized'] = (
            self.df['profitability_factor'] - self.df['profitability_factor'].mean()
        ) / self.df['profitability_factor'].std()
    
    def calculate_investment_factor(self):
        """计算投资因子（资本支出、资产增长率等）"""
        print("🔍 计算投资因子...")
        
        # 基于自由现金流计算投资因子（自由现金流为正的公司得分更高）
        self.df['fcf_factor'] = self.df['freeCashflow'].apply(
            lambda x: 1 if x is not None and x > 0 else 0
        )
        
        # 基于负债率计算投资因子（负债率低的公司得分更高）
        self.df['debt_factor'] = self.df['debtToEquity'].apply(
            lambda x: 1 if x is not None and x < 0.5 else (0.5 if x is not None and x < 1 else 0)
        )
        
        # 综合投资因子
        self.df['investment_factor'] = (self.df['fcf_factor'] + self.df['debt_factor']) / 2
        
        # 标准化投资因子
        self.df['investment_factor_normalized'] = (
            self.df['investment_factor'] - self.df['investment_factor'].mean()
        ) / self.df['investment_factor'].std()
    
    def calculate_composite_score(self):
        """计算综合得分（五因子模型）"""
        print("🎯 计算五因子综合得分...")
        
        # 计算综合得分
        self.df['composite_score'] = (
            self.df['market_factor_normalized'] * self.factor_weights['market_factor'] +
            self.df['size_factor_normalized'] * self.factor_weights['size_factor'] +
            self.df['value_factor_normalized'] * self.factor_weights['value_factor'] +
            self.df['momentum_factor_normalized'] * self.factor_weights['momentum_factor'] +
            self.df['profitability_factor_normalized'] * self.factor_weights['profitability_factor'] +
            self.df['investment_factor_normalized'] * self.factor_weights['investment_factor']
        )
        
        # 标准化综合得分
        self.df['composite_score_normalized'] = (
            self.df['composite_score'] - self.df['composite_score'].mean()
        ) / self.df['composite_score'].std()
        
        print("✅ 五因子综合得分计算完成")
    
    def generate_advanced_factor_report(self):
        """生成高级因子分析报告"""
        if self.df.empty:
            print("❌ 没有股票数据")
            return
        
        print("\n" + "="*100)
        print("📊 高级股票因子分析报告（Fama-French五因子模型）")
        print("="*100)
        
        print(f"📈 分析股票数量：{len(self.df)} 只")
        print(f"🎯 因子模型：Fama-French五因子 + Carhart动量因子")
        
        # 因子统计
        print(f"\n🏭 因子统计：")
        print("-" * 60)
        print(f"{'因子':<20} {'均值':<10} {'标准差':<10} {'最小值':<10} {'最大值':<10}")
        print("-" * 60)
        
        factors = ['market_factor_normalized', 'size_factor_normalized', 'value_factor_normalized',
                  'momentum_factor_normalized', 'profitability_factor_normalized', 'investment_factor_normalized']
        
        for factor in factors:
            if factor in self.df.columns:
                mean_val = self.df[factor].mean()
                std_val = self.df[factor].std()
                min_val = self.df[factor].min()
                max_val = self.df[factor].max()
                print(f"{factor:<20} {mean_val:<10.3f} {std_val:<10.3f} {min_val:<10.3f} {max_val:<10.3f}")
        
        # 显示顶级股票
        print(f"\n🏆 顶级股票（综合得分前10名）：")
        print("-" * 120)
        print(f"{'代码':<8} {'市值(B)':<10} {'PE':<8} {'PB':<8} {'ROE':<8} {'动量':<8} {'综合得分':<10}")
        print("-" * 120)
        
        top_stocks = self.df.nlargest(10, 'composite_score_normalized')
        for _, stock in top_stocks.iterrows():
            market_cap_b = stock['marketCap'] / 1e9 if stock['marketCap'] else 0
            pe = stock['trailingPE'] if stock['trailingPE'] else 0
            pb = stock['priceToBook'] if stock['priceToBook'] else 0
            roe = stock['returnOnEquity'] if stock['returnOnEquity'] else 0
            momentum = stock['momentum_6m'] if stock['momentum_6m'] else 0
            score = stock['composite_score_normalized']
            
            print(f"{stock['ticker']:<8} {market_cap_b:<10.1f} {pe:<8.1f} {pb:<8.2f} "
                  f"{roe:<8.1%} {momentum:<8.1%} {score:<10.3f}")
        
        print("="*100)
    
    def save_advanced_analysis(self, filename=None):
        """保存高级因子分析结果"""
        if self.df.empty:
            print("❌ 没有数据可保存")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tickers/advanced_equity_factor_analysis_{timestamp}.csv"
        
        # 确保目录存在
        import os
        os.makedirs("tickers", exist_ok=True)
        
        # 选择关键列保存
        columns_to_save = [
            'ticker', 'marketCap', 'trailingPE', 'priceToBook', 'returnOnEquity',
            'grossMargins', 'freeCashflow', 'debtToEquity', 'momentum_6m',
            'market_factor_normalized', 'size_factor_normalized', 'value_factor_normalized',
            'momentum_factor_normalized', 'profitability_factor_normalized', 
            'investment_factor_normalized', 'composite_score_normalized'
        ]
        
        # 过滤存在的列
        existing_columns = [col for col in columns_to_save if col in self.df.columns]
        self.df[existing_columns].to_csv(filename, index=False)
        
        print(f"📄 高级因子分析结果已保存：{filename}")
        return filename
    
    def get_top_stocks(self, n=25):
        """获取顶级股票"""
        if self.df.empty:
            return pd.DataFrame()
        
        return self.df.nlargest(n, 'composite_score_normalized')
    
    def run_advanced_analysis(self):
        """运行完整的高级因子分析"""
        print("🚀 开始高级股票因子分析...")
        
        if self.df.empty:
            print("❌ 没有股票数据")
            return False
        
        # 计算各个因子
        self.calculate_market_factor()
        self.calculate_size_factor()
        self.calculate_value_factor()
        self.calculate_momentum_factor()
        self.calculate_profitability_factor()
        self.calculate_investment_factor()
        
        # 计算综合得分
        self.calculate_composite_score()
        
        # 生成报告
        self.generate_advanced_factor_report()
        
        # 保存结果
        self.save_advanced_analysis()
        
        print("✅ 高级股票因子分析完成")
        return True

def run_advanced_equity_factor_analysis(df=None):
    """运行高级股票因子分析"""
    analyzer = AdvancedEquityFactorAnalyzer(df)
    return analyzer.run_advanced_analysis()

if __name__ == "__main__":
    run_advanced_equity_factor_analysis()
