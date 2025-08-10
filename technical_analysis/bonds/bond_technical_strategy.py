# bond_technical_strategy.py
"""
债券技术分析策略模块
实现收益率曲线策略
交易数量限制：2-3个债券
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
    calculate_bollinger_bands, calculate_atr
)

class BondTechnicalStrategy:
    """债券技术分析策略"""
    
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
        
        # 债券ETF列表
        self.bond_etfs = {
            'TLT': '20+ Year Treasury Bond ETF',
            'IEF': '7-10 Year Treasury Bond ETF',
            'SHY': '1-3 Year Treasury Bond ETF',
            'LQD': 'Investment Grade Corporate Bond ETF',
            'HYG': 'High Yield Corporate Bond ETF',
            'TIP': 'TIPS Bond ETF',
            'BND': 'Total Bond Market ETF',
            'AGG': 'Core U.S. Aggregate Bond ETF'
        }
    
    def load_bond_data(self):
        """加载债券数据"""
        print(f"📊 加载债券ETF数据...")
        
        # 首先尝试从基本面分析结果加载
        tickers = []
        if os.path.exists("tickers/bonds_list.txt"):
            with open("tickers/bonds_list.txt", 'r') as f:
                tickers = [line.strip() for line in f if line.strip()]
            print(f"📊 从基本面分析结果加载 {len(tickers)} 个债券ETF...")
        else:
            # 如果没有基本面分析结果，使用默认列表
            tickers = list(self.bond_etfs.keys())
            print(f"📊 使用默认列表加载 {len(tickers)} 个债券ETF...")
        
        # 获取最近60天的数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)  # 获取更多数据用于计算指标
        
        data = {}
        for ticker in tickers:
            try:
                bond_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not bond_data.empty:
                    data[ticker] = bond_data
            except Exception as e:
                print(f"⚠️ {ticker} 数据获取失败：{e}")
        
        return data
    
    def calculate_bond_indicators(self, data):
        """计算债券技术指标"""
        indicators = {}
        
        for ticker, bond_data in data.items():
            if bond_data.empty:
                continue
                
            close = bond_data['Close']
            high = bond_data['High']
            low = bond_data['Low']
            volume = bond_data['Volume']
            
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
                'volatility': close.pct_change().rolling(20).std() * np.sqrt(252)
            }
        
        return indicators
    
    def generate_7_indicator_signals(self, indicators):
        """基于7个技术指标生成投票信号"""
        print("🔍 基于7个技术指标生成投票信号...")
        
        all_signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
            
            current_price = ind['close'].iloc[-1]
            signals = []
            
            # 1. SMA信号 (价格相对20日和50日均线)
            sma_20 = ind['sma_20'].iloc[-1]
            sma_50 = ind['sma_50'].iloc[-1]
            
            if current_price > sma_20 and sma_20 > sma_50:
                signals.append('BUY')  # 上升趋势
            elif current_price < sma_20 and sma_20 < sma_50:
                signals.append('SELL')  # 下降趋势
            else:
                signals.append('HOLD')  # 中性
            
            # 2. EMA信号 (价格相对12日和26日指数均线)
            ema_12 = ind['ema_12'].iloc[-1]
            ema_26 = ind['ema_26'].iloc[-1]
            
            if current_price > ema_12 and ema_12 > ema_26:
                signals.append('BUY')  # 指数均线上升趋势
            elif current_price < ema_12 and ema_12 < ema_26:
                signals.append('SELL')  # 指数均线下降趋势
            else:
                signals.append('HOLD')  # 中性
            
            # 3. RSI信号 (超买超卖)
            rsi = ind['rsi'].iloc[-1]
            
            if rsi < 30:
                signals.append('BUY')  # 超卖
            elif rsi > 70:
                signals.append('SELL')  # 超买
            else:
                signals.append('HOLD')  # 中性
            
            # 4. MACD信号 (MACD线与信号线的关系)
            macd_line = ind['macd_line'].iloc[-1]
            macd_signal = ind['macd_signal'].iloc[-1]
            
            if macd_line > macd_signal and macd_line > 0:
                signals.append('BUY')  # MACD金叉且为正
            elif macd_line < macd_signal and macd_line < 0:
                signals.append('SELL')  # MACD死叉且为负
            else:
                signals.append('HOLD')  # 中性
            
            # 5. 布林带信号 (价格相对布林带位置)
            bb_upper = ind['bb_upper'].iloc[-1]
            bb_lower = ind['bb_lower'].iloc[-1]
            
            if current_price < bb_lower:
                signals.append('BUY')  # 价格触及下轨，超卖
            elif current_price > bb_upper:
                signals.append('SELL')  # 价格触及上轨，超买
            else:
                signals.append('HOLD')  # 价格在通道内
            
            # 6. ATR信号 (波动率突破)
            atr = ind['atr'].iloc[-1]
            price_change = abs(current_price - ind['close'].iloc[-2])
            
            if price_change > atr * 1.5:
                # 价格突破ATR，根据方向判断
                if current_price > ind['close'].iloc[-2]:
                    signals.append('BUY')  # 向上突破
                else:
                    signals.append('SELL')  # 向下突破
            else:
                signals.append('HOLD')  # 无突破
            
            # 7. 成交量信号 (成交量相对变化)
            current_volume = ind['volume'].iloc[-1]
            avg_volume = ind['volume'].rolling(20).mean().iloc[-1]
            
            if current_volume > avg_volume * 1.5:
                # 放量，根据价格方向判断
                if current_price > ind['close'].iloc[-2]:
                    signals.append('BUY')  # 放量上涨
                else:
                    signals.append('SELL')  # 放量下跌
            else:
                signals.append('HOLD')  # 成交量正常
            
            # 统计信号
            buy_count = signals.count('BUY')
            sell_count = signals.count('SELL')
            hold_count = signals.count('HOLD')
            
            # 多数决定原则：3个以上指标建议买入就买入，3个以上建议卖出就卖出
            if buy_count >= 3:
                signal = 'BUY'
                confidence = min(buy_count / 7, 1.0)
                reason = f"7个指标中{buy_count}个建议买入"
            elif sell_count >= 3:
                signal = 'SELL'
                confidence = min(sell_count / 7, 1.0)
                reason = f"7个指标中{sell_count}个建议卖出"
            else:
                signal = 'HOLD'
                confidence = 0.5
                reason = f"信号不明确：买入{buy_count}个，卖出{sell_count}个，中性{hold_count}个"
            
            all_signals[ticker] = {
                'signal': signal,
                'confidence': confidence,
                'reason': reason,
                'buy_count': buy_count,
                'sell_count': sell_count,
                'hold_count': hold_count,
                'price': current_price,
                'atr': atr
            }
        
        print(f"✅ 完成 {len(all_signals)} 个债券的7指标投票分析")
        return all_signals
    
    def yield_curve_strategy(self, indicators):
        """收益率曲线策略"""
        signals = {}
        
        # 获取关键债券ETF
        treasury_20y = indicators.get('TLT')
        treasury_7y = indicators.get('IEF')
        treasury_2y = indicators.get('SHY')
        
        if not all([treasury_20y, treasury_7y, treasury_2y]):
            print("⚠️ 缺少关键债券数据")
            return signals
        
        # 计算收益率曲线斜率（简化版）
        # 使用价格变化作为收益率变化的代理
        tlt_momentum = treasury_20y['close'].pct_change(5).iloc[-1]  # 20年期
        ief_momentum = treasury_7y['close'].pct_change(5).iloc[-1]   # 7年期
        shy_momentum = treasury_2y['close'].pct_change(5).iloc[-1]   # 2年期
        
        # 收益率曲线分析
        curve_steepening = (tlt_momentum - shy_momentum) > 0.01  # 曲线变陡
        curve_flattening = (tlt_momentum - shy_momentum) < -0.01  # 曲线变平
        
        # 生成信号
        if curve_steepening:
            # 曲线变陡，买入长期债券
            signals['TLT'] = {
                'strategy': 'yield_curve_steepening',
                'signal': 'BUY',
                'strength': 2,
                'price': treasury_20y['close'].iloc[-1],
                'stop_loss': treasury_20y['close'].iloc[-1] - 2 * treasury_20y['atr'].iloc[-1],
                'target': treasury_20y['close'].iloc[-1] + 3 * treasury_20y['atr'].iloc[-1],
                'confidence': 0.8,
                'reason': '收益率曲线变陡，长期债券受益'
            }
        elif curve_flattening:
            # 曲线变平，买入短期债券
            signals['SHY'] = {
                'strategy': 'yield_curve_flattening',
                'signal': 'BUY',
                'strength': 2,
                'price': treasury_2y['close'].iloc[-1],
                'stop_loss': treasury_2y['close'].iloc[-1] - 1.5 * treasury_2y['atr'].iloc[-1],
                'target': treasury_2y['close'].iloc[-1] + 2 * treasury_2y['atr'].iloc[-1],
                'confidence': 0.8,
                'reason': '收益率曲线变平，短期债券受益'
            }
        
        return signals
    
    def credit_spread_strategy(self, indicators):
        """信用利差策略"""
        signals = {}
        
        # 获取投资级和高收益债券ETF
        investment_grade = indicators.get('LQD')
        high_yield = indicators.get('HYG')
        
        if not all([investment_grade, high_yield]):
            return signals
        
        # 计算信用利差变化
        lqd_momentum = investment_grade['close'].pct_change(10).iloc[-1]
        hyg_momentum = high_yield['close'].pct_change(10).iloc[-1]
        
        # 信用利差收窄（高收益表现更好）
        spread_narrowing = (hyg_momentum - lqd_momentum) > 0.02
        
        # 信用利差扩大（投资级表现更好）
        spread_widening = (lqd_momentum - hyg_momentum) > 0.02
        
        if spread_narrowing:
            signals['HYG'] = {
                'strategy': 'credit_spread_narrowing',
                'signal': 'BUY',
                'strength': 2,
                'price': high_yield['close'].iloc[-1],
                'stop_loss': high_yield['close'].iloc[-1] - 2 * high_yield['atr'].iloc[-1],
                'target': high_yield['close'].iloc[-1] + 3 * high_yield['atr'].iloc[-1],
                'confidence': 0.7,
                'reason': '信用利差收窄，高收益债券受益'
            }
        elif spread_widening:
            signals['LQD'] = {
                'strategy': 'credit_spread_widening',
                'signal': 'BUY',
                'strength': 2,
                'price': investment_grade['close'].iloc[-1],
                'stop_loss': investment_grade['close'].iloc[-1] - 1.5 * investment_grade['atr'].iloc[-1],
                'target': investment_grade['close'].iloc[-1] + 2 * investment_grade['atr'].iloc[-1],
                'confidence': 0.7,
                'reason': '信用利差扩大，投资级债券受益'
            }
        
        return signals
    
    def technical_breakout_strategy(self, indicators):
        """技术突破策略"""
        signals = {}
        
        for ticker, ind in indicators.items():
            if len(ind['close']) < 50:
                continue
                
            current_price = ind['close'].iloc[-1]
            sma_20 = ind['sma_20'].iloc[-1]
            sma_50 = ind['sma_50'].iloc[-1]
            rsi = ind['rsi'].iloc[-1]
            bb_upper = ind['bb_upper'].iloc[-1]
            bb_lower = ind['bb_lower'].iloc[-1]
            atr = ind['atr'].iloc[-1]
            
            # 突破条件
            price_above_sma20 = current_price > sma_20
            price_above_sma50 = current_price > sma_50
            rsi_oversold = rsi < 30
            rsi_overbought = rsi > 70
            bb_breakout_up = current_price > bb_upper
            bb_breakout_down = current_price < bb_lower
            
            # 生成信号
            if price_above_sma20 and price_above_sma50 and not rsi_overbought:
                signals[ticker] = {
                    'strategy': 'technical_breakout',
                    'signal': 'BUY',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price - 1.5 * atr,
                    'target': current_price + 2 * atr,
                    'confidence': 0.6,
                    'reason': '技术突破，价格突破移动平均线'
                }
            elif rsi_oversold and bb_breakout_down:
                signals[ticker] = {
                    'strategy': 'technical_oversold',
                    'signal': 'BUY',
                    'strength': 1,
                    'price': current_price,
                    'stop_loss': current_price - 1.5 * atr,
                    'target': current_price + 2 * atr,
                    'confidence': 0.6,
                    'reason': '超卖反弹，RSI和布林带双重确认'
                }
        
        return signals
    
    def generate_trading_signals(self):
        """生成交易信号"""
        print("🚀 开始债券技术分析...")
        
        # 加载数据
        data = self.load_bond_data()
        if not data:
            print("❌ 无法加载债券数据")
            return {}
        
        # 计算技术指标
        indicators = self.calculate_bond_indicators(data)
        
        # 首先使用7指标投票系统生成基础信号
        print("🔍 使用7指标投票系统生成基础信号...")
        base_signals = self.generate_7_indicator_signals(indicators)
        
        # 应用传统策略
        yield_curve_signals = self.yield_curve_strategy(indicators)
        credit_spread_signals = self.credit_spread_strategy(indicators)
        technical_signals = self.technical_breakout_strategy(indicators)
        
        # 合并所有信号
        all_signals = {**base_signals, **yield_curve_signals, **credit_spread_signals, **technical_signals}
        
        # 优先使用7指标投票系统的信号，如果没有明确的买卖信号，则使用传统策略
        final_signals = {}
        
        for ticker in all_signals:
            if ticker in base_signals and base_signals[ticker]['signal'] in ['BUY', 'SELL']:
                # 使用7指标投票系统的明确信号
                base_signal = base_signals[ticker]
                final_signals[ticker] = {
                    'strategy': '7_indicator_voting',
                    'signal': base_signal['signal'],
                    'strength': base_signal['buy_count'] if base_signal['signal'] == 'BUY' else base_signal['sell_count'],
                    'price': base_signal['price'],
                    'stop_loss': base_signal['price'] - 2 * base_signal['atr'] if base_signal['signal'] == 'BUY' else base_signal['price'] + 2 * base_signal['atr'],
                    'target': base_signal['price'] + 3 * base_signal['atr'] if base_signal['signal'] == 'BUY' else base_signal['price'] - 3 * base_signal['atr'],
                    'confidence': base_signal['confidence'],
                    'reason': base_signal['reason']
                }
            elif ticker in all_signals and all_signals[ticker].get('signal') in ['BUY', 'SELL']:
                # 使用传统策略的信号
                final_signals[ticker] = all_signals[ticker]
        
        # 按置信度排序
        sorted_signals = sorted(final_signals.items(), 
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
            # 如果没有足够的信号，强制选择一些债券
            remaining_bonds = [ticker for ticker in base_signals if ticker not in selected_signals]
            for ticker in remaining_bonds[:self.min_positions - len(selected_signals)]:
                base_signal = base_signals[ticker]
                selected_signals[ticker] = {
                    'strategy': 'forced_entry',
                    'signal': 'BUY' if base_signal['buy_count'] >= base_signal['sell_count'] else 'SELL',
                    'strength': 1,
                    'price': base_signal['price'],
                    'stop_loss': base_signal['price'] - 1.5 * base_signal['atr'],
                    'target': base_signal['price'] + 2 * base_signal['atr'],
                    'confidence': 0.5,
                    'reason': '强制入场：一周内无明确信号'
                }
        
        self.signals = selected_signals
        return selected_signals
    
    def generate_trading_report(self):
        """生成交易报告"""
        if not self.signals:
            print("❌ 没有交易信号")
            return
        
        print("\n" + "="*100)
        print("📊 债券技术分析交易报告")
        print("="*100)
        
        print(f"📈 分析债券数量：{len(self.signals)} 个")
        print(f"🎯 策略类型：收益率曲线 + 信用利差 + 技术突破")
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
            filename = f"tickers/bond_technical_signals_{timestamp}.csv"
        
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

def run_bond_technical_analysis():
    """运行债券技术分析"""
    strategy = BondTechnicalStrategy()
    signals = strategy.generate_trading_signals()
    
    if signals:
        strategy.generate_trading_report()
        strategy.save_trading_signals()
        return strategy
    else:
        print("❌ 没有生成交易信号")
        return None

if __name__ == "__main__":
    run_bond_technical_analysis()
