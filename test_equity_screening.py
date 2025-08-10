# test_equity_screening.py
"""
测试股票筛选功能
"""

import sys
import os
import pandas as pd
from datetime import datetime

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_stock_list_loading():
    """测试股票列表加载"""
    print("🔍 测试股票列表加载...")
    
    try:
        from fundamental_analysis.equities.equity_list import combine_slickcharts_lists
        combine_slickcharts_lists()
        print("✅ 股票列表加载成功")
        return True
    except Exception as e:
        print(f"❌ 股票列表加载失败：{e}")
        return False

def test_equity_screening():
    """测试股票筛选功能"""
    print("🔍 测试股票筛选功能...")
    
    try:
        from fundamental_analysis.equities.fetch_equity_data import screen_vm_candidates, analyze_selected_stocks
        
        # 运行筛选
        final_df = screen_vm_candidates()
        
        if not final_df.empty:
            print(f"✅ 股票筛选成功，选出 {len(final_df)} 只股票")
            
            # 分析结果
            analyze_selected_stocks(final_df)
            
            # 验证结果
            assert len(final_df) == 40, f"期望40只股票，实际{len(final_df)}只"
            assert final_df['marketCap'].min() >= 10e9, "存在市值小于10亿的股票"
            assert final_df['trailingPE'].min() > 0, "存在PE异常的股票"
            assert final_df['priceToBook'].min() > 0, "存在PB异常的股票"
            
            print("✅ 所有验证通过")
            return True
        else:
            print("❌ 筛选结果为空")
            return False
            
    except Exception as e:
        print(f"❌ 股票筛选失败：{e}")
        return False

def test_config_loading():
    """测试配置加载"""
    print("🔍 测试配置加载...")
    
    try:
        from utils.config import STOCK_SCREENING_CONFIG, BASELINE_WEIGHTS
        
        print(f"✅ 配置加载成功")
        print(f"   最小市值：${STOCK_SCREENING_CONFIG['MIN_MARKET_CAP']/1e9:.1f}B")
        print(f"   目标股票数：{STOCK_SCREENING_CONFIG['TARGET_STOCK_COUNT']}只")
        print(f"   基准权重：{BASELINE_WEIGHTS}")
        
        return True
    except Exception as e:
        print(f"❌ 配置加载失败：{e}")
        return False

def test_main_integration():
    """测试主程序集成"""
    print("🔍 测试主程序集成...")
    
    try:
        from main import TigerAllWeatherPortfolio
        
        # 创建策略实例
        strategy = TigerAllWeatherPortfolio()
        
        # 测试基本面分析
        success = strategy.run_fundamental_analysis()
        
        if success:
            print("✅ 主程序集成测试成功")
            return True
        else:
            print("❌ 主程序集成测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 主程序集成测试失败：{e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行所有测试...")
    print("="*60)
    
    tests = [
        ("配置加载", test_config_loading),
        ("股票列表加载", test_stock_list_loading),
        ("股票筛选", test_equity_screening),
        ("主程序集成", test_main_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 测试：{test_name}")
        print("-" * 40)
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
                
        except Exception as e:
            print(f"❌ {test_name} 测试异常：{e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:15s}: {status}")
    
    print(f"\n总计：{passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查相关功能")

if __name__ == "__main__":
    run_all_tests()
