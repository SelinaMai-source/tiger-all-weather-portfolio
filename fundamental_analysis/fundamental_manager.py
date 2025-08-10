# fundamental_manager.py
"""
统一基本面分析管理器
整合所有资产类别的因子分析
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 导入各个资产类别的因子分析器
try:
    from equities.equity_factors import EquityFactorAnalyzer
    from equities.advanced_equity_factors import AdvancedEquityFactorAnalyzer
    from bonds.bond_factors import BondFactorAnalyzer
    from commodities.commodity_factors import CommodityFactorAnalyzer
    from gold.gold_factors import GoldFactorAnalyzer
except ImportError as e:
    print(f"⚠️ 导入因子分析器失败：{e}")

class FundamentalAnalysisManager:
    """基本面分析管理器"""
    
    def __init__(self, use_advanced_factors=True):
        """
        初始化基本面分析管理器
        
        Args:
            use_advanced_factors: 是否使用高级因子模型，默认True
        """
        self.use_advanced_factors = use_advanced_factors
        self.equity_analyzer = None
        self.advanced_equity_analyzer = None
        self.bond_analyzer = None
        self.commodity_analyzer = None
        self.gold_analyzer = None
        self.all_selected_assets = {}
        
    def run_equity_analysis(self):
        """运行股票基本面分析"""
        print("🚀 开始股票基本面分析...")
        try:
            if self.use_advanced_factors:
                # 使用高级因子模型（Fama-French五因子）
                print("🎯 使用高级因子模型：Fama-French五因子 + Carhart动量因子")
                self.advanced_equity_analyzer = AdvancedEquityFactorAnalyzer()
                success = self.advanced_equity_analyzer.run_advanced_analysis()
                
                if success:
                    # 选择顶级股票
                    selected_stocks = self.advanced_equity_analyzer.get_top_stocks(25)
                    self.all_selected_assets['equities'] = selected_stocks
                    print(f"✅ 高级股票因子分析完成，选出 {len(selected_stocks)} 只股票")
                    return True
                else:
                    print("❌ 高级股票因子分析失败")
                    return False
            else:
                # 使用基础因子模型
                print("🎯 使用基础因子模型：价值因子 + 动量因子")
                self.equity_analyzer = EquityFactorAnalyzer()
                df = self.equity_analyzer.fetch_equity_data()
                if not df.empty:
                    self.equity_analyzer.calculate_additional_factors()
                    self.equity_analyzer.calculate_composite_score()
                    self.equity_analyzer.generate_factor_report()
                    
                    # 选择顶级股票
                    selected_stocks = self.equity_analyzer.get_top_stocks(25)
                    self.all_selected_assets['equities'] = selected_stocks
                    print(f"✅ 基础股票因子分析完成，选出 {len(selected_stocks)} 只股票")
                    return True
                else:
                    print("❌ 基础股票因子分析失败")
                    return False
                    
        except Exception as e:
            print(f"❌ 股票基本面分析失败：{e}")
            return False
    
    def run_bond_analysis(self):
        """运行债券基本面分析"""
        print("🚀 开始债券基本面分析...")
        try:
            self.bond_analyzer = BondFactorAnalyzer()
            df = self.bond_analyzer.fetch_bond_data()
            if not df.empty:
                self.bond_analyzer.calculate_bond_factors()
                self.bond_analyzer.calculate_composite_score()
                self.bond_analyzer.generate_bond_report()
                
                # 选择顶级债券
                selected_bonds = self.bond_analyzer.select_top_bonds()
                self.all_selected_assets['bonds'] = selected_bonds
                
                print(f"✅ 债券基本面分析完成，选出 {len(selected_bonds)} 只债券")
                return True
            else:
                print("❌ 债券基本面分析失败")
                return False
        except Exception as e:
            print(f"❌ 债券基本面分析失败：{e}")
            return False
    
    def run_commodity_analysis(self):
        """运行大宗商品基本面分析"""
        print("🚀 开始大宗商品基本面分析...")
        try:
            self.commodity_analyzer = CommodityFactorAnalyzer()
            df = self.commodity_analyzer.fetch_commodity_data()
            if not df.empty:
                self.commodity_analyzer.calculate_commodity_factors()
                self.commodity_analyzer.calculate_composite_score()
                self.commodity_analyzer.generate_commodity_report()
                
                # 选择顶级大宗商品
                selected_commodities = self.commodity_analyzer.select_top_commodities()
                self.all_selected_assets['commodities'] = selected_commodities
                
                print(f"✅ 大宗商品基本面分析完成，选出 {len(selected_commodities)} 个大宗商品")
                return True
            else:
                print("❌ 大宗商品基本面分析失败")
                return False
        except Exception as e:
            print(f"❌ 大宗商品基本面分析失败：{e}")
            return False
    
    def run_gold_analysis(self):
        """运行黄金基本面分析"""
        print("🚀 开始黄金基本面分析...")
        try:
            self.gold_analyzer = GoldFactorAnalyzer()
            df = self.gold_analyzer.fetch_gold_data()
            if not df.empty:
                self.gold_analyzer.calculate_gold_factors()
                self.gold_analyzer.calculate_composite_score()
                self.gold_analyzer.generate_gold_report()
                
                # 选择顶级黄金
                selected_golds = self.gold_analyzer.select_top_golds()
                self.all_selected_assets['golds'] = selected_golds
                
                print(f"✅ 黄金基本面分析完成，选出 {len(selected_golds)} 个黄金")
                return True
            else:
                print("❌ 黄金基本面分析失败")
                return False
        except Exception as e:
            print(f"❌ 黄金基本面分析失败：{e}")
            return False
    
    def run_all_analysis(self):
        """运行所有资产类别的基本面分析"""
        print("🚀 开始全资产基本面分析...")
        print("="*80)
        
        # 运行各个资产类别的分析
        equity_success = self.run_equity_analysis()
        print("-" * 40)
        
        bond_success = self.run_bond_analysis()
        print("-" * 40)
        
        commodity_success = self.run_commodity_analysis()
        print("-" * 40)
        
        gold_success = self.run_gold_analysis()
        print("-" * 40)
        
        # 生成综合报告
        self.generate_comprehensive_report()
        
        return self.all_selected_assets
    
    def generate_comprehensive_report(self):
        """生成综合基本面分析报告"""
        if not self.all_selected_assets:
            print("❌ 没有基本面分析结果")
            return
        
        print("\n" + "="*100)
        print("📊 全资产基本面分析综合报告")
        print("="*100)
        
        total_assets = sum(len(assets) for assets in self.all_selected_assets.values())
        print(f"📈 总资产数量：{total_assets} 个")
        print(f"📅 分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 按资产类别统计
        print(f"\n🏭 资产类别分布：")
        for asset_class, assets in self.all_selected_assets.items():
            print(f"   {asset_class.upper()}: {len(assets)} 个")
        
        # 显示选中的资产
        print(f"\n🎯 选中的资产详情：")
        for asset_class, assets in self.all_selected_assets.items():
            print(f"\n{asset_class.upper()} 资产：")
            print("-" * 60)
            for _, asset in assets.iterrows():
                ticker = asset['ticker']
                name = asset.get('name', 'N/A')
                score = asset.get('composite_score', 0)
                print(f"   {ticker} - {name} (得分: {score:.3f})")
        
        print("="*100)
        
        # 保存综合报告
        self.save_comprehensive_report()
    
    def save_comprehensive_report(self):
        """保存综合基本面分析报告"""
        if not self.all_selected_assets:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"tickers/comprehensive_fundamental_analysis_{timestamp}.csv"
        
        # 确保目录存在
        import os
        os.makedirs("tickers", exist_ok=True)
        
        # 合并所有资产数据
        all_data = []
        for asset_class, assets in self.all_selected_assets.items():
            for _, asset in assets.iterrows():
                row = asset.copy()
                row['asset_class'] = asset_class.upper()
                all_data.append(row)
        
        if all_data:
            df = pd.DataFrame(all_data)
            df.to_csv(filename, index=False)
            print(f"📄 综合基本面分析报告已保存：{filename}")
        
        return filename
    
    def get_selected_tickers(self, asset_class=None):
        """获取选中的标的代码"""
        if asset_class:
            if asset_class in self.all_selected_assets:
                return self.all_selected_assets[asset_class]['ticker'].tolist()
            else:
                return []
        else:
            all_tickers = []
            for assets in self.all_selected_assets.values():
                all_tickers.extend(assets['ticker'].tolist())
            return all_tickers
    
    def save_ticker_lists(self):
        """保存各个资产类别的标的列表"""
        import os
        os.makedirs("tickers", exist_ok=True)
        
        for asset_class, assets in self.all_selected_assets.items():
            filename = f"tickers/{asset_class}_list.txt"
            with open(filename, 'w') as f:
                for ticker in assets['ticker']:
                    f.write(f"{ticker}\n")
            print(f"📄 {asset_class} 标的列表已保存：{filename}")

def run_comprehensive_fundamental_analysis():
    """运行综合基本面分析"""
    manager = FundamentalAnalysisManager()
    selected_assets = manager.run_all_analysis()
    
    if selected_assets:
        manager.save_ticker_lists()
        print(f"\n🎯 基本面分析完成，共选出 {sum(len(assets) for assets in selected_assets.values())} 个资产")
        return manager
    else:
        print("❌ 基本面分析失败")
        return None

if __name__ == "__main__":
    run_comprehensive_fundamental_analysis()
