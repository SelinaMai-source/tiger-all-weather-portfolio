# commodity_technical_strategy.py
"""
大宗商品技术分析策略模块
实现趋势跟踪策略
交易数量限制：2-3个商品
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
    calculate_bollinger_bands, calculate_atr, calculate_adx
)

class CommodityTechnicalStrategy:
    """大宗商品技术分析策略"""
    
    def __init__(self, max_positions=3, min_positions=2):
        """
        初始化策略
        
        Args:
            max_positions: 最大持仓数量，默认3
            min_positions: 最小持仓数量，默认2
        """
        self.max_positions = max_positions
        self.min_positions = min_positions
        self.signals = {}
        
        # 大宗商品ETF列表
        self.commodity_etfs = {
            'USO': 'United States Oil Fund',
            'UNG': 'United States Natural Gas Fund',
            'GLD': 'SPDR Gold Shares',
            'SLV': 'iShares Silver Trust',
            'DBC': 'Invesco DB Commodity Index Tracking Fund',
            'GSG': 'iShares S&P GSCI Commodity-Indexed Trust',
            'COMT': 'iShares Commodity Select Strategy ETF',
            'PDBC': 'Invesco Optimum Yield Diversified Commodity Strategy No K-1 ETF'
        }
    
    def load_commodity_data(self):
        """加载大宗商品数据"""
        print(f"📊 加载大宗商品ETF数据...")
        
        # 首先尝试从基本面分析结果加载
        tickers = []
        if os.path.exists("tickers/commodities_list.txt"):
            with open("tickers/commodities_list.txt", 'r') as f:
                tickers = [line.strip() for line in f if line.strip()]
            print(f"📊 从基本面分析结果加载 {len(tickers)} 个大宗商品ETF...")
        else:
            # 如果没有基本面分析结果，使用默认列表
            tickers = list(self.commodity_etfs.keys())
            print(f"📊 使用默认列表加载 {len(tickers)} 个大宗商品ETF...")
        
        # 获取最近90天的数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=120)  # 获取更多数据用于计算指标
        
        data = {}
        for ticker in tickers:
            try:
                commodity_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not commodity_data.empty:
                    data[ticker] = commodity_data
            except Exception as e:
                print(f"⚠️ {ticker} 数据获取失败：{e}")
        
        return data
    
    def calculate_commodity_indicators(self, data):
        """计算大宗商品技术指标"""
        indicators = {}
        
        for ticker, commodity_data in data.items():
            if commodity_data.empty:
                continue
                
            close = commodity_data['Close']
            high = commodity_data['High']
            low = commodity_data['Low']
            volume = commodity_data['Volume']
            
            # 计算技术指标
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
                'volatility': close.pct_change().rolling(20).std() * np.sqrt(252),
                'momentum_10': close.pct_change(10),
                'momentum_20': close.pct_change(20)
            }
            
            # 计算ADX（趋势强度）
            try:
                adx, plus_di, minus_di = calculate_adx(high, low, close, 14)
                indicators[ticker]['adx'] = adx
                indicators[ticker]['plus_di'] = plus_di
                indicators[ticker]['minus_di'] = minus_di
            except:
                indicators[ticker]['adx'] = pd.Series([np.nan] * len(close))
                indicators[ticker]['plus_di'] = pd.Series([np.nan] * len(close))
                indicators[ticker]['minus_di'] = pd.Series([np.nan] * len(close))
        
        return indicators
    
    def trend_following_strategy(self, indicators):
        """趋势跟踪策略"""
        signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
                
            current_price = ind['close'].iloc[-1]
            sma_20 = ind['sma_20'].iloc[-1]
            sma_50 = ind['sma_50'].iloc[-1]
            ema_12 = ind['ema_12'].iloc[-1]
            ema_26 = ind['ema_26'].iloc[-1]
            rsi = ind['rsi'].iloc[-1]
            macd_line = ind['macd_line'].iloc[-1]
            macd_signal = ind['macd_signal'].iloc[-1]
            atr = ind['atr'].iloc[-1]
            momentum_10 = ind['momentum_10'].iloc[-1]
            momentum_20 = ind['momentum_20'].iloc[-1]
            
            # 趋势条件
            uptrend = (current_price > sma_20 > sma_50 and 
                      ema_12 > ema_26 and 
                      macd_line > macd_signal and
                      momentum_10 > 0 and momentum_20 > 0)
            
            downtrend = (current_price < sma_20 < sma_50 and 
                        ema_12 < ema_26 and 
                        macd_line < macd_signal and
                        momentum_10 < 0 and momentum_20 < 0)
            
            # 趋势强度
            trend_strength = 0
            if uptrend:
                trend_strength += 1
            if rsi > 50:  # RSI在强势区域
                trend_strength += 1
            if momentum_10 > 0.02:  # 短期动量强
                trend_strength += 1
            if momentum_20 > 0.05:  # 中期动量强
                trend_strength += 1
            
            # 生成信号
            if uptrend and trend_strength >= 3:
                signals[ticker] = {
                    'strategy': 'trend_following_uptrend',
                    'signal': 'BUY',
                    'strength': trend_strength,
                    'price': current_price,
                    'stop_loss': current_price - 2 * atr,
                    'target': current_price + 3 * atr,
                    'confidence': min(trend_strength / 4, 1.0),
                    'reason': '强势上涨趋势，多重技术指标确认'
                }
            elif downtrend and trend_strength >= 3:
                signals[ticker] = {
                    'strategy': 'trend_following_downtrend',
                    'signal': 'SELL',
                    'strength': trend_strength,
                    'price': current_price,
                    'stop_loss': current_price + 2 * atr,
                    'target': current_price - 3 * atr,
                    'confidence': min(trend_strength / 4, 1.0),
                    'reason': '强势下跌趋势，多重技术指标确认'
                }
        
        return signals
    
    def breakout_strategy(self, indicators):
        """突破策略"""
        signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
                
            current_price = ind['close'].iloc[-1]
            bb_upper = ind['bb_upper'].iloc[-1]
            bb_lower = ind['bb_lower'].iloc[-1]
            bb_middle = ind['bb_middle'].iloc[-1]
            rsi = ind['rsi'].iloc[-1]
            atr = ind['atr'].iloc[-1]
            volume = ind['volume'].iloc[-1]
            volume_sma = ind['volume'].rolling(20).mean().iloc[-1]
            
            # 突破条件
            breakout_up = current_price > bb_upper and rsi < 80
            breakout_down = current_price < bb_lower and rsi > 20
            volume_confirmation = volume > volume_sma * 1.5
            
            if breakout_up and volume_confirmation:
                signals[ticker] = {
                    'strategy': 'breakout_up',
                    'signal': 'BUY',
                    'strength': 2,
                    'price': current_price,
                    'stop_loss': current_price - 1.5 * atr,
                    'target': current_price + 2.5 * atr,
                    'confidence': 0.7,
                    'reason': '布林带上轨突破，成交量确认'
                }
            elif breakout_down and volume_confirmation:
                signals[ticker] = {
                    'strategy': 'breakout_down',
                    'signal': 'SELL',
                    'strength': 2,
                    'price': current_price,
                    'stop_loss': current_price + 1.5 * atr,
                    'target': current_price - 2.5 * atr,
                    'confidence': 0.7,
                    'reason': '布林带下轨突破，成交量确认'
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
            
            # 超卖条件
            oversold = rsi < 30 and current_price < bb_lower
            
            # 超买条件
            overbought = rsi > 70 and current_price > bb_upper
            
            if oversold:
                signals[ticker] = {
                    'strategy': 'mean_reversion_oversold',
                    'signal': 'BUY',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price - 1.5 * atr,
                    'target': bb_middle,
                    'confidence': 0.6,
                    'reason': '超卖反弹，RSI和布林带双重确认'
                }
            elif overbought:
                signals[ticker] = {
                    'strategy': 'mean_reversion_overbought',
                    'signal': 'SELL',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price + 1.5 * atr,
                    'target': bb_middle,
                    'confidence': 0.6,
                    'reason': '超买回调，RSI和布林带双重确认'
                }
        
        return signals
    
    def generate_trading_signals(self):
        """生成交易信号"""
        print("🚀 开始大宗商品技术分析...")
        
        # 加载数据
        data = self.load_commodity_data()
        if not data:
            print("❌ 无法加载大宗商品数据")
            return {}
        
        # 计算技术指标
        indicators = self.calculate_commodity_indicators(data)
        
        # 应用策略
        trend_signals = self.trend_following_strategy(indicators)
        breakout_signals = self.breakout_strategy(indicators)
        reversion_signals = self.mean_reversion_strategy(indicators)
        
        # 合并信号
        all_signals = {**trend_signals, **breakout_signals, **reversion_signals}
        
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
        print("📊 大宗商品技术分析交易报告")
        print("="*100)
        
        print(f"📈 分析商品数量：{len(self.signals)} 个")
        print(f"🎯 策略类型：趋势跟踪 + 突破 + 均值回归")
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
            filename = f"tickers/commodity_technical_signals_{timestamp}.csv"
        
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

def run_commodity_technical_analysis():
    """运行大宗商品技术分析"""
    strategy = CommodityTechnicalStrategy()
    signals = strategy.generate_trading_signals()
    
    if signals:
        strategy.generate_trading_report()
        strategy.save_trading_signals()
        return strategy
    else:
        print("❌ 没有生成交易信号")
        return None

if __name__ == "__main__":
    run_commodity_technical_analysis()
