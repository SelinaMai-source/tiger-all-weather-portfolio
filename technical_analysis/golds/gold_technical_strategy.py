# gold_technical_strategy.py
"""
黄金技术分析策略模块
实现技术突破策略
交易数量限制：1-2个黄金相关
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
    calculate_bollinger_bands, calculate_atr, calculate_fibonacci_retracements
)

class GoldTechnicalStrategy:
    """黄金技术分析策略"""
    
    def __init__(self, max_positions=2, min_positions=1):
        """
        初始化策略
        
        Args:
            max_positions: 最大持仓数量，默认2
            min_positions: 最小持仓数量，默认1
        """
        self.max_positions = max_positions
        self.min_positions = min_positions
        self.signals = {}
        
        # 黄金相关ETF列表
        self.gold_etfs = {
            'GLD': 'SPDR Gold Shares',
            'IAU': 'iShares Gold Trust',
            'SGOL': 'Aberdeen Standard Physical Gold ETF',
            'GLDM': 'SPDR Gold MiniShares Trust',
            'BAR': 'GraniteShares Gold Trust',
            'OUNZ': 'VanEck Merk Gold Trust',
            'UGL': 'ProShares Ultra Gold',
            'DGL': 'Invesco DB Gold Fund'
        }
    
    def load_gold_data(self):
        """加载黄金数据"""
        print(f"📊 加载黄金ETF数据...")
        
        # 首先尝试从基本面分析结果加载
        tickers = []
        if os.path.exists("tickers/golds_list.txt"):
            with open("tickers/golds_list.txt", 'r') as f:
                tickers = [line.strip() for line in f if line.strip()]
            print(f"📊 从基本面分析结果加载 {len(tickers)} 个黄金ETF...")
        else:
            # 如果没有基本面分析结果，使用默认列表
            tickers = list(self.gold_etfs.keys())
            print(f"📊 使用默认列表加载 {len(tickers)} 个黄金ETF...")
        
        # 获取最近90天的数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=120)  # 获取更多数据用于计算指标
        
        data = {}
        for ticker in tickers:
            try:
                gold_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not gold_data.empty:
                    data[ticker] = gold_data
            except Exception as e:
                print(f"⚠️ {ticker} 数据获取失败：{e}")
        
        return data
    
    def calculate_gold_indicators(self, data):
        """计算黄金技术指标"""
        indicators = {}
        
        for ticker, gold_data in data.items():
            if gold_data.empty:
                continue
                
            close = gold_data['Close']
            high = gold_data['High']
            low = gold_data['Low']
            volume = gold_data['Volume']
            
            # 计算技术指标
            indicators[ticker] = {
                'close': close,
                'high': high,
                'low': low,
                'volume': volume,
                'sma_20': calculate_sma(close, 20),
                'sma_50': calculate_sma(close, 50),
                'sma_200': calculate_sma(close, 200),
                'ema_12': calculate_ema(close, 12),
                'ema_26': calculate_ema(close, 26),
                'rsi': calculate_rsi(close, 14),
                'macd_line': calculate_macd(close)[0],
                'macd_signal': calculate_macd(close)[1],
                'bb_upper': calculate_bollinger_bands(close)[0],
                'bb_middle': calculate_bollinger_bands(close)[1],
                'bb_lower': calculate_bollinger_bands(close)[2],
                'atr': calculate_atr(high, low, close, 14),
                'volatility': close.pct_change().rolling(20).std() * np.sqrt(252),
                'momentum_10': close.pct_change(10),
                'momentum_20': close.pct_change(20)
            }
            
            # 计算斐波那契回撤位
            if len(close) > 0:
                recent_high = high.rolling(50).max().iloc[-1]
                recent_low = low.rolling(50).min().iloc[-1]
                fib_levels = calculate_fibonacci_retracements(recent_high, recent_low)
                indicators[ticker]['fib_levels'] = fib_levels
        
        return indicators
    
    def technical_breakout_strategy(self, indicators):
        """技术突破策略"""
        signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
                
            current_price = ind['close'].iloc[-1]
            sma_20 = ind['sma_20'].iloc[-1]
            sma_50 = ind['sma_50'].iloc[-1]
            sma_200 = ind['sma_200'].iloc[-1]
            rsi = ind['rsi'].iloc[-1]
            bb_upper = ind['bb_upper'].iloc[-1]
            bb_lower = ind['bb_lower'].iloc[-1]
            atr = ind['atr'].iloc[-1]
            volume = ind['volume'].iloc[-1]
            volume_sma = ind['volume'].rolling(20).mean().iloc[-1]
            
            # 突破条件
            breakout_up = (current_price > sma_20 > sma_50 and 
                          current_price > bb_upper and 
                          rsi > 50 and rsi < 80 and
                          volume > volume_sma * 1.2)
            
            breakout_down = (current_price < sma_20 < sma_50 and 
                           current_price < bb_lower and 
                           rsi < 50 and rsi > 20 and
                           volume > volume_sma * 1.2)
            
            # 生成信号
            if breakout_up:
                signals[ticker] = {
                    'strategy': 'technical_breakout_up',
                    'signal': 'BUY',
                    'strength': 2,
                    'price': current_price,
                    'stop_loss': current_price - 2 * atr,
                    'target': current_price + 3 * atr,
                    'confidence': 0.8,
                    'reason': '技术突破，价格突破布林带上轨和移动平均线'
                }
            elif breakout_down:
                signals[ticker] = {
                    'strategy': 'technical_breakout_down',
                    'signal': 'SELL',
                    'strength': 2,
                    'price': current_price,
                    'stop_loss': current_price + 2 * atr,
                    'target': current_price - 3 * atr,
                    'confidence': 0.8,
                    'reason': '技术突破，价格突破布林带下轨和移动平均线'
                }
        
        return signals
    
    def fibonacci_strategy(self, indicators):
        """斐波那契回撤策略"""
        signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
                
            current_price = ind['close'].iloc[-1]
            fib_levels = ind.get('fib_levels', {})
            rsi = ind['rsi'].iloc[-1]
            atr = ind['atr'].iloc[-1]
            
            if not fib_levels:
                continue
            
            # 检查是否在关键斐波那契水平附近
            fib_382 = fib_levels.get('0.382', 0)
            fib_618 = fib_levels.get('0.618', 0)
            fib_786 = fib_levels.get('0.786', 0)
            
            # 支撑位买入信号
            support_buy = (abs(current_price - fib_382) / current_price < 0.02 or
                          abs(current_price - fib_618) / current_price < 0.02) and rsi < 40
            
            # 阻力位卖出信号
            resistance_sell = (abs(current_price - fib_786) / current_price < 0.02) and rsi > 60
            
            if support_buy:
                signals[ticker] = {
                    'strategy': 'fibonacci_support',
                    'signal': 'BUY',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price - 1.5 * atr,
                    'target': current_price + 2 * atr,
                    'confidence': 0.6,
                    'reason': '斐波那契支撑位，RSI超卖'
                }
            elif resistance_sell:
                signals[ticker] = {
                    'strategy': 'fibonacci_resistance',
                    'signal': 'SELL',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price + 1.5 * atr,
                    'target': current_price - 2 * atr,
                    'confidence': 0.6,
                    'reason': '斐波那契阻力位，RSI超买'
                }
        
        return signals
    
    def momentum_strategy(self, indicators):
        """动量策略"""
        signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
                
            current_price = ind['close'].iloc[-1]
            momentum_10 = ind['momentum_10'].iloc[-1]
            momentum_20 = ind['momentum_20'].iloc[-1]
            rsi = ind['rsi'].iloc[-1]
            macd_line = ind['macd_line'].iloc[-1]
            macd_signal = ind['macd_signal'].iloc[-1]
            atr = ind['atr'].iloc[-1]
            
            # 强势动量条件
            strong_momentum = (momentum_10 > 0.03 and momentum_20 > 0.05 and 
                             macd_line > macd_signal and rsi > 50)
            
            # 弱势动量条件
            weak_momentum = (momentum_10 < -0.03 and momentum_20 < -0.05 and 
                           macd_line < macd_signal and rsi < 50)
            
            if strong_momentum:
                signals[ticker] = {
                    'strategy': 'momentum_strong',
                    'signal': 'BUY',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price - 1.5 * atr,
                    'target': current_price + 2.5 * atr,
                    'confidence': 0.7,
                    'reason': '强势动量，MACD和RSI确认'
                }
            elif weak_momentum:
                signals[ticker] = {
                    'strategy': 'momentum_weak',
                    'signal': 'SELL',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price + 1.5 * atr,
                    'target': current_price - 2.5 * atr,
                    'confidence': 0.7,
                    'reason': '弱势动量，MACD和RSI确认'
                }
        
        return signals
    
    def generate_trading_signals(self):
        """生成交易信号"""
        print("🚀 开始黄金技术分析...")
        
        # 加载数据
        data = self.load_gold_data()
        if not data:
            print("❌ 无法加载黄金数据")
            return {}
        
        # 计算技术指标
        indicators = self.calculate_gold_indicators(data)
        
        # 应用策略
        breakout_signals = self.technical_breakout_strategy(indicators)
        fibonacci_signals = self.fibonacci_strategy(indicators)
        momentum_signals = self.momentum_strategy(indicators)
        
        # 合并信号
        all_signals = {**breakout_signals, **fibonacci_signals, **momentum_signals}
        
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
        print("📊 黄金技术分析交易报告")
        print("="*100)
        
        print(f"📈 分析黄金ETF数量：{len(self.signals)} 个")
        print(f"🎯 策略类型：技术突破 + 斐波那契 + 动量")
        print(f"⏰ 交易周期：一周内完成")
        
        # 按策略分类
        strategy_counts = {}
        for signal in self.signals.values():
            strategy = signal['strategy']
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        print(f"\n🏭 策略分布：")
        for strategy, count in strategy_counts.items():
            print(f"   {strategy}: {count} 个")
        
        # 显示交易信号
        print(f"\n📋 交易信号详情：")
        print("-" * 140)
        print(f"{'代码':<8} {'策略':<25} {'信号':<8} {'价格':<10} {'止损':<10} {'目标':<10} {'置信度':<8} {'原因':<30}")
        print("-" * 140)
        
        for ticker, signal in self.signals.items():
            price = f"${signal['price']:.2f}"
            stop_loss = f"${signal['stop_loss']:.2f}"
            target = f"${signal['target']:.2f}"
            confidence = f"{signal['confidence']:.1%}"
            reason = signal.get('reason', '')[:28]
            
            print(f"{ticker:<8} {signal['strategy']:<25} {signal['signal']:<8} "
                  f"{price:<10} {stop_loss:<10} {target:<10} {confidence:<8} {reason:<30}")
        
        print("="*100)
    
    def save_trading_signals(self, filename=None):
        """保存交易信号"""
        if not self.signals:
            print("❌ 没有交易信号可保存")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tickers/gold_technical_signals_{timestamp}.csv"
        
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

def run_gold_technical_analysis():
    """运行黄金技术分析"""
    strategy = GoldTechnicalStrategy()
    signals = strategy.generate_trading_signals()
    
    if signals:
        strategy.generate_trading_report()
        strategy.save_trading_signals()
        return strategy
    else:
        print("❌ 没有生成交易信号")
        return None

if __name__ == "__main__":
    run_gold_technical_analysis()
