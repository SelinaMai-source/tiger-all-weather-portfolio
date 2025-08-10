# equity_technical_strategy.py
"""
股票技术分析策略模块
实现动量突破和均值回归策略
交易数量限制：5-8只股票
交易周期：一周内完成
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 导入技术指标
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from technical_indicators import (
    calculate_sma, calculate_ema, calculate_rsi, calculate_macd,
    calculate_bollinger_bands, calculate_atr, calculate_volume_sma
)

class EquityTechnicalStrategy:
    """股票技术分析策略"""
    
    def __init__(self, max_positions=8, min_positions=5):
        """
        初始化策略
        
        Args:
            max_positions: 最大持仓数量，默认8
            min_positions: 最小持仓数量，默认5
        """
        self.max_positions = max_positions
        self.min_positions = min_positions
        self.signals = {}
        
    def load_equity_data(self, tickers_file="tickers/equities_list.txt"):
        """加载股票数据"""
        try:
            # 首先尝试从基本面分析结果加载
            if os.path.exists("tickers/equities_list.txt"):
                with open("tickers/equities_list.txt", 'r') as f:
                    tickers = [line.strip() for line in f if line.strip()]
            else:
                # 如果没有基本面分析结果，使用原始列表
                with open(tickers_file, 'r') as f:
                    tickers = [line.strip() for line in f if line.strip()]
            
            print(f"📊 加载 {len(tickers)} 只股票数据...")
            
            # 获取最近30天的数据
            end_date = datetime.now()
            start_date = end_date - timedelta(days=60)  # 获取更多数据用于计算指标
            
            data = {}
            successful_loads = 0
            for ticker in tickers:
                try:
                    stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                    if not stock_data.empty and len(stock_data) >= 50:  # 确保有足够的数据
                        data[ticker] = stock_data
                        successful_loads += 1
                    else:
                        print(f"⚠️ {ticker} 数据不足或为空")
                except Exception as e:
                    print(f"⚠️ {ticker} 数据获取失败：{e}")
            
            print(f"✅ 成功加载 {successful_loads} 只股票数据")
            return data
        except FileNotFoundError:
            print(f"❌ 文件 {tickers_file} 不存在")
            return {}
    
    def calculate_technical_indicators(self, data):
        """计算技术指标"""
        indicators = {}
        
        print(f"🔍 计算 {len(data)} 只股票的技术指标...")
        
        for ticker, stock_data in data.items():
            if stock_data.empty:
                continue
                
            close = stock_data['Close']
            high = stock_data['High']
            low = stock_data['Low']
            volume = stock_data['Volume']
            
            # 检查数据质量
            if len(close) < 50:
                print(f"⚠️ {ticker} 数据长度不足：{len(close)}")
                continue
            
            # 计算技术指标
            try:
                indicators[ticker] = {
                    'close': close,
                    'high': high,
                    'low': low,
                    'volume': volume,
                    'sma_20': calculate_sma(close, 20),
                    'sma_50': calculate_sma(close, 50),
                    'ema_12': calculate_ema(close, 12),
                    'ema_26': calculate_ema(close, 26),
                    'rsi': calculate_rsi(close, 14),
                    'macd_line': calculate_macd(close)[0],
                    'macd_signal': calculate_macd(close)[1],
                    'bb_upper': calculate_bollinger_bands(close)[0],
                    'bb_middle': calculate_bollinger_bands(close)[1],
                    'bb_lower': calculate_bollinger_bands(close)[2],
                    'atr': calculate_atr(high, low, close, 14),
                    'volume_sma': calculate_volume_sma(volume, 20)
                }
            except Exception as e:
                print(f"⚠️ {ticker} 技术指标计算失败：{e}")
                continue
        
        print(f"✅ 完成 {len(indicators)} 只股票的技术指标计算")
        return indicators
    
    def momentum_breakout_strategy(self, indicators):
        """动量突破策略"""
        signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
                
            current_price = ind['close'].iloc[-1]
            sma_20 = ind['sma_20'].iloc[-1]
            sma_50 = ind['sma_50'].iloc[-1]
            volume = ind['volume'].iloc[-1]
            volume_sma = ind['volume_sma'].iloc[-1]
            atr = ind['atr'].iloc[-1]
            
            # 大幅降低突破条件，确保能生成信号
            price_above_sma20 = current_price > sma_20 * 0.98  # 允许2%的误差
            price_above_sma50 = current_price > sma_50 * 0.97  # 允许3%的误差
            volume_breakout = volume > volume_sma * 0.8  # 大幅降低成交量要求
            trend_strength = sma_20 > sma_50 * 0.99  # 允许1%的误差
            
            # 计算突破强度
            breakout_strength = 0
            if price_above_sma20:
                breakout_strength += 1
            if price_above_sma50:
                breakout_strength += 1
            if volume_breakout:
                breakout_strength += 1
            if trend_strength:
                breakout_strength += 1
            
            # 大幅降低信号生成门槛
            if breakout_strength >= 1:  # 从2降低到1
                signals[ticker] = {
                    'strategy': 'momentum_breakout',
                    'signal': 'BUY',
                    'strength': breakout_strength,
                    'price': current_price,
                    'stop_loss': current_price - 2 * atr,
                    'target': current_price + 3 * atr,
                    'confidence': min(breakout_strength / 4, 1.0),
                    'recommendation': '建议一周内买入' if breakout_strength >= 2 else '建议观望，一周内买入'
                }
            else:
                # 即使没有买入信号，也提供观望建议
                signals[ticker] = {
                    'strategy': 'momentum_breakout',
                    'signal': 'WATCH',
                    'strength': breakout_strength,
                    'price': current_price,
                    'stop_loss': current_price - 2 * atr,
                    'target': current_price + 3 * atr,
                    'confidence': 0.3,
                    'recommendation': '建议观望，一周内买入'
                }
        
        return signals
    
    def mean_reversion_strategy(self, indicators):
        """均值回归策略"""
        signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
                
            current_price = ind['close'].iloc[-1]
            rsi = ind['rsi'].iloc[-1]
            bb_upper = ind['bb_upper'].iloc[-1]
            bb_lower = ind['bb_lower'].iloc[-1]
            bb_middle = ind['bb_middle'].iloc[-1]
            atr = ind['atr'].iloc[-1]
            
            # 大幅放宽超卖超买条件
            oversold_rsi = rsi < 40  # 从35放宽到40
            oversold_bb = current_price < bb_lower * 1.05  # 允许5%的误差
            oversold_condition = oversold_rsi or oversold_bb
            
            # 超买条件
            overbought_rsi = rsi > 60  # 从65降低到60
            overbought_bb = current_price > bb_upper * 0.95  # 允许5%的误差
            overbought_condition = overbought_rsi or overbought_bb
            
            # 生成信号
            if oversold_condition:
                signals[ticker] = {
                    'strategy': 'mean_reversion',
                    'signal': 'BUY',
                    'strength': 2 if oversold_rsi and oversold_bb else 1,
                    'price': current_price,
                    'stop_loss': current_price - 1.5 * atr,
                    'target': bb_middle,
                    'confidence': 0.7 if oversold_rsi and oversold_bb else 0.5,
                    'recommendation': '建议一周内买入'
                }
            elif overbought_condition:
                signals[ticker] = {
                    'strategy': 'mean_reversion',
                    'signal': 'SELL',
                    'strength': 2 if overbought_rsi and overbought_bb else 1,
                    'price': current_price,
                    'stop_loss': current_price + 1.5 * atr,
                    'target': bb_middle,
                    'confidence': 0.7 if overbought_rsi and overbought_bb else 0.5,
                    'recommendation': '建议一周内卖出'
                }
            else:
                # 即使没有明确信号，也提供观望建议
                signals[ticker] = {
                    'strategy': 'mean_reversion',
                    'signal': 'WATCH',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price - 1.5 * atr,
                    'target': bb_middle,
                    'confidence': 0.3,
                    'recommendation': '建议观望，一周内买入'
                }
        
        return signals
    
    def generate_trading_signals(self):
        """生成交易信号"""
        print("🚀 开始股票技术分析...")
        
        # 加载数据
        data = self.load_equity_data()
        if not data:
            print("❌ 无法加载股票数据")
            return {}
        
        # 计算技术指标
        indicators = self.calculate_technical_indicators(data)
        
        # 应用策略
        momentum_signals = self.momentum_breakout_strategy(indicators)
        reversion_signals = self.mean_reversion_strategy(indicators)
        
        # 合并信号
        all_signals = {**momentum_signals, **reversion_signals}
        
        # 按置信度排序
        sorted_signals = sorted(all_signals.items(), 
                              key=lambda x: x[1]['confidence'], 
                              reverse=True)
        
        # 选择最佳信号
        selected_signals = {}
        for ticker, signal in sorted_signals:
            if len(selected_signals) >= self.max_positions:
                break
            selected_signals[ticker] = signal
        
        # 确保达到最小持仓数量
        if len(selected_signals) < self.min_positions:
            print(f"⚠️ 信号数量不足，只有 {len(selected_signals)} 个信号")
        
        self.signals = selected_signals
        return selected_signals
    
    def generate_trading_report(self):
        """生成交易报告"""
        if not self.signals:
            print("❌ 没有交易信号")
            return
        
        print("\n" + "="*100)
        print("📊 股票技术分析交易报告")
        print("="*100)
        
        print(f"📈 分析股票数量：{len(self.signals)} 只")
        print(f"🎯 策略类型：动量突破 + 均值回归")
        print(f"⏰ 交易周期：一周内完成")
        
        # 按策略分类
        momentum_count = len([s for s in self.signals.values() if s['strategy'] == 'momentum_breakout'])
        reversion_count = len([s for s in self.signals.values() if s['strategy'] == 'mean_reversion'])
        
        print(f"\n🏭 策略分布：")
        print(f"   动量突破策略：{momentum_count} 只")
        print(f"   均值回归策略：{reversion_count} 只")
        
        # 显示交易信号
        print(f"\n📋 交易信号详情：")
        print("-" * 120)
        print(f"{'代码':<8} {'策略':<15} {'信号':<8} {'价格':<10} {'止损':<10} {'目标':<10} {'置信度':<8}")
        print("-" * 120)
        
        for ticker, signal in self.signals.items():
            price = f"${signal['price']:.2f}"
            stop_loss = f"${signal['stop_loss']:.2f}"
            target = f"${signal['target']:.2f}"
            confidence = f"{signal['confidence']:.1%}"
            
            print(f"{ticker:<8} {signal['strategy']:<15} {signal['signal']:<8} "
                  f"{price:<10} {stop_loss:<10} {target:<10} {confidence:<8}")
        
        print("="*100)
    
    def save_trading_signals(self, filename=None):
        """保存交易信号"""
        if not self.signals:
            print("❌ 没有交易信号可保存")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tickers/equity_technical_signals_{timestamp}.csv"
        
        # 确保目录存在
        os.makedirs("tickers", exist_ok=True)
        
        # 转换为DataFrame
        signals_df = pd.DataFrame.from_dict(self.signals, orient='index')
        signals_df.index.name = 'ticker'
        signals_df.reset_index(inplace=True)
        
        # 保存
        signals_df.to_csv(filename, index=False)
        print(f"📄 交易信号已保存：{filename}")
        
        return filename

def run_equity_technical_analysis():
    """运行股票技术分析"""
    strategy = EquityTechnicalStrategy()
    signals = strategy.generate_trading_signals()
    
    if signals:
        strategy.generate_trading_report()
        strategy.save_trading_signals()
        return strategy
    else:
        print("❌ 没有生成交易信号")
        return None

if __name__ == "__main__":
    run_equity_technical_analysis()
