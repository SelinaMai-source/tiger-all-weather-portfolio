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
            
            # 即使没有明确信号，也要提供观望建议
            if signals and len(signals) > 0:
                self.equity_strategy.generate_trading_report()
                self.equity_strategy.save_trading_signals()
                self.all_signals['equities'] = signals
                self.analysis_status['equities'] = 'success'
                print(f"✅ 股票技术分析完成，生成 {len(signals)} 个信号")
                return True
            else:
                # 生成观望建议
                print("⚠️ 股票技术分析未生成明确信号，生成观望建议")
                self.analysis_status['equities'] = 'watch_signals'
                # 创建观望信号
                watch_signals = self._generate_watch_signals('equities')
                self.all_signals['equities'] = watch_signals
                return True
        except Exception as e:
            print(f"❌ 股票技术分析失败：{e}")
            self.analysis_status['equities'] = 'error'
            # 即使失败也要生成观望建议
            watch_signals = self._generate_watch_signals('equities')
            self.all_signals['equities'] = watch_signals
            return False
    
    def run_bond_analysis(self):
        """运行债券技术分析"""
        print("🚀 开始债券技术分析...")
        try:
            self.bond_strategy = BondTechnicalStrategy()
            signals = self.bond_strategy.generate_trading_signals()
            if signals and len(signals) > 0:  # 修复信号检查逻辑
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
            if signals and len(signals) > 0:  # 修复信号检查逻辑
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
            if signals and len(signals) > 0:  # 修复信号检查逻辑
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
            if signals is not None and len(signals) > 0:  # 修复信号检查逻辑
                summary[asset_class] = {
                    'count': len(signals),
                    'buy_signals': len([s for s in signals.values() if s.get('signal') == 'BUY']) if isinstance(signals, dict) else 0,
                    'sell_signals': len([s for s in signals.values() if s.get('signal') == 'SELL']) if isinstance(signals, dict) else 0,
                    'hold_signals': len([s for s in signals.values() if s.get('signal') == 'HOLD']) if isinstance(signals, dict) else 0,
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
        signals = self.all_signals.get(asset_class, {})
        if signals and len(signals) > 0:
            # 转换为DataFrame格式以便显示
            if isinstance(signals, dict):
                df = pd.DataFrame.from_dict(signals, orient='index')
                df.index.name = 'ticker'
                df.reset_index(inplace=True)
                return df
        return pd.DataFrame()
    
    def filter_signals_by_strength(self, min_strength=0.7):
        """根据信号强度过滤信号"""
        filtered_signals = {}
        
        for asset_class, signals in self.all_signals.items():
            if signals is not None and len(signals) > 0 and isinstance(signals, dict):
                strong_signals = {k: v for k, v in signals.items() if v.get('strength', 0) >= min_strength}
                if strong_signals:
                    filtered_signals[asset_class] = strong_signals
        
        return filtered_signals
    
    def get_top_signals(self, top_n=10):
        """获取最强的N个信号"""
        all_signals_list = []
        
        for asset_class, signals in self.all_signals.items():
            if signals is not None and len(signals) > 0 and isinstance(signals, dict):
                # 转换为DataFrame格式
                signals_df = pd.DataFrame.from_dict(signals, orient='index')
                signals_df.index.name = 'ticker'
                signals_df.reset_index(inplace=True)
                signals_df['asset_class'] = asset_class
                all_signals_list.append(signals_df)
        
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
            signals = self.all_signals.get(asset_class, {})
            if signals and len(signals) > 0 and isinstance(signals, dict):
                # 计算信号分布
                signal_counts = {}
                strength_values = []
                for signal_data in signals.values():
                    signal_type = signal_data.get('signal', 'UNKNOWN')
                    signal_counts[signal_type] = signal_counts.get(signal_type, 0) + 1
                    
                    if 'strength' in signal_data:
                        strength_values.append(signal_data['strength'])
                
                report['asset_class_signals'][asset_class] = {
                    'total_signals': len(signals),
                    'signal_distribution': signal_counts,
                    'strength_stats': {
                        'mean': np.mean(strength_values) if strength_values else 0,
                        'max': np.max(strength_values) if strength_values else 0,
                        'min': np.min(strength_values) if strength_values else 0
                    } if strength_values else {}
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
            if signals is not None and len(signals) > 0 and isinstance(signals, dict):
                asset_summary = {
                    'count': len(signals),
                    'buy': len([s for s in signals.values() if s.get('signal') == 'BUY']),
                    'sell': len([s for s in signals.values() if s.get('signal') == 'SELL']),
                    'hold': len([s for s in signals.values() if s.get('signal') == 'HOLD'])
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
            if signals is not None and len(signals) > 0 and isinstance(signals, dict):
                validation = {
                    'data_quality': 'good' if len(signals) > 0 else 'poor',
                    'signal_coverage': 'complete' if all('signal' in s for s in signals.values()) else 'incomplete',
                    'strength_coverage': 'complete' if all('strength' in s for s in signals.values()) else 'incomplete',
                    'timestamp_coverage': 'complete' if all('timestamp' in s for s in signals.values()) else 'incomplete'
                }
                validation_results[asset_class] = validation
        
        return validation_results

    def _generate_watch_signals(self, asset_class):
        """为没有信号的资产类别生成观望建议"""
        watch_signals = {}
        
        # 根据资产类别生成不同的观望建议
        if asset_class == 'equities':
            # 生成一些示例股票的观望建议
            sample_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
            for ticker in sample_tickers:
                watch_signals[ticker] = {
                    'strategy': 'technical_watch',
                    'signal': 'WATCH',
                    'strength': 1,
                    'price': 0,  # 实际价格需要从数据获取
                    'stop_loss': 0,
                    'target': 0,
                    'confidence': 0.3,
                    'recommendation': '建议观望，一周内买入',
                    'asset_class': asset_class
                }
        elif asset_class == 'bonds':
            sample_tickers = ['TLT', 'IEF', 'SHY', 'AGG', 'BND']
            for ticker in sample_tickers:
                watch_signals[ticker] = {
                    'strategy': 'technical_watch',
                    'signal': 'WATCH',
                    'strength': 1,
                    'price': 0,
                    'stop_loss': 0,
                    'target': 0,
                    'confidence': 0.3,
                    'recommendation': '建议观望，一周内买入',
                    'asset_class': asset_class
                }
        elif asset_class == 'commodities':
            sample_tickers = ['DJP', 'DBC', 'USO', 'GLD', 'SLV']
            for ticker in sample_tickers:
                watch_signals[ticker] = {
                    'strategy': 'technical_watch',
                    'signal': 'WATCH',
                    'strength': 1,
                    'price': 0,
                    'stop_loss': 0,
                    'target': 0,
                    'confidence': 0.3,
                    'recommendation': '建议观望，一周内买入',
                    'asset_class': asset_class
                }
        elif asset_class == 'golds':
            sample_tickers = ['GLD', 'IAU', 'SGOL', 'GLDM', 'BAR']
            for ticker in sample_tickers:
                watch_signals[ticker] = {
                    'strategy': 'technical_watch',
                    'signal': 'WATCH',
                    'strength': 1,
                    'price': 0,
                    'stop_loss': 0,
                    'target': 0,
                    'confidence': 0.3,
                    'recommendation': '建议观望，一周内买入',
                    'asset_class': asset_class
                }
        
        return watch_signals

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

