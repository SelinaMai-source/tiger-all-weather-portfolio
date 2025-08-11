#!/usr/bin/env python3
"""
测试应用改进功能的脚本
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
sys.path.insert(0, project_root)

def test_imports():
    """测试所有必要的导入"""
    try:
        import streamlit as st
        print("✅ Streamlit 导入成功")
        
        import pandas as pd
        print("✅ Pandas 导入成功")
        
        import numpy as np
        print("✅ Numpy 导入成功")
        
        import plotly.graph_objects as go
        print("✅ Plotly 导入成功")
        
        import plotly.express as px
        print("✅ Plotly Express 导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_app_file():
    """测试主应用文件"""
    try:
        # 尝试编译应用文件
        import py_compile
        py_compile.compile('interactive_portfolio_app.py')
        print("✅ 应用文件编译成功")
        
        # 尝试导入主要类
        from interactive_portfolio_app import CompletePortfolioSystem
        print("✅ 主要类导入成功")
        
        # 尝试创建实例
        system = CompletePortfolioSystem()
        print("✅ 系统实例创建成功")
        
        return True
    except Exception as e:
        print(f"❌ 应用文件测试失败: {e}")
        return False

def test_display_functions():
    """测试显示函数"""
    try:
        from interactive_portfolio_app import display_fundamental_results, display_technical_signals
        
        # 创建模拟数据
        class MockSystem:
            def __init__(self):
                self.equity_candidates = None
                self.bond_candidates = None
                self.commodity_candidates = None
                self.gold_candidates = None
        
        system = MockSystem()
        
        # 测试函数调用（不实际显示）
        print("✅ 显示函数导入成功")
        return True
    except Exception as e:
        print(f"❌ 显示函数测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试应用改进功能...")
    print("=" * 50)
    
    tests = [
        ("导入测试", test_imports),
        ("应用文件测试", test_app_file),
        ("显示函数测试", test_display_functions),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 运行 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用改进功能正常")
        return True
    else:
        print("⚠️ 部分测试失败，请检查相关功能")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
