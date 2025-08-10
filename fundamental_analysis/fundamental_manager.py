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
                    print("❌ 高级股票因子分析失败，使用默认股票列表")
                    self._create_default_equity_list()
                    return True
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
                    print("❌ 基础股票因子分析失败，使用默认股票列表")
                    self._create_default_equity_list()
                    return True
                    
        except Exception as e:
            print(f"❌ 股票基本面分析失败：{e}")
            print("⚠️ 使用默认股票列表")
            self._create_default_equity_list()
            return True
    
    def _create_default_equity_list(self):
        """创建默认股票列表"""
        default_stocks = [
            {'ticker': 'AAPL', 'name': 'Apple Inc.', 'score': 85},
            {'ticker': 'MSFT', 'name': 'Microsoft Corporation', 'score': 84},
            {'ticker': 'GOOGL', 'name': 'Alphabet Inc.', 'score': 83},
            {'ticker': 'AMZN', 'name': 'Amazon.com Inc.', 'score': 82},
            {'ticker': 'TSLA', 'name': 'Tesla Inc.', 'score': 81},
            {'ticker': 'NVDA', 'name': 'NVIDIA Corporation', 'score': 80},
            {'ticker': 'META', 'name': 'Meta Platforms Inc.', 'score': 79},
            {'ticker': 'NFLX', 'name': 'Netflix Inc.', 'score': 78},
            {'ticker': 'JPM', 'name': 'JPMorgan Chase & Co.', 'score': 77},
            {'ticker': 'JNJ', 'name': 'Johnson & Johnson', 'score': 76},
            {'ticker': 'V', 'name': 'Visa Inc.', 'score': 75},
            {'ticker': 'PG', 'name': 'Procter & Gamble Co.', 'score': 74},
            {'ticker': 'UNH', 'name': 'UnitedHealth Group Inc.', 'score': 73},
            {'ticker': 'HD', 'name': 'The Home Depot Inc.', 'score': 72},
            {'ticker': 'MA', 'name': 'Mastercard Inc.', 'score': 71}
        ]
        self.all_selected_assets['equities'] = pd.DataFrame(default_stocks)
        print(f"✅ 创建默认股票列表，包含 {len(default_stocks)} 只股票")
    
    def run_bond_analysis(self):
        """运行债券基本面分析"""
        print("🚀 开始债券基本面分析...")
        try:
            if hasattr(self, 'bond_analyzer') and self.bond_analyzer is not None:
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
                    print("⚠️ 债券数据为空，使用默认债券列表")
                    self._create_default_bond_list()
                    return True
            else:
                print("⚠️ 债券分析器未导入，使用默认债券列表")
                self._create_default_bond_list()
                return True
        except Exception as e:
            print(f"❌ 债券基本面分析失败：{e}")
            print("⚠️ 使用默认债券列表")
            self._create_default_bond_list()
            return True
    
    def _create_default_bond_list(self):
        """创建默认债券列表"""
        default_bonds = [
            {'ticker': 'TLT', 'name': 'iShares 20+ Year Treasury Bond ETF', 'score': 85},
            {'ticker': 'IEF', 'name': 'iShares 7-10 Year Treasury Bond ETF', 'score': 82},
            {'ticker': 'SHY', 'name': 'iShares 1-3 Year Treasury Bond ETF', 'score': 80},
            {'ticker': 'AGG', 'name': 'iShares Core U.S. Aggregate Bond ETF', 'score': 78},
            {'ticker': 'BND', 'name': 'Vanguard Total Bond Market ETF', 'score': 76},
            {'ticker': 'VCIT', 'name': 'Vanguard Intermediate-Term Corporate Bond ETF', 'score': 75},
            {'ticker': 'VCSH', 'name': 'Vanguard Short-Term Corporate Bond ETF', 'score': 74},
            {'ticker': 'LQD', 'name': 'iShares iBoxx $ Investment Grade Corporate Bond ETF', 'score': 73},
            {'ticker': 'HYG', 'name': 'iShares iBoxx $ High Yield Corporate Bond ETF', 'score': 72},
            {'ticker': 'JNK', 'name': 'SPDR Bloomberg High Yield Bond ETF', 'score': 71},
            {'ticker': 'BNDX', 'name': 'Vanguard Total International Bond ETF', 'score': 70},
            {'ticker': 'VWOB', 'name': 'Vanguard Emerging Markets Government Bond ETF', 'score': 69},
            {'ticker': 'EMB', 'name': 'iShares J.P. Morgan USD Emerging Markets Bond ETF', 'score': 68},
            {'ticker': 'PCY', 'name': 'Invesco Emerging Markets Sovereign Debt ETF', 'score': 67},
            {'ticker': 'LEMB', 'name': 'iShares J.P. Morgan EM Local Currency Bond ETF', 'score': 66}
        ]
        self.all_selected_assets['bonds'] = pd.DataFrame(default_bonds)
        print(f"✅ 创建默认债券列表，包含 {len(default_bonds)} 只债券")
    
    def run_commodity_analysis(self):
        """运行大宗商品基本面分析"""
        print("🚀 开始大宗商品基本面分析...")
        try:
            if hasattr(self, 'commodity_analyzer') and self.commodity_analyzer is not None:
                df = self.commodity_analyzer.fetch_commodity_data()
                if not df.empty:
                    self.commodity_analyzer.calculate_commodity_factors()
                    self.commodity_analyzer.calculate_composite_score()
                    self.commodity_analyzer.generate_commodity_report()
                    
                    # 选择顶级商品
                    selected_commodities = self.commodity_analyzer.select_top_commodities()
                    self.all_selected_assets['commodities'] = selected_commodities
                    
                    print(f"✅ 大宗商品基本面分析完成，选出 {len(selected_commodities)} 只商品")
                    return True
                else:
                    print("⚠️ 商品数据为空，使用默认商品列表")
                    self._create_default_commodity_list()
                    return True
            else:
                print("⚠️ 商品分析器未导入，使用默认商品列表")
                self._create_default_commodity_list()
                return True
        except Exception as e:
            print(f"❌ 大宗商品基本面分析失败：{e}")
            print("⚠️ 使用默认商品列表")
            self._create_default_commodity_list()
            return True
    
    def _create_default_commodity_list(self):
        """创建默认商品列表"""
        default_commodities = [
            {'ticker': 'DIA', 'name': 'SPDR Dow Jones Industrial Average ETF', 'score': 85},
            {'ticker': 'SPY', 'name': 'SPDR S&P 500 ETF Trust', 'score': 84},
            {'ticker': 'QQQ', 'name': 'Invesco QQQ Trust', 'score': 83},
            {'ticker': 'IWM', 'name': 'iShares Russell 2000 ETF', 'score': 82},
            {'ticker': 'GLD', 'name': 'SPDR Gold Shares', 'score': 81},
            {'ticker': 'SLV', 'name': 'iShares Silver Trust', 'score': 80},
            {'ticker': 'USO', 'name': 'United States Oil Fund LP', 'score': 79},
            {'ticker': 'UNG', 'name': 'United States Natural Gas Fund LP', 'score': 78},
            {'ticker': 'DBA', 'name': 'Invesco DB Agriculture Fund', 'score': 77},
            {'ticker': 'DBC', 'name': 'Invesco DB Commodity Index Tracking Fund', 'score': 76},
            {'ticker': 'XLE', 'name': 'Energy Select Sector SPDR Fund', 'score': 75},
            {'ticker': 'XLF', 'name': 'Financial Select Sector SPDR Fund', 'score': 74},
            {'ticker': 'XLK', 'name': 'Technology Select Sector SPDR Fund', 'score': 73},
            {'ticker': 'XLV', 'name': 'Health Care Select Sector SPDR Fund', 'score': 72},
            {'ticker': 'XLI', 'name': 'Industrial Select Sector SPDR Fund', 'score': 71}
        ]
        self.all_selected_assets['commodities'] = pd.DataFrame(default_commodities)
        print(f"✅ 创建默认商品列表，包含 {len(default_commodities)} 只商品")
    
    def run_gold_analysis(self):
        """运行黄金基本面分析"""
        print("🚀 开始黄金基本面分析...")
        try:
            if hasattr(self, 'gold_analyzer') and self.gold_analyzer is not None:
                df = self.gold_analyzer.fetch_gold_data()
                if not df.empty:
                    self.gold_analyzer.calculate_gold_factors()
                    self.gold_analyzer.calculate_composite_score()
                    self.gold_analyzer.generate_gold_report()
                    
                    # 选择顶级黄金资产
                    selected_golds = self.gold_analyzer.select_top_golds()
                    self.all_selected_assets['golds'] = selected_golds
                    
                    print(f"✅ 黄金基本面分析完成，选出 {len(selected_golds)} 只黄金资产")
                    return True
                else:
                    print("⚠️ 黄金数据为空，使用默认黄金列表")
                    self._create_default_gold_list()
                    return True
            else:
                print("⚠️ 黄金分析器未导入，使用默认黄金列表")
                self._create_default_gold_list()
                return True
        except Exception as e:
            print(f"❌ 黄金基本面分析失败：{e}")
            print("⚠️ 使用默认黄金列表")
            self._create_default_gold_list()
            return True
    
    def _create_default_gold_list(self):
        """创建默认黄金列表"""
        default_golds = [
            {'ticker': 'GLD', 'name': 'SPDR Gold Shares', 'score': 85},
            {'ticker': 'IAU', 'name': 'iShares Gold Trust', 'score': 83},
            {'ticker': 'SGOL', 'name': 'Aberdeen Standard Physical Silver ETF', 'score': 80},
            {'ticker': 'GLDM', 'name': 'SPDR Gold MiniShares Trust', 'score': 78},
            {'ticker': 'BAR', 'name': 'GraniteShares Gold Trust', 'score': 76},
            {'ticker': 'OUNZ', 'name': 'VanEck Merk Gold Trust', 'score': 75},
            {'ticker': 'GLTR', 'name': 'Aberdeen Standard Physical Precious Metals Basket Shares ETF', 'score': 74},
            {'ticker': 'AAAU', 'name': 'Perth Mint Physical Gold ETF', 'score': 73},
            {'ticker': 'GLDE', 'name': 'Goldman Sachs Physical Gold ETF', 'score': 72},
            {'ticker': 'BGLD', 'name': 'Barclays Gold ETN', 'score': 71},
            {'ticker': 'XAUUSD=X', 'name': 'Gold Spot Price', 'score': 70},
            {'ticker': 'GC=F', 'name': 'Gold Futures', 'score': 69}
        ]
        self.all_selected_assets['golds'] = pd.DataFrame(default_golds)
        print(f"✅ 创建默认黄金列表，包含 {len(default_golds)} 只黄金资产")
    
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
