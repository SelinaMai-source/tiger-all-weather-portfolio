# tiger_all_weather_portfolio/main.py
"""
🐯 Tiger All Weather Portfolio - 全天候资产配置策略系统

基于 Ray Dalio 的全天候策略，整合：
1. 宏观面分析 - 动态调整大类资产配置
2. 基本面分析 - 筛选优质资产
3. 技术面分析 - 择时和信号生成

作者：Tiger Group
日期：2024
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 导入各个模块
try:
    from macro_analysis.macro_data import fetch_macro_data
    from macro_analysis.allocation_adjust import adjust_allocation
    from fundamental_analysis.equities.fetch_equity_data import screen_vm_candidates
    print("✅ 所有模块导入成功")
except ImportError as e:
    print(f"⚠️ 模块导入警告：{e}")
    # 设置备用函数
    def screen_vm_candidates():
        print("⚠️ 使用备用股票筛选函数")
        return pd.DataFrame()

class TigerAllWeatherPortfolio:
    """全天候资产配置策略主类"""
    
    def __init__(self):
        self.macro_data = None
        self.asset_allocation = None
        self.equity_candidates = None
        self.portfolio_status = {}
        
    def run_macro_analysis(self):
        """运行宏观分析模块"""
        print("🔍 开始宏观分析...")
        try:
            # 获取宏观数据
            self.macro_data = fetch_macro_data()
            print(f"✅ 成功获取 {len(self.macro_data)} 个宏观指标")
            
            # 计算资产配置调整
            self.asset_allocation = adjust_allocation(self.macro_data)
            print("✅ 资产配置调整完成")
            
            return True
        except Exception as e:
            print(f"❌ 宏观分析失败：{e}")
            return False
    
    def run_fundamental_analysis(self):
        """运行基本面分析模块"""
        print("📊 开始基本面分析...")
        try:
            # 筛选股票候选池
            self.equity_candidates = screen_vm_candidates()
            print(f"✅ 成功筛选 {len(self.equity_candidates)} 支股票")
            
            return True
        except Exception as e:
            print(f"❌ 基本面分析失败：{e}")
            return False
    
    def run_technical_analysis(self):
        """运行技术面分析模块"""
        print("📈 开始技术面分析...")
        try:
            # TODO: 实现技术指标计算和信号生成
            print("⚠️ 技术面分析模块待实现")
            return True
        except Exception as e:
            print(f"❌ 技术面分析失败：{e}")
            return False
    
    def generate_portfolio_recommendation(self):
        """生成投资组合建议"""
        print("🎯 生成投资组合建议...")
        
        if not self.asset_allocation or not self.equity_candidates:
            print("❌ 缺少必要数据，无法生成建议")
            return None
        
        # 计算股票配置
        equity_weight = self.asset_allocation.get('equities', 30)
        num_stocks = min(40, len(self.equity_candidates))
        
        # 选择前N支股票
        selected_stocks = self.equity_candidates.head(num_stocks)
        
        # 计算每支股票的权重
        stock_weight = equity_weight / num_stocks
        
        # 生成投资组合建议
        portfolio = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'asset_allocation': self.asset_allocation,
            'equity_selection': selected_stocks[['ticker', 'marketCap', 'priceToBook', 'trailingPE', 'momentum_6m', '来源']].to_dict('records'),
            'stock_weight': stock_weight,
            'total_stocks': num_stocks,
            'macro_indicators': {k: v['description'] for k, v in self.macro_data.items()}
        }
        
        self.portfolio_status = portfolio
        return portfolio
    
    def print_portfolio_summary(self):
        """打印投资组合摘要"""
        if not self.portfolio_status:
            print("❌ 没有可用的投资组合数据")
            return
        
        print("\n" + "="*60)
        print("🐯 Tiger All Weather Portfolio - 投资组合摘要")
        print("="*60)
        
        # 资产配置
        print(f"\n📊 资产配置建议 ({self.portfolio_status['timestamp']})")
        print("-" * 40)
        for asset, weight in self.portfolio_status['asset_allocation'].items():
            print(f"{asset:15s}: {weight:6.2f}%")
        
        # 股票选择
        print(f"\n📈 股票选择 ({self.portfolio_status['total_stocks']} 支)")
        print("-" * 80)
        print(f"{'代码':<8} {'市值(B)':<10} {'PB':<8} {'PE':<8} {'动量':<8} {'来源':<12}")
        print("-" * 80)
        
        for stock in self.portfolio_status['equity_selection'][:10]:  # 显示前10支
            market_cap_b = stock['marketCap'] / 1e9 if stock['marketCap'] else 0
            print(f"{stock['ticker']:<8} {market_cap_b:<10.1f} {stock['priceToBook']:<8.2f} "
                  f"{stock['trailingPE']:<8.1f} {stock['momentum_6m']:<8.2%} {stock['来源']:<12}")
        
        if len(self.portfolio_status['equity_selection']) > 10:
            print(f"... 还有 {len(self.portfolio_status['equity_selection']) - 10} 支股票")
        
        # 宏观指标状态
        print(f"\n🌍 宏观指标监控 ({len(self.portfolio_status['macro_indicators'])} 个)")
        print("-" * 60)
        for i, (code, desc) in enumerate(self.portfolio_status['macro_indicators'].items()):
            if i < 5:  # 只显示前5个
                print(f"{code}: {desc}")
        
        print("\n" + "="*60)
    
    def save_portfolio_report(self, filename=None):
        """保存投资组合报告"""
        if not self.portfolio_status:
            print("❌ 没有可用的投资组合数据")
            return
        
        if filename is None:
            filename = f"portfolio_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.portfolio_status, f, ensure_ascii=False, indent=2)
            print(f"✅ 投资组合报告已保存到 {filename}")
        except Exception as e:
            print(f"❌ 保存报告失败：{e}")
    
    def run_full_analysis(self):
        """运行完整分析流程"""
        print("🚀 开始全天候策略完整分析...")
        print("="*60)
        
        # 1. 宏观分析
        if not self.run_macro_analysis():
            return False
        
        # 2. 基本面分析
        if not self.run_fundamental_analysis():
            return False
        
        # 3. 技术面分析
        if not self.run_technical_analysis():
            return False
        
        # 4. 生成投资组合建议
        portfolio = self.generate_portfolio_recommendation()
        if not portfolio:
            return False
        
        # 5. 打印摘要
        self.print_portfolio_summary()
        
        # 6. 保存报告
        self.save_portfolio_report()
        
        print("✅ 全天候策略分析完成！")
        return True

def main():
    """主函数"""
    print("🐯 Tiger All Weather Portfolio System")
    print("基于 Ray Dalio 全天候策略的资产管理系统")
    print("="*60)
    
    # 创建策略实例
    strategy = TigerAllWeatherPortfolio()
    
    # 运行完整分析
    success = strategy.run_full_analysis()
    
    if success:
        print("\n🎉 策略执行成功！")
        print("💡 建议：")
        print("   1. 定期更新宏观数据和股票筛选")
        print("   2. 监控投资组合表现")
        print("   3. 根据市场变化调整配置")
    else:
        print("\n❌ 策略执行失败，请检查数据和配置")

if __name__ == "__main__":
    main()
