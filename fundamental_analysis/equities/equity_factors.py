# equity_factors.py
"""
股票因子分析模块
包含详细的因子计算、分析和报告功能
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class EquityFactorAnalyzer:
    """股票因子分析器"""
    
    def __init__(self, df=None):
        """
        初始化因子分析器
        
        Args:
            df: 包含股票数据的DataFrame，如果为None则从文件加载
        """
        self.df = df
        if df is None:
            self.load_equity_data()
    
    def load_equity_data(self, file_path="tickers/equities_list_labeled.csv"):
        """从文件加载股票数据"""
        try:
            self.df = pd.read_csv(file_path)
            print(f"✅ 成功加载 {len(self.df)} 只股票数据")
        except FileNotFoundError:
            print(f"❌ 文件 {file_path} 不存在，请先运行股票筛选")
            self.df = pd.DataFrame()
    
    def calculate_additional_factors(self):
        """计算额外的因子"""
        if self.df.empty:
            print("❌ 没有股票数据")
            return
        
        print("🔍 计算额外因子...")
        
        # 1. 计算ROE因子
        self.df['roe_factor'] = self.df['returnOnEquity'].apply(
            lambda x: 1 if x is not None and x > 0.15 else (0.5 if x is not None and x > 0.08 else 0)
        )
        
        # 2. 计算毛利率因子
        self.df['gross_margin_factor'] = self.df['grossMargins'].apply(
            lambda x: 1 if x is not None and x > 0.3 else (0.5 if x is not None and x > 0.15 else 0)
        )
        
        # 3. 计算自由现金流因子
        self.df['fcf_factor'] = self.df['freeCashflow'].apply(
            lambda x: 1 if x is not None and x > 0 else 0
        )
        
        # 4. 计算负债率因子（越低越好）
        self.df['debt_factor'] = self.df['debtToEquity'].apply(
            lambda x: 1 if x is not None and x < 0.5 else (0.5 if x is not None and x < 1 else 0)
        )
        
        # 5. 计算市值因子（大盘股得分更高）
        self.df['market_cap_factor'] = self.df['marketCap'].apply(
            lambda x: 1 if x >= 100e9 else (0.7 if x >= 50e9 else 0.4)
        )
        
        print("✅ 额外因子计算完成")
    
    def calculate_composite_score(self):
        """计算综合得分"""
        if self.df.empty:
            return
        
        print("🎯 计算综合得分...")
        
        # 权重配置
        weights = {
            'value_score': 0.3,      # 价值因子权重
            'momentum_score': 0.25,  # 动量因子权重
            'roe_factor': 0.15,      # ROE因子权重
            'gross_margin_factor': 0.1,  # 毛利率因子权重
            'fcf_factor': 0.1,       # 自由现金流因子权重
            'debt_factor': 0.05,     # 负债率因子权重
            'market_cap_factor': 0.05  # 市值因子权重
        }
        
        # 计算综合得分
        self.df['composite_score'] = (
            self.df['value_score'] * weights['value_score'] +
            self.df['momentum_score'] * weights['momentum_score'] +
            self.df['roe_factor'] * weights['roe_factor'] +
            self.df['gross_margin_factor'] * weights['gross_margin_factor'] +
            self.df['fcf_factor'] * weights['fcf_factor'] +
            self.df['debt_factor'] * weights['debt_factor'] +
            self.df['market_cap_factor'] * weights['market_cap_factor']
        )
        
        # 按综合得分排序
        self.df = self.df.sort_values('composite_score', ascending=False).reset_index(drop=True)
        
        print("✅ 综合得分计算完成")
    
    def generate_factor_report(self):
        """生成因子分析报告"""
        if self.df.empty:
            print("❌ 没有股票数据")
            return
        
        print("\n" + "="*100)
        print("📊 股票因子分析报告")
        print("="*100)
        
        # 基础统计
        print(f"📈 分析股票数量：{len(self.df)} 只")
        print(f"💰 平均市值：${self.df['marketCap'].mean()/1e9:.1f}B")
        print(f"📊 平均PE：{self.df['trailingPE'].mean():.1f}")
        print(f"📊 平均PB：{self.df['priceToBook'].mean():.2f}")
        print(f"📈 平均动量：{self.df['momentum_6m'].mean():.1%}")
        print(f"🎯 平均综合得分：{self.df['composite_score'].mean():.3f}")
        
        # 因子分布
        print(f"\n🏭 因子分布分析：")
        print(f"   ROE > 15%: {len(self.df[self.df['roe_factor'] == 1])} 只")
        print(f"   毛利率 > 30%: {len(self.df[self.df['gross_margin_factor'] == 1])} 只")
        print(f"   自由现金流 > 0: {len(self.df[self.df['fcf_factor'] == 1])} 只")
        print(f"   负债率 < 50%: {len(self.df[self.df['debt_factor'] == 1])} 只")
        print(f"   大盘股（>100B）: {len(self.df[self.df['market_cap_factor'] == 1])} 只")
        
        # 显示前15只股票
        print(f"\n🏆 前15只股票（按综合得分排序）：")
        print("-" * 120)
        print(f"{'代码':<8} {'市值(B)':<10} {'PE':<8} {'PB':<8} {'动量':<8} {'综合得分':<10} {'ROE':<8} {'毛利率':<8}")
        print("-" * 120)
        
        for _, row in self.df.head(15).iterrows():
            market_cap_b = row['marketCap'] / 1e9
            roe_pct = f"{row['returnOnEquity']*100:.1f}%" if row['returnOnEquity'] is not None else "N/A"
            gross_margin_pct = f"{row['grossMargins']*100:.1f}%" if row['grossMargins'] is not None else "N/A"
            
            print(f"{row['ticker']:<8} {market_cap_b:<10.1f} {row['trailingPE']:<8.1f} "
                  f"{row['priceToBook']:<8.2f} {row['momentum_6m']:<8.1%} "
                  f"{row['composite_score']:<10.3f} {roe_pct:<8} {gross_margin_pct:<8}")
        
        print("="*100)
    
    def save_factor_analysis(self, filename=None):
        """保存因子分析结果"""
        if self.df.empty:
            print("❌ 没有数据可保存")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tickers/equity_factor_analysis_{timestamp}.csv"
        
        # 确保目录存在
        import os
        os.makedirs("tickers", exist_ok=True)
        
        # 保存结果
        self.df.to_csv(filename, index=False)
        print(f"📄 因子分析结果已保存：{filename}")
        
        return filename
    
    def get_top_stocks(self, n=10):
        """获取排名前N的股票"""
        if self.df.empty:
            return pd.DataFrame()
        
        return self.df.head(n)[['ticker', 'marketCap', 'trailingPE', 'priceToBook', 
                               'momentum_6m', 'composite_score', 'returnOnEquity', 'grossMargins']]
    
    def analyze_sector_distribution(self):
        """分析行业分布（简化版）"""
        if self.df.empty:
            return
        
        print(f"\n🏭 行业分布分析（基于市值）：")
        
        # 按市值分类
        large_cap = self.df[self.df['marketCap'] >= 100e9]
        mid_cap = self.df[(self.df['marketCap'] >= 10e9) & (self.df['marketCap'] < 100e9)]
        small_cap = self.df[self.df['marketCap'] < 10e9]
        
        print(f"   大盘股（>100B）：{len(large_cap)} 只，平均得分：{large_cap['composite_score'].mean():.3f}")
        print(f"   中盘股（10B-100B）：{len(mid_cap)} 只，平均得分：{mid_cap['composite_score'].mean():.3f}")
        if len(small_cap) > 0:
            print(f"   小盘股（<10B）：{len(small_cap)} 只，平均得分：{small_cap['composite_score'].mean():.3f}")

def run_factor_analysis(df=None):
    """运行完整的因子分析"""
    print("🚀 开始股票因子分析...")
    
    # 创建分析器
    analyzer = EquityFactorAnalyzer(df)
    
    if analyzer.df.empty:
        print("❌ 没有股票数据，请先运行股票筛选")
        return None
    
    # 计算额外因子
    analyzer.calculate_additional_factors()
    
    # 计算综合得分
    analyzer.calculate_composite_score()
    
    # 生成报告
    analyzer.generate_factor_report()
    
    # 分析行业分布
    analyzer.analyze_sector_distribution()
    
    # 保存结果
    filename = analyzer.save_factor_analysis()
    
    print(f"✅ 因子分析完成，结果已保存到：{filename}")
    
    return analyzer

if __name__ == "__main__":
    # 运行因子分析
    analyzer = run_factor_analysis()
    
    if analyzer:
        # 显示前10只股票
        print(f"\n🏆 最终推荐的前10只股票：")
        top_stocks = analyzer.get_top_stocks(10)
        print(top_stocks[['ticker', 'composite_score', 'marketCap', 'trailingPE', 'momentum_6m']])
