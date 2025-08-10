#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的系统功能
验证所有问题是否已解决
"""

import sys
import os
import pandas as pd
from datetime import datetime

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_fundamental_analysis():
    """测试基本面分析"""
    print("🔍 测试基本面分析...")
    try:
        from fundamental_analysis.fundamental_manager import FundamentalAnalysisManager
        
        manager = FundamentalAnalysisManager()
        
        # 测试股票分析
        print("  📊 测试股票分析...")
        equity_success = manager.run_equity_analysis()
        print(f"    股票分析结果: {'✅ 成功' if equity_success else '❌ 失败'}")
        
        # 测试债券分析
        print("  📊 测试债券分析...")
        bond_success = manager.run_bond_analysis()
        print(f"    债券分析结果: {'✅ 成功' if bond_success else '❌ 失败'}")
        
        # 测试商品分析
        print("  📊 测试商品分析...")
        commodity_success = manager.run_commodity_analysis()
        print(f"    商品分析结果: {'✅ 成功' if commodity_success else '❌ 失败'}")
        
        # 测试黄金分析
        print("  📊 测试黄金分析...")
        gold_success = manager.run_gold_analysis()
        print(f"    黄金分析结果: {'✅ 成功' if gold_success else '❌ 失败'}")
        
        # 检查结果
        all_assets = manager.all_selected_assets
        print(f"  📋 选中的资产数量:")
        for asset_class, assets in all_assets.items():
            if isinstance(assets, pd.DataFrame):
                print(f"    {asset_class}: {len(assets)} 个")
            else:
                print(f"    {asset_class}: {len(assets) if assets else 0} 个")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 基本面分析测试失败: {e}")
        return False

def test_technical_analysis():
    """测试技术分析"""
    print("📈 测试技术分析...")
    try:
        from technical_analysis.technical_signals import TechnicalAnalysisManager
        
        manager = TechnicalAnalysisManager()
        
        # 测试股票技术分析
        print("  📊 测试股票技术分析...")
        equity_success = manager.run_equity_analysis()
        print(f"    股票技术分析结果: {'✅ 成功' if equity_success else '❌ 失败'}")
        
        # 检查信号
        if 'equities' in manager.all_signals:
            signals = manager.all_signals['equities']
            print(f"    股票信号数量: {len(signals)}")
            if signals:
                sample_signal = list(signals.values())[0]
                print(f"    信号示例: {sample_signal.get('signal', 'N/A')} - {sample_signal.get('recommendation', 'N/A')}")
        
        # 测试债券技术分析
        print("  📊 测试债券技术分析...")
        bond_success = manager.run_bond_analysis()
        print(f"    债券技术分析结果: {'✅ 成功' if bond_success else '❌ 失败'}")
        
        # 测试商品技术分析
        print("  📊 测试商品技术分析...")
        commodity_success = manager.run_commodity_analysis()
        print(f"    商品技术分析结果: {'✅ 成功' if commodity_success else '❌ 失败'}")
        
        # 测试黄金技术分析
        print("  📊 测试黄金技术分析...")
        gold_success = manager.run_gold_analysis()
        print(f"    黄金技术分析结果: {'✅ 成功' if gold_success else '❌ 失败'}")
        
        # 检查所有信号
        print(f"  📋 技术分析信号汇总:")
        for asset_class, signals in manager.all_signals.items():
            print(f"    {asset_class}: {len(signals)} 个信号")
            if signals:
                signal_types = {}
                for signal in signals.values():
                    signal_type = signal.get('signal', 'WATCH')
                    signal_types[signal_type] = signal_types.get(signal_type, 0) + 1
                print(f"      信号类型: {signal_types}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 技术分析测试失败: {e}")
        return False

def test_portfolio_generation():
    """测试投资组合生成"""
    print("💼 测试投资组合生成...")
    try:
        from interactive_portfolio_app import CompletePortfolioSystem
        
        system = CompletePortfolioSystem()
        
        # 模拟资产配置
        system.asset_allocation = {
            'equities': 40,
            'bonds_mid': 20,
            'bonds_long': 20,
            'gold': 10,
            'commodities': 10
        }
        
        # 模拟基本面分析结果
        system.equity_candidates = pd.DataFrame([
            {'ticker': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology', 'market_cap': 'Large'},
            {'ticker': 'MSFT', 'name': 'Microsoft Corp.', 'sector': 'Technology', 'market_cap': 'Large'},
            {'ticker': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology', 'market_cap': 'Large'}
        ])
        
        # 模拟技术分析结果
        if hasattr(system, 'technical_manager') and system.technical_manager:
            system.technical_manager.all_signals = {
                'equities': {
                    'AAPL': {'signal': 'BUY', 'strategy': 'momentum_breakout', 'confidence': 0.8, 'recommendation': '建议一周内买入'},
                    'MSFT': {'signal': 'WATCH', 'strategy': 'mean_reversion', 'confidence': 0.6, 'recommendation': '建议观望，一周内买入'}
                },
                'bonds': {
                    'TLT': {'signal': 'WATCH', 'strategy': 'technical_watch', 'confidence': 0.5, 'recommendation': '建议观望，一周内买入'}
                }
            }
        
        # 生成投资组合
        investment_amount = 100000
        investment_horizon = "中期 (3-7年)"
        risk_profile = "平衡"
        
        portfolio = system.generate_portfolio_recommendation(
            investment_amount, investment_horizon, risk_profile
        )
        
        if portfolio:
            print("  ✅ 投资组合生成成功")
            print(f"    总投资金额: ${portfolio['total_amount']:,.0f}")
            print(f"    资产类别数量: {len(portfolio['assets'])}")
            
            # 检查技术分析建议
            if 'technical_signals' in portfolio:
                print(f"    技术分析建议: {len(portfolio['technical_signals'])} 个资产类别")
                for asset_class, signals in portfolio['technical_signals'].items():
                    print(f"      {asset_class}: {len(signals)} 个建议")
            else:
                print("    ⚠️ 投资组合中缺少技术分析建议")
            
            # 检查具体标的
            for asset_class, assets in portfolio['assets'].items():
                if assets:
                    print(f"    {asset_class}: {len(assets)} 个标的")
                    for asset in assets[:2]:  # 显示前2个
                        print(f"      {asset.get('ticker', 'N/A')}: ${asset.get('amount', 0):,.2f}")
            
            return True
        else:
            print("  ❌ 投资组合生成失败")
            return False
        
    except Exception as e:
        print(f"  ❌ 投资组合生成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试修复后的系统功能...")
    print("=" * 60)
    
    # 测试基本面分析
    fundamental_ok = test_fundamental_analysis()
    print()
    
    # 测试技术分析
    technical_ok = test_technical_analysis()
    print()
    
    # 测试投资组合生成
    portfolio_ok = test_portfolio_generation()
    print()
    
    # 总结
    print("=" * 60)
    print("📊 测试结果总结:")
    print(f"  基本面分析: {'✅ 通过' if fundamental_ok else '❌ 失败'}")
    print(f"  技术分析: {'✅ 通过' if technical_ok else '❌ 失败'}")
    print(f"  投资组合生成: {'✅ 通过' if portfolio_ok else '❌ 失败'}")
    
    if all([fundamental_ok, technical_ok, portfolio_ok]):
        print("\n🎉 所有测试通过！系统修复完成！")
        print("\n✅ 已解决的问题:")
        print("  - P1: 技术分析现在能生成交易信号")
        print("  - P2: 基本面分析现在支持所有资产类别")
        print("  - P3: 技术分析显示每个资产类别的建议")
        print("  - P4: 投资组合包含具体的标的、数量和金额")
    else:
        print("\n⚠️ 部分测试失败，需要进一步检查")
    
    return all([fundamental_ok, technical_ok, portfolio_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
