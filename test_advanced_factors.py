# test_advanced_factors.py
"""
测试高级因子分析功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fundamental_analysis.equities.advanced_equity_factors import AdvancedEquityFactorAnalyzer
from fundamental_analysis.fundamental_manager import FundamentalAnalysisManager

def test_advanced_equity_factors():
    """测试高级股票因子分析"""
    print("🧪 测试高级股票因子分析...")
    
    try:
        # 创建高级因子分析器
        analyzer = AdvancedEquityFactorAnalyzer()
        
        # 运行分析
        success = analyzer.run_advanced_analysis()
        
        if success:
            print("✅ 高级因子分析测试成功")
            
            # 获取顶级股票
            top_stocks = analyzer.get_top_stocks(10)
            print(f"\n🏆 顶级股票（前10名）：")
            print("-" * 80)
            print(f"{'代码':<8} {'市值(B)':<10} {'PE':<8} {'PB':<8} {'综合得分':<10}")
            print("-" * 80)
            
            for _, stock in top_stocks.iterrows():
                market_cap_b = stock['marketCap'] / 1e9 if stock['marketCap'] else 0
                pe = stock['trailingPE'] if stock['trailingPE'] else 0
                pb = stock['priceToBook'] if stock['priceToBook'] else 0
                score = stock['composite_score_normalized']
                
                print(f"{stock['ticker']:<8} {market_cap_b:<10.1f} {pe:<8.1f} {pb:<8.2f} {score:<10.3f}")
            
            return True
        else:
            print("❌ 高级因子分析测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

def test_fundamental_manager():
    """测试基本面分析管理器"""
    print("\n🧪 测试基本面分析管理器...")
    
    try:
        # 创建管理器（使用高级因子）
        manager = FundamentalAnalysisManager(use_advanced_factors=True)
        
        # 运行股票分析
        success = manager.run_equity_analysis()
        
        if success:
            print("✅ 基本面分析管理器测试成功")
            
            # 获取选中的股票
            selected_equities = manager.all_selected_assets.get('equities', pd.DataFrame())
            print(f"📊 选中的股票数量：{len(selected_equities)}")
            
            return True
        else:
            print("❌ 基本面分析管理器测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始高级因子分析测试...")
    print("="*60)
    
    # 测试1：高级股票因子分析
    test1_success = test_advanced_equity_factors()
    
    # 测试2：基本面分析管理器
    test2_success = test_fundamental_manager()
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试结果总结：")
    print(f"   高级股票因子分析：{'✅ 通过' if test1_success else '❌ 失败'}")
    print(f"   基本面分析管理器：{'✅ 通过' if test2_success else '❌ 失败'}")
    
    if test1_success and test2_success:
        print("\n🎉 所有测试通过！高级因子分析功能正常。")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息。")

if __name__ == "__main__":
    main()
