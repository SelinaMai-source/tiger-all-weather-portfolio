#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试中期债券和长期债券分离功能
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'macro_analysis'))

from macro_analysis.allocation_adjust import adjust_allocation
from macro_analysis.macro_data import fetch_macro_data

def test_bond_separation():
    """测试债券分离功能"""
    print("🧪 测试中期债券和长期债券分离功能")
    print("=" * 50)
    
    try:
        # 获取宏观数据
        print("📊 获取宏观数据...")
        macro_data = fetch_macro_data()
        
        if macro_data:
            print(f"✅ 成功获取 {len(macro_data)} 个宏观指标")
            
            # 计算资产配置
            print("\n🔍 计算资产配置...")
            allocation = adjust_allocation(macro_data)
            
            print("\n📈 宏观分析得出的资产配置：")
            for asset, weight in allocation.items():
                print(f"  {asset}: {weight}%")
            
            # 验证债券配置
            print("\n🏦 债券配置验证：")
            if 'bonds_mid' in allocation and 'bonds_long' in allocation:
                mid_weight = allocation['bonds_mid']
                long_weight = allocation['bonds_long']
                total_bonds = mid_weight + long_weight
                
                print(f"  中期债券: {mid_weight}%")
                print(f"  长期债券: {long_weight}%")
                print(f"  债券总计: {total_bonds}%")
                
                if mid_weight > 0 and long_weight > 0:
                    print("  ✅ 中期债券和长期债券已正确分离")
                else:
                    print("  ⚠️ 中期债券或长期债券权重为0")
            else:
                print("  ❌ 缺少债券配置信息")
            
            # 验证总权重
            total_weight = sum(allocation.values())
            print(f"\n📊 总权重验证: {total_weight}%")
            if abs(total_weight - 100) < 0.1:
                print("  ✅ 总权重正确")
            else:
                print(f"  ⚠️ 总权重偏离100%: {total_weight}%")
                
        else:
            print("❌ 宏观数据获取失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bond_separation()
