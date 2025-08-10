#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面测试修复后的所有模块功能
"""

import sys
import os
import traceback

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir

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

def test_macro_analysis():
    """测试宏观分析模块"""
    print("\n🔍 测试宏观分析模块...")
    
    try:
        from macro_analysis.macro_data import fetch_macro_data
        print("✅ 宏观分析模块导入成功")
        
        # 测试数据获取
        try:
            macro_data = fetch_macro_data()
            if macro_data:
                print(f"✅ 宏观数据获取成功，指标数量: {len(macro_data)}")
                return True
            else:
                print("⚠️ 宏观数据获取失败")
                return False
        except Exception as e:
            print(f"⚠️ 宏观数据获取异常: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ 宏观分析模块导入失败: {e}")
        return False

def test_fundamental_analysis():
    """测试基本面分析模块"""
    print("\n🔍 测试基本面分析模块...")
    
    try:
        from fundamental_analysis.fundamental_manager import FundamentalAnalysisManager
        print("✅ 基本面分析模块导入成功")
        
        # 创建管理器实例
        try:
            manager = FundamentalAnalysisManager()
            print("✅ 基本面分析管理器创建成功")
            
            # 测试获取选中标的
            tickers = manager.get_selected_tickers('equities')
            print(f"✅ 获取股票标的成功，数量: {len(tickers)}")
            
            return True
            
        except Exception as e:
            print(f"⚠️ 基本面分析管理器测试异常: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ 基本面分析模块导入失败: {e}")
        return False

def test_technical_analysis():
    """测试技术分析模块"""
    print("\n🔍 测试技术分析模块...")
    
    try:
        from technical_analysis.technical_signals import TechnicalAnalysisManager
        print("✅ 技术分析模块导入成功")
        
        # 创建管理器实例
        try:
            manager = TechnicalAnalysisManager()
            print("✅ 技术分析管理器创建成功")
            
            # 测试获取信号汇总
            summary = manager.get_trading_summary()
            print(f"✅ 获取信号汇总成功: {summary}")
            
            # 测试各个资产类别的分析
            print("\n📊 测试各资产类别分析...")
            
            # 股票分析
            try:
                equity_result = manager.run_equity_analysis()
                print(f"✅ 股票技术分析: {'成功' if equity_result else '未生成信号'}")
            except Exception as e:
                print(f"⚠️ 股票技术分析异常: {e}")
            
            # 债券分析
            try:
                bond_result = manager.run_bond_analysis()
                print(f"✅ 债券技术分析: {'成功' if bond_result else '未生成信号'}")
            except Exception as e:
                print(f"⚠️ 债券技术分析异常: {e}")
            
            # 大宗商品分析
            try:
                commodity_result = manager.run_commodity_analysis()
                print(f"✅ 大宗商品技术分析: {'成功' if commodity_result else '未生成信号'}")
            except Exception as e:
                print(f"⚠️ 大宗商品技术分析异常: {e}")
            
            # 黄金分析
            try:
                gold_result = manager.run_gold_analysis()
                print(f"✅ 黄金技术分析: {'成功' if gold_result else '未生成信号'}")
            except Exception as e:
                print(f"⚠️ 黄金技术分析异常: {e}")
            
            return True
            
        except Exception as e:
            print(f"⚠️ 技术分析管理器测试异常: {e}")
            traceback.print_exc()
            return False
            
    except ImportError as e:
        print(f"❌ 技术分析模块导入失败: {e}")
        return False

def test_streamlit_app():
    """测试Streamlit应用主文件"""
    print("\n🔍 测试Streamlit应用主文件...")
    
    try:
        # 测试主应用文件是否可以正常导入
        import interactive_portfolio_app
        print("✅ Streamlit应用主文件导入成功")
        
        # 检查关键类是否存在
        if hasattr(interactive_portfolio_app, 'CompletePortfolioSystem'):
            print("✅ CompletePortfolioSystem类存在")
        else:
            print("❌ CompletePortfolioSystem类不存在")
            return False
        
        # 检查主函数是否存在
        if hasattr(interactive_portfolio_app, 'main'):
            print("✅ main函数存在")
        else:
            print("❌ main函数不存在")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit应用测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始全面测试修复后的模块...")
    print("=" * 60)
    
    test_results = {}
    
    # 测试各个模块
    test_results['macro'] = test_macro_analysis()
    test_results['fundamental'] = test_fundamental_analysis()
    test_results['technical'] = test_technical_analysis()
    test_results['streamlit'] = test_streamlit_app()
    
    # 显示测试结果汇总
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    for module, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{module.upper():<15}: {status}")
    
    success_count = sum(test_results.values())
    total_count = len(test_results)
    
    print(f"\n总体结果: {success_count}/{total_count} 个模块测试通过")
    
    if success_count == total_count:
        print("🎉 所有模块测试通过！应用应该可以正常运行。")
    elif success_count > 0:
        print("⚠️ 部分模块测试通过，应用可能有限制功能。")
    else:
        print("❌ 所有模块测试失败，需要进一步检查。")
    
    return test_results

if __name__ == "__main__":
    main()
