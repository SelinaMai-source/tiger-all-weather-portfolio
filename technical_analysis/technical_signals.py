# technical_signals.py
"""
统一技术分析信号生成模块
整合所有资产类别的技术分析策略
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 导入各个资产类别的策略
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from equities.equity_technical_strategy import EquityTechnicalStrategy
    from bonds.bond_technical_strategy import BondTechnicalStrategy
    from commodities.commodity_technical_strategy import CommodityTechnicalStrategy
    from golds.gold_technical_strategy import GoldTechnicalStrategy
    print("✅ 所有技术策略模块导入成功")
except ImportError as e:
    print(f"⚠️ 导入策略模块失败：{e}")

class TechnicalAnalysisManager:
    """技术分析管理器"""
    
    def __init__(self):
        """初始化技术分析管理器"""
        self.equity_strategy = None
        self.bond_strategy = None
        self.commodity_strategy = None
        self.gold_strategy = None
        self.all_signals = {}
        self.analysis_status = {}
        
    def run_equity_analysis(self):
        """运行股票技术分析"""
        print("🚀 开始股票技术分析...")
        try:
            self.equity_strategy = EquityTechnicalStrategy()
            signals = self.equity_strategy.generate_trading_signals()
            if signals and not signals.empty:
                self.equity_strategy.generate_trading_report()
                self.equity_strategy.save_trading_signals()
                self.all_signals['equities'] = signals
                self.analysis_status['equities'] = 'success'
                print(f"✅ 股票技术分析完成，生成 {len(signals)} 个信号")
                return True
            else:
                print("⚠️ 股票技术分析未生成信号")
                self.analysis_status['equities'] = 'no_signals'
                return False
        except Exception as e:
            print(f"❌ 股票技术分析失败：{e}")
            self.analysis_status['equities'] = 'error'
            return False
    
    def run_bond_analysis(self):
        """运行债券技术分析"""
        print("🚀 开始债券技术分析...")
        try:
            self.bond_strategy = BondTechnicalStrategy()
            signals = self.bond_strategy.generate_trading_signals()
            if signals and not signals.empty:
                self.bond_strategy.generate_trading_report()
                self.bond_strategy.save_trading_signals()
                self.all_signals['bonds'] = signals
                self.analysis_status['bonds'] = 'success'
                print(f"✅ 债券技术分析完成，生成 {len(signals)} 个信号")
                return True
            else:
                print("⚠️ 债券技术分析未生成信号")
                self.analysis_status['bonds'] = 'no_signals'
                return False
        except Exception as e:
            print(f"❌ 债券技术分析失败：{e}")
            self.analysis_status['bonds'] = 'error'
            return False
    
    def run_commodity_analysis(self):
        """运行大宗商品技术分析"""
        print("🚀 开始大宗商品技术分析...")
        try:
            self.commodity_strategy = CommodityTechnicalStrategy()
            signals = self.commodity_strategy.generate_trading_signals()
            if signals and not signals.empty:
                self.commodity_strategy.generate_trading_report()
                self.commodity_strategy.save_trading_signals()
                self.all_signals['commodities'] = signals
                self.analysis_status['commodities'] = 'success'
                print(f"✅ 大宗商品技术分析完成，生成 {len(signals)} 个信号")
                return True
            else:
                print("⚠️ 大宗商品技术分析未生成信号")
                self.analysis_status['commodities'] = 'no_signals'
                return False
        except Exception as e:
            print(f"❌ 大宗商品技术分析失败：{e}")
            self.analysis_status['commodities'] = 'error'
            return False
    
    def run_gold_analysis(self):
        """运行黄金技术分析"""
        print("🚀 开始黄金技术分析...")
        try:
            self.gold_strategy = GoldTechnicalStrategy()
            signals = self.gold_strategy.generate_trading_signals()
            if signals and not signals.empty:
                self.gold_strategy.generate_trading_report()
                self.gold_strategy.save_trading_signals()
                self.all_signals['golds'] = signals
                self.analysis_status['golds'] = 'success'
                print(f"✅ 黄金技术分析完成，生成 {len(signals)} 个信号")
                return True
            else:
                print("⚠️ 黄金技术分析未生成信号")
                self.analysis_status['golds'] = 'no_signals'
                return False
        except Exception as e:
            print(f"❌ 黄金技术分析失败：{e}")
            self.analysis_status['golds'] = 'error'
            return False
    
    def run_all_analysis(self):
        """运行所有资产类别的技术分析"""
        print("🚀 开始全面技术分析...")
        
        results = {
            'equities': self.run_equity_analysis(),
            'bonds': self.run_bond_analysis(),
            'commodities': self.run_commodity_analysis(),
            'golds': self.run_gold_analysis()
        }
        
        success_count = sum(results.values())
        total_count = len(results)
        
        print(f"✅ 技术分析完成：{success_count}/{total_count} 个资产类别成功")
        return results
    
    def get_signals_summary(self):
        """获取所有信号的汇总信息"""
        summary = {}
        
        for asset_class, signals in self.all_signals.items():
            if signals is not None and not signals.empty:
                summary[asset_class] = {
                    'count': len(signals),
                    'buy_signals': len(signals[signals['signal'] == 'BUY']) if 'signal' in signals.columns else 0,
                    'sell_signals': len(signals[signals['signal'] == 'SELL']) if 'signal' in signals.columns else 0,
                    'hold_signals': len(signals[signals['signal'] == 'HOLD']) if 'signal' in signals.columns else 0,
                    'latest_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                summary[asset_class] = {
                    'count': 0,
                    'buy_signals': 0,
                    'sell_signals': 0,
                    'hold_signals': 0,
                    'latest_update': 'N/A'
                }
        
        return summary
    
    def get_asset_class_signals(self, asset_class):
        """获取特定资产类别的信号"""
        return self.all_signals.get(asset_class, pd.DataFrame())
    
    def filter_signals_by_strength(self, min_strength=0.7):
        """根据信号强度过滤信号"""
        filtered_signals = {}
        
        for asset_class, signals in self.all_signals.items():
            if signals is not None and not signals.empty and 'strength' in signals.columns:
                strong_signals = signals[signals['strength'] >= min_strength]
                if not strong_signals.empty:
                    filtered_signals[asset_class] = strong_signals
        
        return filtered_signals
    
    def get_top_signals(self, top_n=10):
        """获取最强的N个信号"""
        all_signals_list = []
        
        for asset_class, signals in self.all_signals.items():
            if signals is not None and not signals.empty:
                signals_copy = signals.copy()
                signals_copy['asset_class'] = asset_class
                all_signals_list.append(signals_copy)
        
        if all_signals_list:
            combined_signals = pd.concat(all_signals_list, ignore_index=True)
            if 'strength' in combined_signals.columns:
                return combined_signals.nlargest(top_n, 'strength')
            else:
                return combined_signals.head(top_n)
        
        return pd.DataFrame()
    
    def generate_comprehensive_report(self):
        """生成综合技术分析报告"""
        print("📊 生成综合技术分析报告...")
        
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_status': self.analysis_status,
            'signals_summary': self.get_signals_summary(),
            'top_signals': self.get_top_signals(20),
            'asset_class_signals': {}
        }
        
        # 为每个资产类别生成详细报告
        for asset_class in ['equities', 'bonds', 'commodities', 'golds']:
            signals = self.get_asset_class_signals(asset_class)
            if not signals.empty:
                report['asset_class_signals'][asset_class] = {
                    'total_signals': len(signals),
                    'signal_distribution': signals['signal'].value_counts().to_dict() if 'signal' in signals.columns else {},
                    'strength_stats': {
                        'mean': signals['strength'].mean() if 'strength' in signals.columns else 0,
                        'max': signals['strength'].max() if 'strength' in signals.columns else 0,
                        'min': signals['strength'].min() if 'strength' in signals.columns else 0
                    } if 'strength' in signals.columns else {}
                }
        
        return report
    
    def save_comprehensive_report(self):
        """保存综合技术分析报告"""
        try:
            report = self.generate_comprehensive_report()
            
            # 创建报告目录
            report_dir = "reports/technical_analysis"
            os.makedirs(report_dir, exist_ok=True)
            
            # 保存报告
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{report_dir}/comprehensive_technical_report_{timestamp}.json"
            
            # 转换DataFrame为可序列化格式
            serializable_report = report.copy()
            if not report['top_signals'].empty:
                serializable_report['top_signals'] = report['top_signals'].to_dict('records')
            
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serializable_report, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"✅ 综合技术分析报告已保存：{filename}")
            return filename
            
        except Exception as e:
            print(f"❌ 保存综合技术分析报告失败：{e}")
            return None
    
    def get_trading_summary(self):
        """获取交易信号汇总"""
        summary = {
            'total_signals': 0,
            'buy_signals': 0,
            'sell_signals': 0,
            'hold_signals': 0,
            'asset_class_breakdown': {},
            'strongest_signals': []
        }
        
        for asset_class, signals in self.all_signals.items():
            if signals is not None and not signals.empty:
                asset_summary = {
                    'count': len(signals),
                    'buy': len(signals[signals['signal'] == 'BUY']) if 'signal' in signals.columns else 0,
                    'sell': len(signals[signals['signal'] == 'SELL']) if 'signal' in signals.columns else 0,
                    'hold': len(signals[signals['signal'] == 'HOLD']) if 'signal' in signals.columns else 0
                }
                
                summary['asset_class_breakdown'][asset_class] = asset_summary
                summary['total_signals'] += asset_summary['count']
                summary['buy_signals'] += asset_summary['buy']
                summary['sell_signals'] += asset_summary['sell']
                summary['hold_signals'] += asset_summary['hold']
        
        # 获取最强信号
        top_signals = self.get_top_signals(5)
        if not top_signals.empty:
            summary['strongest_signals'] = top_signals[['ticker', 'signal', 'strength', 'asset_class']].to_dict('records')
        
        return summary
    
    def validate_signals(self):
        """验证信号的有效性"""
        validation_results = {}
        
        for asset_class, signals in self.all_signals.items():
            if signals is not None and not signals.empty:
                validation = {
                    'data_quality': 'good' if len(signals) > 0 else 'poor',
                    'signal_coverage': 'complete' if 'signal' in signals.columns else 'incomplete',
                    'strength_coverage': 'complete' if 'strength' in signals.columns else 'incomplete',
                    'timestamp_coverage': 'complete' if 'timestamp' in signals.columns else 'incomplete'
                }
                validation_results[asset_class] = validation
        
        return validation_results

def run_comprehensive_technical_analysis():
    """运行全面的技术分析"""
    print("🚀 启动全面技术分析系统...")
    
    manager = TechnicalAnalysisManager()
    
    # 运行所有分析
    results = manager.run_all_analysis()
    
    # 生成报告
    report = manager.generate_comprehensive_report()
    
    # 保存报告
    filename = manager.save_comprehensive_report()
    
    # 打印汇总
    summary = manager.get_trading_summary()
    print(f"\n📊 技术分析汇总：")
    print(f"总信号数：{summary['total_signals']}")
    print(f"买入信号：{summary['buy_signals']}")
    print(f"卖出信号：{summary['sell_signals']}")
    print(f"持有信号：{summary['hold_signals']}")
    
    return manager, report, filename

if __name__ == "__main__":
    manager, report, filename = run_comprehensive_technical_analysis()

